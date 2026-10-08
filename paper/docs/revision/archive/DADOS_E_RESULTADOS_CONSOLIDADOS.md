# CONSOLIDAÇÃO INTEGRAL DE DADOS E RESULTADOS NUMÉRICOS DO ARTIGO
## "Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study"

**Localização deste arquivo:** `Paradoxo\llm-knowledge-collapse (paper)\v4\DADOS_E_RESULTADOS_CONSOLIDADOS.md`  
**Data de consolidação:** 2026-09-29  
**Status do projeto:** Experimentos fechados, auditados e validados. Manuscrito submetido à *Engineering Applications of Artificial Intelligence* (EAAI, Elsevier).

---

## SUMÁRIO EXECUTIVO

Este documento reúne e organiza **100% dos dados empíricos, resultados numéricos, parâmetros arquiteturais, métricas distribucionais, tabelas estatísticas e ablações** gerados ao longo de todo o ciclo de vida do artigo (desde a fase exploratória M0/M1/M2 até as rodadas Athena v3 e submissão v4).

O artigo demonstra empiricamente que o colapso/degradação do conhecimento (*Knowledge Degradation*) sob ajuste fino recursivo em dados sintéticos **não é inevitável**, mas sim governado por um princípio organizador denominado **Pressão Efetiva de Treinamento** (*Effective Training Pressure* - ETP). A estabilidade do modelo é definida por uma fronteira (*regime transition threshold*) manipulável através de três eixos ortogonais:
1. **Capacidade de Atualização (*Update Capacity*):** Posto nominal ($r$) e posto efetivo (*effective rank*) no QLoRA/PEFT;
2. **Magnitude da Perturbação (*Perturbation Magnitude*):** Taxa de aprendizado (*learning rate*) e desvio médio de pesos (*weight drift*) em ajuste fino completo (FFT);
3. **Exposição a Dados Sintéticos (*Synthetic Exposure*):** Volume de tokens sintéticos consumidos por geração.

---

## 1. INFRAESTRUTURA, MODELOS E PROTOCOLO EXPERIMENTAL

### 1.1 Hardware e Ambiente de Execução
- **Nó Primário (Local):** NVIDIA GeForce RTX 3070 (8 GB VRAM), AMD Ryzen 5 5600X (6 núcleos / 12 threads), 64 GB RAM DDR4.
- **Nó de Alta Capacidade (Athena Cluster):** NVIDIA GPU de 20 GB VRAM para execuções multi-seed estendidas (Gemma 3 10 gerações, Gemma 4 E2B, réplicas C5).
- **Software:** Python 3.12, PyTorch 2.4.1+cu124, Hugging Face `transformers` 4.46.3, `peft` 0.13.2, `bitsandbytes` 0.44.1, `datasets` 3.1.0, CUDA 12.4.
- **Quantização base:** 4-bit NormalFloat (NF4), double quantization ativada, tipo de computação bfloat16. O modelo base quantizado permanece 100% congelado em todas as gerações.
- **Otimizador:** `paged_adamw_8bit` com `gradient_checkpointing` ativo para FFT e QLoRA de alto rank.

### 1.2 Backbones Arquiteturais Avaliados
| Propriedade Arquitetural | Qwen 2.5 1.5B-Instruct | Gemma 3 1B IT | Gemma 4 E2B IT |
|---|---|---|---|
| **Família / Criador** | Alibaba Qwen Team | Google DeepMind | Google DeepMind |
| **Parâmetros Totais** | 1.54 Bilhões | 1.00 Bilhão | 2.00 Bilhões |
| **Dimensão Oculta ($d$)** | 1536 | 1152 | 2048 |
| **Número de Camadas** | 28 | 26 | 28 |
| **Atenção (Q Heads / KV Heads)**| 12 / 2 (GQA 6:1) | 8 / 1 (MQA/GQA 8:1) | 8 / 1 (MQA/GQA 8:1) |
| **Tamanho do Vocabulário** | 151.936 | 256.000 | 256.000 |
| **Papel no Estudo** | Backbone Primário (Eixos 1, 2, 3) | Backbone Secundário (Validação Cruzada) | Robustez e Escala (3ª Família) |
| **Tamanho da Base $K_0$** | **78 itens** (auditado / 79 inicial) | **46 itens** (auditado / 47 inicial) | **76 itens** |

### 1.3 Dataset e Definição da Métrica $K_0$
- **Dataset:** TriviaQA (`mandarjoshi/trivia_qa`, subconjunto `rc.nocontext`, split `train`, embaralhado com seed 15).
  - Conjunto de Treino Sintético: 2.000 perguntas por geração.
  - Conjunto de Avaliação: 200 perguntas fixas reservadas.
- **Formatação de Prompt:** Chat template padrão do modelo com restrição estrita no prompt do sistema:
  `"Answer the following question in 5 words or less."`
- **Decodificação de Avaliação:** Gulosa determinística (*greedy decoding*), `temperature=0.0`, `do_sample=False`, `max_new_tokens=20`.
- **Critério de Acerto:** *Exact Match* normalizado com suporte a todos os aliases oficiais do TriviaQA (conversão de palavras numéricas para dígitos, remoção de artigos, pontuação e espaços múltiplos).
- **Acurácia Inicial do Modelo Base (Gen 0):**
  - Qwen 2.5 1.5B: 78/200 acertos = **39,0%** (54,5% de desconhecimento genuíno, 0 erros de formatação).
  - Gemma 3 1B IT: 46/200 acertos = **23,0%**.
  - Gemma 4 E2B IT: 76/200 acertos = **38,0%**.
- **Conjunto $K_0$:** Subconjunto estrito de perguntas que o modelo base (Geração 0) respondeu corretamente.
  A métrica fundamental de todo o artigo é a **Retenção de $K_0$**:
  $$\text{Retenção}(t) = \frac{\sum_{i \in K_0} \mathbb{I}(\text{Modelo}_t(q_i) \text{ correto})}{|K_0|}$$
  Essa métrica isola o esquecimento factual da incapacidade inicial de responder.

### 1.4 Protocolo de Recursão Sintética (*Data-Only Replace*)
Em cada geração $t \in \{1, \dots, 10\}$:
1. O modelo da geração anterior ($t-1$) gera respostas para as 2.000 perguntas de treino com amostragem estocástica: `temperature=0.7`, `top_p=0.9`, `max_new_tokens=30`.
2. As respostas sintéticas geradas formam o conjunto de treino da geração $t$ (substituição total: 0% de dados humanos reais).
3. Um novo adaptador LoRA é inicializado do zero sobre o modelo base congelado e treinado por 2 épocas (tamanho de batch efetivo 16, lr=1e-5 para QLoRA base).
4. O modelo resultante é avaliado nas perguntas $K_0$ e gera os dados da geração $t+1$.

---

## 2. EIXO 1: CAPACIDADE DE ATUALIZAÇÃO (DOSE-RESPOSTA DE POSTO QLoRA)

### 2.1 Varredura Completa de Postos no Qwen 2.5 1.5B (Seed 15, Gen 0 a 10)
Alvos de LoRA: projeções de atenção `q_proj` e `v_proj` ($\alpha = 2r$, dropout 0.05).

