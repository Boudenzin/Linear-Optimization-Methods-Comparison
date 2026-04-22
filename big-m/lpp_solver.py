M=float("1000000")
maximization = 'max'
def assign_variables(n):
    variables = []
    for i in range(n):
        variables.append(f'x{i+1}')
    return variables

def assign_slag_variables(n):
    slag_variables = []
    for i in range(n):
        slag_variables.append(f's{i+1}')
    return slag_variables

def assign_artificial_variables(n):
    artificial_variables = []
    for i in range(n):
        artificial_variables.append(f'a{i+1}')
    return artificial_variables

def create_identity(n):
    I = []
    row = [0]*n
    for i in range(n):
        row[i] = 1
        I.append(row.copy())
        row[i] = 0
    return I

def min_positive_index(arr):
    min_no = M
    for i in arr:
        if i>0 and i<min_no:
            min_no = i
    return arr.index(min_no)

def merge_matrix(A, B):
    merged = []
    for i in range(len(A)):
        merged.append(A[i]+B[i])
    return merged
        
def find_ratio(A, B):
    ratio_matrix = []
    for i in range(len(A)):
        if B[i]==0:
            ratio_matrix.append(float('inf'))
            continue
        ratio_matrix.append(A[i]/B[i])
    return ratio_matrix

def find_sigmaAB(A, B):
    ans = 0
    for i in range(len(A)):
        ans+=A[i]*B[i]
    return ans

def get_col(A, n):
    col = []
    for i in A:
        col.append(i[n])
    return col

def sub_arr(A, B):
    ans = []
    for i in range(len(A)):
        ans.append(A[i]-B[i])
    return ans

def parse_input():
    global maximization
    num_vars = int(input("Enter the number of variables: "))
    num_constraints = int(input("Enter the number of constraint equations: "))
    max_min = input("Maximize (max) or Minimize (min)? ").lower()
    if max_min.strip(' ')=="max" or max_min.strip(' ')=='min':
        maximization=max_min


    # Parse objective function
    objective_str = input("Enter the objective function (e.g., 3x1 + 4x2 - 3x3): ")
    c = parse_equation(objective_str, num_vars)

    A = []
    b = []
    extra_coefficients_matrix = []

    # Parse constraint equations
    for i in range(num_constraints):
        equation_str = input(f"Enter constraint equation {i + 1} (e.g., 2x1 + 3x2 - 4x3 >= 5): ")
        extra_coefficients, constraint_A, constraint_b = parse_equation(equation_str, num_vars)
        A.append(constraint_A)
        b.append(constraint_b)
        extra_coefficients_matrix.append(extra_coefficients)

    if maximization == 'min':
        c = [-x for x in c] # Convert minimization to maximization

    return c, A, b, extra_coefficients_matrix

def parse_equation(eqn, num_vars):
    eqn = eqn.replace(" ", '')
    A = [0.0] * num_vars
    value = ""
    b = None
    i=0
    while i<len(eqn):
        if eqn[i] in 'xX':
            index = int(eqn[i+1])-1
            if (value=='' or value =="+" or value=="-"):
                value+='1'
            A[index] += float(value)
            value = ""
            i += 2
            continue
        elif eqn[i] in '<':
            b = float(eqn[i+2:])
            return [1, 0], A, b
        elif eqn[i] in '>':
            b = float(eqn[i+2:])
            return [-1, 1], A, b
        elif eqn[i] in '=':
            b = float(eqn[i+2:])
            return [0, 1], A, b
        value += eqn[i]
        i+=1

    if b==None:
        return A
    else:
        return A, b
    
def all_greater_equal_zero(z):
    res = True
    for i in z:
        if i<0:
            res = False
    return res

def find_cefficient(var, c, no_of_variables):
    if var[0]=='x':
        index = int(var[1:])-1
    else:
        index = no_of_variables+int(var[1:])-1
    return c[index]


