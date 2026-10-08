# CONSOLIDAÇÃO INTEGRAL E DEFINITIVA DE DADOS, VALORES E RESULTADOS DO DIRETÓRIO PARADOXO
## Mapeamento Unificado de Pesquisa: Artigo Empírico, Survey Teórico, Revisões Laboratoriais e Estratégia Editorial

**Arquivo de Destino:** `Paradoxo\llm-knowledge-collapse (paper)\v4\DADOS_E_RESULTADOS_CONSOLIDADOS.md`  
**Escopo do Mapeamento:** Todo o ecossistema presente em `G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo`  
**Data de Atualização:** 2026-09-29  
**Status do Projeto:** Manuscrito empírico submetido à *Engineering Applications of Artificial Intelligence* (EAAI, Elsevier); Survey teórico submetido à *Computer Science Review* (Elsevier) / ACM. Experimentos 100% concluídos e auditados.

---

## 1. VISÃO GERAL E RELACIONAMENTO ENTRE OS TRABALHOS

No diretório raiz `Paradoxo`, coexistem **duas vertentes complementares e interdependentes** desenvolvidas pelo laboratório:

```
G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\
├── llm-knowledge-collapse\               # Repositório de código, pipelines e dados brutos de execução
├── llm-knowledge-collapse (paper)\       # Manuscritos empíricos (v1, v2, v3 e v4 final submetida)
├── new-submisions\
│   ├── computer-science-review\          # Survey teórico para Elsevier Computer Science Review (CSR)
│   └── acm\                              # Survey teórico adaptado para ACM Computing Surveys
├── Related papers\                       # Versões e materiais da submissão inicial da Survey
├── Review\Carlos\                        # Rodadas de auditoria interna e peer-review do Prof. Carlos André (v1 e v3)
├── ideias\                               # Proposta de extensão ("Adaptive Pressure Control")
├── analise-revistas.md                   # Auditoria bibliométrica (ToolHub CAPES, Qualis A1, JIFs, APC)
├── perguntas e respostas.txt             # Síntese epistemológica profunda sobre Model Collapse (16 fontes)
└── Resumo.txt                            # Briefing executivo sobre colapso em LLMs e riscos em Federated Learning
```

### 1.1 O Artigo Empírico (Foco Principal em `v4`)
- **Título Oficial:** *"Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study"*
- **Autores:** Julio Azancort Neto, et al.
- **Revista-Alvo:** *Engineering Applications of Artificial Intelligence* (Elsevier) — Qualis Capes: **A1** (Engenharias IV), Fator de Impacto: **8.0** (Q1).
- **Proposta Central:** Investigar as condições sob as quais a degradação recursiva de conhecimento emerge ou permanece contida sob ajuste fino com parâmetros eficientes (PEFT/QLoRA), formulando o princípio unificador da **Pressão Efetiva de Treinamento (ETP)**.

### 1.2 O Artigo Teórico / Survey (Origem dos Conceitos em `new-submisions`)
- **Título Oficial:** *"Recursive Training Failures in Large Language Models: A Unified Taxonomy, Security Analysis, and Governance Framework"*
- **Autores:** Julio Leite Azancort Neto, Carlos André de Mattos Teixeira, Carlos Renato Lisboa Francês (Laboratório de Computação Urbana e Tecnologias de Informação - Labcity / UFPA).
- **Proposta:** Unificar a literatura matemática e empírica (2023–2026) sobre falhas recursivas, categorizar regimes de colapso, formalizar o vetor de ataque em Aprendizado Federado (backdoor injection via modelos fundacionais) e propor governança técnica e institucional.

---

## 2. A BASE TEÓRICA E A TAXONOMIA DE COLAPSO (SURVEY COMPANION)

Os dados teóricos estruturados em `new-submisions/computer-science-review/main.tex`, `Resumo.txt` e `perguntas e respostas.txt` estabeleceram as premissas testadas experimentalmente no artigo empírico.

### 2.1 Taxonomia dos Regimes de Colapso (2023–2026)
| Regime de Colapso | Mecanismo Primário | Resultado Formal Central | Assinatura Observável | Referências-Chave |
|---|---|---|---|---|
| **Model Collapse (Estatístico)** | Acúmulo de erros de amostragem, aproximação funcional e otimização. | Caudas da distribuição desaparecem; variância colapsa a zero. | Perda de diversidade lexical; convergência para respostas modais repetitivas. | Shumailov et al. (Nature 2024) |
| **Strong Model Collapse** | Fração arbitrária $k > 0$ de contaminação sintética no corpus de treino. | $\mathbb{E}[\mathcal{L}_T] \geq \mathbb{E}[\mathcal{L}_0] + \alpha k T$; invalidação de scaling laws. | Crescimento linear monotônico do erro de teste ao longo das gerações. | Dohmatob et al. (ICLR 2025) |
| **Total Collapse** | Cadeia recursiva de Markov no simplex de probabilidades sem dados reais. | $\lim_{T\to\infty} p_T = \delta_{\tau^*}$ (massa pontual Dirac). | Entropia zero nas saídas; previsões determinísticas idênticas (*gibberish*). | Seddik et al. (COLM 2024) |
| **Knowledge Collapse (Estágio B)** | Treinamento sintético recursivo com formato persistente de instruções. | Acurácia factual colapsa ($\to 0$), enquanto fluência e confiança permanecem altas. | Saídas "confiantemente erradas" (*confidently incorrect*); métricas de fluência falham. | Keisha et al. (arXiv 2025) |
| **Directed Collapse (Adversarial)** | Injeção de gatilho via In-Context Learning (ICL) em dados sintéticos para Federated Learning. | Taxa de Sucesso de Ataque (ASR) $> 90\%$; persistência por rodadas de FL. | Desempenho normal em entradas limpas; classificação errônea direcionada em gatilhos. | Li et al. (2023), Bi et al. (2024) |