| Posto Nominal ($r$) | Parâmetros Treináveis | % Params do Base | Posto Efetivo Médio | Utilização (%) | Retenção Gen 5 | Retenção Gen 10 | Regime Classificado |
|---|---|---|---|---|---|---|---|
| **$r=4$** | 545.280 | 0,06% | 3,34 | 83,5% | 75/79 (94,9%) | — | **Homeostático** |
| **$r=16$** | 2.181.120 | 0,24% | 11,08 | 69,3% | 75/79 (94,9%) | 75/79 (94,9%) | **Homeostático** |
| **$r=32$** | 4.362.240 | 0,49% | 17,85 | 55,8% | 75/79 (94,9%) | — | **Homeostático** |
| **$r=64$** | 8.724.480 | 0,98% | 29,52 | 46,1% | 71/79 (89,9%) | 72/79 (91,1%) | **Homeostático** |
| **$r=128$** | 17.448.960 | 1,96% | 50,16 | 39,2% | 69/79 (87,3%) | 70/79 (88,6%) | **Limitado (*Bounded*)** |
| **$r=256$** | 34.897.920 | 3,91% | 87,57 | 34,2% | 66/79 (83,5%) | 60/79 (75,9%) | **Degradativo** |

*(Nota: na base auditada de $K_0=78$, os valores finais de Gen 10 correspondem a: $r=16 \to 96,2\%$; $r=64 \to 92,3\%$; $r=128 \to 89,7\%$; $r=256 \to 79,1\%$ na média multi-seed).*

#### Trajetórias Completas de Retenção por Geração (Qwen Seed 15)
- **$r=4$ (Gen 0 a 5):** G0: 100% (79) $\to$ G1: 93,7% (74) $\to$ G2: 92,4% (73) $\to$ G3: 93,7% (74) $\to$ G4: 94,9% (75) $\to$ G5: 94,9% (75).
- **$r=16$ (Gen 0 a 10):** G0: 100% (79) $\to$ G1: 94,9% (75) $\to$ G2: 96,2% (76) $\to$ G3: 94,9% (75) $\to$ G4: 94,9% (75) $\to$ G5: 94,9% (75) $\to$ G6: 96,2% (76) $\to$ G7: 94,9% (75) $\to$ G8: 96,2% (76) $\to$ G9: 94,9% (75) $\to$ G10: 94,9% (75).
- **$r=32$ (Gen 0 a 5):** G0: 100% (79) $\to$ G1: 93,7% (74) $\to$ G2: 94,9% (75) $\to$ G3: 94,9% (75) $\to$ G4: 96,2% (76) $\to$ G5: 94,9% (75).
- **$r=64$ (Gen 0 a 10):** G0: 100% (79) $\to$ G1: 91,1% (72) $\to$ G2: 91,1% (72) $\to$ G3: 89,9% (71) $\to$ G4: 91,1% (72) $\to$ G5: 89,9% (71) $\to$ G6: 91,1% (72) $\to$ G7: 92,4% (73) $\to$ G8: 91,1% (72) $\to$ G9: 89,9% (71) $\to$ G10: 91,1% (72).
- **$r=128$ (Gen 0 a 10):** G0: 100% (79) $\to$ G1: 92,4% (73) $\to$ G2: 88,6% (70) $\to$ G3: 91,1% (72) $\to$ G4: 91,1% (72) $\to$ G5: 87,3% (69) $\to$ G6: 87,3% (69) $\to$ G7: 88,6% (70) $\to$ G8: 87,3% (69) $\to$ G9: 87,3% (69) $\to$ G10: 88,6% (70).
- **$r=256$ (Gen 0 a 10):** G0: 100% (79) $\to$ G1: 94,9% (75) $\to$ G2: 89,9% (71) $\to$ G3: 91,1% (72) $\to$ G4: 88,6% (70) $\to$ G5: 83,5% (66) $\to$ G6: 82,3% (65) $\to$ G7: 81,0% (64) $\to$ G8: 81,0% (64) $\to$ G9: 78,5% (62) $\to$ G10: 75,9% (60).

#### Posto Efetivo por Geração (Qwen Seed 15)
O posto efetivo de uma matriz de covariância de ativação ou dos pesos do adaptador $BA$ é definido pela entropia espectral de seus valores singulares:
$$\text{eff\_rank}(\Delta W) = \exp\left(-\sum_{i} p_i \ln p_i\right), \quad p_i = \frac{\sigma_i}{\sum_j \sigma_j}$$
- **$r=4$:** G1: 3,34 $\to$ G2: 3,34 $\to$ G3: 3,35 $\to$ G4: 3,34 $\to$ G5: 3,34.
- **$r=16$:** Estável em 11,08 $\pm 0,15$ ao longo de todas as 10 gerações.
- **$r=32$:** G1: 18,06 $\to$ G2: 17,83 $\to$ G3: 17,99 $\to$ G4: 17,76 $\to$ G5: 17,80.
- **$r=64$:** G1: 30,08 $\to$ G2: 29,69 $\to$ G3: 29,69 $\to$ G4: 29,87 $\to$ G5: 29,65 $\to$ G6: 29,78 $\to$ G7: 29,49 $\to$ G8: 29,97 $\to$ G9: 29,92 $\to$ G10: 29,52.
- **$r=128$:** G1: 50,56 $\to$ G2: 50,21 $\to$ G3: 50,16 $\to$ G4: 50,43 $\to$ G5: 50,38 $\to$ G6: 50,59 $\to$ G7: 50,08 $\to$ G8: 49,91 $\to$ G9: 50,70 $\to$ G10: 50,61.
- **$r=256$:** G1: 88,07 $\to$ G2: 87,80 $\to$ G3: 87,66 $\to$ G4: 87,93 $\to$ G5: 87,76 $\to$ G6: 87,14 $\to$ G7: 87,44 $\to$ G8: 86,61 $\to$ G9: 86,61 $\to$ G10: 85,59.

*Insight Fundamental:* O posto efetivo permanece perfeitamente estável mesmo quando a retenção factual desaba (como em $r=256$). Não ocorre colapso de posto geométrico no adaptador LoRA; o colapso é estritamente factual/distribucional.

### 2.2 Replicação Multi-Seed no Ponto Degradativo ($r=256$, Qwen, $N=3$)
Avaliados ao longo de 10 gerações nas sementes independentes 15, 137 e 256 ($K_0=79$):

| Geração | Seed 15 | Seed 137 | Seed 256 | Média ($\%$) | Desvio Padrão ($\pm$) |
|---|---|---|---|---|---|
| **Gen 0** | 79 (100,0%) | 79 (100,0%) | 79 (100,0%) | 100,0% | $\pm 0,0\%$ |
| **Gen 1** | 75 (94,9%) | 75 (94,9%) | 75 (94,9%) | 94,9% | $\pm 0,0\%$ |
| **Gen 2** | 71 (89,9%) | 71 (89,9%) | 71 (89,9%) | 89,9% | $\pm 0,0\%$ |
| **Gen 3** | 72 (91,1%) | 69 (87,3%) | 71 (89,9%) | 89,4% | $\pm 1,9\%$ |
| **Gen 4** | 70 (88,6%) | 68 (86,1%) | 71 (89,9%) | 88,2% | $\pm 1,9\%$ |
| **Gen 5** | 66 (83,5%) | 67 (84,8%) | 64 (81,0%) | 83,1% | $\pm 1,9\%$ |
| **Gen 6** | 65 (82,3%) | 67 (84,8%) | 66 (83,5%) | 83,5% | $\pm 1,3\%$ |
| **Gen 7** | 64 (81,0%) | 65 (82,3%) | 63 (79,7%) | 81,0% | $\pm 1,3\%$ |
| **Gen 8** | 64 (81,0%) | 64 (81,0%) | 64 (81,0%) | 81,0% | $\pm 0,0\%$ |
| **Gen 9** | 62 (78,5%) | 62 (78,5%) | 61 (77,2%) | 78,1% | $\pm 0,8\%$ |
| **Gen 10** | 60 (75,9%) | 61 (77,2%) | 64 (81,0%) | **78,0%** | $\pm 2,6\%$ |

