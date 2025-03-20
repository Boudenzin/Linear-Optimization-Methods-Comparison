import numpy as np
from scipy.optimize import linprog
import time
import psutil
import os

# Medição de tempo e memória
start_time = time.time()
process = psutil.Process(os.getpid())
mem_before = process.memory_info().rss / (1024 ** 2)

# Parâmetros do problema
n_produtos = 10
n_meses = 12
capacidade_producao = 2000
M = 10000

# Índices auxiliares
idx = lambda i, t: (i - 1) * n_meses + (t - 1)

# Custos
custos_producao = [10 + i + t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)]
custos_estoque = [2 + 0.5 * i + 0.1 * t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)]
custos_fixos = [50 * i for i in range(1, n_produtos + 1)]
custos_fixos_expandido = [custos_fixos[i - 1] for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)]

# Demandas
demandas = [20 + 2 * i + 5 * t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)]

# Variáveis: X[i,t], S[i,t], Y[i,t] => total 3 * n_produtos * n_meses
num_vars = n_produtos * n_meses
total_vars = 3 * num_vars

# Função objetivo
c = custos_producao + custos_estoque + custos_fixos_expandido

# Restrições de igualdade (balanço de estoque)
A_eq = []
b_eq = []

for i in range(1, n_produtos + 1):
    for t in range(1, n_meses + 1):
        row = [0.0] * total_vars
        x_idx = idx(i, t)
        s_idx = num_vars + idx(i, t)
        if t == 1:
            # S[i,1] - X[i,1] = -demandas[i,1]
            row[x_idx] = -1
            row[s_idx] = 1
            b_eq.append(-demandas[idx(i, t)])
        else:
            s_prev_idx = num_vars + idx(i, t - 1)
            row[s_prev_idx] = 1
            row[x_idx] = -1
            row[s_idx] = -1
            b_eq.append(-demandas[idx(i, t)])
        A_eq.append(row)

# Restrição de capacidade por mês: somatório X[i,t] <= capacidade
A_ub = []
b_ub = []

for t in range(1, n_meses + 1):
    row = [0.0] * total_vars
    for i in range(1, n_produtos + 1):
        x_idx = idx(i, t)
        row[x_idx] = 1
    A_ub.append(row)
    b_ub.append(capacidade_producao)

# Restrição Big M: X[i,t] - M*Y[i,t] <= 0
for i in range(1, n_produtos + 1):
    for t in range(1, n_meses + 1):
        row = [0.0] * total_vars
        x_idx = idx(i, t)
        y_idx = 2 * num_vars + idx(i, t)
        row[x_idx] = 1
        row[y_idx] = -M
        A_ub.append(row)
        b_ub.append(0)

# Bounds: [0, None] para X e S; [0,1] para Y (relaxação binária)
bounds = [(0, None)] * (2 * num_vars) + [(0, 1)] * num_vars

# Resolver com o Simplex Revisado
res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
              bounds=bounds, method='revised simplex')

# Medição de tempo e memória
end_time = time.time()
execution_time = end_time - start_time
mem_after = process.memory_info().rss / (1024 ** 2)
memory_usage = mem_after - mem_before

# Resultados
if res.success:
    print(f"Status: {res.message}")
    print(f"Custo Total Ótimo: R$ {res.fun:.2f}")
else:
    print("Problema não resolvido:", res.message)

print(f"Tempo de Execução: {execution_time:.2f} segundos")
print(f"Uso de Memória: {memory_usage:.2f} MB")

# Exibir variáveis de decisão (opcional)
X_vals = res.x[:num_vars]
S_vals = res.x[num_vars:2*num_vars]
Y_vals = res.x[2*num_vars:]

for i in range(1, n_produtos + 1):
    for t in range(1, n_meses + 1):
        idx_ = idx(i, t)
        print(f"X[{i},{t}] = {X_vals[idx_]:.2f}, S[{i},{t}] = {S_vals[idx_]:.2f}, Y[{i},{t}] = {Y_vals[idx_]:.2f}")