### 2.2 Estratégias Teóricas de Mitigação Confrontadas no Estudo
1. **Acumulação de Dados (*Data Accumulation*) [Gerstgrasser et al., ICML 2024]:**
   - *Mecanismo:* Novos dados sintéticos são adicionados ao corpus real original em vez de substituí-lo.
   - *Garantia:* Limite superior finito para o erro quadrático médio: $\text{MSE}_T \le \frac{\sigma^2 d}{T - d - 1} \cdot \frac{\pi^2}{6}$.
   - *Contraste com nosso artigo:* O artigo empírico adotou intencionalmente o protocolo severo de **substituição total (*replace-only*, 0% dados reais)** para provar que a estabilidade pode ser garantida no eixo dos *updates* (PEFT) sem demandar acúmulo de dados reais.
2. **Entropia Cruzada Truncada (*Truncated Cross-Entropy - TCE*) [Zibakhsh et al., 2024]:**
   - *Mecanismo:* Mascara tokens de confiança excessiva ($p_\theta \ge \tau$) do cálculo do gradiente, forçando aprendizado nas caudas. Aumenta a tolerância a dados sintéticos em **2,3$\times$**.
3. **Verificação Externa Sintética (*Synthetic Data Verification*) [Yi et al., 2025]:**
   - *Mecanismo:* Filtra dados sintéticos por um verificador externo. O modelo converge para o centro de conhecimento do verificador ($\theta_c$).
4. **Ancoragem em Domínio Específico [Keisha et al., 2025]:**
   - *Mecanismo:* Restringe os dados a corpora semanticamente alinhados, reduzindo a taxa de colapso em até **15$\times$**.

---

## 3. HISTÓRICO DE REVISÕES LABORATORIAIS E AUDITORIA ATHENA (`Review\Carlos`)

O artigo passou por duas rodadas exaustivas de revisão crítica interna conduzidas pelo Prof. Carlos André (detalhadas em `Review\Carlos\v1` e `v3`), com **41 comentários na Revisão 1** e **56 anotações na Revisão 2**, originando a bateria Athena v3.

### 3.1 Mapeamento das Demandas Críticas do Reviewer vs. Execução Empírica
| Item da Revisão | Objeção / Demanda do Prof. Carlos André | Resolução / Experimento Executado | Localização dos Dados |
|---|---|---|---|
| **#12 (v1)** | "Eu não usaria few minutes, melhor ser mais específico no tempo." | Cronometragem rigorosa inserida: **~3 min** em postos baixos ($r \le 16$) e **~12 min** em $r=256$ por geração na RTX 3070. | Metodologia §3 |
| **#37 (v2)** | "Gemma 3 para na gen 5? Não deveria ir até 10? Padronizar." | Execução de **5 seeds $\times$ 10 gerações completas** no nó Athena ($r=4$ e $r=16$). | `v3_gemma3_rank*` |
| **#39 (v2)** | "E2B precisa de gráficos comparáveis e dose-resposta clara." | Execução de **3 postos ($r=4, 16, 64$) $\times$ 10 gerações** no nó Athena. | `v3_gemma4_rank*` |
| **#43 (v2)** | "E2B no FFT ou justificar ausência formalmente." | Justificativa técnica formalizada: 20 GB de VRAM insuficiente para FFT completo em backbone de 2B sem OOM. | Seção de Limitações §6 |
| **#45/#47 (v2)** | "Tabelas e métricas distribucionais para Gemma 3 e E2B." | Extração completa de distinct-1, distinct-2, stopwords, comprimento médio e MTLD. | `complete_metrics.csv` |
| **#49 (v2)** | "Intervenções C3 e C5 ambas replicadas com intervalos." | C3 replicado em **3 seeds** (15, 137, 256); C5 replicado em **3 máscaras** aleatórias (15, 42, 99). | `intervention_validation` |
| **#51 (v2)** | "Figura de intervenções precisa de C4 e barras de erro." | Gráfico vertical regenerado com todas as condições C1-C5 e faixas de desvio. | `fig_interventions.png` |

---

## 4. ANÁLISE EDITORIAL E ESCOLHA DO PERIÓDICO (`analise-revistas.md`)

Levantamento conduzido com a ferramenta ToolHub CAPES (base completa de 4.988 periódicos) e consulta direta à Plataforma Sucupira (Qualis 2021–2024, comitê Engenharias IV):

| Periódico Avaliado | Editora | Qualis Eng. IV | JIF (Clarivate) | Quartil | Acordo CAPES (Isenção APC) | Avaliação de Fit |
|---|---|---|---|---|---|---|
| **Eng. Applications of AI (EAAI)** | Elsevier | **A1** | **8.0** | **Q1** | **Sim (100% Coberto - USD 3.040)** | **EXCELENTE (Submetido)** |
| **Neural Networks** | Elsevier | **A1** | **6.3** | **Q1** | **Sim (100% Coberto)** | **EXCELENTE (Plano B)** |
| **Expert Systems with Applications**| Elsevier | **A1** | **7.5** | **Q1** | **Sim (100% Coberto - USD 3.490)** | **MUITO BOM (Rápido)** |
| **IEEE Trans. on Neural Net. & Learn.**| IEEE | **A1** | **10.4** | **Q1** | Não (Sem acordo institucional)| Excelente, mas moroso |

