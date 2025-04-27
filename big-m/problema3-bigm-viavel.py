# Importação das bibliotecas necessárias
import pulp  # Biblioteca para modelar e resolver problemas de Programação Linear e Inteira
import time  # Biblioteca para medir o tempo de execução
import psutil  # Biblioteca para medir o uso de memória do processo

# Início da contagem de tempo para medir desempenho
start_time = time.time()

# -----------------------------
# Definição dos dados do problema
# -----------------------------

n_produtos = 10  # Número de produtos considerados
n_meses = 12     # Número de meses para planejamento de produção
capacidade_producao = 2000  # Capacidade de produção total permitida por mês
M = 10000  # Valor grande usado no método Big M para vincular produção e decisão binária

# Custos de produção: aumentam conforme o número do produto e o mês
custos_producao = {(i, t): 10 + i + t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)}

# Custos de armazenamento de estoque: aumentam conforme produto e mês
custos_estoque = {(i, t): 2 + 0.5 * i + 0.1 * t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)}

# Custos fixos para iniciar a produção de um produto (valores reduzidos)
custos_fixos = {i: 50 * i for i in range(1, n_produtos + 1)}

# Demanda por produto e por mês (valores relativamente menores)
demandas = {(i, t): 20 + 2 * i + 5 * t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)}

# -----------------------------
# Criação do modelo de otimização
# -----------------------------

# Define o problema como de minimização (minimizar os custos)
prob = pulp.LpProblem("Planejamento_Producao_Com_Custos_Fixos", pulp.LpMinimize)

# Variáveis de decisão:
# X[i,t]: quantidade produzida do produto i no mês t
# S[i,t]: quantidade em estoque do produto i ao final do mês t
# Y[i,t]: variável binária que indica se o produto i foi produzido no mês t
X = pulp.LpVariable.dicts("Producao", ((i, t) for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)), lowBound=0, cat="Continuous")
S = pulp.LpVariable.dicts("Estoque", ((i, t) for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)), lowBound=0, cat="Continuous")
Y = pulp.LpVariable.dicts("Producao_Binaria", ((i, t) for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)), cat="Binary")

# -----------------------------
# Definição da função objetivo
# -----------------------------

# A função objetivo minimiza o custo total:
# Custo de produção + Custo de armazenagem + Custo fixo para iniciar a produção
prob += pulp.lpSum(
    custos_producao[(i, t)] * X[(i, t)] +
    custos_estoque[(i, t)] * S[(i, t)] +
    custos_fixos[i] * Y[(i, t)]
    for i in range(1, n_produtos + 1)
    for t in range(1, n_meses + 1)
)

# -----------------------------
# Definição das restrições
# -----------------------------

# 1. Balanço de estoque: produz, armazena ou atende a demanda de cada produto a cada mês
for i in range(1, n_produtos + 1):
    for t in range(1, n_meses + 1):
        if t == 1:
            # No primeiro mês, não há estoque inicial
            prob += S[(i, t)] == X[(i, t)] - demandas[(i, t)]
        else:
            # Nos meses seguintes, estoque é saldo do mês anterior + produção - demanda
            prob += S[(i, t)] == S[(i, t - 1)] + X[(i, t)] - demandas[(i, t)]

# 2. Capacidade de produção: limite de produção mensal
for t in range(1, n_meses + 1):
    prob += pulp.lpSum(X[(i, t)] for i in range(1, n_produtos + 1)) <= capacidade_producao

# 3. Restrições do Big M:
# Se Y[i,t] = 0, então X[i,t] deve ser 0
# Se Y[i,t] = 1, então X[i,t] pode ser positivo (até o valor M)
for i in range(1, n_produtos + 1):
    for t in range(1, n_meses + 1):
        prob += X[(i, t)] <= M * Y[(i, t)]

# -----------------------------
# Resolução do problema
# -----------------------------

# Resolver o problema utilizando o solver padrão do PuLP (CBC)
prob.solve()

# -----------------------------
# Coleta e exibição dos resultados
# -----------------------------

# Tempo total de execução
end_time = time.time()
execution_time = end_time - start_time

# Uso de memória do processo atual
process = psutil.Process()
memory_usage = process.memory_info().rss / (1024 ** 2)  # Convertendo para megabytes

# Status da resolução (Ótimo, Inviável, etc.)
print(f"Status: {pulp.LpStatus[prob.status]}")

# Valor ótimo da função objetivo (custo mínimo)
print(f"Custo Total Ótimo: R$ {pulp.value(prob.objective):.2f}")

# Tempo de execução e memória consumida
print(f"Tempo de Execução: {execution_time:.2f} segundos")
print(f"Uso de Memória: {memory_usage:.2f} MB")

# Exibição dos valores de produção, estoque e decisão de produção
for i in range(1, n_produtos + 1):
    for t in range(1, n_meses + 1):
        print(f"X[{i},{t}] = {X[(i, t)].varValue}")  # Quantidade produzida
        print(f"S[{i},{t}] = {S[(i, t)].varValue}")  # Estoque final
        print(f"Y[{i},{t}] = {Y[(i, t)].varValue}")  # Se houve produção (1) ou não (0)
