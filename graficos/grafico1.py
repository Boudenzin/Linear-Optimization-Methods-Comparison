import matplotlib.pyplot as plt
import numpy as np

# Configuração de Estilo Acadêmico
modo_sbc = False  # True para tons de cinza (impressão), False para colorido
plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})

if modo_sbc:
    cor_revised = '#777777'
    cor_bigm = '#333333'
else:
    cor_revised = '#1f77b4' # Azul
    cor_bigm = '#d62728'    # Vermelho (contraste acadêmico)


# --- DADOS BRUTOS (Sem divisão por repetições) ---
testes = ['P1 (10x8)', 'P2 (60x40)', 'P3 (150x25)']

# Tempos Brutos de CPU
cpu_bigm = [4.737896, 4.407365, 0.335343]
cpu_revised = [0.004075, 0.024978, 0.012071]

# Tempos Brutos de Wall
wall_bigm = [4.738636, 4.411720, 0.335795]
wall_revised = [0.004076, 0.024978, 0.012082]

# Memória permanece igual (pico é independente do número de execuções)
mem_bigm = [0.024495, 0.392227, 0.359978]
mem_revised = [0.011195, 0.121892, 0.117589]

def plot_comparativo(labels, dados_rev, dados_bigm, titulo, ylabel, filename, log_scale=False):
    index = np.arange(len(labels))
    bar_width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    rects1 = ax.bar(index - bar_width/2, dados_rev, bar_width, label='Simplex Revisado', color=cor_revised, edgecolor='black')
    rects2 = ax.bar(index + bar_width/2, dados_bigm, bar_width, label='Big M', color=cor_bigm, edgecolor='black')

    ax.set_xlabel('Instâncias do Problema')
    ax.set_ylabel(ylabel)
    ax.set_title(titulo, pad=20)
    ax.set_xticks(index)
    ax.set_xticklabels(labels)
    ax.legend()
    
    if log_scale:
        ax.set_yscale('log')
        ax.set_ylabel(ylabel + ' (Escala Logarítmica)')
    
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    # Função para adicionar rótulos de dados
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            # Formatação científica para valores muito pequenos
            label = f'{height:.1e}' if height < 0.01 else f'{height:.3f}'
            ax.annotate(label,
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # offset de 3 pontos
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

# --- GERAR GRÁFICOS ---

import matplotlib.pyplot as plt
import numpy as np

# Configuração de Estilo Acadêmico
modo_sbc = False  # True para tons de cinza (impressão), False para colorido
plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})

if modo_sbc:
    cor_revised = '#777777'
    cor_bigm = '#333333'
else:
    cor_revised = '#1f77b4' # Azul
    cor_bigm = '#d62728'    # Vermelho (contraste acadêmico)


# --- DADOS BRUTOS (Sem divisão por repetições) ---
testes = ['P1 (10x8)', 'P2 (60x40)', 'P3 (150x25)']

# Tempos Brutos de CPU
cpu_bigm = [4.737896, 4.407365, 0.335343]
cpu_revised = [0.004075, 0.024978, 0.012071]

# Tempos Brutos de Wall
wall_bigm = [4.738636, 4.411720, 0.335795]
wall_revised = [0.004076, 0.024978, 0.012082]

# Memória permanece igual (pico é independente do número de execuções)
mem_bigm = [0.024495, 0.392227, 0.359978]
mem_revised = [0.011195, 0.121892, 0.117589]

def plot_comparativo(labels, dados_rev, dados_bigm, titulo, ylabel, filename, log_scale=False):
    index = np.arange(len(labels))
    bar_width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    rects1 = ax.bar(index - bar_width/2, dados_rev, bar_width, label='Simplex Revisado', color=cor_revised, edgecolor='black')
    rects2 = ax.bar(index + bar_width/2, dados_bigm, bar_width, label='Big M', color=cor_bigm, edgecolor='black')

    ax.set_xlabel('Instâncias do Problema')
    ax.set_ylabel(ylabel)
    ax.set_title(titulo, pad=20)
    ax.set_xticks(index)
    ax.set_xticklabels(labels)
    ax.legend()
    
    if log_scale:
        ax.set_yscale('log')
        ax.set_ylabel(ylabel + ' (Escala Logarítmica)')
    
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    # Função para adicionar rótulos de dados
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            # Formatação científica para valores muito pequenos
            label = f'{height:.1e}' if height < 0.01 else f'{height:.3f}'
            ax.annotate(label,
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # offset de 3 pontos
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

# --- GERAR GRÁFICOS ---

# --- GERAR GRÁFICOS ATUALIZADOS ---

# 1. Gráfico de Tempo (CPU Time) - DADOS BRUTOS
plot_comparativo(testes, cpu_revised, cpu_bigm, 
                 'Figura 1 — Comparação de Tempo de CPU (Dados Brutos Acumulados)', 
                 'Tempo (s)', 'figura1_tempo_cpu_bruto.png', log_scale=True)

# 2. Gráfico de Tempo (Wall Time) - DADOS BRUTOS
plot_comparativo(testes, wall_revised, wall_bigm, 
                 'Figura 2 — Comparação de Tempo de Parede (Dados Brutos Acumulados)', 
                 'Tempo (s)', 'figura2_tempo_wall_bruto.png', log_scale=True)

# 3. Gráfico de Memória (RAM)
plot_comparativo(testes, mem_revised, mem_bigm, 
                 'Figura 3 — Comparação de Pico de Memória RAM', 
                 'Memória (MB)', 'figura3_memoria_bruto.png', log_scale=False)