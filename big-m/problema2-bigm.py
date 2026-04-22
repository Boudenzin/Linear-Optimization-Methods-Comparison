import numpy as np
import time
import tracemalloc
import statistics
import lpp_solver
from lpp_solver import big_M


def preparar_dados_para_lpp_solver(c, A, b, extra_coefficient_matrix, maximization='max'):
    m, n = len(A), len(c)
    M = 1000000
    coef_artificial = -M if maximization == 'max' else M
    c_mod = list(c) + [0] * m + [coef_artificial] * m
    val = [row[:] + [0] * (2 * m) for row in A]
    for i in range(m):
        val[i][n + i] = extra_coefficient_matrix[i][0]
        val[i][n + m + i] = extra_coefficient_matrix[i][1]
    return c_mod, val, b, n, extra_coefficient_matrix

def executar_experimento_problema_2():
    # --- GERAÇÃO DE DADOS 
    np.random.seed(202)
    n_vars, n_restricoes = 60, 40
    custos = np.random.randint(5, 30, size=n_vars)
    A = np.random.randint(-3, 8, size=(n_restricoes, n_vars))
    b = np.random.randint(100, 500, size=n_restricoes)
    sinais = ['<='] * (n_restricoes // 2) + ['>='] * (n_restricoes // 2)
    
    extra_coefficient_matrix = []
    for sentido in sinais:
        if sentido == '<=': extra_coefficient_matrix.append([1, 0])
        elif sentido == '>=': extra_coefficient_matrix.append([-1, 1])
        else: extra_coefficient_matrix.append([0, 1])

    c_mod, val, b_list, no_vars, extra_m = preparar_dados_para_lpp_solver(
        custos.tolist(), A.tolist(), b.tolist(), extra_coefficient_matrix, maximization='max'
    )

    # --- CONFIGURAÇÃO DO BENCHMARK ---
    K_REPS_INTERNAS = 1
    lpp_solver.maximization = 'max'

    # Warm-up (essencial para carregar bibliotecas na RAM)
    big_M(c_mod, val, b_list, no_vars, extra_coefficient_matrix)

    # --- MEDIÇÃO ---
    tracemalloc.start()
    start_perf = time.perf_counter()
    start_cpu = time.process_time()

    for _ in range(K_REPS_INTERNAS):
        big_M(c_mod, val, b_list, no_vars, extra_coefficient_matrix)

    end_cpu = time.process_time()
    end_perf = time.perf_counter()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "wall_time": (end_perf - start_perf) / K_REPS_INTERNAS,
        "cpu_time": (end_cpu - start_cpu) / K_REPS_INTERNAS,
        "peak_mem_mb": peak_mem / (1024 * 1024)
    }

if __name__ == "__main__":
    N_AMOSTRAS = 30
    resultados = {"wall": [], "cpu": [], "mem": []}

    print(f"Iniciando Benchmark Problema 2 (60x40): {N_AMOSTRAS} amostras...")

    for i in range(N_AMOSTRAS):
        res = executar_experimento_problema_2()
        resultados["wall"].append(res["wall_time"])
        resultados["cpu"].append(res["cpu_time"])
        resultados["mem"].append(res["peak_mem_mb"])
        if (i+1) % 5 == 0: print(f"Progresso: {i+1}/{N_AMOSTRAS}")

    print("\n" + "="*50)
    print("RELATÓRIO ACADÊMICO - BIG M (PROBLEMA 2 - 60x40)")
    print("="*50)
    for metrica, valores in resultados.items():
        media = statistics.mean(valores)
        desvio = statistics.stdev(valores)
        print(f"{metrica.upper()}:")
        print(f"  Média: {media:.6f}")
        print(f"  Desvio Padrão: {desvio:.6f}")
        print(f"  RSD (Variabilidade): {(desvio/media)*100:.2f}%")
        print("-" * 30)