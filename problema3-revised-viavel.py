import pulp
import time
import psutil

# Iniciar a medição do tempo
start_time = time.time()

# Dados do problema
n_produtos = 10
n_meses = 12
capacidade_producao = 2000
M = 10000

# Custos de produção, estoque e fixos
custos_producao = {(i, t): 10 + i + t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)}
custos_estoque = {(i, t): 2 + 0.5 * i + 0.1 * t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)}
custos_fixos = {i: 50 * i for i in range(1, n_produtos + 1)}
demandas = {(i, t): 20 + 2 * i + 5 * t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)}

# Criar o problema de minimização
prob = pulp.LpProblem("Planejamento_Producao_Com_Custos_Fixos", pulp.LpMinimize)

# Variáveis de decisão
X = pulp.LpVariable.dicts("Producao", ((i, t) for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)), lowBound=0, cat="Continuous")
S = pulp.LpVariable.dicts("Estoque", ((i, t) for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)), lowBound=0, cat="Continuous")
Y = pulp.LpVariable.dicts("Producao_Binaria", ((i, t) for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)), cat="Binary")

# Função objetivo
prob += pulp.lpSum([custos_producao[(i, t)] * X[(i, t)] + custos_estoque[(i, t)] * S[(i, t)] + custos_fixos[i] * Y[(i, t)]
                    for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)])

# Restrições de balanço de estoque
for i in range(1, n_produtos + 1):
    for t in range(1, n_meses + 1):
        if t == 1:
            prob += S[(i, t)] == X[(i, t)] - demandas[(i, t)]
        else:
            prob += S[(i, t)] == S[(i, t - 1)] + X[(i, t)] - demandas[(i, t)]

# Restrições de capacidade de produção
for t in range(1, n_meses + 1):
    prob += pulp.lpSum([X[(i, t)] for i in range(1, n_produtos + 1)]) <= capacidade_producao

# Restrições do método Big M
for i in range(1, n_produtos + 1):
    for t in range(1, n_meses + 1):
        prob += X[(i, t)] <= M * Y[(i, t)]

# Resolver o problema
prob.solve(pulp.PULP_CBC_CMD(msg=False))  # Usando o solver CBC

# Medir tempo e memória
end_time = time.time()
execution_time = end_time - start_time
process = psutil.Process()
memory_usage = process.memory_info().rss / (1024 ** 2)  # Em MB

# Exibir resultados
print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Custo Total Ótimo: R$ {pulp.value(prob.objective):.2f}")
print(f"Tempo de Execução: {execution_time:.2f} segundos")
print(f"Uso de Memória: {memory_usage:.2f} MB")