---

## 5. DADOS EXPERIMENTAIS COMPLETOS DO ARTIGO EMPÍRICO

### 5.1 Infraestrutura de Hardware e Setup Experimental
- **Nó Local:** NVIDIA GeForce RTX 3070 (8 GB VRAM), AMD Ryzen 5 5600X, 64 GB RAM DDR4. VRAM alocada pelo modelo base em repouso: **1,07 GB**.
- **Nó Athena:** NVIDIA GPU de 20 GB VRAM para execuções 10-gerações multi-seed e E2B.
- **Quantização Base:** NF4 (*NormalFloat 4-bit*) com desquantização para `bfloat16` na inferência/gradiente. O modelo base quantizado permanece **estritamente inalterado e congelado**.
- **Dataset:** TriviaQA (`mandarjoshi/trivia_qa`, `rc.nocontext`, split `train`, seed 15).
  - Treino por ciclo: 2.000 perguntas sintéticas.
  - Avaliação fixa: 200 perguntas humanas.
- **Definição e Tamanho de $K_0$ (Acurácia Baseline Gen 0):**
  - **Qwen 2.5 1.5B-Instruct:** $K_0 = \mathbf{78\text{ itens}}$ (39,0% de acerto base; 54,5% de erro genuíno, 0 formatação incorreta; contagem inicial não auditada: 79 itens).
  - **Gemma 3 1B IT:** $K_0 = \mathbf{46\text{ itens}}$ (23,0% de acerto base; contagem inicial: 47 itens).
  - **Gemma 4 E2B IT:** $K_0 = \mathbf{76\text{ itens}}$ (38,0% de acerto base).
- **Protocolo de Decodificação:** Gulosa determinística (`temperature=0.0`, `do_sample=False`, `max_new_tokens=20`).

---

### 5.2 Eixo 1: Capacidade de Atualização (Varredura QLoRA no Qwen 2.5 1.5B)
Alvos de LoRA: projeções de atenção `q_proj` e `v_proj` ($\alpha = 2r$, dropout 0.05, lr = 1e-5, 2 épocas).

#### A. Tabela Consolidada de Postos (Seed 15)
| Posto Nominal ($r$) | Parâmetros Treináveis | % Params Base | Posto Efetivo Médio | Retenção Gen 5 | Retenção Gen 10 | Regime Classificado |
|---|---|---|---|---|---|---|
| **$r=4$** | 545.280 | 0,06% | 3,34 | 75/79 (94,9%) | — | **Homeostático** |
| **$r=16$** | 2.181.120 | 0,24% | 11,08 | 75/79 (94,9%) | 75/79 (94,9%) | **Homeostático** |
| **$r=32$** | 4.362.240 | 0,49% | 17,85 | 75/79 (94,9%) | — | **Homeostático** |
| **$r=64$** | 8.724.480 | 0,98% | 29,52 | 71/79 (89,9%) | 72/79 (91,1%) | **Homeostático** |
| **$r=128$** | 17.448.960 | 1,96% | 50,16 | 69/79 (87,3%) | 70/79 (88,6%) | **Limitado (*Bounded*)** |
| **$r=256$** | 34.897.920 | 3,91% | 87,57 | 66/79 (83,5%) | 60/79 (75,9%) | **Degradativo** |

*(Nota: considerando o subconjunto estrito de 78 itens, as retenções de Gen 10 correspondem a: $r=16 \to 96,2\%$; $r=64 \to 92,3\%$; $r=128 \to 89,7\%$; $r=256 \to 79,1\%$ na média multi-seed).*

#### B. Trajetórias Completas de Retenção por Geração (Qwen Seed 15)
- **$r=4$ (Gen 0--5):** G0: 100% $\to$ G1: 93,7% $\to$ G2: 92,4% $\to$ G3: 93,7% $\to$ G4: 94,9% $\to$ G5: 94,9%.
- **$r=16$ (Gen 0--10):** G0: 100% $\to$ G1: 94,9% $\to$ G2: 96,2% $\to$ G3: 94,9% $\to$ G4: 94,9% $\to$ G5: 94,9% $\to$ G6: 96,2% $\to$ G7: 94,9% $\to$ G8: 96,2% $\to$ G9: 94,9% $\to$ G10: 94,9%.
- **$r=32$ (Gen 0--5):** G0: 100% $\to$ G1: 93,7% $\to$ G2: 94,9% $\to$ G3: 94,9% $\to$ G4: 96,2% $\to$ G5: 94,9%.
- **$r=64$ (Gen 0--10):** G0: 100% $\to$ G1: 91,1% $\to$ G2: 91,1% $\to$ G3: 89,9% $\to$ G4: 91,1% $\to$ G5: 89,9% $\to$ G6: 91,1% $\to$ G7: 92,4% $\to$ G8: 91,1% $\to$ G9: 89,9% $\to$ G10: 91,1%.
- **$r=128$ (Gen 0--10):** G0: 100% $\to$ G1: 92,4% $\to$ G2: 88,6% $\to$ G3: 91,1% $\to$ G4: 91,1% $\to$ G5: 87,3% $\to$ G6: 87,3% $\to$ G7: 88,6% $\to$ G8: 87,3% $\to$ G9: 87,3% $\to$ G10: 88,6%.
- **$r=256$ (Gen 0--10):** G0: 100% $\to$ G1: 94,9% $\to$ G2: 89,9% $\to$ G3: 91,1% $\to$ G4: 88,6% $\to$ G5: 83,5% $\to$ G6: 82,3% $\to$ G7: 81,0% $\to$ G8: 81,0% $\to$ G9: 78,5% $\to$ G10: 75,9%.

