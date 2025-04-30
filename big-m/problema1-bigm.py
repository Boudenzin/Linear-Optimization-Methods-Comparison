# Importação das bibliotecas
import numpy as np
import pulp
import time
import psutil
import os

def problema_1_melhorado_big_m():
    """
    Problema 1 (pequena escala) com 10 variáveis e 8 restrições, resolvido com Big M.
    Adiciona variáveis artificiais para restrições do tipo 'maior ou igual' (≥) e penaliza na função objetivo.
    """

    # -----------------------------
    # Iniciar medições
    # -----------------------------
    start_time = time.time()
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 ** 2)  # Em MB

    # -----------------------------
    # Geração dos dados do problema (mesmos da versão Revised)
    # -----------------------------
    np.random.seed(101)

    n_vars = 10
    n_restricoes = 8
    M = 10000  # Valor grande para penalizar variáveis artificiais

    # Função objetivo (custos)
    c = np.random.randint(1, 20, size=n_vars)

    # Matriz de coeficientes das restrições
    A = np.random.randint(-5, 10, size=(n_restricoes, n_vars))

    # Lado direito
    b = np.random.randint(10, 100, size=n_restricoes)

    # Metade das restrições será ≤, metade ≥
    sentidos = ['<='] * (n_restricoes // 2) + ['>='] * (n_restricoes // 2)

    # -----------------------------
    # Modelagem com PuLP
    # -----------------------------
    prob = pulp.LpProblem("Problema_1_Melhorado_BigM", pulp.LpMinimize)

    # Variáveis de decisão
    x_vars = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(n_vars)]

    # Lista de variáveis artificiais
    artificiais = []

    # Função objetivo inicial (custos das variáveis de decisão)
    objetivo = pulp.lpSum([c[i] * x_vars[i] for i in range(n_vars)])

    # Adiciona as restrições e variáveis artificiais
    for j in range(n_restricoes):
        expr = pulp.lpSum([A[j][i] * x_vars[i] for i in range(n_vars)])

        if sentidos[j] == '<=':
            prob += expr <= b[j], f"Restricao_{j+1}"
        else:
                # Para restrições do tipo '>=', adicione:
            s = pulp.LpVariable(f"s{j+1}", lowBound=0)  # Variável de folga negativa (surplus)
            a = pulp.LpVariable(f"a{j+1}", lowBound=0)  # Variável artificial
            prob += expr - s + a == b[j]  # Restrição convertida para igualdade
            objetivo += M * a  # Penalização da artificial

    # Define função objetivo com penalidade
    prob += objetivo

    # -----------------------------
    # Resolução
    # -----------------------------
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # -----------------------------
    # Coleta de desempenho
    # -----------------------------
    end_time = time.time()
    mem_after = process.memory_info().rss / (1024 ** 2)
    memoria_usada = mem_after - mem_before
    tempo_execucao = end_time - start_time

    # -----------------------------
    # Impressão dos resultados
    # -----------------------------
    print("\n### Resultado - Problema 1 Melhorado (Big M Manual) ###")
    print(f"Status: {pulp.LpStatus[prob.status]}")
    print(f"Valor ótimo: {pulp.value(prob.objective):.2f}")
    print(f"Tempo de execução: {tempo_execucao:.4f} segundos")
    print(f"Uso de memória: {memoria_usada:.4f} MB")

    # Valores das variáveis de decisão
    for i, var in enumerate(x_vars):
        print(f"{var.name} = {var.varValue:.4f}")

    # Verificar variáveis artificiais
    for a in artificiais:
        if a.varValue > 1e-5:
            print(f"⚠️ Variável artificial {a.name} > 0 ({a.varValue:.4f}) → Solução pode não ser viável sem Big M.")

# Executar
problema_1_melhorado_big_m()
