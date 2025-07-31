# Detalhes dos Problemas de Programação Linear

Este documento contém os coeficientes completos dos problemas de programação linear apresentados no artigo. Os dados foram gerados com sementes aleatórias fixas para garantir reprodutibilidade. Para acessar o código completo, consulte [[Linear-Optimization-Methods-Comparison
](https://github.com/Boudenzin/Linear-Optimization-Methods-Comparison.git)].

## 🔹 **Teste 1 — Problema de Alocação Linear (10 variáveis, 8 restrições)**

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

Sim, posso te ajudar com isso! Para transformar esses dados em uma boa visualização no seu Markdown, recomendo a seguinte organização por seções, com base nos três componentes do problema: custos (função objetivo), restrições (matriz A e lado direito), e variáveis de decisão. Aqui vai um esboço de como formatar isso:

---

## 🧪 Teste 2 — Problema de Alocação Robusta

### **Função Objetivo**

**Minimizar:**

$$
Z = c_1x_1 + c_2x_2 + \dots + c_{60}x_{60}
$$

Onde os coeficientes da função objetivo (custos) são:

```text
[24, 28, 17, 13, 14, 12, 11, 27, 6, 12, 21, 19, 24, 14, 9, 25, 28, 26, 25, 13,
 14, 20, 16, 25, 28, 8, 22, 21, 8, 22, 25, 13, 27, 15, 21, 14, 8, 15, 13, 25,
 14, 7, 11, 10, 21, 29, 14, 28, 27, 10, 27, 12, 13, 8, 23, 28, 26, 15, 19, 21]
```

---

### **Restrições**

#### Lado Direito (`b`):

```text
[262, 298, 354, 132, 140, 178, 256, 248, 224, 295, 380, 325, 423, 248, 404,
 431, 225, 242, 101, 437, 157, 285, 329, 397, 443, 351, 200, 260, 187, 251,
 143, 285, 405, 375, 248, 445, 400, 252, 206, 448]
```

#### Matriz de Coeficientes (`A`):

Matriz 40x60, exibida parcialmente abaixo (primeiras 5 linhas como exemplo):

```text
7,2,-1,3,4,4,7,7,-2,0,2,4,-2,7,2,7,4,2,1,4,...
2,1,-2,5,6,3,7,0,3,-3,0,-3,0,5,-3,6,7,-3,0,2,...
-3,0,-1,1,2,2,3,0,1,4,6,6,6,3,5,1,7,3,3,-1,...
-1,0,4,-3,6,-3,7,-3,1,4,1,-2,7,-3,-1,0,5,5,-2,-1,...
2,4,0,5,6,3,-1,7,0,0,-3,0,7,0,-1,2,4,4,2,2,...
...
(total: 40 linhas)
```

---

### **Variáveis de Decisão**

Todas as variáveis são contínuas e não-negativas:

```text
x₁, x₂, ..., x₆₀ ≥ 0
```

---

### 💡 Observações Técnicas

* O problema é do tipo **minimização**.
* As restrições foram balanceadas entre desigualdades `≤` e `≥`, convertidas para igualdade com uso de variáveis artificiais (Big M).
* A geração dos coeficientes foi feita via `numpy.random.seed(1)` para garantir **reprodutibilidade total**.
* Este modelo simula um problema realista de alocação de recursos com múltiplos centros de decisão.

---

Claro! Aqui está sua descrição do **Problema 3** formatada adequadamente para Markdown — ideal para inserir no seu `README.md` ou em outro arquivo `.md` no GitHub:

---

## 🧪 Teste 3 — Problema de Balanceamento de Produção e Transporte

### **Descrição Geral**

Este problema simula um **sistema de transporte**, onde **15 fábricas** devem abastecer **10 centros de distribuição** com **custo mínimo de transporte**. Cada fábrica possui uma capacidade limitada, e cada centro possui uma demanda mínima. O objetivo é determinar a **quantidade ótima de produtos a serem transportados** de cada fábrica para cada centro.

---

### **Variáveis de Decisão**

* $x_{ij}$: Quantidade transportada da **fábrica $i$** para o **centro $j$**.
  Onde:

  * $i = 1, 2, \dots, 15$ (fábricas)
  * $j = 1, 2, \dots, 10$ (centros)

Total de variáveis: $15 \times 10 = 150$.

---

### **Função Objetivo**

**Minimizar o custo total de transporte:**

$$
Z = \sum_{i=1}^{15} \sum_{j=1}^{10} c_{ij} \cdot x_{ij}
$$

Onde:

* $c_{ij}$: Custo unitário de transporte da fábrica $i$ ao centro $j$, **gerado aleatoriamente** entre R\$10 e R\$100 com `np.random.seed(42)`.
* $x_{ij} \geq 0$: Quantidade transportada.

---

### **Restrições**

#### 1. **Capacidade das Fábricas** $(\leq)$

Cada fábrica $i$ possui uma capacidade máxima $K_i$:

$$
\sum_{j=1}^{10} x_{ij} \leq K_i, \quad \forall i \in \{1, \dots, 15\}
$$

* Capacidades geradas aleatoriamente entre **500 e 1500 unidades**.

#### 2. **Demanda dos Centros** $(\geq)$

Cada centro $j$ tem uma demanda mínima $D_j$:

$$
\sum_{i=1}^{15} x_{ij} \geq D_j, \quad \forall j \in \{1, \dots, 10\}
$$

* Convertido para a forma padrão do Simplex Revisado:

$$
-\sum_{i=1}^{15} x_{ij} \leq -D_j
$$

* Demandas geradas aleatoriamente entre **200 e 800 unidades**.

#### 3. **Não Negatividade**

$$
x_{ij} \geq 0, \quad \forall i, j
$$

---

### **Dados Gerados no Código**

* **Semente aleatória utilizada:** `np.random.seed(42)`

* **Custos (`custos`)**:
  Vetor de 150 elementos, com valores entre 10 e 100
  (gerado via `np.random.randint(10, 100, size=150)`)

* **Capacidades das fábricas (`capacidades_fabricas`)**:
  Vetor de 15 elementos, com valores entre 500 e 1500
  (gerado via `np.random.randint(500, 1500, size=15)`)

* **Demandas dos centros (`demandas_centros`)**:
  Vetor de 10 elementos, com valores entre 200 e 800
  (gerado via `np.random.randint(200, 800, size=10)`)

---

### ✅ Nota sobre Viabilidade

O problema foi **intencionalmente projetado para ser viável**, garantindo que a **soma das capacidades das fábricas** seja **maior ou igual à soma das demandas dos centros**.
Isso evita casos inviáveis e permite comparações reais e consistentes entre os métodos de solução (Simplex Revisado e Big M).

---