#### C. Posto Efetivo Espectral ($\text{eff\_rank}$) por Geração (Qwen Seed 15)
- **$r=4$:** G1: 3,34 | G2: 3,34 | G3: 3,35 | G4: 3,34 | G5: 3,34.
- **$r=16$:** Estável em 11,08 $\pm 0,15$ ao longo das 10 gerações.
- **$r=32$:** G1: 18,06 | G2: 17,83 | G3: 17,99 | G4: 17,76 | G5: 17,80.
- **$r=64$:** Estável entre 29,49 e 30,08 (média 29,75).
- **$r=128$:** Estável entre 49,91 e 50,70 (média 50,37).
- **$r=256$:** G1: 88,07 | G2: 87,80 | G3: 87,66 | G4: 87,93 | G5: 87,76 | G6: 87,14 | G7: 87,44 | G8: 86,61 | G9: 86,61 | G10: 85,59.

#### D. Replicação Multi-Seed na Fronteira Degradativa ($r=256$, $N=3$, $K_0=79$)
| Geração | Seed 15 | Seed 137 | Seed 256 | Média Multi-Seed | Desvio Padrão ($\pm$) |
|---|---|---|---|---|---|
| **Gen 1** | 75 (94,9%) | 75 (94,9%) | 75 (94,9%) | 94,9% | $\pm 0,0\%$ |
| **Gen 2** | 71 (89,9%) | 71 (89,9%) | 71 (89,9%) | 89,9% | $\pm 0,0\%$ |
| **Gen 3** | 72 (91,1%) | 69 (87,3%) | 71 (89,9%) | 89,4% | $\pm 1,9\%$ |
| **Gen 4** | 70 (88,6%) | 68 (86,1%) | 71 (89,9%) | 88,2% | $\pm 1,9\%$ |
| **Gen 5** | 66 (83,5%) | 67 (84,8%) | 64 (81,0%) | 83,1% | $\pm 1,9\%$ |
| **Gen 6** | 65 (82,3%) | 67 (84,8%) | 66 (83,5%) | 83,5% | $\pm 1,3\%$ |
| **Gen 7** | 64 (81,0%) | 65 (82,3%) | 63 (79,7%) | 81,0% | $\pm 1,3\%$ |
| **Gen 8** | 64 (81,0%) | 64 (81,0%) | 64 (81,0%) | 81,0% | $\pm 0,0\%$ |
| **Gen 9** | 62 (78,5%) | 62 (78,5%) | 61 (77,2%) | 78,1% | $\pm 0,8\%$ |
| **Gen 10**| 60 (75,9%) | 61 (77,2%) | 64 (81,0%) | **78,0%** | $\pm 2,6\%$ |

- Base $K_0=78$: Média Gen 10 = **79,1%** (Faixa: 76,9% a 82,1%).
- Separação com o regime homeostático ($r=16 \to 97,4\%$): **19,4 pontos percentuais** de distância líquida sem sobreposição.

#### E. Dinâmica de Transições Item a Item (Qwen Seed 15, $K_0=78$)
| Posto | Gerações | Fatos Perdidos ($C \to W$) | Fatos Recuperados ($W \to C$) | Saldo Líquido | Comportamento Dinâmico |
|---|---|---|---|---|---|
| **$r=4$** | 5 | 1 | 0 | +1 | Oscilação homeostática mínima |
| **$r=16$** | 10 | 3 | 3 | **0** | **Equilíbrio perfeito de conservação** |
| **$r=32$** | 5 | 2 | 3 | -1 | Recuperação supera perda |
| **$r=64$** | 10 | 7 | 7 | **0** | Plasticidade preservada |
| **$r=128$** | 10 | 10 | 7 | +3 | Leve erosão factual |
| **$r=256$** | 10 | 19 | 4 | **+15** | **Esgotamento severo de plasticidade** |

#### F. Ablação Modular: Invariância de Topologia (Atenção vs. Linear Completo)
- **Attention-Only ($q, v$) $r=4$:** 545K params | erank 3,34 | Retenção Gen 5: 94,9%.
- **Attention-Only ($q, v$) $r=16$:** 2,2M params | erank 11,08 | Retenção Gen 5: 94,9% | Gen 10: 94,9%.
- **Attention-Only ($q, v$) $r=128$:** 17,4M params | erank 50,16 | Retenção Gen 5: 87,3% | Gen 10: 88,6%.
- **Full-Linear ($q,k,v,o,gate,up,down$) $r=4$:** 4,6M params | erank 3,43 | Retenção Gen 5: **94,9%** (idêntico ao attention $r=16$).
- **Full-Linear ($q,k,v,o,gate,up,down$) $r=16$:** 18,4M params | erank 11,54 | Retenção Gen 5: 91,1% | Gen 10: **87,3%** (comparável a attention $r=128$).

---

### 5.3 Validação Multi-Backbone (Gemma 3 1B e Gemma 4 E2B)

#### A. Gemma 3 1B IT — 5 Seeds $\times$ 10 Gerações ($K_0=46$)
**Posto $r=4$ (Homeostático, erank médio = 3,07):**
- Seed 15: G1: 95,7% $\to$ G5: 93,5% $\to$ G10: 93,5%.
- Seed 137: G1: 93,5% $\to$ G5: 93,5% $\to$ G10: 95,7%.
- Seed 256: G1: 95,7% $\to$ G5: 91,3% $\to$ G10: 93,5%.
- Seed 42: G1: 93,5% $\to$ G5: 95,7% $\to$ G10: 93,5%.
- Seed 77: G1: 95,7% $\to$ G5: 89,1% $\to$ G10: 95,7%.
- **Médias Gerais $r=4$:** Gen 1: **94,8%** | Gen 5: **92,6%** | Gen 10: **94,4%** (Faixa: 93,5% a 95,7%).