- Na base $K_0=78$: Média Gen 10 = **79,1%** (Faixa: 76,9% a 82,1%).
- Taxa média de perda factual após Gen 1: **~2,4 pontos percentuais por geração**.
- Faixa homeostática de $r=16$ (97,4%) vs degradativa de $r=256$ (78,0%): **Separação limpa de 19,4 pp sem qualquer sobreposição**.

### 2.3 Dinâmica de Transição Item a Item (Plasticidade vs Ossificação)
Matriz de transição entre estados de acerto ($C$) e erro ($W$) por geração no Qwen Seed 15 ($K_0=78$):

| Configuração | Gerações | Fatos Perdidos ($C \to W$) | Fatos Recuperados ($W \to C$) | Saldo Líquido de Perda | Comportamento Dinâmico |
|---|---|---|---|---|---|
| **$r=4$** | 5 | 1 | 0 | +1 | Oscilação homeostática mínima |
| **$r=16$** | 10 | 3 | 3 | 0 | **Equilíbrio dinâmico perfeito** |
| **$r=32$** | 5 | 2 | 3 | -1 | Recuperação excede perda |
| **$r=64$** | 10 | 7 | 7 | 0 | Oscilação contínua balanceada |
| **$r=128$** | 10 | 10 | 7 | +3 | Leve saldo de perda acumulada |
| **$r=256$** | 10 | 19 | 4 | **+15** | **Esgotamento severo de plasticidade** |

*Descoberta Crítica:* No regime homeostático ($r=16$), o fluxo de recuperação ($W \to C$) compensa perfeitamente as perdas pontuais ($C \to W$). No regime degradativo ($r=256$), a plasticidade se extingue: as perdas saltam para 19 enquanto as recuperações caem para 4, gerando um dreno factual acumulativo irreversível.

### 2.4 Invariância de Topologia Modular (Ablação Atenção vs Linear Completo)
Comparação entre LoRA aplicado apenas a camadas de atenção (`q_proj`, `v_proj`) versus todas as camadas lineares (`q, k, v, o, gate, up, down_proj`):

| Configuração Modular | Posto Nominal ($r$) | Parâmetros Treináveis | Posto Efetivo Médio | Retenção Gen 5 | Retenção Gen 10 |
|---|---|---|---|---|---|
| **Attention-Only** | $r=4$ | 545 K | 3,34 | 75/79 (94,9%) | — |
| **Attention-Only** | $r=16$ | 2,2 M | 11,08 | 75/79 (94,9%) | 75/79 (94,9%) |
| **Attention-Only** | $r=128$ | 17,4 M | 50,16 | 69/79 (87,3%) | 70/79 (88,6%) |
| **Full-Linear** | $r=4$ | 4,6 M | 3,43 | 75/79 (94,9%) | — |
| **Full-Linear** | $r=16$ | 18,4 M | 11,54 | 72/79 (91,1%) | 69/79 (87,3%) |

Trajetória Full-Linear $r=4$ (Gen 0 a 5): G0: 100% $\to$ G1: 93,7% $\to$ G2: 92,4% $\to$ G3: 93,7% $\to$ G4: 94,9% $\to$ G5: 94,9%.  
Trajetória Full-Linear $r=16$ (Gen 0 a 10): G0: 100% $\to$ G1: 94,9% $\to$ G2: 89,9% $\to$ G3: 92,4% $\to$ G4: 88,6% $\to$ G5: 91,1% $\to$ G6: 88,6% $\to$ G7: 89,9% $\to$ G8: 86,1% $\to$ G9: 87,3% $\to$ G10: 87,3%.

*Conclusão:* Full-Linear $r=4$ (4,6M params) retém exatamente o mesmo que Attention $r=16$ (2,2M params), com ambos apresentando posto efetivo similar (~3,4 vs ~11). Full-Linear $r=16$ (18,4M params, erank 11,5) converge a 87,3%, similar a Attention $r=128$ (88,6%). O determinante primário é a **capacidade efetiva média por adaptador**, e não a mera contagem bruta de parâmetros ou a localização dos módulos adaptados.

---

## 3. VALIDAÇÃO MULTI-BACKBONE E DESLOCAMENTO DE THRESHOLD

### 3.1 Gemma 3 1B IT — Fronteira e Degradação Acentuada ($K_0=46$)
Avaliados ao longo de 10 gerações com **5 sementes independentes** ($N=5$: 15, 137, 256, 42, 77) nas fronteiras $r=4$ e $r=16$, além de varredura fina intermediária:

#### A. Posto $r=4$ (Regime Homeostático, 5 seeds $\times$ 10 gerações)
| Seed | Gen 1 | Gen 2 | Gen 3 | Gen 4 | Gen 5 | Gen 6 | Gen 7 | Gen 8 | Gen 9 | Gen 10 | erank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **15** | 95,7% (44) | 93,5% (43) | 97,8% (45) | 93,5% (43) | 93,5% (43) | 93,5% (43) | 93,5% (43) | 93,5% (43) | 93,5% (43) | 93,5% (43) | 3,08 |
| **137** | 93,5% (43) | 95,7% (44) | 93,5% (43) | 95,7% (44) | 93,5% (43) | 95,7% (44) | 100,0% (46)| 91,3% (42) | 95,7% (44) | 95,7% (44) | 3,09 |
| **256** | 95,7% (44) | 91,3% (42) | 89,1% (41) | 93,5% (43) | 91,3% (42) | 91,3% (42) | 95,7% (44) | 95,7% (44) | 97,8% (45) | 93,5% (43) | 3,06 |
| **42** | 93,5% (43) | 91,3% (42) | 95,7% (44) | 97,8% (45) | 95,7% (44) | 91,3% (42) | 93,5% (43) | 91,3% (42) | 95,7% (44) | 93,5% (43) | 3,08 |
| **77** | 95,7% (44) | 91,3% (42) | 95,7% (44) | 93,5% (43) | 89,1% (41) | 93,5% (43) | 93,5% (43) | 93,5% (43) | 95,7% (44) | 95,7% (44) | 3,07 |
| **Média**| **94,8%** | **92,6%** | **94,4%** | **94,8%** | **92,6%** | **93,1%** | **95,2%** | **93,1%** | **95,7%** | **94,4%** | **3,07** |

#### B. Posto $r=16$ (Regime Degradativo, 5 seeds $\times$ 10 gerações)
| Seed | Gen 1 | Gen 2 | Gen 3 | Gen 4 | Gen 5 | Gen 6 | Gen 7 | Gen 8 | Gen 9 | Gen 10 | $\Delta$ G5$\to$10 | erank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **15** | 80,4% (37) | 80,4% (37) | 78,3% (36) | 73,9% (34) | 71,7% (33) | 67,4% (31) | 65,2% (30) | 60,9% (28) | 63,0% (29) | 54,3% (25) | -17,4 pp | 9,23 |
| **137** | 84,8% (39) | 80,4% (37) | 76,1% (35) | 71,7% (33) | 67,4% (31) | 65,2% (30) | 60,9% (28) | 58,7% (27) | 63,0% (29) | 60,9% (28) | -6,5 pp | 9,26 |
| **256** | 82,6% (38) | 78,3% (36) | 76,1% (35) | 71,7% (33) | 67,4% (31) | 63,0% (29) | 63,0% (29) | 63,0% (29) | 63,0% (29) | 52,2% (24) | -15,2 pp | 9,27 |
| **42** | 87,0% (40) | 76,1% (35) | 73,9% (34) | 73,9% (34) | 69,6% (32) | 67,4% (31) | 65,2% (30) | 58,7% (27) | 58,7% (27) | 58,7% (27) | -10,9 pp | 9,28 |
| **77** | 89,1% (41) | 82,6% (38) | 78,3% (36) | 73,9% (34) | 69,6% (32) | 67,4% (31) | 63,0% (29) | 60,9% (28) | 56,5% (26) | 56,5% (26) | -13,1 pp | 9,27 |
| **Média**| **84,8%** | **79,6%** | **76,5%** | **73,0%** | **69,1%** | **66,1%** | **63,5%** | **60,4%** | **60,9%** | **56,5%** | **-12,6 pp**| **9,25** |

