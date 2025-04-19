import numpy as np
import time
import psutil
import os

def simplex_revisado(c, A, b, M):
    n = len(c)
    m = len(b)

    # Adiciona variáveis de folga e artificiais às restrições
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    A_ext = np.hstack([A, np.zeros((m, 3))])  # Adiciona 3 colunas extras (s1, s2, a1)

    # Ajusta as colunas específicas: s1 na restrição 1, s2 e a1 na restrição 2
    A_ext[0, n] = 1       # s1
    A_ext[1, n+1] = -1    # s2
    A_ext[1, n+2] = 1     # a1

    # Função objetivo com penalização da artificial
    c_ext = np.array(c + [0, 0, -M], dtype=float)

    # Base inicial: s1 e a1
    base = [n, n+2]
    non_base = [0, 1, n+1]

    B = A_ext[:, base]
    N = A_ext[:, non_base]
    B_inv = np.linalg.inv(B)

    while True:
        x_B = B_inv @ b
        c_B = c_ext[base]
        c_N = c_ext[non_base]

        lambda_ = c_B @ B_inv
        r_N = c_N - lambda_ @ N

        if np.all(r_N <= 0):
            break

        entering_idx = np.argmax(r_N)
        entering = non_base[entering_idx]

        d_B = B_inv @ A_ext[:, entering]

        if np.all(d_B <= 0):
            raise Exception("Problema ilimitado.")

        ratios = np.array([x_B[i]/d_B[i] if d_B[i] > 0 else np.inf for i in range(len(d_B))])
        leaving_idx = np.argmin(ratios)
        leaving = base[leaving_idx]

        base[leaving_idx] = entering
        non_base[entering_idx] = leaving

        B = A_ext[:, base]
        B_inv = np.linalg.inv(B)
        N = A_ext[:, non_base]

    x = np.zeros(n + 3)
    x[base] = x_B
    return x[:n]

# --- Medição de tempo e memória ---
process = psutil.Process(os.getpid())
mem_before = process.memory_info().rss / (1024 * 1024)  # Memória antes (em MB)
start_time = time.perf_counter()

# Dados do problema
c = [1, 2]
A = [[1, 1], [1, -1]]
b = [5, 1]
M = 1000

solucao = simplex_revisado(c, A, b, M)

end_time = time.perf_counter()
mem_after = process.memory_info().rss / (1024 * 1024)  # Memória depois (em MB)

# Resultados
print(f"Solução ótima: x = {solucao[0]:.3f}, y = {solucao[1]:.3f}")
print(f"Tempo de execução: {end_time - start_time:.6f} segundos")
print(f"Uso de memória: {mem_after - mem_before:.6f} MB")
