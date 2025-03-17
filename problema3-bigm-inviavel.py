import pulp
import time
import psutil

# Iniciar a medição do tempo
start_time = time.time()

# Dados do problema
n_produtos = 10
n_meses = 12
capacidade_producao = 1000  # Capacidade de produção mensal
M = 10000  # Valor grande o suficiente para o método Big M

# Custos de produção (exemplo fictício: custo aumenta com o produto e o mês)
custos_producao = {(i, t): 10 + i + t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)}

# Custos de estoque (exemplo fictício: custo aumenta com o produto e o mês)
custos_estoque = {(i, t): 2 + 0.5 * i + 0.1 * t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)}

# Custos fixos (exemplo fictício: custo fixo para iniciar a produção de um produto)
custos_fixos = {i: 100 * i for i in range(1, n_produtos + 1)}  # Custo fixo aumenta com o produto

# Demandas (exemplo fictício: demanda aumenta com o produto e o mês)
demandas = {(i, t): 50 + 5 * i + 10 * t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)}

# Criar o problema de minimização
prob = pulp.LpProblem("Planejamento_Producao_Com_Custos_Fixos", pulp.LpMinimize)

# Variáveis de decisão
X = pulp.LpVariable.dicts("Producao", ((i, t) for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)), lowBound=0, cat="Continuous")
S = pulp.LpVariable.dicts("Estoque", ((i, t) for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)), lowBound=0, cat="Continuous")
Y = pulp.LpVariable.dicts("Producao_Binaria", ((i, t) for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)), cat="Binary")

# Função objetivo: Minimizar custos de produção, estoque e custos fixos
prob += pulp.lpSum([custos_producao[(i, t)] * X[(i, t)] + custos_estoque[(i, t)] * S[(i, t)] + custos_fixos[i] * Y[(i, t)]
                    for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)])

# Restrições de balanço de estoque
for i in range(1, n_produtos + 1):
    for t in range(1, n_meses + 1):
        if t == 1:
            # Estoque inicial é zero
            prob += S[(i, t)] == X[(i, t)] - demandas[(i, t)]
        else:
            # Estoque no mês t = Estoque no mês t-1 + Produção no mês t - Demanda no mês t
            prob += S[(i, t)] == S[(i, t - 1)] + X[(i, t)] - demandas[(i, t)]

# Restrições de capacidade de produção
for t in range(1, n_meses + 1):
    prob += pulp.lpSum([X[(i, t)] for i in range(1, n_produtos + 1)]) <= capacidade_producao

# Restrições do método Big M
for i in range(1, n_produtos + 1):
    for t in range(1, n_meses + 1):
        # Se Y[(i, t)] = 0, então X[(i, t)] = 0
        # Se Y[(i, t)] = 1, então X[(i, t)] pode ser maior que 0 (limitado por M)
        prob += X[(i, t)] <= M * Y[(i, t)]

# Resolver o problema
prob.solve()

# Medir o tempo de execução
end_time = time.time()
execution_time = end_time - start_time

# Medir o uso de memória
process = psutil.Process()
memory_usage = process.memory_info().rss / (1024 ** 2)  # Em MB

# Exibir resultados
print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Custo Total Ótimo: R$ {pulp.value(prob.objective):.2f}")
print(f"Tempo de Execução: {execution_time:.2f} segundos")
print(f"Uso de Memória: {memory_usage:.2f} MB")

# Exibir valores das variáveis de decisão (opcional)
for i in range(1, n_produtos + 1):
    for t in range(1, n_meses + 1):
        print(f"X[{i},{t}] = {X[(i, t)].varValue}")  # Produção
        print(f"S[{i},{t}] = {S[(i, t)].varValue}")  # Estoque
        print(f"Y[{i},{t}] = {Y[(i, t)].varValue}")  # Decisão binária (produção ocorreu?)