**Posto $r=16$ (Degradativo, erank médio = 9,25):**
- Seed 15: G1: 80,4% $\to$ G5: 71,7% $\to$ G10: 54,3% ($\Delta = -17,4\text{ pp}$).
- Seed 137: G1: 84,8% $\to$ G5: 67,4% $\to$ G10: 60,9% ($\Delta = -6,5\text{ pp}$).
- Seed 256: G1: 82,6% $\to$ G5: 67,4% $\to$ G10: 52,2% ($\Delta = -15,2\text{ pp}$).
- Seed 42: G1: 87,0% $\to$ G5: 69,6% $\to$ G10: 58,7% ($\Delta = -10,9\text{ pp}$).
- Seed 77: G1: 89,1% $\to$ G5: 69,6% $\to$ G10: 56,5% ($\Delta = -13,1\text{ pp}$).
- **Médias Gerais $r=16$:** Gen 1: **84,8%** | Gen 5: **69,1%** | Gen 10: **56,5%** (Queda adicional média pós-Gen 5 de **-12,6 pp**).

**Varredura Fina Intermediária (Seed 15, Gen 5, $K_0=46$):**
- $r=2$: 97,9% (erank 1,8) $\to$ Homeostático
- $r=4$: 93,5% (erank 3,05) $\to$ Homeostático
- $r=10$: 78,3% (erank 6,37) $\to$ Início da Degradação
- $r=12$: 73,9% (erank 7,35) $\to$ Degradativo
- $r=14$: 69,6% (erank 8,37) $\to$ Degradativo
- $r=16$: 71,7% (erank 9,29) $\to$ Degradativo
- $r=256$: 70,2% (erank ~62) $\to$ Degradativo (Platô a curto prazo)

#### B. Gemma 4 E2B IT — Três Postos $\times$ 10 Gerações (Seed 15, $K_0=76$)
- **$r=4$ (erank 2,04):** G1: 97,4% $\to$ G5: 93,4% $\to$ **G10: 94,7%** (72/76 acertos) $\to$ **Homeostático**.
- **$r=16$ (erank 5,10):** G1: 92,1% $\to$ G5: 90,8% $\to$ **G10: 88,2%** (67/76 acertos) $\to$ **Limitado (*Bounded*)**.
- **$r=64$ (erank 13,28):** G1: 86,8% $\to$ G5: 82,9% $\to$ **G10: 75,0%** (57/76 acertos) $\to$ **Degradativo**.

#### C. Incomensurabilidade de Limiares e Tentativa de Normalização
| Backbone | Dimensão Oculta ($d$) | Camadas | Cabeças Atenção | Limiar Homeostático | Limiar Degradativo | Faixa de Transição ($\text{eff\_rank}$) |
|---|---|---|---|---|---|---|
| **Qwen 2.5 1.5B** | 1536 | 28 | 12 | $r \le 64$ ($\text{erank} \le 30$) | $r = 256$ ($\text{erank} \sim 88$) | **~50 a ~88** |
| **Gemma 3 1B** | 1152 | 26 | 8 | $r \le 4$ ($\text{erank} \le 3,1$) | $r \ge 10$ ($\text{erank} \ge 6,4$) | **~3,0 a ~6,4** |
| **Gemma 4 E2B** | 2048 | 28 | 8 | $r = 4$ ($\text{erank} \sim 2,0$) | $r = 64$ ($\text{erank} \sim 13,3$) | **~5,1 a ~13,3** |

*Resultado Negativo de Normalização:* Testou-se a divisão do posto efetivo por $d$, $\sqrt{d}$, $n_{\text{camadas}}$, $n_{\text{cabeças}}$ e $n_{\text{cabeças\_KV}}$. Nenhuma métrica conseguiu fechar o gap de 10$\times$ entre Qwen e Gemma 3. O limiar de pressão é uma propriedade geométrica não redutível a dimensões simples.

---

### 5.4 Eixo 2: Magnitude da Perturbação (Ajuste Fino Completo - FFT vs. QLoRA)

#### A. Varredura de LR em FFT no Qwen (Seed 15, Gen 1--3, $K_0=78$)
- **QLoRA $r=16$ (Ref.):** LR = 1e-5 | $\|BA\|_F = 0,4237$ | G1: 97,4% $\to$ G2: 97,4% $\to$ **G3: 96,2%**.
- **FFT LR = 1e-6:** Drift = 0,3886 | G1: 93,6% $\to$ G2: 91,0% $\to$ **G3: 92,3%**.
- **FFT LR = 5e-6:** Drift = 1,5954 | G1: 91,0% $\to$ G2: 91,0% $\to$ **G3: 91,0%**.
- **FFT LR = 1e-5:** Drift = 1,9642 | G1: 91,0% $\to$ G2: 89,7% $\to$ **G3: 89,7%**.
- **FFT LR = 2e-5:** Drift = 3,5212 | G1: 89,7% $\to$ G2: 89,7% $\to$ **G3: 84,6%**.