# def print_table(bv_with_var, c_with_var, val, sol, ratio, zi_ci, key_row, key_col):

    #first row
    print("\n")
    print("\t \033[91m   \t  \tCj \033[00m", end="")
    for i in range(len(val[0])):
        if (c_with_var[i][0][0]=='a' and maximization=='max'):
            to_print = f"\t-M" 
        elif (c_with_var[i][0][0]=='a' and maximization=='min'):
            to_print = f'\tM'
        else:
            to_print = f"\t{round(c_with_var[i][1], 2)}"
        print(to_print, end="")
    print('\t')

    #second row
    print("\t\033[91mCb\tBv\tXb\033[00m", end="")
    for i in range(len(val[0])):
        print(f"\t\033[91m{c_with_var[i][0]}\033[00m", end='')
    print('\t\033[91mR\033[00m')

    #middle table
    for i in range(len(sol)):
        if i!=key_row:
            if (bv_with_var[i][0][0]=='a' and maximization=='max'):
                to_print = f"\t-M" 
            elif (bv_with_var[i][0][0]=='a' and maximization=='min'):
                to_print = f'\tM'
            else:
                to_print = f"\t{round(bv_with_var[i][1], 2)}"
            print(f"{to_print}\t{bv_with_var[i][0]}\t{round(sol[i], 2)}", end='')
            for j in range(len(val[0])):
                if j == key_col:
                    print(f"\t\033[92m{str(round(val[i][j],2))}\033[00m", end='')
                else:
                    print(f"\t{str(round(val[i][j],2))}", end='')            
            print(f"\t{round(ratio[i], 2)}")
        else:
            if (bv_with_var[i][0][0]=='a' and maximization=='max'):
                to_print = f"\t-M" 
            elif (bv_with_var[i][0][0]=='a' and maximization=='min'):
                to_print = f'\tM'
            else:
                to_print = f"\t{round(bv_with_var[i][1], 2)}"
            print(f"\033[92m{to_print}\t{bv_with_var[i][0]}\t{round(sol[i], 2)}\t"+'\t'.join([str(round(x,2)) for x in val[i]])+f"\t{round(ratio[i], 2)}\033[00m")

    #last row
    print("\t\t\t\033[91mZj-Cj\033[00m", end='')
    for i in range(len(val[0])):
        to_print = f"{round(zi_ci[i],2)}" if round(zi_ci[i]/M,2)==0 else f"{round(zi_ci[i]/M,2)}M"
        if i==key_col:
            print('\t\033[92m'+to_print+'\033[00m', end='')
        else:
            print('\t'+to_print, end='')

    print("\n")




def simplex(c, val, b, no_of_variables, bv=None, bv_with_var=None, c_with_var=None):
    n = no_of_variables
    no_of_constraints = len(b)
    if not bv:
        # if maximization=='min':
        #     c = [-x for x in c]
        m = len(b)
        bv = [0]*m
        bv_with_var = merge_matrix([[x] for x in assign_slag_variables(m)], [[x] for x in bv])
        c_with_var =  merge_matrix([[x] for x in assign_variables(no_of_variables)+assign_slag_variables(m)], [[x] for x in c])
    else:
        m=2*len(b)
    zi_ci=[-1]*(m+n)#let it so that the loop runs at least once
    while True:
        # print(bv_with_var, val)
        z = []
        for i in range(m+n):
            z.append(find_sigmaAB(bv, get_col(val, i)))

        zi_ci = sub_arr(z, c)
        key_col = zi_ci.index(min(zi_ci))
        ratio = find_ratio(b, get_col(val, key_col))

        if(all_greater_equal_zero(zi_ci)):
            break
        unbound = True
        for abc in ratio:
            if abc>0 and abc!=float('inf'):
                unbound = False
        if unbound:
            print("\033[95mUnbounded Solution!\033[00m\n")
            return
        key_row = min_positive_index(ratio)
         # print_table(bv_with_var, c_with_var, val, b, ratio, zi_ci, key_row, key_col)
        key_element = val[key_row][key_col]
        new_val = [0]*no_of_constraints
        new_b = [0]*no_of_constraints
        bv[key_row] = c[key_col]
        bv_with_var[key_row] = c_with_var[key_col]

        new_val[key_row]=[]
        for i in range(m+n):
            new_val[key_row].append(val[key_row][i]/key_element)
        new_b[key_row] = b[key_row]/key_element
        
        for i in range(no_of_constraints):
            if i==key_row:
                continue
            temp_row = []
            for j in range(m+n):
                temp_row.append(new_val[key_row][j]*get_col(val, key_col)[i])
            new_val[i]  = sub_arr(val[i], temp_row)

            new_b[i] = b[i] - new_b[key_row]*get_col(val, key_col)[i]


        val = new_val
        b = new_b
        bv = get_col(bv_with_var, 1)


    final_sol = [[x, 0] for x in assign_variables(no_of_variables)]
    index = 0
    for i in bv_with_var:
        if i[0] in get_col(final_sol, 0):
            final_sol[int(i[0][1:])-1][1] = b[index]
        index+=1

    infeasible = False
    index = 0
    for i in bv_with_var:
        if i[0][0]=='a':
            if b[index]>0:
                infeasible = True
        index+=1
    # if infeasible:
        # print("\033[95mNo Feasible Solution Exists!\033[00m\n")
        # return

    
    # print("\n")
    # for i in (final_sol):
     #    print(f"\033[96m{i[0]} ==\033[00m \033[93m{round(i[1],2)}\033[00m")
    optimal_value = find_sigmaAB(get_col(bv_with_var, 1), b)
    # print("\n")
    # if maximization=='min':
      #   print("\033[96mOptimal: \033[00m", f"\033[93m{round((-1)*optimal_value, 2)}\033[00m", '\n')
    # else:
    # USE A LINHA SEGUINTE PARA DEBUG DO VALOR OTIMO
    # print("\033[96mOptimal Value: \033[00m", f"\033[93m{round(optimal_value, 2)}\033[00m", '\n')

            
    for basic_variable_value in zi_ci[:n]:
        if basic_variable_value==0:
            return 


