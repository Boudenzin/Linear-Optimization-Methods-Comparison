import numpy as np
from scipy.optimize import linprog
import time
import psutil
import os

def solve_transportation_problem():
    # Medir uso de memória antes da execução
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024)  # Em MB

    # Medir tempo de execução
    start_time = time.perf_counter()

    # Coeficientes da função objetivo (custos de transporte)
    c = [5, 3, 6, 2, 7, 4, 6, 3, 5, 8, 7, 4, 2, 6, 3]

    # Matriz de coeficientes das restrições
    A_eq = [
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Capacidade Fábrica 1
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],  # Capacidade Fábrica 2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],  # Capacidade Fábrica 3
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # Demanda Centro 1
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],  # Demanda Centro 2
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],  # Demanda Centro 3
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],  # Demanda Centro 4
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]   # Demanda Centro 5
    ]

    # Lado direito das restrições
    b_eq = [110, 150, 200, 80, 90, 120, 70, 100]

    # Limites das variáveis (quantidades não negativas)
    bounds = [(0, None)] * 15

    # Resolver o problema usando o método simplex revisado (HiGHS)
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs', options={"simplex_strategy": 2})  # 2 = Simplex dual

    # Medir tempo de execução e uso de memória após a execução
    end_time = time.perf_counter()
    mem_after = process.memory_info().rss / (1024 * 1024)
    memory_used = mem_after - mem_before

    # Exibir resultados
    print("\n### Resultado do Problema de Transporte (Simplex Revisado) ###")
    print(f"Tempo de execução: {end_time - start_time:.6f} s")
    print(f"Uso de memória: {memory_used:.2f} MB")
    print(f"Status: {result.message}")
    print(f"Valor ótimo encontrado: {result.fun:.6f}")

    # Exibir os valores das variáveis
    for i, value in enumerate(result.x):
        print(f"X{i//5 + 1}{i%5 + 1} = {value:.3f}")

# Executar
solve_transportation_problem()