#### B. Pareamento Controlado por Perturbação (10 Gerações $\times$ 3 Seeds, $K_0=78$)
Comparou-se **QLoRA $r=16$** ($\|BA\|_F \approx 0,41-0,42$) contra **FFT $\text{LR}=10^{-6}$** (desvio absoluto médio $\approx 0,38-0,39$):
- **QLoRA $r=16$ (Seeds 15, 137, 256):** Todas as 3 seeds atingem **97,4%** (76/78 acertos) na Gen 10. Média = **97,4% $\pm 0,0\%$**.
- **FFT $\text{LR}=10^{-6}$ (Seeds 15, 137, 256):** Seed 15: 92,3% (72) | Seed 137: 91,0% (71) | Seed 256: 92,3% (72). Média = **91,9% $\pm 0,7\%$**.
- **Custo Único de Adaptação:** O gap de 5,5 pp surge inteiramente na Gen 1 e permanece constante por 10 gerações. Ambos os métodos exibem trajetórias homeostáticas após a adaptação.
- **Piso Frágil Determinístico vs. Proteção de Subespaço:**
  - O FFT perde exatamente os mesmos 6 fatos em todas as 3 seeds: **[24, 46, 48, 56, 69, 74]** (Jaccard cross-seed = **1,0**).
  - O QLoRA perde apenas 2 a 3 fatos por seed: **[11, 12]** nas seeds 15 e 256; **[11, 12, 57]** na seed 137.
  - **Sobreposição entre fatos perdidos por FFT e QLoRA:** **Zero (Jaccard = 0,0)**. O subespaço LoRA isola os pesos dos modos vulneráveis ao FFT.

#### C. Generalização de Magnitude: FFT no Gemma 3 1B ($K_0=46$, Seed 15)
- **$\text{LR} = 10^{-6}$:** G1: 87,0% $\to$ G2: 82,6% $\to$ G3: 84,8% $\to$ G4: 80,4% $\to$ **G5: 78,3%** (36/46).
- **$\text{LR} = 5 \times 10^{-6}$:** G1: 93,5% $\to$ G2: 87,0% $\to$ G3: 80,4% $\to$ G4: 58,7% $\to$ **G5: 54,3%** (25/46).
- **$\text{LR} = 10^{-5}$:** G1: 91,3% $\to$ G2: 89,1% $\to$ G3: 73,9% $\to$ G4: 69,6% $\to$ **G5: 63,0%** (29/46).

---

### 5.5 Interação Eixo 1 $\times$ Eixo 2 (Matriz $3 \times 3$ Posto $\times$ LR no Qwen, $K_0=78$)
Avaliados ao longo de 5 gerações com semente 15:

| Posto Nominal ($r$) \ LR | $\mathbf{LR = 5 \times 10^{-6}}$ | $\mathbf{LR = 10^{-5}}$ | $\mathbf{LR = 2 \times 10^{-5}}$ |
|---|---|---|---|
| **$r = 16$** | 76/78 (**97,4%**) | 76/78 (**97,4%**) | 72/78 (**92,3%**) |
| **$r = 64$** | 76/78 (**97,4%**) | 72/78 (**92,3%**) | 69/78 (**88,5%**) |
| **$r = 256$** | 70/78 (**89,7%**) | 66/78 (**84,6%**) | 64/78 (**82,1%**) |

- Trajetória $r=16, \text{LR}=5\times10^{-6}$: 76, 76, 76, 78, 76 (Gen 5: 97,4%).
- Trajetória $r=16, \text{LR}=10^{-5}$: 76, 75, 75, 76, 76 (Gen 5: 97,4%).
- Trajetória $r=16, \text{LR}=2\times10^{-5}$: 74, 73, 72, 73, 72 (Gen 5: 92,3%).
- Trajetória $r=64, \text{LR}=5\times10^{-6}$: 76, 76, 75, 75, 76 (Gen 5: 97,4%).
- Trajetória $r=64, \text{LR}=10^{-5}$: 73, 72, 72, 72, 72 (Gen 5: 92,3%).
- Trajetória $r=64, \text{LR}=2\times10^{-5}$: 75, 73, 71, 73, 69 (Gen 5: 88,5%).
- Trajetória $r=256, \text{LR}=5\times10^{-6}$: 73, 72, 72, 71, 70 (Gen 5: 89,7%).
- Trajetória $r=256, \text{LR}=10^{-5}$: 75, 72, 70, 69, 66 (Gen 5: 84,6%).
- Trajetória $r=256, \text{LR}=2\times10^{-5}$: 70, 69, 69, 70, 64 (Gen 5: 82,1%).

*Conclusão da Interação:* Reduzir a LR compensa o aumento de posto (r=256 a 5e-6 atinge 89,7%), enquanto elevar a LR deteriora até adaptadores estreitos (r=16 a 2e-5 cai para 92,3%).

---

### 5.6 Assinaturas Mecanísticas e Deriva Distribucional (10 Gerações)

#### A. O Fenômeno de Dissociação em $r=128$
- Retenção Factual: Mantida limitada em **88,6%--89,7%** na Gen 10.
- Colapso Distribucional Simultâneo:
  - Comprimento médio das respostas infla de **2,47 para 6,95 palavras** (+281%).
  - Fração de stopwords dobra de **12,57% para 25,12%**.
  - Eficiência de conteúdo colapsa de **0,4055 para 0,1274** (diluição de 3,2$\times$).
  - MTLD desaba de **2.672,7 para 744,8**.
  - Persistência das respostas originais da Gen 0 cai para **5,2%**.

