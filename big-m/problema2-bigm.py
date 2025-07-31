import numpy as np
import pulp
import time
import psutil
import os

def problema_2_robusto_big_m():
    """
    Problema 2 (média escala) com 60 variáveis e 40 restrições, resolvido com Big M.
    Adiciona variáveis artificiais nas restrições do tipo 'maior ou igual' e penaliza na função objetivo.
    """

    # -----------------------------
    # Início da medição
    # -----------------------------
    start_time = time.time()
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 ** 2)  # Em MB

    # -----------------------------
    # Geração de dados consistentes
    # -----------------------------
    np.random.seed(202)

    n_vars = 60
    n_restricoes = 40
    M = 10000  # Penalidade para variáveis artificiais

    custos = np.random.randint(5, 30, size=n_vars)
    A = np.random.randint(-3, 8, size=(n_restricoes, n_vars))
    b = np.random.randint(100, 500, size=n_restricoes)

    np.savetxt('matriz_A_2.csv', A, delimiter=',', fmt='%d')
    np.savetxt('lado_b_2.csv', b, delimiter=',', fmt='%d')
    np.savetxt('custos_2.csv', custos, delimiter=',', fmt='%d')

    sinais = ['<='] * (n_restricoes // 2) + ['>='] * (n_restricoes // 2)

    # -----------------------------
    # Modelagem com PuLP
    # -----------------------------
    prob = pulp.LpProblem("Problema_2_Robusto_BigM", pulp.LpMinimize)

    # Variáveis de decisão (x1 a x60)
    x = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(n_vars)]

    # Variáveis artificiais (só nas restrições do tipo ≥)
    artificiais = []

    # Função objetivo inicial
    objetivo = pulp.lpSum([custos[i] * x[i] for i in range(n_vars)])

    # Adição de restrições e construção da função objetivo com Big M
    for i in range(n_restricoes):
        expr = pulp.lpSum([A[i][j] * x[j] for j in range(n_vars)])

        if sinais[i] == '<=':
            prob += expr <= b[i], f"Restricao_{i+1}"
        else:
            s = pulp.LpVariable(f"s{i+1}", lowBound=0)  # Surplus
            a = pulp.LpVariable(f"a{i+1}", lowBound=0)  # Artificial
            artificiais.append(a)
            prob += expr - s + a == b[i], f"Restricao_{i+1}"
            objetivo += M * a

    # Define função objetivo com penalidades
    prob += objetivo

    # -----------------------------
    # Resolução com CBC
    # -----------------------------
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # -----------------------------
    # Medição final
    # -----------------------------
    end_time = time.time()
    mem_after = process.memory_info().rss / (1024 ** 2)
    tempo = end_time - start_time
    memoria = mem_after - mem_before

    # -----------------------------
    # Impressão dos resultados
    # -----------------------------
    print("\n### Resultado - Problema 2 Robusto (Big M Manual) ###")
    print(f"Status: {pulp.LpStatus[prob.status]}")
    print(f"Valor ótimo: {pulp.value(prob.objective):.2f}")
    print(f"Tempo de execução: {tempo:.4f} segundos")
    print(f"Uso de memória: {memoria:.4f} MB")

    # Mostrar primeiras variáveis
    for var in x[:10]:
        print(f"{var.name} = {var.varValue:.4f}")
    if len(x) > 10:
        print(f"... (exibindo apenas os 10 primeiros de {len(x)} variáveis)")

    # Checagem das artificiais
    for a in artificiais:
        if a.varValue > 1e-5:
            print(f"⚠️ Variável artificial {a.name} = {a.varValue:.4f} → Solução pode não ser viável sem Big M.")

# Executar
problema_2_robusto_big_m()
