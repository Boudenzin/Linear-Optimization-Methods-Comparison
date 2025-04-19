import matplotlib.pyplot as plt
import numpy as np

# Dados
testes = ['Teste 1', 'Teste 2', 'Teste 3 (Inv.)', 'Teste 3 (Viável)']
uso_memoria_revised = [0.25, 1.78, 6.93, 31.85]
uso_memoria_big_m = [0.59, 0.59, 32.03, 31.91]

# Largura das barras
bar_width = 0.35
index = np.arange(len(testes))

# Criar a figura
plt.figure(figsize=(10, 6))
bars1 = plt.bar(index, uso_memoria_revised, bar_width, label='Simplex Revisado', color='gray')
bars2 = plt.bar(index + bar_width, uso_memoria_big_m, bar_width, label='Big M', color='black')

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
plt.title('Comparação do Uso de Memória entre Métodos')
plt.xticks(index + bar_width / 2, testes)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Salvar figura
plt.tight_layout()
plt.savefig('uso_memoria_comparacao.png', dpi=300)
plt.show()