#### B. Métricas Distribucionais Detalhadas por Configuração (Auditoria `complete_metrics.csv`)
- **Qwen $r=16$ (Homeostático):**
  - Gen 0: Retenção 1,00 | Distinct-1 0,6711 | MTLD 2672,7 | Stopwords 12,57% | Comprimento 2,47w | Eficiência 0,4055.
  - Gen 5: Retenção 0,949 | Distinct-1 0,6395 | MTLD 2001,9 | Stopwords 15,58% | Comprimento 2,68w | Eficiência 0,3536 | Persistência 35,6%.
  - Gen 10: Retenção 0,949 | Distinct-1 0,6369 | MTLD 2035,6 | Stopwords 16,28% | Comprimento 2,70w | Eficiência 0,3520 | Persistência 36,1%.
- **Qwen $r=128$ (Bounded / Dissociação):**
  - Gen 0: Retenção 1,00 | Distinct-1 0,6711 | MTLD 2672,7 | Stopwords 12,57% | Comprimento 2,47w | Eficiência 0,4055.
  - Gen 5: Retenção 0,873 | Distinct-1 0,6026 | MTLD 1986,8 | Stopwords 16,88% | Comprimento 3,60w | Eficiência 0,2422 | Persistência 16,5%.
  - Gen 10: Retenção 0,886 | Distinct-1 0,4621 | MTLD 744,8 | Stopwords 25,12% | Comprimento 6,95w | Eficiência 0,1274 | Persistência 5,2%.
- **Qwen $r=256$ (Degradativo):**
  - Gen 0: Retenção 1,00 | Distinct-1 0,6711 | MTLD 2672,7 | Stopwords 12,57% | Comprimento 2,47w | Eficiência 0,4055.
  - Gen 5: Retenção 0,831 | Distinct-1 0,6510 | MTLD 2586,8 | Stopwords 13,57% | Comprimento 3,09w | Eficiência 0,2692 | Persistência 20,2%.
  - Gen 10: Retenção 0,780 | Distinct-1 0,6574 | MTLD 3804,1 | Stopwords 9,27% | Comprimento 3,56w | Eficiência 0,2194 | Persistência 3,8%.
- **Gemma 3 $r=4$ (Homeostático):**
  - Gen 5: Retenção 0,922 | Distinct-1 0,7005 | MTLD 2925,7 | Stopwords 8,09% | Comprimento 2,29w | Eficiência 0,4020 | Persistência 48,6%.
  - Gen 10: Retenção 0,936 | Distinct-1 0,7025 | MTLD 3005,4 | Stopwords 8,39% | Comprimento 2,33w | Eficiência 0,4018 | Persistência 46,1%.
- **Gemma 3 $r=16$ (Degradativo):**
  - Gen 5: Retenção 0,688 | Distinct-1 0,6464 | MTLD 3867,3 | Stopwords 9,79% | Comprimento 3,85w | Eficiência 0,1788 | Persistência 3,5%.
  - Gen 10: Retenção 0,565 | Distinct-1 0,6597 | Comprimento 3,65w | Eficiência 0,1548 | Persistência < 2,0%.
- **Gemma 4 E2B $r=64$ (Degradativo):**
  - Gen 1: Comprimento 3,61w | Distinct-1 0,5469 | Stopwords 22,81%.
  - Gen 5: Comprimento 3,91w | Distinct-1 0,4745 | Stopwords 28,05%.
  - Gen 10: Comprimento 4,44w | Distinct-1 0,4266 | Stopwords 28,42% | Retenção 75,0%.

#### C. Correlações Temporais e Precedência Causal (*Cross-Lag*)
- Correlação bruta $\rho(L_t, R_{t+1}) = \mathbf{-0,965}$ no Qwen $r=256$.
- Correlação parcial controlando a geração: $\rho = \mathbf{-0,220}$.
- Primeira diferença: $\rho = \mathbf{-0,433}$.
- Lag reverso $\rho(R_t, L_{t+1}) = \mathbf{-0,986}$.
- Conclusão: A deriva no comprimento é um **co-sintoma diagnóstico**, não o motor causal único.

#### D. Synthetic Drift Index (SDI-3)
- Gemma 3 $r=4$: **0,038** (Mínimo / Estável)
- Qwen $r=16$: **0,161**
- Qwen $r=256$: **0,437**
- Gemma 3 $r=16$: **0,705**
- Qwen $r=128$: **1,530** (Colapso distribucional extremo)

---

### 5.7 Eixo 3: Intervenções de Exposição Sintética (Reversão em Qwen $r=256$, Gen 5, $K_0=78$)
| Condição | Estratégia de Filtragem / Controle | Retenção Gen 5 | Fração $K_0$ | Ganho ($\Delta$) | Volume Tokens |
|---|---|---|---|---|---|
| **C1: Normal** | Geração estocástica padrão sem intervenção | **83,3%** | 65/78 | — | ~57k tokens |
| **C2: Short** | Prompt de sistema forçando $\le 5$ palavras | **91,0%** | 71/78 | **+7,7 pp** | ~60k tokens |
| **C3: Length-Filtered** | Remoção de saídas sintéticas $>5$ palavras | **92,3%** | 72,0/78 | **+9,0 pp** | ~54k tokens |
| **C4: Canonical** | Extração de formato canônico heurístico | **88,5%** | 69/78 | **+5,1 pp** | ~52k tokens |
| **C5: Random Downsample**| Corte aleatório pareado ao orçamento C3 | **92,7%** | 72,3/78 | **+9,4 pp** | ~54k tokens |

