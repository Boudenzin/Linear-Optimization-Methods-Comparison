import matplotlib.pyplot as plt
import numpy as np

# Dados
testes = ['Teste 1', 'Teste 2', 'Teste 3 (Inv.)', 'Teste 3 (Viável)']
uso_memoria_revised = [0.25, 1.78, 6.93, 31.85]
uso_memoria_big_m = [0.59, 0.59, 32.03, 31.91]

# Largura das barras
bar_width = 0.35
index = np.arange(len(testes))

# Plot
plt.figure(figsize=(10, 6))
plt.bar(index, uso_memoria_revised, bar_width, label='Simplex Revisado', color='seagreen')
plt.bar(index + bar_width, uso_memoria_big_m, bar_width, label='Big M', color='firebrick')

# Configurações
plt.xlabel('Testes')
plt.ylabel('Uso de Memória (MB)')
plt.title('Comparação do Uso de Memória entre Métodos')
plt.xticks(index + bar_width / 2, testes)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Salvar figura (opcional)
plt.tight_layout()
plt.savefig('uso_memoria_comparacao.png', dpi=300)
plt.show()
