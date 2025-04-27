# Importação das bibliotecas necessárias
import numpy as np  # Biblioteca para operações numéricas e manipulação de vetores/matrizes
from scipy.optimize import linprog  # Função para resolver problemas de Programação Linear
import time  # Biblioteca para medir o tempo de execução
import psutil  # Biblioteca para medir o uso de memória
import os  # Biblioteca para acessar informações do sistema operacional

def planejamento_producao():
    """
    Resolve um problema de planejamento de produção com múltiplos produtos e múltiplos períodos.

    Objetivo: minimizar o custo total de produção, estoque e ativação de produção,
    respeitando a capacidade de produção mensal e a demanda prevista.

    Método de resolução: Simplex Revisado.
    """

    # -----------------------------
    # Iniciar medição de tempo e memória
    # -----------------------------
    start_time = time.time()
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 ** 2)  # Memória inicial em MB

    # -----------------------------
    # Definição dos dados do problema
    # -----------------------------

    n_produtos = 10  # Número de produtos
    n_meses = 12     # Número de meses de planejamento
    capacidade_producao = 1000  # Capacidade máxima de produção mensal

    # Vetor de custos de produção (crescentes com produto e mês)
    custos_producao = np.array([10 + i + t for t in range(n_meses) for i in range(n_produtos)])

    # Vetor de custos de estoque (crescentes com produto e mês)
    custos_estoque = np.array([2 + 0.5 * (i + 1) + 0.1 * (t + 1) for t in range(n_meses) for i in range(n_produtos)])

    # Vetor de custos fixos para iniciar a produção
    custos_fixos = np.array([100 * (i + 1) for i in range(n_produtos)])

    # Vetor de demandas previstas
    demandas = np.array([50 + 5 * (i + 1) + 10 * (t + 1) for t in range(n_meses) for i in range(n_produtos)])

    # Número total de variáveis contínuas (produção e estoque) e binárias (ativação)
    num_variaveis = n_produtos * n_meses

    # Função objetivo: Minimizar custos de produção + estoque + custos fixos
    c = np.concatenate([
        custos_producao,            # Custos de produção
        custos_estoque,             # Custos de estoque
        np.repeat(custos_fixos, n_meses)  # Custos fixos replicados para cada mês
    ])

    # -----------------------------
    # Construção das restrições
    # -----------------------------

    A_eq = []  # Matriz das restrições de igualdade
    b_eq = []  # Vetor do lado direito das igualdades

    # Restrições de balanço de estoque
    for i in range(n_produtos):
        for t in range(n_meses):
            row = np.zeros(3 * num_variaveis)
            if t == 0:
                # Estoque inicial: S[i,0] - X[i,0] = -demanda[i,0]
                row[i * n_meses + t] = -1  # Produção
                row[num_variaveis + i * n_meses + t] = 1  # Estoque
                b_eq.append(-demandas[i * n_meses + t])
            else:
                # Estoque ao longo dos meses: S[i,t-1] + X[i,t] - S[i,t] = demanda[i,t]
                row[num_variaveis + i * n_meses + (t - 1)] = 1  # Estoque anterior
                row[i * n_meses + t] = -1  # Produção atual
                row[num_variaveis + i * n_meses + t] = -1  # Estoque atual
                b_eq.append(-demandas[i * n_meses + t])
            A_eq.append(row)

    # Restrições de capacidade de produção mensal
    for t in range(n_meses):
        row = np.zeros(3 * num_variaveis)
        for i in range(n_produtos):
            row[i * n_meses + t] = 1  # Produção
        A_eq.append(row)
        b_eq.append(capacidade_producao)

    # Restrições de ligação entre produção e ativação (Big M)
    M = 10000  # Valor grande para método Big M
    A_ub = []  # Matriz das restrições de desigualdade
    b_ub = []  # Vetor do lado direito das desigualdades

    for i in range(n_produtos):
        for t in range(n_meses):
            row = np.zeros(3 * num_variaveis)
            row[i * n_meses + t] = 1  # Produção
            row[2 * num_variaveis + i * n_meses + t] = -M  # Ativação (Big M)
            A_ub.append(row)
            b_ub.append(0)

    # Conversão das listas para arrays numpy
    A_eq = np.array(A_eq)
    b_eq = np.array(b_eq)
    A_ub = np.array(A_ub)
    b_ub = np.array(b_ub)

    # -----------------------------
    # Resolução do problema
    # -----------------------------

    resultado = linprog(
        c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        method='revised simplex'  # Usando método Simplex Revisado
    )

    # -----------------------------
    # Coleta de resultados
    # -----------------------------

    # Tempo de execução
    end_time = time.time()
    execution_time = end_time - start_time

    # Memória utilizada
    mem_after = process.memory_info().rss / (1024 ** 2)  # Em MB
    memory_usage = mem_after - mem_before

    # Impressão dos resultados
    if resultado.success:
        print(f"Status: {resultado.message}")
        print(f"Custo Total Ótimo: R$ {resultado.fun:.2f}")
    else:
        print("A solução não foi encontrada.")

    print(f"Tempo de Execução: {execution_time:.2f} segundos")
    print(f"Uso de Memória: {memory_usage:.2f} MB")

    # Separação dos resultados para facilitar análise
    X_values = resultado.x[:num_variaveis].reshape((n_produtos, n_meses))
    S_values = resultado.x[num_variaveis:2 * num_variaveis].reshape((n_produtos, n_meses))
    Y_values = resultado.x[2 * num_variaveis:].reshape((n_produtos, n_meses))

    # Exibir valores das variáveis
    for i in range(n_produtos):
        for t in range(n_meses):
            print(f"Produção X[{i + 1},{t + 1}] = {X_values[i, t]:.2f}")
            print(f"Estoque S[{i + 1},{t + 1}] = {S_values[i, t]:.2f}")
            print(f"Decisão Binária Y[{i + 1},{t + 1}] = {Y_values[i, t]:.2f}")

# Executar a função
planejamento_producao()
