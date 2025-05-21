### 🔹 **Teste 1 — Problema de Alocação Linear (10 variáveis, 8 restrições)**
---
Este problema foi desenvolvido com o objetivo de testar o desempenho computacional dos métodos em um **cenário simples, porém suficientemente complexo** para demonstrar diferenças entre os algoritmos. Trata-se de um problema de **minimização de custos de produção**, com 10 variáveis de decisão contínuas e não negativas, sujeitas a 8 restrições lineares (sendo 4 do tipo `≤` e 4 do tipo `≥`).

A **função objetivo** é dada por:

$$
\min Z = 12x_1 + 18x_2 + 7x_3 + 12x_4 + 16x_5 + 10x_6 + 14x_7 + 9x_8 + 5x_9 + 9x_{10}
$$

As **restrições do tipo `≤`** são:

$$
\begin{cases}
0x_1 + 7x_2 + 7x_3 -5x_4 + 9x_5 + 0x_6 + 7x_7 + 8x_8 + 3x_9 -4x_{10} \leq 56 \\
-2x_1 + 5x_2 + 3x_3 -2x_4 + 8x_5 -2x_6 + 6x_7 -3x_8 + 7x_9 + 3x_{10} \leq 57 \\
4x_1 -2x_2 + 9x_3 +5x_4 + 7x_5 +6x_6 +2x_7 -5x_8 +4x_9 +2x_{10} \leq 64 \\
4x_1 +3x_2 +9x_3 -x_4 -2x_5 -2x_6 +7x_7 +2x_8 +5x_9 -x_{10} \leq 96
\end{cases}
$$

As **restrições do tipo `≥`** são:

$$
\begin{cases}
3x_1 + 2x_2 + x_3 + 9x_4 + 4x_5 - x_6 - 3x_7 + 2x_8 + 2x_9 + 2x_{10} \geq 19 \\
7x_1 -5x_2 -x_3 + 5x_4 + 7x_5 -4x_6 + 3x_7 + 6x_8 -2x_9 -4x_{10} \geq 55 \\
8x_1 + 3x_2 -x_3 + 7x_4 -2x_5 -3x_6 -2x_7 + 9x_8 + 5x_9 -2x_{10} \geq 12 \\
7x_1 + 2x_2 -x_3 + 6x_4 + 3x_5 + x_6 + 5x_7 + 5x_8 -2x_9 + 2x_{10} \geq 28
\end{cases}
$$

Todas as variáveis de decisão possuem restrição de **não negatividade**:

$$
x_1, x_2, \dots, x_{10} \geq 0
$$

A **solução ótima** encontrada (com ambos os métodos) é:

* **Valor ótimo:** \$Z = 85{,}29\$
* **Variáveis com valor não nulo:**
  $x_1 = 1{,}8571 \quad \text{e} \quad x_8 = 7{,}0000$

Este problema é **viável e possui solução ótima única**, o que o torna ideal para comparação de desempenho em termos de tempo de execução, memória utilizada e comportamento das variáveis artificiais no método Big M.

---
