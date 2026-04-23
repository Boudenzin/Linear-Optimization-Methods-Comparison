

### DADOS CONSOLIDADOS DE BENCHMARK (BIG M vs. SIMPLEX REVISADO)

**Validação de Corretude:** As soluções ótimas entre os métodos são equivalentes dentro da tolerância numérica de **$\epsilon = 10^{-8}$**.

---

**PROBLEMA 1 (10 Variáveis, 8 Restrições)**
*Valor ótimo: 12015.00*

**1.1 RELATÓRIO: BIG M (30 amostras, 500 repetições internas)**
- **WALL (Bloco):** Média 4.738636s | RSD 1.92%
- **CPU (Bloco):** Média 4.737896s | RSD 1.92%
- **MEM (Pico):** Média 0.024495 MB | RSD 2.17%
- **TEMPO UNITÁRIO (NORMALIZADO): 0.009476 segundos**

**1.2 RELATÓRIO: SIMPLEX REVISADO (30 amostras, 500 repetições internas)**
- **WALL (Bloco):** Média  0.004076s | RSD 7.37%
- **CPU (Bloco):** Média 0.004075s | RSD 7.71%
- **MEM (Pico):** Média 0.011195 MB | RSD 7.91%
- **TEMPO UNITÁRIO (NORMALIZADO): 0,00000815 segundos**

---

**PROBLEMA 2 (60 Variáveis, 40 Restrições)**
*Valor ótimo: 5638.18*

**2.1 RELATÓRIO: BIG M (30 amostras, 1 execução por amostra)**
- **WALL:** Média 4.411720s | RSD 3.10%
- **CPU:** Média 4.407365s | RSD 3.10%
- **MEM (Pico):** Média 0.392227 MB | RSD 0.00%
- **TEMPO UNITÁRIO: 4.407365 segundos**

**2.2 RELATÓRIO: SIMPLEX REVISADO (30 amostras, 1 execução por amostra)**
- **WALL (Bloco):** Média 0.039381s | RSD 7.61%
- **CPU (Bloco):** Média 0.039381s | RSD 7.61%
- **MEM (Pico):** Média 0.121483 MB | RSD 0.00%
- **TEMPO UNITÁRIO : 0.039381s segundos**

---

**PROBLEMA 3 (150 Variáveis, 25 Restrições)**
*Valor ótimo: 1338498.00*

**3.1 RELATÓRIO: BIG M (30 amostras, 100 repetições internas)**
- **WALL (Bloco):** Média 0.335795s | RSD 2.75%
- **CPU (Bloco):** Média 0.335343s | RSD 2.74%
- **MEM (Pico):** Média 0.359978 MB | RSD 0.09%
- **TEMPO UNITÁRIO (NORMALIZADO): 0.003353 segundos**

**3.2 RELATÓRIO: SIMPLEX REVISADO (30 amostras, 100 repetições internas)**
- **WALL (Bloco):** Média 0.012082s | RSD 4.07%
- **CPU (Bloco):** Média 0.012071s | RSD 4.05%
- **MEM (Pico):** Média 0.117589 MB | RSD 0.65%
- **TEMPO UNITÁRIO (NORMALIZADO): 0.000121 segundos**

---

### NOTA METODOLÓGICA
Todas as execuções foram realizadas em ambiente isolado via **Docker** (limitado a **1.0 CPU** e **512MB RAM**). O tempo unitário foi calculado através da razão entre a média de tempo de CPU e o número de repetições por amostra ($t_u = \bar{t}_{cpu} / k$). As medições de memória utilizam o pico de consumo de RAM (*Peak Resident Set Size*) identificado pelo `tracemalloc`.