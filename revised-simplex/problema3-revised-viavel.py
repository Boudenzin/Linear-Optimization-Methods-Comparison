# Importação das bibliotecas necessárias
import numpy as np
from scipy.optimize import linprog
import time
import psutil
import os

def problema_balanceamento_producao():
    """
    Gera e resolve um problema de balanceamento de produção com mais de 100 variáveis e 100 restrições,
    usando Simplex Revisado
    
    O problema é um grande problema de transporte: fábricas abastecendo centros de distribuição.
    """

    # Iniciar a medição de tempo
    start_time = time.time()

    # Iniciar a medição de memória
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 ** 2)  # Memória em MB

    # -----------------------------
    # Definição dos parâmetros do problema
    # -----------------------------

    n_fabricas = 15  # Número de fábricas
    n_centros = 10   # Número de centros de distribuição

    n_variaveis = n_fabricas * n_centros  # Cada fábrica pode enviar para cada centro

    # Gerar custos aleatórios de transporte (entre 10 e 100)
    np.random.seed(42)
    custos = np.random.randint(10, 100, size=n_variaveis)

    # Gerar capacidades aleatórias para fábricas (entre 500 e 1500)
    capacidades_fabricas = np.random.randint(500, 1500, size=n_fabricas)

    # Gerar demandas aleatórias para centros (entre 200 e 800)
    demandas_centros = np.random.randint(200, 800, size=n_centros)

    # -----------------------------
    # Construção das restrições
    # -----------------------------

    # Restrições de capacidade de fábricas (cada linha limita uma fábrica)
    A_fabricas = np.zeros((n_fabricas, n_variaveis))
    for i in range(n_fabricas):
        for j in range(n_centros):
            A_fabricas[i, i * n_centros + j] = 1

    # Restrições de atendimento de centros (cada linha garante demanda de um centro)
    A_centros = np.zeros((n_centros, n_variaveis))
    for j in range(n_centros):
        for i in range(n_fabricas):
            A_centros[j, i * n_centros + j] = 1

    # Lados direitos
    b_fabricas = capacidades_fabricas
    b_centros = demandas_centros

    # Junção das restrições: fabricas (≤) + centros (≥ convertidos para ≤ usando sinal)
    A_ub = np.vstack([
        A_fabricas,     # Capacidade: soma das saídas <= capacidade
        -A_centros      # Demanda: -soma das entradas <= -demanda
    ])
    b_ub = np.concatenate([
        b_fabricas,
        -b_centros
    ])

    # -----------------------------
    # Resolução do problema
    # -----------------------------

    resultado = linprog(
        custos,
        A_ub=A_ub,
        b_ub=b_ub,
        bounds=[(0, None)] * n_variaveis,  # Quantidade enviada deve ser não negativa
        method='revised simplex'  # Usar Simplex Revisado puro
    )

    # -----------------------------
    # Medição de tempo e memória
    # -----------------------------

    end_time = time.time()
    execution_time = end_time - start_time

    mem_after = process.memory_info().rss / (1024 ** 2)  # Memória final em MB
    memory_used = mem_after - mem_before

    # -----------------------------
    # Impressão dos resultados
    # -----------------------------

    print("\n### Resultado do Problema de Balanceamento de Produção ###")
    if resultado.success:
        print(f"Status: {resultado.message}")
        print(f"Custo Total Ótimo: R$ {resultado.fun:.2f}")
    else:
        print("❌ Solução não encontrada.")

    print(f"Tempo de Execução: {execution_time:.2f} segundos")
    print(f"Uso de Memória: {memory_used:.2f} MB")

    # (Opcional) Exibir quantidade enviada de cada fábrica para cada centro
    for i in range(n_fabricas):
        for j in range(n_centros):
            idx = i * n_centros + j
            print(f"Fábrica {i+1} -> Centro {j+1}: {resultado.x[idx]:.2f}")

# Executar o problema
problema_balanceamento_producao()
