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

# --- DADOS CONSOLIDADOS (Médias de CPU e Memória) ---
testes = ['P1 (10x8)', 'P2 (60x40)', 'P3 (150x25)']

# Tempos Médios de CPU (ajustados pelas repetições internas nos seus logs)
# P1 BigM: 4.73/500 | P1 Rev: 0.0041/100
# P2 BigM: 4.40 | P2 Rev: 0.024/100 (ajustado conforme log)
# P3 BigM: 0.33 | P3 Rev: 0.012/100 (ajustado conforme log)
tempo_bigm = [4.737896 / 500, 4.407365, 0.335343]
tempo_revised = [0.004198 / 100, 0.024978 / 100, 0.012071 / 100]

# Memória Média (Pico RAM em MB)
mem_bigm = [0.024495, 0.392227, 0.359978]
mem_revised = [0.011164, 0.121892, 0.117589]

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
    print(f"Gráfico salvo como: {filename}")

# --- GERAR GRÁFICOS ---

# 1. Gráfico de Tempo (CPU Time) - USANDO LOG SCALE
plot_comparativo(testes, tempo_revised, tempo_bigm, 
                 'Figura 1 — Comparação de Tempo de CPU (Média por Execução)', 
                 'Tempo (s)', 'figura1_tempo_cpu.png', log_scale=True)

# 2. Gráfico de Memória (RAM)
plot_comparativo(testes, mem_revised, mem_bigm, 
                 'Figura 2 — Comparação de Pico de Memória RAM', 
                 'Memória (MB)', 'figura2_memoria.png', log_scale=False)

plt.show()