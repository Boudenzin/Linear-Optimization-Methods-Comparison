import numpy as np
import time
import tracemalloc
import statistics
from Simplex import Simplex, PickingRule, ResultCode

def preparar_dados_revisado_p3():
    """Gera dados de transporte (150 vars, 25 restrições) para Simplex Revisado."""
    n_fabricas, n_centros = 15, 10
    n_vars = n_fabricas * n_centros
    np.random.seed(42) # Seed consistente com o Big M P3
    
    custos = np.random.randint(10, 100, size=n_vars)
    capacidades = np.random.randint(500, 1500, size=n_fabricas)
    demandas = np.random.randint(200, 800, size=n_centros)
    
    A_ub, b_ub = [], []
    
    # Restrições de capacidade (Σ x_ij <= cap_i)
    for i in range(n_fabricas):
        row = np.zeros(n_vars)
        for j in range(n_centros):
            row[i * n_centros + j] = 1
        A_ub.append(row)
        b_ub.append(capacidades[i])
    
    # Restrições de demanda (Σ x_ij >= dem_j -> -Σ x_ij <= -dem_j)
    for j in range(n_centros):
        row = np.zeros(n_vars)
        for i in range(n_fabricas):
            row[i * n_centros + j] = -1
        A_ub.append(row)
        b_ub.append(-demandas[j])
        
    return np.array(A_ub, dtype=float), np.array(b_ub, dtype=float), custos

def executar_experimento_revisado_p3():
    A_ub, b_ub, c = preparar_dados_revisado_p3()
    solver = Simplex()
    
    # 100 repetições para diluir o custo de inicialização do Python
    K_REPS_INTERNAS = 100 
    
    # --- WARM-UP ---
    resultado = solver.get_optimal_solution(A_ub, b_ub, c, rule=PickingRule.DANTZING_RULE)

    # --- DEBUG PARA SOLUÇÃO OTIMA ---
    # K_REPS_INTERNAS = 1
    # print(resultado.optimal_score)

    # --- INÍCIO DA MEDIÇÃO ---
    tracemalloc.start()
    start_perf = time.perf_counter()
    start_cpu = time.process_time()

    for _ in range(K_REPS_INTERNAS):
        solver.get_optimal_solution(A_ub, b_ub, c, rule=PickingRule.DANTZING_RULE)

    end_cpu = time.process_time()
    end_perf = time.perf_counter()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    # --- FIM DA MEDIÇÃO ---

    return {
        "wall_time": (end_perf - start_perf) / K_REPS_INTERNAS,
        "cpu_time": (end_cpu - start_cpu) / K_REPS_INTERNAS,
        "peak_mem_mb": peak_mem / (1024 * 1024)
    }

if __name__ == "__main__":
    N_EXECUCOES = 30
    resultados = {"wall": [], "cpu": [], "mem": []}

    print(f"Benchmark Simplex Revisado (P3 - 150x25): {N_EXECUCOES} amostras (100 reps/cada)...")

    for i in range(N_EXECUCOES):
        res = executar_experimento_revisado_p3()
        resultados["wall"].append(res["wall_time"])
        resultados["cpu"].append(res["cpu_time"])
        resultados["mem"].append(res["peak_mem_mb"])
        
        if (i + 1) % 5 == 0:
            print(f"Progresso: {i+1}/{N_EXECUCOES}")

    print("\n" + "="*55)
    print("RELATÓRIO ACADÊMICO - SIMPLEX REVISADO (P3 - 150x25)")
    print("="*55)
    for metrica, valores in resultados.items():
        media = statistics.mean(valores)
        desvio = statistics.stdev(valores)
        print(f"{metrica.upper()}:")
        print(f"  Média: {media:.6f}")
        print(f"  Desvio Padrão: {desvio:.6f}")
        print(f"  RSD (Variabilidade): {(desvio/media)*100:.2f}%")
        print("-" * 35)