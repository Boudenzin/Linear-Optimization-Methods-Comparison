import numpy as np
import time
import psutil
from scipy.optimize import linprog

def problema_2_robusto():
    """
    Problema 2 (média escala): alocação de recursos entre 60 projetos.
    Contém 60 variáveis, 40 restrições (mistura de ≤ e ≥), com viabilidade garantida.
    Resolve com Simplex Revisado puro.
    """

    # Iniciar medições
    start_time = time.time()
    process = psutil.Process()
    mem_before = process.memory_info().rss / (1024 ** 2)  # Memória inicial (MB)

    # -----------------------------
    # Parâmetros do problema
    # -----------------------------
    np.random.seed(202)  # Seed fixa para reprodutibilidade

    n_variaveis = 60   # Número de projetos (variáveis)
    n_restricoes = 40  # Número de restrições (equilibrada para escala média)

    # Custos aleatórios entre 5 e 30 para cada projeto
    custos = np.random.randint(5, 30, size=n_variaveis)

    # Matriz de restrições A: entre -3 e 8
    A = np.random.randint(-3, 8, size=(n_restricoes, n_variaveis))

    # Lado direito (b): entre 100 e 500
    b = np.random.randint(100, 500, size=n_restricoes)

    # Metade das restrições será ≤, metade será ≥ (Big M necessário)
    sinais = ['<='] * (n_restricoes // 2) + ['>='] * (n_restricoes // 2)

    # -----------------------------
    # Preparar restrições para linprog
    # -----------------------------
    A_ub = []
    b_ub = []

    for i in range(n_restricoes):
        if sinais[i] == '<=':
            A_ub.append(A[i])
            b_ub.append(b[i])
        else:
            # Multiplica por -1 para converter para ≤
            A_ub.append(-A[i])
            b_ub.append(-b[i])

    A_ub = np.array(A_ub)
    b_ub = np.array(b_ub)

    # -----------------------------
    # Resolver com Simplex Revisado
    # -----------------------------
    resultado = linprog(
        c=custos,
        A_ub=A_ub,
        b_ub=b_ub,
        bounds=[(0, None)] * n_variaveis,
        method='revised simplex'
    )

    # -----------------------------
    # Medições finais
    # -----------------------------
    end_time = time.time()
    mem_after = process.memory_info().rss / (1024 ** 2)
    tempo = end_time - start_time
    memoria = mem_after - mem_before

    # -----------------------------
    # Exibir resultados
    # -----------------------------
    print("\n### Resultado - Problema 2 (Robusto, Revisado) ###")
    if resultado.success:
        print(f"Status: {resultado.message}")
        print(f"Valor ótimo: {resultado.fun:.2f}")
    else:
        print("❌ Não foi possível encontrar uma solução.")

    print(f"Tempo de execução: {tempo:.4f} segundos")
    print(f"Uso de memória: {memoria:.4f} MB")

    # Valores das variáveis (parciais)
    for i, val in enumerate(resultado.x[:10]):
        print(f"x{i+1} = {val:.4f}")
    if n_variaveis > 10:
        print(f"... (exibindo apenas os 10 primeiros de {n_variaveis} projetos)")

# Executar
problema_2_robusto()
