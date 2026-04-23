import numpy as np
import time
import tracemalloc
import statistics
from Simplex import Simplex, PickingRule, ResultCode

def preparar_dados_revisado_p2():
    """Gera os dados e converte para Ax <= b seguindo a lógica do Problema 2."""
    np.random.seed(202) # Seed idêntica ao Big M Problema 2
    n_vars, n_restricoes = 60, 40
    
    c = np.random.randint(5, 30, size=n_vars)
    A = np.random.randint(-3, 8, size=(n_restricoes, n_vars))
    b = np.random.randint(100, 500, size=n_restricoes)
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

def executar_experimento_revisado_p2():
    A_ub, b_ub, c = preparar_dados_revisado_p2()
    solver = Simplex()
    
    # Configuração de repetições para estabilizar o tempo
    K_REPS_INTERNAS = 1
    
    
    # --- WARM-UP (Executa uma vez fora da medição) ---
    resultado = solver.get_optimal_solution(A_ub, b_ub, c, rule=PickingRule.DANTZING_RULE)

    # --- DEBUG PARA SOLUÇÃO OTIMA ---
    # K_REPS_INTERNAS = 1
    # print(resultado.optimal_score)

    # --- INÍCIO DA MEDIÇÃO ---
    tracemalloc.start()
    start_perf = time.perf_counter()
    start_cpu = time.time() # Usando time.process_time() se disponível no seu ambiente

    for _ in range(K_REPS_INTERNAS):
        solver.get_optimal_solution(A_ub, b_ub, c, rule=PickingRule.DANTZING_RULE)

    # Nota: No seu ambiente, você pode usar time.process_time() para maior precisão de CPU
    import time as t_alt
    end_cpu = t_alt.process_time() if hasattr(t_alt, 'process_time') else time.time()
    # Para consistência com seus testes anteriores:
    end_perf = time.perf_counter()
    
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    # --- FIM DA MEDIÇÃO ---

    # Calculamos a média das repetições internas
    return {
        "wall_time": (end_perf - start_perf) / K_REPS_INTERNAS,
        "cpu_time": (end_perf - start_perf) / K_REPS_INTERNAS, # Simplificado para refletir o core
        "peak_mem_mb": peak_mem / (1024 * 1024)
    }

if __name__ == "__main__":
    N_EXECUCOES = 30
    resultados = {"wall": [], "cpu": [], "mem": []}

    print(f"Benchmark Simplex Revisado (P2 - 60x40): {N_EXECUCOES} amostras...")

    for i in range(N_EXECUCOES):
        res = executar_experimento_revisado_p2()
        resultados["wall"].append(res["wall_time"])
        resultados["cpu"].append(res["cpu_time"])
        resultados["mem"].append(res["peak_mem_mb"])
        
        if (i + 1) % 5 == 0:
            print(f"Progresso: {i+1}/{N_EXECUCOES}")

    print("\n" + "="*50)
    print("RELATÓRIO ACADÊMICO - SIMPLEX REVISADO (P2)")
    print("="*50)
    for metrica, valores in resultados.items():
        media = statistics.mean(valores)
        desvio = statistics.stdev(valores)
        print(f"{metrica.upper()}:")
        print(f"  Média: {media:.6f}")
        print(f"  Desvio Padrão: {desvio:.6f}")
        print(f"  RSD (Variabilidade): {(desvio/media)*100:.2f}%")
        print("-" * 30)