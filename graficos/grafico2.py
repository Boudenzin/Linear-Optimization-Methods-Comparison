import matplotlib.pyplot as plt
import numpy as np

modo_sbc = False  # Altere para False para versão colorida

if modo_sbc:
    cor_revised = 'gray'
    cor_bigm = 'black'
else:
    cor_revised = '#1f77b4'
    cor_bigm = '#ff7f0e'

# Dados reais (uso de memória em MB)
testes = ['Teste 1', 'Teste 2', 'Teste 3']
uso_memoria_revised = [0.85, 1.14, 1.02]
uso_memoria_big_m = [3.29, 4.72, 4.13]

# Largura das barras
bar_width = 0.35
index = np.arange(len(testes))

# Criar a figura
plt.figure(figsize=(10, 6))
bars1 = plt.bar(index, uso_memoria_revised, bar_width, label='Simplex Revisado', color=cor_revised)
bars2 = plt.bar(index + bar_width, uso_memoria_big_m, bar_width, label='Big M', color=cor_bigm)

# Adicionar valores acima das barras
for bar in bars1:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', ha='center', va='bottom', fontsize=10)

for bar in bars2:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', ha='center', va='bottom', fontsize=10)

# Configurações do gráfico
plt.xlabel('Testes')
plt.ylabel('Uso de Memória (MB)')
plt.title('Figura 2 — Comparação do Uso de Memória entre Métodos')
plt.xticks(index + bar_width / 2, testes)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Salvar figura
plt.tight_layout()
plt.savefig('figura2_uso_memoria.png', dpi=300)
plt.show()