#### Réplicas Individuais Gen 1 a 5:
- **C1 Normal:** G1: 74 $\to$ G2: 72 $\to$ G3: 70 $\to$ G4: 68 $\to$ **G5: 65 (83,3%)**.
- **C2 Short:** G1: 74 $\to$ G2: 72 $\to$ G3: 72 $\to$ G4: 71 $\to$ **G5: 71 (91,0%)**.
- **C3 Length-Filtered (3 Seeds):**
  - Seed 15: 74, 74, 71, 71, **73 (93,6%)**.
  - Seed 137: 74, 73, 72, 72, **71 (91,0%)**.
  - Seed 256: 75, 73, 72, 71, **72 (92,3%)**.
  - Média C3: **92,3% $\pm 1,3\%$**.
- **C4 Canonical:** G1: 74 $\to$ G2: 74 $\to$ G3: 71 $\to$ G4: 68 $\to$ **G5: 69 (88,5%)**.
- **C5 Random Downsampling (3 Máscaras Independentes):**
  - Seed 15 (Máscara 1): 74, 73, 74, 72, **72 (92,3%)**.
  - Máscara 42: 74, 73, 74, 72, **73 (93,6%)**.
  - Máscara 99: 74, 73, 72, 73, **72 (92,3%)**.
  - Média C5: **92,7% $\pm 0,7\%$**.

*Conclusão:* A sobreposição de Jaccard entre exemplos descartados por C3 e C5 foi de apenas **0,015** (conjuntos essencialmente disjuntos). A estabilização de +9,4 pp decorre puramente da **redução quantitativa marginal de ~5% no volume de exposição sintética**, confirmando a natureza abrupta da fronteira de pressão.

---

### 5.8 Controles Secundários e Alinhamento Representacional (Fase M2)
- **Controle G1 (Sintético Recursivo) vs. G2 (Dados Reais Independentes) no Qwen $r=16$ ($K_0=79$):**
  - Retenção após 3 gerações: G1 = **94,5% $\pm 0,7\%$** | G2 = **95,4% $\pm 0,8\%$**.
  - Transições Fatuais: No G1 sintético, o modelo **congela** completamente após a Gen 1 ($C \to W = 0$, $W \to C = 0$ nas Gens 2 e 3) — **Ossificação Factual**. No G2 real, o fluxo factual continua ativo (2 a 7 transições por geração) — **Plasticidade Preservada**.
- **Análise CKA (Centered Kernel Alignment) na Camada 13 (Token Factual):**
  - CKA vs. Gen 0: G1 = 0,9836 (Gen 1), 0,9824 (Gen 2), 0,9826 (Gen 3).
  - CKA vs. Gen 0: G2 = 0,9827 (Gen 1), ~0,982 (Gen 2), ~0,982 (Gen 3).
  - O CKA Linear mede o custo geométrico invariável de adaptação ao formato, **não distinguindo** dados sintéticos de reais.

---

## 6. EXTENSÃO E PESQUISAS FUTURAS (`ideias\adaptive-pressure-control-paper.md`)

A partir da interação com os revisores na Revisão 2 (Comentário #25 do Prof. Carlos André), estruturou-se uma proposta para um **Paper 2**:
- **Título Proposto:** *"Adaptive Pressure Control for Recursive Synthetic Fine-Tuning"*
- **Problema:** Intervenções estáticas de exposição (como C3 e C5) aplicadas desde a Gen 1 restringem desnecessariamente a capacidade de aprendizado do modelo em estágios iniciais saudáveis.
- **Solução:** Um controlador adaptativo (*closed-loop controller*) baseado em monitoramento contínuo das assinaturas distribucionais (comprimento de resposta, eficiência de conteúdo e persistência de baseline) que aciona intervenções dinâmicas e dosadas (A0 No-op, A1 Light filter 5%, A2 Heavy filter 15%, A4 Short constraint, A6 Skip generation) apenas quando a deriva distributiva ultrapassa o limiar, otimizando a Área Sob a Curva de Retenção (AURC).

---

## 7. RASTREABILIDADE TOTAL DOS ARQUIVOS NO REPOSITÓRIO

| Componente de Dados | Arquivo-Fonte no Disco |
|---|---|
| Varredura Qwen QLoRA (r=4 a 256) | `Paradoxo\llm-knowledge-collapse\outputs\g1_rank*_seed15\results.json` |
| Qwen r=256 Multi-Seed 10 Gerações | `Paradoxo\llm-knowledge-collapse\outputs\g1_rank256_seed*\results.json` |
| Gemma 3 Multi-Seed 10 Gerações | `Paradoxo\llm-knowledge-collapse\outputs\v3_gemma3_rank*\results.json` |
| Gemma 4 E2B 10 Gerações | `Paradoxo\llm-knowledge-collapse\outputs\v3_gemma4_rank*\results.json` |
| FFT vs QLoRA 10 Gerações Multi-Seed| `Paradoxo\llm-knowledge-collapse\outputs\fft_drift_gen10\*.json` |
| Matriz 3x3 Posto x Taxa de Aprendizado| `Paradoxo\llm-knowledge-collapse\outputs\rank_lr_matrix\*.json` |
| Intervenções C1 a C5 e Réplicas | `outputs\causal_intervention\`, `outputs\intervention_validation\`, `outputs\c5_masks\` |
| Métricas Distribucionais Completas | `outputs\diversity_analysis\complete_metrics.csv` e `refined_analysis.csv` |
| Manuscrito Oficial de Submissão | `Paradoxo\llm-knowledge-collapse (paper)\v4\manuscript-anonymous.tex` |
| Survey Teórico Original | `Paradoxo\new-submisions\computer-science-review\main.tex` |
| Auditoria Interna do Laboratório | `Paradoxo\Review\Carlos\v1\` e `v3\` |
| Análise Bibliométrica Qualis/JIF | `Paradoxo\analise-revistas.md` |

---
*Documento consolidado de auditoria e referência científica.*
