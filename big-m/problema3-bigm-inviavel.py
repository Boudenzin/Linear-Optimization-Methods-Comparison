# Importação das bibliotecas necessárias
import pulp  # Biblioteca para modelar e resolver problemas de Programação Linear e Inteira
import time  # Biblioteca para medir o tempo de execução
import psutil  # Biblioteca para medir o uso de memória

# Início da contagem de tempo para medir desempenho
start_time = time.time()

# -----------------------------
# Definição dos dados do problema
# -----------------------------

n_produtos = 10  # Número de produtos diferentes
n_meses = 12     # Número de meses no horizonte de planejamento
capacidade_producao = 1000  # Capacidade máxima de produção por mês
M = 10000  # Valor grande usado no método Big M para ativar/desativar variáveis

# Custos de produção para cada produto em cada mês
# (Aumentam conforme o índice do produto e o mês)
custos_producao = {(i, t): 10 + i + t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)}

# Custos de estoque para armazenar produtos
custos_estoque = {(i, t): 2 + 0.5 * i + 0.1 * t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)}

# Custos fixos para iniciar a produção de um produto
custos_fixos = {i: 100 * i for i in range(1, n_produtos + 1)}

# Demandas previstas para cada produto e mês
demandas = {(i, t): 50 + 5 * i + 10 * t for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)}

# -----------------------------
# Criação do modelo de otimização
# -----------------------------

# Define que o objetivo é minimizar o custo total
prob = pulp.LpProblem("Planejamento_Producao_Com_Custos_Fixos", pulp.LpMinimize)

# Variáveis de decisão:
# X[i,t]: quantidade de produto i produzido no mês t
# S[i,t]: estoque de produto i no fim do mês t
# Y[i,t]: variável binária indicando se houve produção do produto i no mês t
X = pulp.LpVariable.dicts("Producao", ((i, t) for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)), lowBound=0, cat="Continuous")
S = pulp.LpVariable.dicts("Estoque", ((i, t) for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)), lowBound=0, cat="Continuous")
Y = pulp.LpVariable.dicts("Producao_Binaria", ((i, t) for i in range(1, n_produtos + 1) for t in range(1, n_meses + 1)), cat="Binary")

# Função objetivo: Minimizar o custo total (produção + estoque + fixos)
prob += pulp.lpSum(
    custos_producao[(i, t)] * X[(i, t)] +
    custos_estoque[(i, t)] * S[(i, t)] +
    custos_fixos[i] * Y[(i, t)]
    for i in range(1, n_produtos + 1)
    for t in range(1, n_meses + 1)
)

# -----------------------------
# Restrições do modelo
# -----------------------------

# 1. Balanço de estoque
# O estoque atual depende da produção, estoque anterior e demanda
for i in range(1, n_produtos + 1):
    for t in range(1, n_meses + 1):
        if t == 1:
            # No primeiro mês, estoque inicial considerado como zero
            prob += S[(i, t)] == X[(i, t)] - demandas[(i, t)]
        else:
            prob += S[(i, t)] == S[(i, t - 1)] + X[(i, t)] - demandas[(i, t)]

# 2. Capacidade total de produção
# A produção de todos os produtos em um mês não pode exceder a capacidade mensal
for t in range(1, n_meses + 1):
    prob += pulp.lpSum(X[(i, t)] for i in range(1, n_produtos + 1)) <= capacidade_producao

# 3. Restrições Big M
# Vincula a produção (X) à decisão binária (Y)
# Se Y[i,t] = 0, então X[i,t] = 0
# Se Y[i,t] = 1, então X[i,t] pode ser positivo (até no máximo M)
for i in range(1, n_produtos + 1):
    for t in range(1, n_meses + 1):
        prob += X[(i, t)] <= M * Y[(i, t)]

# -----------------------------
# Resolução do problema
# -----------------------------

# Resolve o problema usando o solver padrão do PuLP (CBC)
prob.solve()

# -----------------------------
# Coleta de resultados
# -----------------------------

# Tempo total de execução
end_time = time.time()
execution_time = end_time - start_time

# Uso de memória no processo atual
process = psutil.Process()
memory_usage = process.memory_info().rss / (1024 ** 2)  # Convertido para MB

# -----------------------------
# Impressão dos resultados
# -----------------------------

# Status do problema (ótimo, inviável, etc.)
print(f"Status: {pulp.LpStatus[prob.status]}")

# Custo total ótimo encontrado
print(f"Custo Total Ótimo: R$ {pulp.value(prob.objective):.2f}")

# Tempo e memória usados na execução
print(f"Tempo de Execução: {execution_time:.2f} segundos")
print(f"Uso de Memória: {memory_usage:.2f} MB")

# Exibe os valores encontrados para as variáveis de decisão
for i in range(1, n_produtos + 1):
    for t in range(1, n_meses + 1):
        print(f"X[{i},{t}] = {X[(i, t)].varValue}")  # Produção
        print(f"S[{i},{t}] = {S[(i, t)].varValue}")  # Estoque
        print(f"Y[{i},{t}] = {Y[(i, t)].varValue}")  # Se houve produção (1) ou não (0)