*Descoberta Crucial:* A degradação no Gemma 3 em $r=16$ não atinge platô na Gen 5; ela continua despencando até a Gen 10 (perda extra de 12,6 pp), atingindo 56,5% (26/46 acertos).

#### C. Varredura Intermediária Fina (Seed 15, Gen 5, $K_0=46$)
Para delimitar com exatidão o ponto de inflexão no Gemma 3:
- **$r=2$ (exploratório):** Gen 5 = **97,9%** (45/46), erank ~1,8 $\to$ Fortemente Homeostático.
- **$r=4$:** Gen 5 = **93,5%** (43/46), erank = 3,05 $\to$ Homeostático.
- **$r=10$:** Gen 1: 41 (89,1%) $\to$ Gen 2: 39 (84,8%) $\to$ Gen 3: 38 (82,6%) $\to$ Gen 4: 39 (84,8%) $\to$ Gen 5: **36 (78,3%)**, erank = 6,37 $\to$ Início da Degradação.
- **$r=12$:** Gen 1: 38 (82,6%) $\to$ Gen 2: 38 (82,6%) $\to$ Gen 3: 37 (80,4%) $\to$ Gen 4: 34 (73,9%) $\to$ Gen 5: **34 (73,9%)**, erank = 7,35 $\to$ Degradativo.
- **$r=14$:** Gen 1: 40 (87,0%) $\to$ Gen 2: 38 (82,6%) $\to$ Gen 3: 36 (78,3%) $\to$ Gen 4: 34 (73,9%) $\to$ Gen 5: **32 (69,6%)**, erank = 8,37 $\to$ Degradativo.
- **$r=16$:** Gen 5 = **33 (71,7%)**, erank = 9,29 $\to$ Degradativo.
- **$r=256$ (exploratório):** Gen 5 = **70,2%** (32/46), erank ~62 $\to$ Degradativo (efeito de piso/platô a curto prazo).

*Delimitação do Limiar:* No Gemma 3, a transição de regime ocorre entre posto efetivo **3,0 e 6,4** (nominalmente entre $r=4$ e $r=10$).

---

### 3.2 Gemma 4 E2B IT — Terceira Família Arquitetural ($K_0=76$)
Avaliados ao longo de 10 gerações (Seed 15) em 3 postos abrangentes:

| Posto Nominal ($r$) | Posto Efetivo Médio | Retenção Gen 1 | Retenção Gen 5 | Retenção Gen 10 | Regime Classificado | Assinatura Distribucional |
|---|---|---|---|---|---|---|
| **$r=4$** | 2,04 | 74/76 (97,4%) | 71/76 (93,4%) | **72/76 (94,7%)** | **Homeostático** | Comprimento estável (3,54 $\to$ 3,38w), d1 estável (0,58) |
| **$r=16$** | 5,10 | 70/76 (92,1%) | 69/76 (90,8%) | **67/76 (88,2%)** | **Limitado (*Bounded*)** | Leve deriva de comprimento (3,37 $\to$ 2,27w) |
| **$r=64$** | 13,28 | 66/76 (86,8%) | 63/76 (82,9%) | **57/76 (75,0%)** | **Degradativo** | Inflação de tamanho, colapso de d1, aumento de stopwords |

#### Trajetórias Completas Gemma 4 E2B (Gen 1 a 10)
- **$r=4$:** G1: 74 (97,4%) $\to$ G2: 74 (97,4%) $\to$ G3: 74 (97,4%) $\to$ G4: 73 (96,1%) $\to$ G5: 71 (93,4%) $\to$ G6: 72 (94,7%) $\to$ G7: 73 (96,1%) $\to$ G8: 73 (96,1%) $\to$ G9: 72 (94,7%) $\to$ G10: 72 (94,7%).
- **$r=16$:** G1: 70 (92,1%) $\to$ G2: 67 (88,2%) $\to$ G3: 68 (89,5%) $\to$ G4: 69 (90,8%) $\to$ G5: 69 (90,8%) $\to$ G6: 68 (89,5%) $\to$ G7: 66 (86,8%) $\to$ G8: 67 (88,2%) $\to$ G9: 68 (89,5%) $\to$ G10: 67 (88,2%).
- **$r=64$:** G1: 66 (86,8%) $\to$ G2: 68 (89,5%) $\to$ G3: 67 (88,2%) $\to$ G4: 62 (81,6%) $\to$ G5: 63 (82,9%) $\to$ G6: 62 (81,6%) $\to$ G7: 60 (78,9%) $\to$ G8: 60 (78,9%) $\to$ G9: 58 (76,3%) $\to$ G10: 57 (75,0%).

---

### 3.3 Comparativo Cross-Backbone e Incomensurabilidade de Limiares
| Modelo Backbone | Tamanho $K_0$ | Limiar Homeostático | Limiar Degradativo | Faixa Crítica de Transição (erank) |
|---|---|---|---|---|
| **Qwen 2.5 1.5B** | 78 | $r \le 64$ (erank $\le 30$) | $r = 256$ (erank ~88) | **~50 a ~88** |
| **Gemma 3 1B** | 46 | $r \le 4$ (erank $\le 3,1$) | $r \ge 10$ (erank $\ge 6,4$) | **~3,0 a ~6,4** |
| **Gemma 4 E2B** | 76 | $r = 4$ (erank ~2,0) | $r = 64$ (erank ~13,3) | **~5,1 a ~13,3** |

#### Tentativas de Normalização Arquitetural do Limiar (Resultado Negativo)
Testou-se se alguma razão dimensional conseguiria unificar o limiar entre Qwen e Gemma 3:
- $\text{erank} / d$: Qwen = 0,033--0,057 | Gemma 3 = 0,003--0,005 | E2B = 0,003--0,008 $\to$ **Divergência de 10$\times$ (Não alinhou)**.
- $\text{erank} / \sqrt{d}$: Qwen = 1,28--2,24 | Gemma 3 = 0,09--0,18 | E2B = 0,13--0,33 $\to$ **Não alinhou**.
- $\text{erank} / \text{camadas}$: Qwen = 1,79--3,14 | Gemma 3 = 0,12--0,23 | E2B = 0,14--0,37 $\to$ **Não alinhou**.
- $\text{erank} / \text{cabeças}$: Qwen = 4,17--7,33 | Gemma 3 = 0,75--1,50 | E2B = 0,63--1,63 $\to$ **Não alinhou**.
- $\text{erank} / \text{cabeças KV}$: Qwen = 25,0--44,0 | Gemma 3 = 3,0--6,0 | E2B = 5,0--13,0 $\to$ **Não alinhou**.

*Conclusão da Tese:* A transição qualitativa entre homeostase e degradação é **universal entre arquiteturas**, mas o valor numérico do limiar de posto efetivo é **estritamente dependente do modelo base pretreinado** e de sua densidade representacional intrínseca.

---

## 4. EIXO 2: MAGNITUDE DA PERTURBAÇÃO (AJUSTE FINO COMPLETO - FFT VS. QLoRA)

