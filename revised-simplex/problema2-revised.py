# Importação das bibliotecas necessárias
import numpy as np  # Biblioteca para operações numéricas (não usada diretamente aqui, mas importada)
from scipy.optimize import linprog  # Função para resolver problemas de Programação Linear
import time  # Biblioteca para medir o tempo de execução
import psutil  # Biblioteca para medir o uso de memória do processo
import os  # Biblioteca para acessar informações do sistema operacional

def solve_transportation_problem():
    """
    Resolve um problema clássico de transporte usando o método Simplex Revisado (HiGHS).
    
    Minimiza o custo total de transporte, respeitando as capacidades de produção das fábricas
    e as demandas dos centros de distribuição.
    """

    # Medição de memória antes da execução
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024)  # Memória em MB

    # Início da medição do tempo de execução
    start_time = time.perf_counter()

    # -----------------------------
    # Definição dos dados do problema
    # -----------------------------

    # Vetor de custos de transporte (custo unitário de enviar produtos)
    c = [5, 3, 6, 2, 7, 4, 6, 3, 5, 8, 7, 4, 2, 6, 3]

    # Matriz de coeficientes das restrições (A_eq)
    # Cada linha representa uma capacidade ou uma demanda
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

    # Lados direitos das restrições (b_eq)
    b_eq = [110, 150, 200, 80, 90, 120, 70, 100]

    # Limites das variáveis (quantidades não podem ser negativas)
    bounds = [(0, None)] * 15

    # -----------------------------
    # Resolução do problema
    # -----------------------------

    # Resolver usando o método 'highs' da SciPy, com estratégia 2 (Simplex Dual)
    result = linprog(
        c,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds,
        method='highs',
        options={"simplex_strategy": 2}  # 2 = simplex dual (focado em estabilidade e eficiência)
    )

    # -----------------------------
    # Medição de tempo e memória depois da execução
    # -----------------------------

    end_time = time.perf_counter()
    mem_after = process.memory_info().rss / (1024 * 1024)
    memory_used = mem_after - mem_before

    # -----------------------------
    # Impressão dos resultados
    # -----------------------------

    print("\n### Resultado do Problema de Transporte (Simplex Revisado) ###")
    print(f"Tempo de execução: {end_time - start_time:.6f} s")
    print(f"Uso de memória: {memory_used:.2f} MB")
    print(f"Status: {result.message}")
    print(f"Valor ótimo encontrado: {result.fun:.6f}")

    # Exibição dos valores das variáveis de decisão (quantidades enviadas)
    for i, value in enumerate(result.x):
        print(f"X{i//5 + 1}{i%5 + 1} = {value:.3f}")

# Executar a função
solve_transportation_problem()
