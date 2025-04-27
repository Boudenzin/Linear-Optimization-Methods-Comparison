# Importação das bibliotecas necessárias
import numpy as np  # Biblioteca para operações matriciais
import time  # Biblioteca para medir o tempo de execução
import psutil  # Biblioteca para medir o uso de memória do processo
import os  # Biblioteca para acessar informações do sistema operacional

def simplex_revisado_puro(c, A, b):
    """
    Implementação do Método Simplex Revisado puro, sem Big M.
    
    Resolve problemas de Programação Linear com todas as restrições no formato ≤.
    
    Parâmetros:
    - c: vetor de custos da função objetivo (a maximizar).
    - A: matriz de coeficientes das restrições (no formato ≤).
    - b: vetor do lado direito das restrições.

    Retorna:
    - vetor solução x (variáveis originais).
    """

    n = len(c)  # Número de variáveis originais
    m = len(b)  # Número de restrições

    # Ajusta o problema para maximização: cria matriz extendida com variáveis de folga
    A_ext = np.hstack([A, np.identity(m)])  # Adiciona uma variável de folga para cada restrição

    # Ajusta o vetor de custos (custos das variáveis de folga são zero)
    c_ext = np.array(c + [0] * m, dtype=float)

    # Definimos a base inicial: as variáveis de folga
    base = list(range(n, n + m))  # índices das variáveis de folga
    non_base = list(range(n))     # índices das variáveis originais

    # Matrizes iniciais
    B = A_ext[:, base]  # Colunas correspondentes às variáveis básicas
    N = A_ext[:, non_base]  # Colunas correspondentes às variáveis não básicas
    B_inv = np.linalg.inv(B)  # Inversa da matriz básica

    # -----------------------------
    # Início do algoritmo iterativo do Simplex Revisado
    # -----------------------------

    while True:
        # Solução básica atual
        x_B = B_inv @ b

        # Custos das variáveis básicas e não básicas
        c_B = c_ext[base]
        c_N = c_ext[non_base]

        # Multiplicadores simplex
        lambda_ = c_B @ B_inv

        # Custos reduzidos
        r_N = c_N - lambda_ @ N

        # Critério de parada: se todos os custos reduzidos forem <= 0, encontramos a solução ótima
        if np.all(r_N <= 0):
            break

        # Variável de entrada: aquela com maior custo reduzido positivo
        entering_idx = np.argmax(r_N)
        entering = non_base[entering_idx]

        # Direção de movimento no espaço das variáveis básicas
        d_B = B_inv @ A_ext[:, entering]

        # Teste de ilimitabilidade
        if np.all(d_B <= 0):
            raise Exception("Problema ilimitado.")

        # Regra do mínimo quociente
        ratios = np.array([x_B[i] / d_B[i] if d_B[i] > 0 else np.inf for i in range(len(d_B))])
        leaving_idx = np.argmin(ratios)
        leaving = base[leaving_idx]

        # Atualiza base e não-base
        base[leaving_idx] = entering
        non_base[entering_idx] = leaving

        # Atualiza as matrizes B, B_inv e N
        B = A_ext[:, base]
        B_inv = np.linalg.inv(B)
        N = A_ext[:, non_base]

    # Reconstrói o vetor solução completo
    x = np.zeros(n + m)
    x[base] = x_B

    # Retorna apenas as variáveis originais
    return x[:n]

# -----------------------------
# Execução prática e coleta de dados
# -----------------------------

# Medir memória antes de resolver
process = psutil.Process(os.getpid())
mem_before = process.memory_info().rss / (1024 * 1024)  # Memória antes (em MB)

# Medir tempo de execução
start_time = time.perf_counter()

# Definição dos dados do problema
c = [1, 2]  # Função objetivo: Maximizar x + 2y
A = [
    [1, 1],    # x + y <= 5
    [-1, 1]    # -x + y <= -1  (transformação da desigualdade ≥ para ≤)
]
b = [5, -1]  # Lados direitos das restrições

# Resolver o problema
solucao = simplex_revisado_puro(c, A, b)

# Medir tempo e memória após resolver
end_time = time.perf_counter()
mem_after = process.memory_info().rss / (1024 * 1024)  # Memória depois (em MB)

# -----------------------------
# Impressão dos resultados
# -----------------------------

# Mostra a solução ótima encontrada
print(f"Solução ótima: x = {solucao[0]:.3f}, y = {solucao[1]:.3f}")

# Mostra o tempo de execução
print(f"Tempo de execução: {end_time - start_time:.6f} segundos")

# Mostra o uso de memória
print(f"Uso de memória: {mem_after - mem_before:.6f} MB")
