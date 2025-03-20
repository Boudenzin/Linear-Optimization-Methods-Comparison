import numpy as np
from scipy.optimize import linprog
import time
import psutil
import os

def planejamento_producao():
    # Iniciar a medição do tempo
    start_time = time.time()

    # Obter o uso de memória antes da execução
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 ** 2)  # Convertendo para MB

    # Dados do problema
    n_produtos = 10
    n_meses = 12
    capacidade_producao = 1000  # Capacidade de produção mensal

    # Custos de produção (exemplo fictício: custo aumenta com o produto e o mês)
    custos_producao = np.array([10 + i + t for t in range(n_meses) for i in range(n_produtos)])

    # Custos de estoque (exemplo fictício: custo aumenta com o produto e o mês)
    custos_estoque = np.array([2 + 0.5 * (i + 1) + 0.1 * (t + 1) for t in range(n_meses) for i in range(n_produtos)])

    # Custos fixos (exemplo fictício: custo fixo para iniciar a produção de um produto)
    custos_fixos = np.array([100 * (i + 1) for i in range(n_produtos)])

    # Demandas (exemplo fictício: demanda aumenta com o produto e o mês)
    demandas = np.array([50 + 5 * (i + 1) + 10 * (t + 1) for t in range(n_meses) for i in range(n_produtos)])

    # Variáveis de decisão: X (produção), S (estoque), Y (binária para custos fixos)
    num_variaveis = n_produtos * n_meses
    c = np.concatenate([custos_producao, custos_estoque, np.repeat(custos_fixos, n_meses)])

    # Matrizes para restrições
    A_eq = []
    b_eq = []

    # Restrições de balanço de estoque
    for i in range(n_produtos):
        for t in range(n_meses):
            row = np.zeros(3 * num_variaveis)
            if t == 0:
                # S[i,0] - X[i,0] = -demanda[i,0]
                row[i * n_meses + t] = -1  # X[i,0]
                row[num_variaveis + i * n_meses + t] = 1  # S[i,0]
                b_eq.append(-demandas[i * n_meses + t])
            else:
                # S[i,t-1] + X[i,t] - S[i,t] = demanda[i,t]
                row[num_variaveis + i * n_meses + (t - 1)] = 1  # S[i,t-1]
                row[i * n_meses + t] = -1  # X[i,t]
                row[num_variaveis + i * n_meses + t] = -1  # S[i,t]
                b_eq.append(-demandas[i * n_meses + t])
            A_eq.append(row)

    # Restrições de capacidade de produção
    for t in range(n_meses):
        row = np.zeros(3 * num_variaveis)
        for i in range(n_produtos):
            row[i * n_meses + t] = 1  # X[i,t]
        A_eq.append(row)
        b_eq.append(capacidade_producao)

    # Restrições de ligação entre X e Y (X <= M * Y)
    M = 10000  # Valor grande para o método Big M
    A_ub = []
    b_ub = []
    for i in range(n_produtos):
        for t in range(n_meses):
            row = np.zeros(3 * num_variaveis)
            row[i * n_meses + t] = 1  # X[i,t]
            row[2 * num_variaveis + i * n_meses + t] = -M  # -M * Y[i,t]
            A_ub.append(row)
            b_ub.append(0)

    # Converter listas para arrays numpy
    A_eq = np.array(A_eq)
    b_eq = np.array(b_eq)
    A_ub = np.array(A_ub)
    b_ub = np.array(b_ub)

    # Resolver o problema usando o método Simplex Revisado
    resultado = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method='revised simplex')

    # Medir o tempo de execução
    end_time = time.time()
    execution_time = end_time - start_time

    # Medir o uso de memória após a execução
    mem_after = process.memory_info().rss / (1024 ** 2)  # Convertendo para MB
    memory_usage = mem_after - mem_before

    # Exibir resultados
    if resultado.success:
        print(f"Status: {resultado.message}")
        print(f"Custo Total Ótimo: R$ {resultado.fun:.2f}")
    else:
        print("A solução não foi encontrada.")

    print(f"Tempo de Execução: {execution_time:.2f} segundos")
    print(f"Uso de Memória: {memory_usage:.2f} MB")

    # Exibir valores das variáveis de decisão (opcional)
    X_values = resultado.x[:num_variaveis].reshape((n_produtos, n_meses))
    S_values = resultado.x[num_variaveis:2 * num_variaveis].reshape((n_produtos, n_meses))
    Y_values = resultado.x[2 * num_variaveis:].reshape((n_produtos, n_meses))

    for i in range(n_produtos):
        for t in range(n_meses):
            print(f"Produção X[{i + 1},{t + 1}] = {X_values[i, t]:.2f}")
            print(f"Estoque S[{i + 1},{t + 1}] = {S_values[i, t]:.2f}")
            print(f"Decisão Binária Y[{i + 1},{t + 1}] = {Y_values[i, t]:.2f}")

# Executar a função
planejamento_producao()