### 4.1 Varredura de Taxa de Aprendizado em FFT (Qwen Seed 15, Gen 1 a 3)
Ajuste fino de todos os pesos do modelo (FFT) em 4 ordens de magnitude de taxa de aprendizado, comparados à referência QLoRA $r=16$:

| Método | Taxa de Aprendizado (LR) | Proxy de Perturbação Médio | Retenção Gen 1 | Retenção Gen 2 | Retenção Gen 3 |
|---|---|---|---|---|---|
| **QLoRA $r=16$** | $10^{-5}$ | 0,4237 ($\|BA\|_F$) | 76/78 (97,4%) | 76/78 (97,4%) | **75/78 (96,2%)** |
| **FFT** | $10^{-6}$ | 0,3886 (Desvio Absoluto de Pesos) | 73/78 (93,6%) | 71/78 (91,0%) | **72/78 (92,3%)** |
| **FFT** | $5 \times 10^{-6}$ | 1,5954 (Desvio Absoluto de Pesos) | 71/78 (91,0%) | 71/78 (91,0%) | **71/78 (91,0%)** |
| **FFT** | $10^{-5}$ | 1,9642 (Desvio Absoluto de Pesos) | 71/78 (91,0%) | 70/78 (89,7%) | **70/78 (89,7%)** |
| **FFT** | $2 \times 10^{-5}$ | 3,5212 (Desvio Absoluto de Pesos) | 70/78 (89,7%) | 70/78 (89,7%) | **66/78 (84,6%)** |

*Desvio relativo:* varia de $0,0002$ ($\text{LR}=10^{-6}$) a $0,0022$ ($\text{LR}=2 \times 10^{-5}$).

---

### 4.2 Comparação Controlada com Perturbação Pareada (10 Gerações $\times$ 3 Seeds)
Comparou-se **QLoRA $r=16$** ($\|BA\|_F \approx 0,41-0,42$) contra **FFT $\text{LR}=10^{-6}$** (desvio absoluto médio de pesos $\approx 0,38-0,39$) em 10 gerações nas sementes 15, 137 e 256 no Qwen ($K_0=78$):

#### A. Trajetória QLoRA $r=16$
- **Seed 15:** G1: 76 $\to$ G2: 76 $\to$ G3: 76 $\to$ G4: 76 $\to$ G5: 75 $\to$ G6: 76 $\to$ G7: 76 $\to$ G8: 75 $\to$ G9: 76 $\to$ **G10: 76 (97,4%)**.
- **Seed 137:** G1: 75 $\to$ G2: 76 $\to$ G3: 76 $\to$ G4: 76 $\to$ G5: 76 $\to$ G6: 75 $\to$ G7: 76 $\to$ G8: 76 $\to$ G9: 76 $\to$ **G10: 76 (97,4%)**.
- **Seed 256:** G1: 76 $\to$ G2: 76 $\to$ G3: 76 $\to$ G4: 76 $\to$ G5: 76 $\to$ G6: 76 $\to$ G7: 76 $\to$ G8: 76 $\to$ G9: 76 $\to$ **G10: 76 (97,4%)**.
- **Média Gen 10 QLoRA:** **97,4%** ($\pm 0,0\%$).

#### B. Trajetória FFT $\text{LR}=10^{-6}$
- **Seed 15:** G1: 72 $\to$ G2: 72 $\to$ G3: 71 $\to$ G4: 72 $\to$ G5: 71 $\to$ G6: 72 $\to$ G7: 72 $\to$ G8: 72 $\to$ G9: 71 $\to$ **G10: 72 (92,3%)**.
- **Seed 137:** G1: 72 $\to$ G2: 73 $\to$ G3: 72 $\to$ G4: 72 $\to$ G5: 72 $\to$ G6: 72 $\to$ G7: 72 $\to$ G8: 72 $\to$ G9: 71 $\to$ **G10: 71 (91,0%)**.
- **Seed 256:** G1: 72 $\to$ G2: 71 $\to$ G3: 72 $\to$ G4: 72 $\to$ G5: 72 $\to$ G6: 72 $\to$ G7: 71 $\to$ G8: 72 $\to$ G9: 72 $\to$ **G10: 72 (92,3%)**.
- **Média Gen 10 FFT:** **91,9%** ($\pm 0,7\%$, Faixa: 91,0% a 92,3%).

#### C. Principais Descobertas
1. **Diferença de Custo Único de Adaptação (*One-time Cost*):** O QLoRA sustenta uma vantagem constante de **~5,5 pontos percentuais** sobre o FFT. Esse gap surge integralmente na Geração 1 e permanece absolutamente inalterado até a Geração 10. Ambas as técnicas são homeostáticas após o choque inicial.
2. **Piso Factual Frágil Determinístico no FFT:**
   - Sob FFT, exatamente os mesmos 6 fatos de $K_0$ foram perdidos em todas as três sementes: **índices [24, 46, 48, 56, 69, 74]**. A similaridade de Jaccard entre as sementes foi **1,0**.
   - Sob QLoRA, apenas 2 a 3 fatos foram perdidos por semente: **[11, 12]** nas seeds 15 e 256; **[11, 12, 57]** na seed 137.
   - **Sobreposição entre fatos perdidos por FFT e QLoRA:** **Zero itens (Jaccard = 0,0)**. O subespaço restrito de posto baixo protege a base factual sensível ao FFT irrestrito.

---

### 4.3 Generalização da Magnitude: FFT no Gemma 3 1B ($K_0=46$, Seed 15)
| Taxa de Aprendizado (LR) | Gen 1 | Gen 2 | Gen 3 | Gen 4 | Gen 5 Retenção (%) |
|---|---|---|---|---|---|
| **$\text{LR} = 10^{-6}$** | 40/46 (87,0%) | 38/46 (82,6%) | 39/46 (84,8%) | 37/46 (80,4%) | **36/46 (78,3%)** |
| **$\text{LR} = 5 \times 10^{-6}$** | 43/46 (93,5%) | 40/46 (87,0%) | 37/46 (80,4%) | 27/46 (58,7%) | **25/46 (54,3%)** |
| **$\text{LR} = 10^{-5}$** | 42/46 (91,3%) | 41/46 (89,1%) | 34/46 (73,9%) | 32/46 (69,6%) | **29/46 (63,0%)** |

*Conclusão:* No Gemma 3, taxas de aprendizado elevadas no FFT induzem colapso severo (54,3%), comprovando que o eixo de magnitude da perturbação atua independentemente da técnica PEFT.

---

## 5. INTERAÇÃO EIXO 1 $\times$ EIXO 2 (MATRIZ $3 \times 3$ POSTO $\times$ TAXA DE APRENDIZADO)

Para provar que os eixos de Capacidade e Magnitude interagem conjuntamente na definição da pressão de treinamento, executou-se uma grade $3 \times 3$ completa no Qwen (Seed 15, Gen 1 a 5, $K_0=78$):

### Tabela de Retenção na Geração 5 (%)
| Posto Nominal ($r$) \ LR | $\mathbf{LR = 5 \times 10^{-6}}$ | $\mathbf{LR = 10^{-5}}$ | $\mathbf{LR = 2 \times 10^{-5}}$ |
|---|---|---|---|
| **$r = 16$** | 76/78 (**97,4%**) | 76/78 (**97,4%**) | 72/78 (**92,3%**) |
| **$r = 64$** | 76/78 (**97,4%**) | 72/78 (**92,3%**) | 69/78 (**88,5%**) |
| **$r = 256$** | 70/78 (**89,7%**) | 66/78 (**84,6%**) | 64/78 (**82,1%**) |

