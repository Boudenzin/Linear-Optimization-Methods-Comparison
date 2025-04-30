# Importação das bibliotecas
import numpy as np
import time
import psutil
from scipy.optimize import linprog

def problema_1_melhorado():
    """
    Problema 1 (pequena escala) com 10 variáveis e 8 restrições.
    Objetivo: Minimizar custos com restrições de capacidade e limites técnicos.
    Compatível com Simplex Revisado e Big M.
    """

    # -----------------------------
    # Iniciar medições
    # -----------------------------
    start_time = time.time()
    process = psutil.Process()
    mem_before = process.memory_info().rss / (1024 ** 2)  # Memória inicial em MB

    # -----------------------------
    # Gerar dados do problema
    # -----------------------------
    np.random.seed(101)  # Semente fixa

    n_vars = 10
    n_restricoes = 8

    # Coeficientes da função objetivo (custos aleatórios de 1 a 20)
    c = np.random.randint(1, 20, size=n_vars)

    # Matriz A de restrições (valores entre -5 e 10)
    A = np.random.randint(-5, 10, size=(n_restricoes, n_vars))

    # Lado direito b das restrições (entre 10 e 100)
    b = np.random.randint(10, 100, size=n_restricoes)

    # Sinais das restrições: metade ≤, metade ≥
    sentidos = ['<='] * (n_restricoes // 2) + ['>='] * (n_restricoes // 2)

    # Separar as restrições em A_ub e A_eq de acordo com o tipo
    A_ub, b_ub = [], []
    for i in range(n_restricoes):
        if sentidos[i] == '<=':
            A_ub.append(A[i])
            b_ub.append(b[i])
        else:
            A_ub.append(-A[i])  # Multiplica por -1 para virar ≤
            b_ub.append(-b[i])

    A_ub = np.array(A_ub)
    b_ub = np.array(b_ub)

    # -----------------------------
    # Resolver com Simplex Revisado
    # -----------------------------
    resultado = linprog(
        c,
        A_ub=A_ub,
        b_ub=b_ub,
        bounds=[(0, None)] * n_vars,
        method='revised simplex'
    )

    # -----------------------------
    # Coleta de desempenho
    # -----------------------------
    end_time = time.time()
    mem_after = process.memory_info().rss / (1024 ** 2)
    memoria_usada = mem_after - mem_before
    tempo_execucao = end_time - start_time

    # -----------------------------
    # Resultados
    # -----------------------------
    print("\n### Resultado - Problema 1 Melhorado (Simplex Revisado) ###")
    if resultado.success:
        print(f"Status: {resultado.message}")
        print(f"Valor ótimo: {resultado.fun:.2f}")
    else:
        print("❌ Não foi possível encontrar solução viável.")

    print(f"Tempo de execução: {tempo_execucao:.4f} segundos")
    print(f"Uso de memória: {memoria_usada:.4f} MB")

    # Exibir valores das variáveis
    for i, x in enumerate(resultado.x):
        print(f"x{i+1} = {x:.4f}")

# Executar
problema_1_melhorado()
