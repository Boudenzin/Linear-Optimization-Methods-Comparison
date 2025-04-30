# Importação das bibliotecas necessárias
import numpy as np
import pulp
import time
import psutil
import os

def problema_balanceamento_producao_big_m():
    """
    Gera e resolve o problema de balanceamento de produção usando a técnica Big M,
    adicionando variáveis artificiais nas restrições de atendimento dos centros.
    """

    # Iniciar a medição de tempo
    start_time = time.time()

    # Iniciar a medição de memória
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 ** 2)  # Memória em MB

    # -----------------------------
    # Definição dos parâmetros do problema
    # -----------------------------

    n_fabricas = 15  # Número de fábricas
    n_centros = 10   # Número de centros de distribuição

    n_variaveis = n_fabricas * n_centros

    # Gerar custos aleatórios de transporte (entre 10 e 100)
    np.random.seed(42)
    custos = np.random.randint(10, 100, size=n_variaveis)

    # Gerar capacidades das fábricas (entre 500 e 1500)
    capacidades_fabricas = np.random.randint(500, 1500, size=n_fabricas)

    # Gerar demandas dos centros (entre 200 e 800)
    demandas_centros = np.random.randint(200, 800, size=n_centros)

    # Valor grande para penalizar variáveis artificiais (Big M)
    M = 10000

    # -----------------------------
    # Modelagem do problema usando PuLP
    # -----------------------------

    # Criar o problema de minimização
    prob = pulp.LpProblem("Balanceamento_Producao_BigM", pulp.LpMinimize)

    # Variáveis de decisão: quantidade enviada da fábrica i para centro j
    X = pulp.LpVariable.dicts("Envio", ((i, j) for i in range(n_fabricas) for j in range(n_centros)), lowBound=0)

    # Variáveis artificiais para atender as demandas dos centros
    artificiais = pulp.LpVariable.dicts("Artificial", (j for j in range(n_centros)), lowBound=0)

    # -----------------------------
    # Definição da função objetivo
    # -----------------------------

    # Minimizar custo de transporte + penalidade das variáveis artificiais
    prob += pulp.lpSum([
        custos[i * n_centros + j] * X[(i, j)] for i in range(n_fabricas) for j in range(n_centros)
    ]) + M * pulp.lpSum([artificiais[j] for j in range(n_centros)])

    # -----------------------------
    # Definição das restrições
    # -----------------------------

    # 1. Capacidade de produção das fábricas
    for i in range(n_fabricas):
        prob += pulp.lpSum([X[(i, j)] for j in range(n_centros)]) <= capacidades_fabricas[i], f"Capacidade_Fabrica_{i+1}"

    # 2. Atendimento de demanda dos centros (com variável artificial para ajustar)
    for j in range(n_centros):
        prob += pulp.lpSum([X[(i, j)] for i in range(n_fabricas)]) + artificiais[j] >= demandas_centros[j], f"Demanda_Centro_{j+1}"

    # -----------------------------
    # Resolução do problema
    # -----------------------------

    prob.solve(pulp.PULP_CBC_CMD(msg=False))  # Resolver com CBC

    # -----------------------------
    # Medição de tempo e memória
    # -----------------------------

    end_time = time.time()
    execution_time = end_time - start_time

    mem_after = process.memory_info().rss / (1024 ** 2)
    memory_used = mem_after - mem_before

    # -----------------------------
    # Impressão dos resultados
    # -----------------------------

    print("\n### Resultado do Problema de Balanceamento de Produção com Big M ###")
    print(f"Status: {pulp.LpStatus[prob.status]}")
    print(f"Custo Total Ótimo: R$ {pulp.value(prob.objective):.2f}")
    print(f"Tempo de Execução: {execution_time:.2f} segundos")
    print(f"Uso de Memória: {memory_used:.2f} MB")

    # (Opcional) Mostrar valores das variáveis de decisão
    for i in range(n_fabricas):
        for j in range(n_centros):
            print(f"Fábrica {i+1} -> Centro {j+1}: {X[(i, j)].varValue:.2f}")

# Executar o problema
problema_balanceamento_producao_big_m()
