import numpy as np
import time
import tracemalloc
import statistics
from Simplex import Simplex, PickingRule, ResultCode

def preparar_dados_simplex_revisado(n_vars, n_restricoes):
    """Gera os dados e converte para Ax <= b."""
    np.random.seed(101)
    c = np.random.randint(1, 20, size=n_vars)
    A = np.random.randint(-5, 10, size=(n_restricoes, n_vars))
    b = np.random.randint(10, 100, size=n_restricoes)
    sentidos = ['<='] * (n_restricoes // 2) + ['>='] * (n_restricoes // 2)

    A_ub, b_ub = [], []
    for i in range(n_restricoes):
        if sentidos[i] == '<=':
            A_ub.append(A[i])
            b_ub.append(b[i])
        else:
            A_ub.append(-A[i])
            b_ub.append(-b[i])
            
    return np.array(A_ub, dtype=float), np.array(b_ub, dtype=float), c

def executar_experimento_revisado():
    n_vars, n_restricoes = 10, 8
    A_ub, b_ub, c = preparar_dados_simplex_revisado(n_vars, n_restricoes)
    solver = Simplex()
    
    # --- WARM-UP (Executa uma vez fora da medição) ---
    resultado = solver.get_optimal_solution(A_ub, b_ub, c, rule=PickingRule.DANTZING_RULE)

    # --- DEBUG PARA SOLUÇÃO OTIMA ---

    # print(resultado.optimal_score)


    K_INTERACOES = 1
    # K_INTERACOES = 1
    
    # --- INÍCIO DA MEDIÇÃO ---
    tracemalloc.start()
    start_perf = time.perf_counter()
    start_cpu = time.process_time()

    for _ in range(K_INTERACOES):
        solver.get_optimal_solution(A_ub, b_ub, c, rule=PickingRule.DANTZING_RULE)

    end_cpu = time.process_time()
    end_perf = time.perf_counter()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    # --- FIM DA MEDIÇÃO ---

    return {
        "wall_time": (end_perf - start_perf) / K_INTERACOES,
        "cpu_time": (end_cpu - start_cpu) / K_INTERACOES,
        "peak_mem_mb": peak_mem / (1024 * 1024)
    }

if __name__ == "__main__":
    N_EXECUCOES = 30
    resultados = {"wall": [], "cpu": [], "mem": []}

    print(f"Iniciando benchmark Simplex Revisado: {N_EXECUCOES} amostras (1000 reps cada)...")

    for i in range(N_EXECUCOES):
        res = executar_experimento_revisado()
        resultados["wall"].append(res["wall_time"])
        resultados["cpu"].append(res["cpu_time"])
        resultados["mem"].append(res["peak_mem_mb"])

    print("\n" + "="*45)
    print("RELATÓRIO ACADÊMICO - SIMPLEX REVISADO")
    print("="*45)
    for metrica, valores in resultados.items():
        media = statistics.mean(valores)
        desvio = statistics.stdev(valores)
        print(f"{metrica.upper()}:")
        print(f"  Média: {media:.6f}")
        print(f"  Desvio Padrão: {desvio:.6f}")
        print(f"  RSD: {(desvio/media)*100:.2f}%")
        print("-" * 25)
   # print(print("Valor ótimo:", resultado.optimal_score))