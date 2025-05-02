import matplotlib.pyplot as plt
import numpy as np

modo_sbc = False  # Altere para False para versão colorida

if modo_sbc:
    cor_revised = 'gray'
    cor_bigm = 'black'
else:
    cor_revised = '#1f77b4'
    cor_bigm = '#ff7f0e'


# Novos dados reais (tempo de execução em segundos)
testes = ['Teste 1', 'Teste 2', 'Teste 3']
tempo_revised = [0.0263, 0.0721, 0.0300]
tempo_big_m = [1.1374, 0.2714, 0.2200]

# Largura das barras
bar_width = 0.35
index = np.arange(len(testes))

# Criar a figura
plt.figure(figsize=(10, 6))
bars1 = plt.bar(index, tempo_revised, bar_width, label='Simplex Revisado', color=cor_revised)
bars2 = plt.bar(index + bar_width, tempo_big_m, bar_width, label='Big M', color=cor_bigm)

# Adicionar valores acima das barras
for bar in bars1:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.4f}', ha='center', va='bottom', fontsize=10)

for bar in bars2:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.4f}', ha='center', va='bottom', fontsize=10)

# Configurações do gráfico
plt.xlabel('Testes')
plt.ylabel('Tempo de Execução (s)')
plt.title('Figura 1 — Comparação do Tempo de Execução entre Métodos')
plt.xticks(index + bar_width / 2, testes)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Salvar figura
plt.tight_layout()
plt.savefig('figura1_tempo_execucao.png', dpi=300)
plt.show()
