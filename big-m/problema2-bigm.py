# Importação das bibliotecas necessárias
import pulp  # Biblioteca usada para modelar e resolver problemas de Programação Linear
import time  # Biblioteca para medir o tempo de execução
import psutil  # Biblioteca para medir o uso de memória do processo
import os  # Biblioteca para acessar informações do sistema operacional

def solve_transportation_problem():
    """
    Resolve um problema clássico de transporte usando Programação Linear.
    
    O objetivo é minimizar o custo total de transporte entre fábricas e centros de distribuição,
    respeitando as capacidades de produção e as demandas dos centros.
    """

    # Inicia o monitoramento de memória do processo
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024)  # Memória antes da execução (em MB)

    # Inicia a contagem do tempo de execução
    start_time = time.time()

    # Cria o modelo de otimização (problema de minimização)
    prob = pulp.LpProblem("Problema_Transporte", pulp.LpMinimize)

    # Definição das variáveis de decisão
    # Cada variável representa a quantidade transportada da fábrica i para o centro j
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

    # Definição da função objetivo
    # Cada termo representa o custo unitário multiplicado pela quantidade transportada
    prob += (
        5*X11 + 3*X12 + 6*X13 + 2*X14 + 7*X15 +
        4*X21 + 6*X22 + 3*X23 + 5*X24 + 8*X25 +
        7*X31 + 4*X32 + 2*X33 + 6*X34 + 3*X35
    ), "Custo Total"

    # Definição das restrições de capacidade das fábricas
    prob += X11 + X12 + X13 + X14 + X15 <= 110, "Capacidade_Fábrica_1"
    prob += X21 + X22 + X23 + X24 + X25 <= 150, "Capacidade_Fábrica_2"
    prob += X31 + X32 + X33 + X34 + X35 <= 200, "Capacidade_Fábrica_3"

    # Definição das restrições de demanda dos centros de distribuição
    prob += X11 + X21 + X31 >= 80, "Demanda_Centro_1"
    prob += X12 + X22 + X32 >= 90, "Demanda_Centro_2"
    prob += X13 + X23 + X33 >= 120, "Demanda_Centro_3"
    prob += X14 + X24 + X34 >= 70, "Demanda_Centro_4"
    prob += X15 + X25 + X35 >= 100, "Demanda_Centro_5"

    # Resolver o problema usando o solver CBC
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # Finaliza a contagem de tempo e memória
    end_time = time.time()
    mem_after = process.memory_info().rss / (1024 * 1024)  # Memória depois da execução (em MB)
    memory_used = mem_after - mem_before  # Diferença de memória usada

    # Captura o valor ótimo da função objetivo (custo mínimo)
    optimal_value = pulp.value(prob.objective)

    # Impressão dos resultados
    print(f"\n### Resultado do Problema de Transporte ###")
    print(f"Tempo de execução: {end_time - start_time:.6f} s")
    print(f"Uso de memória: {memory_used:.2f} MB")
    print(f"Valor ótimo encontrado: {optimal_value:.6f}")

    # Exibe os valores das variáveis de decisão
    for v in prob.variables():
        print(f"{v.name} = {v.varValue:.3f}")

# Executa a função principal
solve_transportation_problem()
