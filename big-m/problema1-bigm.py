# Importação das bibliotecas necessárias
import pulp  # Biblioteca usada para modelar e resolver problemas de Programação Linear
import time  # Biblioteca para medir o tempo de execução
import psutil  # Biblioteca para medir o uso de memória do processo
import os  # Biblioteca para acessar informações do sistema operacional

def solve_big_m_manual():
    """
    Resolve manualmente um problema de Programação Linear
    utilizando o Método Big M.

    O objetivo é maximizar a função x + 2y, considerando
    penalidades para variáveis artificiais (a1) usando um grande valor M.
    """

    # Inicia o monitoramento de memória
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024)  # Memória antes da execução (em MB)

    # Inicia a contagem do tempo de execução
    start_time = time.time()

    # Cria o modelo de otimização (problema de maximização)
    prob = pulp.LpProblem("BigM_Manual", pulp.LpMaximize)

    # Definição das variáveis de decisão
    x = pulp.LpVariable("x", lowBound=0)  # Variável x >= 0
    y = pulp.LpVariable("y", lowBound=0)  # Variável y >= 0
    a1 = pulp.LpVariable("a1", lowBound=0)  # Variável artificial a1 >= 0 (será penalizada)

    # Definição da função objetivo
    # Queremos maximizar x + 2y, mas penalizando a presença da variável artificial a1
    M = 1000  # Valor grande de penalização (Big M)
    prob += x + 2 * y - M * a1, "Função Objetivo com Big M"

    # Definição das restrições do problema
    prob += x + y <= 5, "Restrição_1"             # Restrição normal
    prob += x - y + a1 == 1, "Restrição_2"         # Restrição com variável artificial

    # Resolve o problema usando o solver padrão do PuLP (CBC)
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # Finaliza a contagem de tempo e memória
    end_time = time.time()
    mem_after = process.memory_info().rss / (1024 * 1024)  # Memória depois da execução (em MB)
    memory_used = mem_after - mem_before  # Diferença de memória usada durante a execução

    # Impressão dos resultados encontrados
    print(f"\n### Big M (Manual) ###")
    print(f"Tempo de execução: {end_time - start_time:.6f} s")
    print(f"Uso de memória: {memory_used:.6f} MB")
    print(f"Valor ótimo encontrado: {pulp.value(prob.objective):.6f}")
    print(f"x = {x.value():.3f}, y = {y.value():.3f}, a1 = {a1.value():.3f}")

    # Verificação importante:
    # Se a variável artificial a1 tiver valor diferente de zero, 
    # significa que a solução encontrada pode não ser viável.
    if a1.value() > 1e-5:
        print("⚠️ Variável artificial diferente de zero: solução pode ser inviável!")

# Executa a função principal
solve_big_m_manual()
