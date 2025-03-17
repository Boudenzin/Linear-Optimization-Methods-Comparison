import pulp
import time
import psutil
import os

def solve_big_m_manual():
    M = 1000  # Valor grande para penalizar a1
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024)

    start_time = time.time()

    # Problema com Big M
    prob = pulp.LpProblem("BigM_Manual", pulp.LpMaximize)
    x = pulp.LpVariable("x", lowBound=0)
    y = pulp.LpVariable("y", lowBound=0)
    s1 = pulp.LpVariable("s1", lowBound=0)
    s2 = pulp.LpVariable("s2", lowBound=0)
    a1 = pulp.LpVariable("a1", lowBound=0)

    # Função objetivo com penalização
    prob += x + 2*y - M*a1, "Função Objetivo com Big M"

    # Restrições transformadas em igualdades
    prob += x + y + s1 == 5, "Restrição_1"
    prob += x - y - s2 + a1 == 1, "Restrição_2"

    # Resolver
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    end_time = time.time()
    mem_after = process.memory_info().rss / (1024 * 1024)
    memory_used = mem_after - mem_before

    optimal_value = pulp.value(prob.objective)
    theoretical_optimum = 10  # Ajuste se souber o valor teórico
    precision_error = abs(optimal_value - theoretical_optimum)

    print(f"\n### Big M (Manual) ###")
    print(f"Tempo de execução: {end_time - start_time:.6f} s")
    print(f"Uso de memória: {memory_used:.2f} MB")
    print(f"Precisão da solução: {precision_error:.6f}")
    print(f"Valor ótimo encontrado: {optimal_value:.6f}")
    print(f"x = {x.value():.3f}, y = {y.value():.3f}, a1 = {a1.value():.3f}")

    # Verifica se variável artificial foi eliminada (idealmente zero)
    if a1.value() > 1e-5:
        print("⚠️ Variável artificial diferente de zero: solução pode ser inviável!")

# Executar
solve_big_m_manual()