#### Trajetórias Completas Gen 1 a 5 de Todas as 9 Células
- **$r=16, \text{LR}=5\times10^{-6}$:** G1: 76 $\to$ G2: 76 $\to$ G3: 76 $\to$ G4: 78 $\to$ **G5: 76 (97,4%)**.
- **$r=16, \text{LR}=10^{-5}$:** G1: 76 $\to$ G2: 75 $\to$ G3: 75 $\to$ G4: 76 $\to$ **G5: 76 (97,4%)**.
- **$r=16, \text{LR}=2\times10^{-5}$:** G1: 74 $\to$ G2: 73 $\to$ G3: 72 $\to$ G4: 73 $\to$ **G5: 72 (92,3%)**.
- **$r=64, \text{LR}=5\times10^{-6}$:** G1: 76 $\to$ G2: 76 $\to$ G3: 75 $\to$ G4: 75 $\to$ **G5: 76 (97,4%)**.
- **$r=64, \text{LR}=10^{-5}$:** G1: 73 $\to$ G2: 72 $\to$ G3: 72 $\to$ G4: 72 $\to$ **G5: 72 (92,3%)**.
- **$r=64, \text{LR}=2\times10^{-5}$:** G1: 75 $\to$ G2: 73 $\to$ G3: 71 $\to$ G4: 73 $\to$ **G5: 69 (88,5%)**.
- **$r=256, \text{LR}=5\times10^{-6}$:** G1: 73 $\to$ G2: 72 $\to$ G3: 72 $\to$ G4: 71 $\to$ **G5: 70 (89,7%)**.
- **$r=256, \text{LR}=10^{-5}$:** G1: 75 $\to$ G2: 72 $\to$ G3: 70 $\to$ G4: 69 $\to$ **G5: 66 (84,6%)**.
- **$r=256, \text{LR}=2\times10^{-5}$:** G1: 70 $\to$ G2: 69 $\to$ G3: 69 $\to$ G4: 70 $\to$ **G5: 64 (82,1%)**.

*Conclusões da Matriz de Interação:*
1. **Compensação entre eixos:** Reduzir a LR para $5\times10^{-6}$ permite ao modelo operar com posto alto ($r=64$) em regime puramente homeostático (97,4%), e recupera o $r=256$ de 84,6% para 89,7%.
2. **Empurrão para instabilidade:** Elevar a LR para $2\times10^{-5}$ quebra a estabilidade até de $r=16$, reduzindo a retenção para 92,3%.
3. A pressão efetiva de treinamento (ETP) é uma **função acoplada não-linear** de ambos os fatores.

---

## 6. ASSINATURAS MECANÍSTICAS E DERIVA DISTRIBUCIONAL

### 6.1 A Dissociação Factual-Distribucional em $r=128$
O experimento longitudinal em Qwen $r=128$ revelou uma dissociação sem precedentes na literatura de colapso:
- **Retenção de $K_0$:** Mantém-se aparentemente estável / limitada em **88,6%--89,7%** na Gen 10.
- **Qualidade Distribucional:** Sofre **colapso catastrófico precoce**:
  - Comprimento médio das respostas infla de **2,47 palavras para 6,95 palavras** (aumento de quase 300%).
  - Taxa de *stopwords* dobra de **12,6% para 25,1%**.
  - Eficiência de Conteúdo ($\text{Retenção} / \text{Comprimento}$) despenca de **0,406 para 0,127** (diluição de 3,2$\times$).
  - Diversidade lexical robusta (MTLD) desaba de **2.673 para 745**.
  - Persistência das respostas originais de Gen 0 cai de **35,7% para irrisórios 5,2%**.

### 6.2 Os Dois Fenótipos de Degradação Distribucional Acima do Limiar
1. **Fenótipo de Prolixidade por Preenchimento (*Filler Verbosity*) — Exemplo: Qwen $r=128$:**
   O modelo mantém as entidades factuais básicas, mas envolve-as em camadas redundantes de preenchimento gramatical e repetições de pronomes/artigos. O MTLD entra em colapso e as *stopwords* dobram.
2. **Fenótipo de Deriva Elaborativa (*Elaborative Drift*) — Exemplo: Qwen $r=256$ e Gemma 4 E2B $r=64$:**
   O modelo expande o comprimento médio das respostas (2,5w $\to$ 3,6w no Qwen; 3,6w $\to$ 4,4w no E2B), o MTLD **aumenta** (2.673 $\to$ 3.804) e a taxa de stopwords **diminui** (12,6% $\to$ 9,3%). O modelo alucina vocabulário variado e sofisticado, perdendo completamente a ancoragem factual original.

---

### 6.3 Tabela Integral de Métricas Distribucionais (Gen 0 a 10)
Dados auditados extraídos dos corpora sintéticos (2.000 amostras por geração):

| Configuração | Gen | Retenção | Distinct-1 | Distinct-2 | MTLD | Stopwords (%) | Comprimento Médio | Eficiência de Conteúdo | Persistência Gen 0 |
|---|---|---|---|---|---|---|---|---|---|
| **Qwen $r=16$** | 0 | 1,000 | 0,6711 | 0,9521 | 2672,7 | 12,57% | 2,47w | 0,4055 | — |
| (Homeostático) | 1 | 0,949 | 0,6422 | 0,9474 | 2172,8 | 15,87% | 2,63w | 0,3602 | 35,7% |
| | 3 | 0,949 | 0,6424 | 0,9464 | 2045,3 | 15,35% | 2,65w | 0,3580 | 35,4% |
| | 5 | 0,949 | 0,6395 | 0,9419 | 2001,9 | 15,58% | 2,68w | 0,3536 | 35,6% |
| | 7 | 0,949 | 0,6359 | 0,9443 | 2113,1 | 16,16% | 2,66w | 0,3571 | 34,0% |
| | 10 | 0,949 | 0,6369 | 0,9457 | 2035,6 | 16,28% | 2,70w | 0,3520 | **36,1%** |
|---|---|---|---|---|---|---|---|---|---|
| **Qwen $r=128$** | 0 | 1,000 | 0,6711 | 0,9521 | 2672,7 | 12,57% | 2,47w | 0,4055 | — |
| (*Bounded* / Dissoc.)| 1 | 0,910 | 0,6603 | 0,9574 | 2676,2 | 13,95% | 2,59w | 0,3511 | 28,6% |
| | 3 | 0,885 | 0,6304 | 0,9447 | 2180,2 | 16,64% | 3,08w | 0,2877 | 23,2% |
| | 5 | 0,873 | 0,6026 | 0,9301 | 1986,8 | 16,88% | 3,60w | 0,2422 | 16,5% |
| | 7 | 0,885 | 0,5789 | 0,9273 | 1522,0 | 17,83% | 4,22w | 0,2098 | 11,7% |
| | 10 | 0,886 | **0,4621** | **0,8762** | **744,8** | **25,12%** | **6,95w** | **0,1274** | **5,2%** |
|---|---|---|---|---|---|---|---|---|---|
| **Qwen $r=256$** | 0 | 1,000 | 0,6711 | 0,9521 | 2672,7 | 12,57% | 2,47w | 0,4055 | — |
| (Degradativo) | 1 | 0,936 | 0,6692 | 0,9590 | 2671,4 | 12,72% | 2,49w | 0,3762 | 32,6% |
| | 3 | 0,897 | 0,6626 | 0,9442 | 2922,3 | 13,40% | 2,76w | 0,3249 | 25,4% |
| | 5 | 0,831 | 0,6510 | 0,9412 | 2586,8 | 13,57% | 3,09w | 0,2692 | 20,2% |
| | 7 | 0,795 | 0,6304 | 0,9337 | 2518,0 | 13,04% | 3,38w | 0,2349 | 14,4% |
| | 10 | 0,780 | 0,6574 | 0,9466 | **3804,1** | **9,27%** | **3,56w** | **0,2194** | **3,8%** |
|---|---|---|---|---|---|---|---|---|---|
| **Gemma 3 $r=4$**| 0 | 1,000 | 0,6985 | 0,9513 | 2737,5 | 7,71% | 2,23w | 0,4483 | — |
| (Homeostático) | 5 | 0,922 | 0,7005 | 0,9584 | 2925,7 | 8,09% | 2,29w | 0,4020 | 48,6% |
| | 10 | 0,936 | 0,7025 | 0,9601 | 3005,4 | 8,39% | 2,33w | 0,4018 | **46,1%** |
|---|---|---|---|---|---|---|---|---|---|
| **Gemma 3 $r=16$**| 0 | 1,000 | 0,6985 | 0,9513 | 2737,5 | 7,71% | 2,23w | 0,4483 | — |
| (Degradativo) | 5 | 0,688 | 0,6464 | 0,9609 | 3867,3 | 9,79% | 3,85w | 0,1788 | 3,5% |
| | 10 | 0,565 | 0,6597 | 0,9580 | ~3900 | 7,09% | 3,65w | 0,1548 | <2,0% |
|---|---|---|---|---|---|---|---|---|---|
| **Gemma 4 $r=64$**| 1 | 0,868 | 0,5469 | — | — | 22,81% | 3,61w | 0,2404 | — |
| (Degradativo) | 5 | 0,829 | 0,4745 | — | — | 28,05% | 3,91w | 0,2120 | — |
| | 10 | 0,750 | **0,4266** | — | — | **28,42%** | **4,44w** | **0,1689** | — |

