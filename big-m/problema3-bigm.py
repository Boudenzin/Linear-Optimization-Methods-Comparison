import numpy as np
import time
import tracemalloc
import statistics
import lpp_solver
from lpp_solver import big_M

def preparar_dados_balanceamento_para_lpp_solver(custos, capacidades_fabricas, demandas_centros, maximization='max'):
    n_fabricas = len(capacidades_fabricas)
    n_centros = len(demandas_centros)
    n_variaveis = n_fabricas * n_centros
    n_restricoes = n_fabricas + n_centros
    M = 1000000
    
    A = []
    # Restrições de capacidade (≤)
    for i in range(n_fabricas):
        row = [0] * n_variaveis
        for j in range(n_centros):
            row[i * n_centros + j] = 1
        A.append(row)
    # Restrições de demanda (≥)
    for j in range(n_centros):
        row = [0] * n_variaveis
        for i in range(n_fabricas):
            row[i * n_centros + j] = 1
        A.append(row)
    
    b = list(capacidades_fabricas) + list(demandas_centros)
    extra_coefficient_matrix = [[1, 0] for _ in range(n_fabricas)] + [[-1, 1] for _ in range(n_centros)]
    
    coef_artificial = -M if maximization == 'max' else M
    c_mod = list(custos) + [0] * n_restricoes + [coef_artificial] * n_restricoes
    val = [row[:] + [0] * (2 * n_restricoes) for row in A]
    
    for i in range(n_restricoes):
        val[i][n_variaveis + i] = extra_coefficient_matrix[i][0]
        val[i][n_variaveis + n_restricoes + i] = extra_coefficient_matrix[i][1]
    
    return c_mod, val, b, n_variaveis, extra_coefficient_matrix

def executar_experimento_problema_3_max():
    # --- PARÂMETROS FIXOS (15 fábricas x 10 centros = 150 variáveis) ---
    n_fabricas, n_centros = 15, 10
    n_variaveis = n_fabricas * n_centros
    np.random.seed(42)
    
    lucros = np.random.randint(10, 100, size=n_variaveis)
    capacidades = np.random.randint(500, 1500, size=n_fabricas)
    demandas = np.random.randint(200, 800, size=n_centros)
    
    c_mod, val, b_list, no_vars, extra_m = preparar_dados_balanceamento_para_lpp_solver(
        lucros.tolist(), capacidades.tolist(), demandas.tolist(), maximization='max'
    )

    # --- CONFIGURAÇÃO DO BENCHMARK ---
    K_REPS_INTERNAS = 10
    lpp_solver.maximization = 'max'

    # Warm-up (essencial para carregar bibliotecas e o solver na memória)
    big_M(c_mod, val, b_list, no_vars, extra_m)

    # --- MEDIÇÃO ---
    tracemalloc.start()
    start_perf = time.perf_counter()
    start_cpu = time.process_time()

    for _ in range(K_REPS_INTERNAS):
        big_M(c_mod, val, b_list, no_vars, extra_m)

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

    print(f"Iniciando Benchmark P3 (Big M - 150x25): {N_AMOSTRAS} amostras...")

    for i in range(N_AMOSTRAS):
        res = executar_experimento_problema_3_max()
        resultados["wall"].append(res["wall_time"])
        resultados["cpu"].append(res["cpu_time"])
        resultados["mem"].append(res["peak_mem_mb"])
        
        # O print com -u no docker mostrará isso em tempo real
        print(f"Progresso: {i+1}/{N_AMOSTRAS} | CPU Time: {res['cpu_time']:.4f}s")

    print("\n" + "="*55)
    print("RELATÓRIO ACADÊMICO - BIG M (PROBLEMA 3 - 150x25)")
    print("="*55)
    for metrica, valores in resultados.items():
        media = statistics.mean(valores)
        desvio = statistics.stdev(valores)
        print(f"{metrica.upper()}:")
        print(f"  Média: {media:.6f}")
        print(f"  Desvio Padrão: {desvio:.6f}")
        print(f"  RSD (Variabilidade): {(desvio/media)*100:.2f}%")
        print("-" * 35)