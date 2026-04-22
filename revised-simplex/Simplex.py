import math
import sys
from dataclasses import dataclass
from typing import Optional, Tuple, Iterable

import numpy as np
from scipy.special import comb
from scipy import linalg
from enum import Enum


class PickingRule(Enum):
    """
    Rule for picking the next entering variable. for more information see
    http://elib.mi.sanu.ac.rs/files/journals/yjor/50/yujorn50p321-332.pdf
    """

    BLAND_RULE = 1
    DANTZING_RULE = 2


class ResultCode(Enum):
    """
    Codes indicating the result type given by the simplex algorithm
    """

    INFEASIBLE = 1
    FINITE_OPTIMAL = 2
    UNBOUNDED_OPTIMAL = 3
    CYCLE_DETECTED = 4


@dataclass
class SimplexResult(object):
    """
    The returned object from the simplex get_optimal_solution.
    """

    res_code: ResultCode
    assignment: Optional[np.ndarray]
    optimal_score: Optional[float]


EPSILON = sys.float_info.epsilon
PAIRS_LIMIT = 5


def is_close_to_zero(arr: np.ndarray, or_below=False, or_above=False) -> np.ndarray:
    """
    An array version of elementwise < 0 / <= 0 / >= 0 / == 0.
    The exact operation is determined by the booleans args or_below & or_above
    :param arr: numpy array of any shape
    :param or_below: if True allows for elements to be < 0
    :param or_above: if True allows for elements to be > 0
    :return: Array of booleans values to whether each element compiles with the
    checked condition (< 0 / <= 0 / >= 0 / == 0).
    """
    if or_below and or_above:
        return np.full(arr.shape, True)
    elif not or_below and not or_above:
        return np.isclose(arr, 0, atol=EPSILON)
    elif or_below:
        return np.logical_or(np.isclose(arr, 0, atol=EPSILON), arr <= 0)
    else:
        return np.logical_or(np.isclose(arr, 0, atol=EPSILON), arr >= 0)