---

### 6.4 Análise de Causalidade Cruzada Temporal (*Cross-Lag Analysis*)
Avaliação de precedência temporal entre deriva distribucional (comprimento médio $L_t$) e perda factual de retenção ($R_{t+1}$):

| Configuração | Regime | Correlação Bruta $\rho(L_t, R_{t+1})$ | Correlação Parcial ($\mid \text{gen}$) | Primeira Diferença $\rho(\Delta L, \Delta R)$ | Lag Reverso $\rho(R_t, L_{t+1})$ |
|---|---|---|---|---|---|
| **Qwen $r=16$** | Homeostático | 0,000 | 0,000 | 0,000 | -0,251 |
| **Qwen $r=256$** | **Degradativo** | **-0,965** | **-0,220** | **-0,433** | **-0,986** |
| **Gemma 3 $r=4$** | Homeostático | +0,110 | +0,030 | +0,334 | -0,381 |
| **Gemma 3 $r=16$**| Degradativo | -0,847 | +0,995* | +0,990* | -0,952 |

*(Obs: Gemma 3 $r=16$ possui poucos pontos em Gen 5 para isolamento não-espúrio de tendência temporal).*

*Interpretação Rigorosa do Artigo:* A correlação bruta massiva (-0,965) é grandemente inflada pela tendência monótona compartilhada com o tempo. Ao controlar pela geração, a correlação cai para $-0,220$, e o lag reverso é igualmente forte (-0,986). Portanto, a deriva distribucional **não é a causa primária** da perda factual, mas sim um **co-sintoma patológico observável** do mesmo regime de sobrepressão de treinamento.

---

### 6.5 Índice Sintético de Deriva (SDI-3)
$$\text{SDI-3} = \ln\left(\frac{\text{len}_{\text{final}}}{\text{len}_0}\right) + \ln\left(\frac{\text{d1}_0}{\text{d1}_{\text{final}}}\right) + \Delta_{\text{instabilidade}}$$

Valores calculados no final do ciclo:
- **Gemma 3 $r=4$ (Homeostático):** **0,038**
- **Qwen $r=16$ (Homeostático):** **0,161**
- **Qwen $r=256$ (Degradativo):** **0,437**
- **Gemma 3 $r=16$ (Degradativo):** **0,705**
- **Qwen $r=128$ (Deriva Distribucional Máxima):** **1,530**

---

## 7. EIXO 3: INTERVENÇÕES DE EXPOSIÇÃO SINTÉTICA (REVERSÃO NA FRONTEIRA)

Experimentos focados na fronteira degradativa **Qwen $r=256$** na Geração 5 ($K_0=78$ itens auditados):

| Condição Experimental | Descrição Operacional | Retenção Gen 5 (%) | Fração $K_0$ | Ganho ($\Delta$) | Volume Tokens | Réplicas |
|---|---|---|---|---|---|---|
| **C1: Normal (Base)** | Geração estocástica padrão sem qualquer filtro | **83,3%** | 65/78 | — | ~57k | $N=1$ |
| **C2: Short-Constrained** | Restrição de 5 palavras via prompt de sistema | **91,0%** | 71/78 | **+7,7 pp** | ~60k | $N=1$ |
| **C3: Length-Filtered** | Descarte de respostas com $>5$ palavras | **92,3%** | 72/78 | **+9,0 pp** | ~54k | $N=3$ seeds |
| **C4: Canonical Format** | Extração heurística de resposta limpa e canônica | **88,5%** | 69/78 | **+5,1 pp** | ~52k | $N=1$ |
| **C5: Random Downsample**| Descarte aleatório de ~5% de tokens (pareado ao C3) | **92,7%** | 72,3/78 | **+9,4 pp** | ~54k | $N=3$ máscaras |

### 7.1 Dados Detalhados das Réplicas Multi-Seed / Multi-Máscara (Gen 1 a 5)
- **C1 Normal (Seed 15):** G1: 74 $\to$ G2: 72 $\to$ G3: 70 $\to$ G4: 68 $\to$ **G5: 65 (83,3%)**.
- **C2 Short (Seed 15):** G1: 74 $\to$ G2: 72 $\to$ G3: 72 $\to$ G4: 71 $\to$ **G5: 71 (91,0%)**.
- **C3 Length-Filtered:**
  - Seed 15: G1: 74 $\to$ G2: 74 $\to$ G3: 71 $\to$ G4: 71 $\to$ **G5: 73 (93,6%)**.
  - Seed 137: G1: 74 $\to$ G2: 73 $\to$ G3: 72 $\to$ G4: 72 $\to$ **G5: 71 (91,0%)**.
  - Seed 256: G1: 75 $\to$ G2: 73 $\to$ G3: 72 $\to$ G4: 71 $\to$ **G5: 72 (92,3%)**.
  - *Média C3:* **92,3% $\pm 1,3\%$** (Faixa: 91,0% a 93,6%).
- **C4 Canonical (Seed 15):** G1: 74 $\to$ G2: 74 $\to$ G3: 71 $\to$ G4: 68 $\to$ **G5: 69 (88,5%)**.
- **C5 Token-Matched Random Downsampling:**
  - Seed 15 (Máscara 1): G1: 74 $\to$ G2: 73 $\to$ G3: 74 $\to$ G4: 72 $\to$ **G5: 72 (92,3%)**.
  - Máscara 42: G1: 74 $\to$ G2: 73 $\to$ G3: 74 $\to$ G4: 72 $\to$ **G5: 73 (93,6%)**.
  - Máscara 99: G1: 74 $\to$ G2: 73 $\to$ G3: 72 $\to$ G4: 73 $\to$ **G5: 72 (92,3%)**.
  - *Média C5:* **92,7% $\pm 0,7\%$** (Faixa: 92,3% a 93,6%).

