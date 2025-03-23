import pulp
import time
import psutil
import os

def solve_big_m_manual():
    # Inicia medição de tempo e memória
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024)  # Memória antes (em MB)
    start_time = time.time()

    # Cria o problema
    prob = pulp.LpProblem("BigM_Manual", pulp.LpMaximize)

    # Variáveis de decisão
    x = pulp.LpVariable("x", lowBound=0)
    y = pulp.LpVariable("y", lowBound=0)
    a1 = pulp.LpVariable("a1", lowBound=0)  # Variável artificial

    # Função objetivo com penalização (Big M)
    M = 1000  # Valor grande para penalizar a1
    prob += x + 2 * y - M * a1, "Função Objetivo com Big M"

    # Restrições
    prob += x + y <= 5, "Restrição_1"
    prob += x - y + a1 == 1, "Restrição_2"

    # Resolve o problema
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # Finaliza medição de tempo e memória
    end_time = time.time()
    mem_after = process.memory_info().rss / (1024 * 1024)  # Memória depois (em MB)
    memory_used = mem_after - mem_before

    # Resultados
    print(f"\n### Big M (Manual) a ###")
    print(f"Tempo de execução: {end_time - start_time:.6f} s")
    print(f"Uso de memória: {memory_used:.6f} MB")
    print(f"Valor ótimo encontrado: {pulp.value(prob.objective):.6f}")
    print(f"x = {x.value():.3f}, y = {y.value():.3f}, a1 = {a1.value():.3f}")

    # Verifica se a variável artificial foi eliminada
    if a1.value() > 1e-5:
        print("⚠️ Variável artificial diferente de zero: solução pode ser inviável!")

# Executa o código
solve_big_m_manual()