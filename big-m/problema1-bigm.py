# Importação das bibliotecas
import numpy as np
import time
import tracemalloc
import statistics
import lpp_solver
from lpp_solver import big_M

def preparar_dados_para_lpp_solver(c, A, b, extra_coefficient_matrix, maximization='max'):
    """
    Prepara os dados no formato esperado pelo lpp_solver.big_M()
    
    Parâmetros:
    - c: lista de coeficientes da função objetivo (tamanho n_vars)
    - A: matriz de coeficientes das restrições (n_restricoes x n_vars)
    - b: lado direito das restrições (tamanho n_restricoes)
    - extra_coefficient_matrix: lista de pares [coef_folga, coef_artificial] para cada restrição
      * [1, 0] para '≤' (adiciona variável de folga, sem artificial)
      * [-1, 1] para '≥' (adiciona surplus negativa + artificial)
      * [0, 1] para '=' (adiciona artificial)
    - maximization: 'max' ou 'min'
    
    Retorna:
    - c_mod: função objetivo com coeficientes zerados para folgas e -M para artificiais (maximização)
    - val: matriz aumentada do sistema (incluindo folgas e artificiais)
    - b: lado direito (inalterado)
    - no_of_variables: número original de variáveis
    - extra_coefficient_matrix: inalterado
    """
    m = len(A)  # número de restrições
    n = len(c)  # número de variáveis originais
    M = 1000000  # mesmo valor definido no lpp_solver
    
    # 1. Modifica função objetivo para incluir folgas (coef 0) e artificiais
    if maximization == 'max':
        # Para maximização: artificiais têm coeficiente -M (penalidade negativa)
        coef_artificial = -M
    else:  # min
        # Para minimização: o solver converte internamente para maximização
        # Portanto, artificiais devem ter coeficiente +M (será negativado na conversão)
        coef_artificial = M
    
    # Coeficientes: [variáveis originais] + [folgas com 0] + [artificiais com coef_artificial]
    c_mod = list(c) + [0] * m + [coef_artificial] * m
    
    # 2. Constrói a matriz aumentada val
    # Inicializa com zeros para colunas de folgas e artificiais
    val = [row[:] + [0] * (2 * m) for row in A]
    
    # Preenche as colunas de folgas e artificiais baseado no extra_coefficient_matrix
    for i in range(m):
        # Coluna da variável de folga (posição n + i)
        val[i][n + i] = extra_coefficient_matrix[i][0]
        # Coluna da variável artificial (posição n + m + i)
        val[i][n + m + i] = extra_coefficient_matrix[i][1]
    
    return c_mod, val, b, n, extra_coefficient_matrix





def problema_1_bigm():
    """
    Problema 1 (pequena escala) com 10 variáveis e 8 restrições, resolvido com Big M.
    Adiciona variáveis artificiais para restrições do tipo 'maior ou igual' (≥) e penaliza na função objetivo.
    """

    # Geração de dados (fixar seed para reprodutibilidade)
    np.random.seed(101)
    n_vars, n_restricoes = 10, 8
    c = np.random.randint(1, 20, size=n_vars)
    A = np.random.randint(-5, 10, size=(n_restricoes, n_vars))
    b = np.random.randint(10, 100, size=n_restricoes)
    sentidos = ['<='] * (n_restricoes // 2) + ['>='] * (n_restricoes // 2)
    
    extra_coefficient_matrix = [[1, 0] if s == '<=' else [-1, 1] for s in sentidos]
    
    
    c_mod, val, b_list, n_orig, extra_m = preparar_dados_para_lpp_solver(
        c.tolist(), A.tolist(), b.tolist(), extra_coefficient_matrix, maximization='max'
    )


    # --- INÍCIO DA MEDIÇÃO ---

    K_INTERACOES = 500
    # K_INTERACOES = 1 
    tracemalloc.start()
    start_perf = time.perf_counter()
    start_cpu = time.process_time()

    # Execução do Solver
    lpp_solver.maximization = 'max'
    # Silenciamos prints internos do solver para não sujar o log/influenciar tempo
    for _ in range(K_INTERACOES):
        lpp_solver.big_M(c_mod, val, b_list, n_orig, extra_coefficient_matrix)
    
    end_cpu = time.process_time()
    end_perf = time.perf_counter()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    # --- FIM DA MEDIÇÃO ---

    return {
        "wall_time": end_perf - start_perf,
        "cpu_time": end_cpu - start_cpu,
        "peak_mem_mb": peak_mem / (1024 * 1024)
    }

if __name__ == "__main__":
    N_EXECUCOES = 30
    resultados = {"wall": [], "cpu": [], "mem": []}

    print(f"Iniciando benchmark: {N_EXECUCOES} execuções...")

    for i in range(N_EXECUCOES):
        res = problema_1_bigm()
        resultados["wall"].append(res["wall_time"])
        resultados["cpu"].append(res["cpu_time"])
        resultados["mem"].append(res["peak_mem_mb"])

    print("\n" + "="*40)
    print("RELATÓRIO ACADÊMICO DE PERFORMANCE")
    print("="*40)
    for metrica, valores in resultados.items():
        media = statistics.mean(valores)
        desvio = statistics.stdev(valores)
        print(f"{metrica.upper()}:")
        print(f"  Média: {media:.6f}")
        print(f"  Desvio Padrão: {desvio:.6f}")
        print(f"  RSD (Variabilidade): {(desvio/media)*100:.2f}%")
        print("-" * 20)
    print()