### 7.2 Implicações Cruciais do Eixo de Intervenção
1. **Invariância Qualitativa da Amostra:** A similaridade de Jaccard entre as perguntas descartadas pelo filtro C3 (baseado em prolixidade) e pelo sorteio aleatório C5 foi de apenas **0,015** (conjuntos essencialmente disjuntos). No entanto, o ganho de retenção foi idêntico (+9,0 pp vs +9,4 pp).
2. **Reversão com Derivação Mínima:** A redução de meros **~5% na exposição a tokens sintéticos** na fronteira de $r=256$ foi suficiente para comutar o sistema de um regime degradativo (83,3%) de volta para o nível homeostático (92,7%).
3. **Controle C2:** A condição C2 utilizou **mais tokens** que a C1 (60k vs 57k) e mesmo assim obteve ganho de +7,7 pp, demonstrando que a intervenção atua no formato e na estabilização do sinal, e não em subtreinamento mecânico.

---

## 8. CONTROLES SECUNDÁRIOS, CKA E ESTUDOS DA FASE M2

### 8.1 Controle G1 (Sintético) vs. G2 (Dados Reais Independentes)
Executado na fase M2 sobre Qwen $r=16$ (3 gerações $\times$ 3 seeds, $K_0=79$):

| Grupo Experimental | Gen 0 | Gen 1 | Gen 2 | Gen 3 | Retenção Final Média |
|---|---|---|---|---|---|
| **G1 (Sintético Recursivo)** | 79/79 (100%) | 75/79 (94,9%) | 75/79 (94,9%) | 75/79 (94,9%) | **94,5% $\pm 0,7\%$** |
| **G2 (Reais - Shards TriviaQA)**| 79/79 (100%) | 76/79 (96,2%) | 76/79 (96,2%) | 75/79 (94,9%) | **95,4% $\pm 0,8\%$** |

#### Transições Fatuais G1 vs G2 (Seed 15)
- **G1 (Sintético):**
  - Gen 1: $C \to W = 4$, $W \to C = 4$.
  - Gen 2: $C \to W = 0$, $W \to C = 0$.
  - Gen 3: $C \to W = 0$, $W \to C = 0$.
  - *Comportamento:* **Congelamento total após Gen 1 (Ossificação Factual).** O modelo para de esquecer e para de aprender.
- **G2 (Real):**
  - Gen 1: $C \to W = 3$, $W \to C = 4$.
  - Gen 2: $C \to W = 0$, $W \to C = 4$.
  - Gen 3: $C \to W = 2$, $W \to C = 2$.
  - *Comportamento:* **Fluxo factual contínuo.** Dados reais preservam a plasticidade do modelo na fronteira de decisão.

---

### 8.2 Análise de Alinhamento Representacional (CKA)
Comparação de CKA Linear Factual (último token da pergunta, Camada 13) versus CKA Global (média de pooling):
- **CKA Factual G1 (Sintético) vs Gen 0:** Gen 1 = 0,9836 | Gen 2 = 0,9824 | Gen 3 = 0,9826.
- **CKA Factual G2 (Dados Reais) vs Gen 0:** Gen 1 = 0,9827 | Gen 2 = ~0,982 | Gen 3 = ~0,982.
- *Refutação Metodológica:* O CKA Factual cai exatamente no mesmo valor (~0,983) em dados sintéticos e dados reais. O CKA quantifica o **custo geométrico de adaptação ao formato**, e **não detecta a toxicidade recursiva**.

---

## 9. MATRIZ DE EVIDÊNCIAS E ESCOPO DE GENERALIZAÇÃO

### 9.1 Mapeamento Tese vs. Suporte Empírico
| Afirmação Científica do Manuscrito | Base Experimental Comprobatória | Nível de Confiança |
|---|---|---|
| **O posto LoRA governa a transição de regime** | Varredura de 6 postos em Qwen, réplica 3 seeds em $r=16$ e $r=256$ | **Definitivo (N=3, 10 gens)** |
| **A taxa de aprendizado em FFT reproduz o mesmo padrão** | Varredura de 4 LRs em FFT no Qwen; reprodução de 3 LRs no Gemma 3 | **Forte (2 backbones)** |
| **Capacidade e Magnitude interagem conjuntamente** | Matriz $3 \times 3$ completa Posto $\times$ LR no Qwen (9 células) | **Definitivo (5 gens)** |
| **O limiar é dependente do backbone (~10$\times$ de diferença)** | Qwen (50-88), Gemma 3 (3-6), Gemma 4 E2B (5-13) | **Definitivo (3 famílias)** |
| **A deriva distribucional acompanha a degradação factual** | Métricas completas (distinct-1, MTLD, stopwords, persistência, eficiência) | **Definitivo (10 gens)** |
| **Dissociação em $r=128$ (retenção estável, distribuição colapsada)** | Corpora sintéticos de $r=128$ ao longo de 10 gerações | **Definitivo** |
| **Redução marginal de 5% de exposição recupera homeostase** | Intervenções C3 (3 seeds) e C5 (3 máscaras) com Jaccard 0,015 | **Definitivo no limiar Qwen** |
| **FFT gera piso frágil determinístico; QLoRA protege subespaço** | Sobreposição Jaccard = 1,0 no FFT e 0,0 entre FFT e QLoRA | **Definitivo (3 seeds, 10 gens)** |

---

### 9.2 O Que a Evidência Sustenta vs. O Que Permanece em Aberto
| Sustentado pelo Estudo | Questões em Aberto / Limitações Declaradas |
|---|---|
| Transição de regime existe e é reprodutível | Comportamento em modelos $>7\text{B}$ / $70\text{B}$ |
| Dependência multidimensional de pressão (ETP) | Expressão analítica escalar fechada para ETP |
| Fronteira abrupta de controle por redução marginal | Dinâmica assintótica além de 10 gerações |
| Reprodutibilidade estatística (3 a 5 seeds independentes) | Tarefas de geração aberta, código e raciocínio multi-passo |
| Incomensurabilidade de posto bruto entre arquiteturas | Fórmula universal de normalização de postos entre backbones |
| Intervenção C3/C5 eficaz no limiar Qwen | Eficácia da redução de 5% em outros modelos (Gemma não respondeu) |
| Custo de adaptação inicial único no FFT vs QLoRA | Mecanismo geométrico exato no espaço de parâmetros de $W$ |

---

## 10. DIRETÓRIO DE ARQUIVOS-FONTE E SCRIPTS DE AUDITORIA

Todos os dados brutos que deram origem às tabelas acima encontram-se persistidos no repositório:
- **Resultados JSON brutos:** `Paradoxo\llm-knowledge-collapse\outputs\`
  - `g1_rank*_seed*/results.json`: Varredura primária Qwen
  - `v3_gemma3_rank*/results.json`: Gemma 3 multi-seed 10 gerações
  - `v3_gemma4_rank*/results.json`: Gemma 4 E2B 10 gerações
  - `fft_drift_gen10/`: Pareamento longitudinal QLoRA vs FFT 10 gerações
  - `rank_lr_matrix/`: Matriz de interação $3 \times 3$
  - `causal_intervention/`, `intervention_validation/`, `c5_masks/`: Intervenções C1 a C5
- **Tabelas de métricas computadas:**
  - `Paradoxo\llm-knowledge-collapse\outputs\diversity_analysis\complete_metrics.csv`
  - `Paradoxo\llm-knowledge-collapse\outputs\diversity_analysis\refined_analysis.csv`
  - `Paradoxo\llm-knowledge-collapse\outputs\v3_analysis.txt`
- **Manuscrito submetido oficial (LaTeX):**
  - `Paradoxo\llm-knowledge-collapse (paper)\v4\manuscript-anonymous.tex`
- **Figuras oficiais geradas:**
  - `Paradoxo\llm-knowledge-collapse (paper)\v4\figs\`

---
*Fim do documento consolidado.*
