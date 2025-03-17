import pulp
import time
import psutil
import os

def solve_transportation_problem():
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024)

    start_time = time.time()

    # Problema de Transporte
    prob = pulp.LpProblem("Problema_Transporte", pulp.LpMinimize)

    # Definir variáveis de decisão (quantidades de produto a serem transportadas)
    X11 = pulp.LpVariable("X11", lowBound=0)
    X12 = pulp.LpVariable("X12", lowBound=0)
    X13 = pulp.LpVariable("X13", lowBound=0)
    X14 = pulp.LpVariable("X14", lowBound=0)
    X15 = pulp.LpVariable("X15", lowBound=0)
    X21 = pulp.LpVariable("X21", lowBound=0)
    X22 = pulp.LpVariable("X22", lowBound=0)
    X23 = pulp.LpVariable("X23", lowBound=0)
    X24 = pulp.LpVariable("X24", lowBound=0)
    X25 = pulp.LpVariable("X25", lowBound=0)
    X31 = pulp.LpVariable("X31", lowBound=0)
    X32 = pulp.LpVariable("X32", lowBound=0)
    X33 = pulp.LpVariable("X33", lowBound=0)
    X34 = pulp.LpVariable("X34", lowBound=0)
    X35 = pulp.LpVariable("X35", lowBound=0)

    # Função objetivo (minimizar o custo total de transporte)
    prob += 5*X11 + 3*X12 + 6*X13 + 2*X14 + 7*X15 + \
            4*X21 + 6*X22 + 3*X23 + 5*X24 + 8*X25 + \
            7*X31 + 4*X32 + 2*X33 + 6*X34 + 3*X35, "Custo Total"

    # Restrições de capacidade das fábricas
    prob += X11 + X12 + X13 + X14 + X15 <= 100, "Capacidade_Fábrica_1"
    prob += X21 + X22 + X23 + X24 + X25 <= 150, "Capacidade_Fábrica_2"
    prob += X31 + X32 + X33 + X34 + X35 <= 200, "Capacidade_Fábrica_3"

    # Restrições de demanda dos centros de distribuição
    prob += X11 + X21 + X31 >= 80, "Demanda_Centro_1"
    prob += X12 + X22 + X32 >= 90, "Demanda_Centro_2"
    prob += X13 + X23 + X33 >= 120, "Demanda_Centro_3"
    prob += X14 + X24 + X34 >= 70, "Demanda_Centro_4"
    prob += X15 + X25 + X35 >= 100, "Demanda_Centro_5"

    # Resolver
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    end_time = time.time()
    mem_after = process.memory_info().rss / (1024 * 1024)
    memory_used = mem_after - mem_before

    optimal_value = pulp.value(prob.objective)

    print(f"\n### Resultado do Problema de Transporte ###")
    print(f"Tempo de execução: {end_time - start_time:.6f} s")
    print(f"Uso de memória: {memory_used:.2f} MB")
    print(f"Valor ótimo encontrado: {optimal_value:.6f}")

    # Exibir os valores das variáveis
    for v in prob.variables():
        print(f"{v.name} = {v.varValue:.3f}")

# Executar
solve_transportation_problem()