def big_M(c, val, b, no_of_variables, extra_coefficient_matrix):
    m, n = len(val), no_of_variables

    # if maximization=='min':
    #     c = [-x for x in c]

    bv = [0]*m
    bv_with_var = merge_matrix([[x] for x in assign_slag_variables(m)], [[x] for x in bv]) #can be any matrix of 2x1 [x1, 2]
    index = 0
    for i in extra_coefficient_matrix:
        if i[1]==1:
            bv[index]=(-1)*M
            bv_with_var[index] = [f'a{index+1}', bv[index]]
        else:
            bv[index]=0
            bv_with_var[index] = [f's{index+1}', bv[index]]
        index+=1
        
    c_with_var =  merge_matrix([[x] for x in assign_variables(no_of_variables)+assign_slag_variables(m)+assign_artificial_variables(m)], [[x] for x in c])

    simplex(c, val, b, no_of_variables, bv=bv, bv_with_var=bv_with_var, c_with_var=c_with_var)


if __name__ == "__main__":

    print("\t\t\t\t\t\t\t\t\033[91m     __             ___              ___      ___                 \033[00m")
    print("\t\t\t\t\t\t\t\t\033[91m    |  \    /\     |   \     /\     |   \    /   \    \   /       \033[00m")
    print("\t\t\t\t\t\t\t\t\033[91m    |__/   /__\    |___/    /__\    |    \  |     |    \ /        \033[00m")
    print("\t\t\t\t\t\t\t\t\033[91m    |     /    \   | \     /    \   |    /  |     |    / \        \033[00m")
    print("\t\t\t\t\t\t\t\t\033[91m    |    /      \  |  \   /      \  |___/    \___/    /   \       \033[00m")

    # c = [107, 1, 2, 0]
    # A = [[14, 1, -6, 3], [16, 0.5, -6, 0], [3, -1, -1, 0]]
    # b = [7, 5, 0]
    # extra_coefficient_matrix = [[0, 1], [1, 0], [1, 0]]
    c, A, b, extra_coefficient_matrix = parse_input()
    no_of_variables = len(c)
    c = c + [0]*len(b) +[(-1)*M]*len(b)
    val = merge_matrix(A, [[0]*(2*len(b))]*len(b))
    for i in range(len(b)):
        val[i][no_of_variables+i] = extra_coefficient_matrix[i][0]
        val[i][no_of_variables+len(b)+i] = extra_coefficient_matrix[i][1]

    big_M(c, val, b, no_of_variables, extra_coefficient_matrix)
    # c = c + [0]*len(A)
    # val = merge_matrix(A, create_identity(len(b)))
    # simplex(c, val, b, no_of_variables, bv=None, bv_with_var=None, c_with_var=None)