class Simplex(object):
    """
    A simplex solver object for solving max problems.
    It has 2 external api methods: get_optimal_solution & has_feasible_solution
    """

    def __init__(self):
        self.A = None
        self.b = None
        self.c = None
        self.cur_assignment = None

    def _load_scenario(self, A: np.ndarray, b: np.ndarray, c: np.ndarray) -> None:
        """
        Loading a linear programming case into the solver.
        The case is of the form:
            maximize cx
            where Ax <= b
            and x >= 0 (elementwise)

        :param A: 2 dimensions numpy array of some shape (n x m)
        :param b: numpy array with n elements
        :param c: numpy array with m elements
        """
        self.nrows, self.original_nvars = A.shape
        self.A = np.hstack((A, np.eye(self.nrows)))
        self.b = b.astype(float).reshape((-1, 1))
        self.c = np.hstack((c, np.zeros(self.nrows)))
        self.nvars = self.A.shape[1]

        self.xb = np.arange(self.nvars - self.nrows, self.nvars)
        self.xn = np.arange(0, self.nvars - self.nrows)

        self.cur_assignment = np.hstack(
            (np.zeros(self.original_nvars), self.b.copy().reshape(-1))
        )
        self.cur_assignment = self.cur_assignment.astype(float)

        self.estimated_B = np.eye(self.nrows).astype(float)
        self.estimated_inverse_B = np.eye(self.nrows).astype(float)

        self.cur_iteration = 1
        self.max_iterations = comb(self.nvars, self.nrows)

    def _reconstruct_z_coefs(self) -> np.ndarray:
        """
        Constructing a representation of the objective function's coefficients
        for all the non-basis variables. This will help us measure their effect
        and to choose the next entering variable
        :return: An 1d array of the coefficients corresponding to the non-basis
        variables in the objective function
        """
        return (
            self.c[self.xn]
            - self.c[self.xb] @ self.estimated_inverse_B @ self.A[:, self.xn]
        )

    def _get_entering_options(self, z_coefs: np.ndarray, rule: PickingRule) -> Iterable:
        """
        Get options for possible valid entering variables
        (variables to enter the basis). This method returns at most
        PAIRS_LIMIT candidates (this limit value can be changed globally).
        :param z_coefs: An array of the coefficients corresponding
        to the non-basis variables in the objective function
        :param rule: A methodology rule for how to prioritize the candidates
        :return: An iterable of optional indexes of entering variables (sorted
        by priority based on the picking rule)
        """
        if rule == PickingRule.DANTZING_RULE:
            sorted_indices = z_coefs.argsort()[-PAIRS_LIMIT:][::-1]
            return self.xn[sorted_indices]
        elif rule == PickingRule.BLAND_RULE:
            sorted_positive_vars = sorted(self.xn[np.where(z_coefs > 0)])
            return sorted_positive_vars[:PAIRS_LIMIT]
        else:
            raise ValueError(f"Unrecognized picking rule: {rule}")

    def _pick_leaving_var(self, d: np.ndarray) -> Tuple[int, int]:
        """
        Get the index of the leaving variable (the variable we want to remove
        from the basis). The leaving variable chosen is the variable that allows
        for the maximal assignment of the entering variable
        (the first variable of the basis which reaches 0 value as we increase
        the value of the entering variable).
        :param d: A vector of the coefficients of the leaving variable in the
        basis variables representation.
        :return: A tuple of the leaving variable's index and the new value
        of the entering variable after the swap.
        """
        bounded_vars_idxs = self.xb[d > 0]
        bounds_vector = self.cur_assignment[bounded_vars_idxs] / d[d > 0]
        t = min(bounds_vector)
        leaving_idx = bounded_vars_idxs[np.argmin(bounds_vector)]
        return leaving_idx, t

    def _pick_pair_to_swap(
        self, z_coefs: np.ndarray, rule: PickingRule
    ) -> Tuple[int, int, np.ndarray, int]:
        """
        Pick a pair of entering variable and leaving variable to swap.
        This method makes tries to avoid pairs in which there is a very small
        element in the diagonal of the eta matrix inorder for avoiding
        numerical stability problems.
        :param z_coefs: An array of the coefficients corresponding
        to the non-basis variables in the objective function
        :param rule: A methodology rule for how to prioritize the candidates
        :return: A tuple containing (entering_var_idx, leaving_var_idx, d, t).
        In case the method discovers that the problem is unbounded
        it returns (-1, -1, d, 0)
        """
        potential_entering = self._get_entering_options(z_coefs, rule)
        optional_pairs = []
        for entering_var_idx in potential_entering:
            d = self._get_d(entering_var_idx)
            if all(is_close_to_zero(d, or_below=True)):
                return -1, -1, d, 0

            leaving_var_idx, t = self._pick_leaving_var(d)
            leaving_basis_loc = np.where(self.xb == leaving_var_idx)[0][0]
            eta_diag_element = d[leaving_basis_loc]
            if eta_diag_element > EPSILON:
                return entering_var_idx, leaving_var_idx, d, t
            else:
                optional_pairs.append(
                    (eta_diag_element, entering_var_idx, leaving_var_idx, d, t)
                )

        optional_etas = [x[0] for x in optional_pairs]
        largest_eta_option_index = int(np.argmax(optional_etas))
        return optional_pairs[largest_eta_option_index][1:]

    def _get_d(self, entering_var_idx: int) -> np.ndarray:
        """
        Get a vector of the coefficients of the leaving variable in the
        basis variables representation. This will be used to determine the
        value of the new entering variable after swapping him with the leaving
        variable. This value will be the maximum value which will keep the
        values of all other basis variables >= 0.
        :param entering_var_idx: The of the column representing the entering
        variable in A matrix
        :return: A vector of the coefficients of the leaving variable in the
        basis variables representation
        """
        return self.estimated_inverse_B @ self.A[:, entering_var_idx]

    def _get_eta_and_inverse(
        self, loc_replaced: int, d: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get the eta matrix and its inverse for the variables swap. This
        will allow to update the estimation of B (The basis slice of A)
        and its inverse.
        :param loc_replaced: The index of the location of the leaving variable
        in the basis (which is now replaced by the entering variable)
        :param d: A vector of the coefficients of the leaving variable in the
        basis variables representation.
        :return: Tuple of eta matrix and eta's inverse matrix
        """
        new_eta = np.eye(self.nrows).astype(float)
        new_eta[:, loc_replaced] = d

        new_inverse_eta = new_eta.copy()
        new_loc_on_diag = 1.0 / new_inverse_eta[loc_replaced, loc_replaced]
        new_inverse_eta[:, loc_replaced] *= -new_loc_on_diag
        new_inverse_eta[loc_replaced, loc_replaced] = new_loc_on_diag
        return new_eta, new_inverse_eta

    def _refactor_if_needed(self) -> None:
        """
        Refactors the basis inverse if the estimation of B doesn't allow for
        an epsilon-close reconstruction of the b vector. This is another
        safeguard tool for numerical stability.
        """
        estimated_b = self.estimated_B @ self.cur_assignment[self.xb]
        estimated_b = estimated_b.reshape((-1, 1))
        if not np.allclose(estimated_b, self.b, atol=EPSILON):
            self._refactor_basis_inverse()

    def _refactor_basis_inverse(self) -> None:
        """
        LU refactoring the inverse of the basis
        """
        l, u = linalg.lu(self.A[:, self.xb], True)
        self.estimated_inverse_B = linalg.inv(u) @ linalg.inv(l)

    def _update_estimated_b_and_inverse(self, loc_replaced: int, d: np.ndarray) -> None:
        """
        Updates the estimation of B (the basis slice of A) and its inverse.
        The inverse is important to reconstruct z and get d.
        :param loc_replaced: The index of the location of the leaving variable
        in the basis (which is now replaced by the entering variable)
        :param d: A vector of the coefficients of the leaving variable in the
        basis variables representation.
        """
        new_eta, new_inverse_eta = self._get_eta_and_inverse(loc_replaced, d)
        self.estimated_B = self.estimated_B @ new_eta
        self.estimated_inverse_B = new_inverse_eta @ self.estimated_inverse_B

    def _swap_vars(self, entering_var_idx: int, leaving_var_idx: int) -> None:
        """
        Inserts the entering variable into the basis and remove the leaving
        variable from it
        :param entering_var_idx: The index of the entering variable
        :param leaving_var_idx: The index of the leaving variable
        """
        d = self._get_d(entering_var_idx)
        loc_in_xb = np.where(self.xb == leaving_var_idx)[0][0]
        loc_in_xn = np.where(self.xn == entering_var_idx)[0][0]
        self.xb[loc_in_xb] = entering_var_idx
        self.xn[loc_in_xn] = leaving_var_idx

        self._update_estimated_b_and_inverse(loc_in_xb, d)

    def _update_assignment(self, d: np.ndarray, t: int, entering_var_idx: int) -> None:
        """
        Updates the assignments of the variables after a swap
        :param d: A vector of the coefficients of the leaving variable in the
        basis variables representation.
        :param t: The new value of the entering variable
        :param entering_var_idx: The index of the entering variable
        """
        self.cur_assignment[self.xn] = 0
        self.cur_assignment[self.xb] -= t * d
        self.cur_assignment[entering_var_idx] = t

    def _init_aux_problem(self, A: np.ndarray, b: np.ndarray, c: np.ndarray) -> None:
        """
        Initialize the solver with the auxiliary problem to the standard
        linear programming problem. For more information on the auxiliary
        problem see page 3 (slide 4) in
        http://www.mi.fu-berlin.de/wiki/pub/Main/GunnarKlauP1winter0708/discMath_klau_linProg_III.pdf
        :param A: 2 dimensions numpy array of some shape (n x m)
        :param b: numpy array with n elements
        :param c: numpy array with m elements
        """
        x_0_coefs = np.full((self.nrows, 1), -1)
        A = np.hstack((x_0_coefs, A))
        c = np.hstack((np.array([-1]), np.zeros(c.shape[0])))
        self._load_scenario(A, b, c)
        self.cur_assignment = np.zeros(self.cur_assignment.shape[0])

        most_negative_b = np.argmin(b)
        leaving_var_idx = self.xb[most_negative_b]
        self._swap_vars(0, leaving_var_idx)

        # adapt assignment
        self.cur_assignment[self.xn] = 0
        self.cur_assignment[self.xb] = self.b.reshape(-1) - float(min(b))
        self.cur_assignment[0] = -min(b)

    def _pivot_to_original_problem(self, original_c: np.ndarray) -> None:
        """
        Pivot the solver from auxiliary problem it was solving to the
        original problem in the standard form keeping the current assignments
        of the variables
        :param original_c: A vector of the original coefficients of the
        objective function
        """
        self.A = self.A[:, 1:]
        self.xb -= 1
        self.xn = self.xn[np.where(self.xn != 0)] - 1
        self.c = np.hstack((original_c, np.zeros(self.nrows)))
        self.cur_assignment = self.cur_assignment[1:]
        self.cur_iteration = 1

    def _get_optimal_from_feasible_solution(self, rule: PickingRule) -> SimplexResult:
        """
        Gets the optimal solution for a linear programming problem
        (already loaded to the solver) which is known
        to have a feasible solution
        :param rule: Picking rule to prioritize picks of entering variables
        :return: The optimal solution in the form of SimplexResult object
        """
        while self.cur_iteration <= self.max_iterations:
            z_coefs = self._reconstruct_z_coefs()
            if all(is_close_to_zero(z_coefs, or_below=True)):
                optimal_score = sum(self.cur_assignment * self.c)
                return SimplexResult(
                    ResultCode.FINITE_OPTIMAL,
                    self.cur_assignment,
                    optimal_score,
                )

            entering_idx, leaving_idx, d, t = self._pick_pair_to_swap(z_coefs, rule)
            if all(is_close_to_zero(d, or_below=True)):
                return SimplexResult(
                    ResultCode.UNBOUNDED_OPTIMAL, self.cur_assignment, math.inf
                )

            self._swap_vars(entering_idx, leaving_idx)
            self._update_assignment(d, t, entering_idx)

            self.cur_iteration += 1
            self._refactor_if_needed()

        cur_score = sum(self.cur_assignment * self.c)
        return SimplexResult(ResultCode.CYCLE_DETECTED, self.cur_assignment, cur_score)

    def get_optimal_solution(
        self, A: np.ndarray, b: np.ndarray, c: np.ndarray, rule=PickingRule.BLAND_RULE
    ) -> SimplexResult:
        """
        Gets the optimal solution for a linear programming problem in the form
        of:
            maximize cx
            where Ax <= b
            and x >= 0 (elementwise)
        :param A: 2 dimensions numpy array of some shape (n x m)
        :param b: numpy array with n elements
        :param c: numpy array with m elements
        :param rule: picking rule to prioritize picks of entering variables
        :return: The optimal solution in the form of SimplexResult object
        """
        self._load_scenario(A, b, c)

        if not all(is_close_to_zero(b, or_above=True)):
            self._init_aux_problem(A, b, c)
            aux_res = self._get_optimal_from_feasible_solution(rule=rule)
            if aux_res.optimal_score != 0:
                return SimplexResult(ResultCode.INFEASIBLE, None, None)
            self._pivot_to_original_problem(c)

        return self._get_optimal_from_feasible_solution(rule)

    def has_feasible_solution(
        self, A: np.ndarray, b: np.ndarray, c: np.ndarray
    ) -> bool:
        """
        Check if the linear programming case represented by A, b, c has some
        feasible solution where feasible solution is some x >= 0 (elementwise)
        where Ax <= b
        :param A: 2 dimensions numpy array of some shape (n x m)
        :param b: numpy array with n elements
        :param c: numpy array with m elements
        :return: True if it has a feasible solution, otherwise False
        """
        self._load_scenario(A, b, c)
        if all(is_close_to_zero(b, or_above=True)):
            return True
        else:
            self._init_aux_problem(A, b, c)
            aux_optimal_score = self._get_optimal_from_feasible_solution(
                rule=PickingRule.BLAND_RULE
            ).optimal_score
            if aux_optimal_score == 0:
                return True
            return False
