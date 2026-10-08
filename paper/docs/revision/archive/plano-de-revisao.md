# Plano de Revisão — KNOSYS-D-26-21490 (v3 → v4)

**Prazo:** 20 de outubro de 2026
**Decisão:** Major revision — conditionally accepted pending revision
**Revisores:** 2
**Título:** Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study *(inalterado)*

---

## Legenda

**Prioridade:**
🔴 Bloqueador — sem isso não passa
🟠 Alta — afeta diretamente a aceitação
🟡 Média — melhora significativa, não bloqueia
🟢 Baixa — cosmético/forma

**Tipo de ação:**
`TEX` edição no `manuscript-anonymous.tex`
`BIB` edição no `cas-refs.bib`
`RESP` redigir resposta (sem mudança no MS)
`EXP` requer experimento novo ou reanálise
`INFRA` repositório, script, arquivo externo

---

## Estratégia geral

Os dois revisores pedem três coisas distintas:

1. **Consistência e forma** — notação, equações malformadas, números que se contradizem, referências erradas. Resolve-se com edição pura.
2. **Rigor** — estatística formal, qualificação de "sharp", seeds. Resolve-se com reanálise dos dados já existentes.
3. **Generalização** — ETP como preditor quantitativo, outros datasets, efeito de exposição em mais de um backbone. Requer alguns experimentos novos, que cabem no prazo se priorizados.

Princípio: aceitar o que é justo, reduzir afirmações onde os dados são fracos, acrescentar evidência onde o custo é baixo. A KBS deu "conditionally accepted" — não vale reescrever tudo, vale fechar cada objeção de forma verificável.

---

## PARTE 0 — Alertas críticos (problemas não levantados pelos revisores)

> Cruzamento entre o PDF submetido e o `DADOS_E_RESULTADOS_CONSOLIDADOS.md`. Corrigir antes que um revisor da 2ª rodada encontre.

### A1 — Cover letter endereçada à revista errada 🔴 `INFRA`

- **Problema:** A carta de apresentação menciona *Engineering Applications of AI* (EAAI). O arquivo de dados também diz "submetido à EAAI". A submissão é para a *Knowledge-Based Systems* (KBS).
- **Ação:** Refazer a cover letter completamente endereçada à KBS. O editor percebe isso imediatamente.

### A2 — Hardware mal descrito no §3.3 🟠 `TEX`

- **Problema:** O artigo diz "RTX 4000 Ada 20 GB". Os dados mostram RTX 3070 8 GB (local) + nó Athena 20 GB, com tempos (~3 min / ~12 min) atribuídos à 3070.
- **Ação:** Dizer explicitamente quais experimentos rodaram em qual GPU. Isso também fortalece a resposta a R1.Q2 (não-determinismo de kernels).

### A3 — Avaliação gulosa não descrita no §3.1/3.2 🟠 `TEX`

- **Problema:** O artigo só descreve a geração sintética (temp 0.7, top-p 0.9, 30 tokens). Os dados mostram avaliação gulosa (temp 0, 20 tokens), que não aparece no artigo.
- **Ação:** Descrever as duas configurações explicitamente: geração sintética e avaliação do K0.

### A4 — Mesmo seed, dois resultados: Qwen r=16 seed 15 🟠 `TEX`

- **Problema:** Seed 15 dá 75/78 (96,2%) na varredura de rank e 76/78 (97,4%) no experimento FFT-vs-QLoRA. Table 2 vs §4.3.1 se contradizem.
- **Ação:** Explicar a discrepância (não-determinismo de kernels bitsandbytes/cuBLAS, ou versão diferente do pipeline) e reportar ambos os valores explicitamente. Um revisor atento vai perguntar.

### A5 — K0 misturado (78/79 Qwen, 46/47 Gemma 3) 🔴 `INFRA` + `TEX`

- **Problema:** Percentuais como "97,9%" e "70,2%" para Gemma 3 são impossíveis com K0=46 (dariam 46/47 e 33/47 aproximadamente). O K0 não está auditado de forma consistente.
- **Ação:** Criar script único que regenera todas as tabelas a partir dos `results.json` com o K0 auditado (78/46/76). Todo número percentual deve ter denominador explícito.

### A6 — Definição de drift inconsistente: Eq. 3 vs §3.4 vs Tab. 6 🔴 `TEX`

- **Problema:** Eq. 3 diz "mean absolute parameter change"; §3.4 diz "L2 norm". Um valor de 0,39–3,48 não pode ser média absoluta por parâmetro (pesos são da ordem de 10⁻²). Também: ‖BA‖_F — é por matriz ou somado? Inclui o fator α/r?
- **Ação:** Conferir no código qual métrica é realmente calculada e corrigir Eq. 3, §3.4 e Tab. 6 para usar a mesma definição com precisão.

### A7 — Taxa de degradação: Fig. 1 vs texto 🟠 `TEX`

- **Problema:** Fig. 1 diz "~2–6 pp/gen" e o texto diz "~2 pp/gen" para r=256. Isso inclui a queda de adaptação Gen0→1. A inclinação real pós-adaptação (Gen5→Gen10) é −1,0 pp/gen (Qwen r=256) e −2,5 pp/gen (Gemma 3 r=16).
- **Ação:** Usar a inclinação pós-adaptação como definição de regime. Tabela de inclinações (§3):

  | Configuração | pp/geração (Gen5→Gen10) |
  |---|---|
  | Qwen r=16 / 64 / 128 / 256 | 0,00 / +0,24 / +0,26 / −1,02 |
  | Gemma 3 r=4 / r=16 | +0,36 / −2,52 |
  | E2B r=4 / 16 / 64 | +0,26 / −0,52 / −1,58 |

### A8 — Arquitetura: verificar config.json (o .tex pode estar certo) 🟠 `TEX`

- **Status revisado (D1):** O arquivo de dados consolidado diz E2B com d=2048/28 camadas e Gemma 3 com 8 heads — mas verificação independente indica que o `config.json` do `google/gemma-4-E2B-it` tem `hidden_size=1536`, 35 camadas, 8 attention heads, 1 KV head. Ou seja, o `.tex` provavelmente está certo e o arquivo de dados estava errado. O valor 2048 é do Gemma 2 2B, não do E2B.
- **Ação obrigatória antes de submeter:** Confirmar no `config.json` real do HF Hub (com commit hash da versão usada) e **não alterar o .tex** até confirmar. Se o .tex estiver certo, a Tab. 11 não muda — dizer ao revisor que os valores foram re-verificados e confirmados.
- **Detalhe novo:** O E2B compartilha KV cache em ~20 das 35 camadas. Se o LoRA tem `v_proj` como alvo, parte desses adapters pode não existir nessas camadas. Imprimir a lista de módulos treináveis e confirmar o número real de matrizes adaptadas — isso muda o erank agregado do E2B.

### A9 — Possível artefato do casamento por substring bidirecional 🟠 `EXP`

- **Problema:** Respostas mais longas (r=128 tem ~7 palavras) têm mais chance de "conter" um alias por substring bidirecional. A dissociação em r=128 pode estar inflada.
- **Ação:** Recalcular com EM estrito e contains unidirecional a partir das saídas brutas (barato, sem treino). Isso fortalece a resposta a R1.Q3.

### A10 — Baseline C1 é N=1; ganho de +9 pp suspeito 🟠 `EXP`

- **Problema:** O ganho de +9 pp com 5% de remoção aleatória é surpreendente com baseline single-seed. Um revisor cético pode suspeitar de diferença no código (C3/C5 podem ter ~5% menos passos de otimização).
- **Ação:** Controles baratos: (i) rodar C1 pelo mesmo código de intervenção com 0% de remoção; (ii) C5 com número de passos igualado; 2–3 seeds, Gen5. Nota: a média Gen5 do r=256 em 3 seeds (81,0–84,8%) já sustenta parcialmente a C1.

---

## PARTE 1 — Consistência e forma (edição pura)

### 1.1 — Inconsistências factuais texto↔tabela (R2.3)

| ID | Problema | Ação | Prior. | Tipo |
|----|----------|------|--------|------|
| 1.1.1 | Abstract diz "erank 50–88"; Sec 5.1 diz "até 150" (era "∼50", tilde virou "1" no render); Table 2 mostra r=256 erank 87.57 degradativo | O "150" é artefato de encoding — explicar isso na resposta. Corrigir render; alinhar Abstract com Table 2 | 🔴 | `TEX` |
| 1.1.2 | r=128: "Bounded" em Table 2 vs "above-threshold" em §4.4.3 | Introduzir duas fronteiras explícitas θ_H e θ_D (ver §1.5 abaixo); r=128 fica "above θ_H, below θ_D" | 🔴 | `TEX` |
| 1.1.3 | r=256 chamado de "boundary configuration" mas é degradativo na Table 2 | Substituir por "the lowest-pressure degradative configuration tested, adjacent to θ_D"; remover "boundary configuration" de todas as ocorrências | 🔴 | `TEX` |
| 1.1.4 | §5.2 diz "r ≥ 16 degradativo no Gemma 3"; Table 4 mostra r=10,12,14 já degradativos na Gen5 | Corrigir para "r ≥ 10 (erank ≥ 6.4)" em §5.2 | 🔴 | `TEX` |
| 1.1.5 | Abstract: "3 a 5 seeds independentes por condição" — falso para muitas condições | Substituir por: "headline comparisons replicated with three to five independent seeds; supporting ablations single-seed and labelled as such" | 🔴 | `TEX` |
| 1.1.6 | FFT Gemma 3: resultado não-monotônico; a conclusão diz "confirms" — overclaim single-seed | Substituir "confirms" por "is consistent with"; adicionar ressalva de single-seed e não-monotonicidade | 🟠 | `TEX` |
| 1.1.7 | §3.4 diz "15° removal"; §4.5 diz "~5% token reduction" (C5). "15˜" é "∼5%" com encoding quebrado | Corrigir encoding; reportar contagens exatas de exemplos por geração para C3 e C5 | 🟠 | `TEX` |

### 1.2 — Encoding e caracteres quebrados (R2.2 — causa raiz)

> Os símbolos quebrados são falha de fonte/encoding na montagem do PDF pelo Editorial Manager. Mapeamento identificado:
> - İ → × (times)
> - í → ∼ (approximately)
> - Ë → ∈ (element of)
> - ˆ' → { } (braces)
> - *5 → −5 (minus)
> - "15˜" → "∼5%"

| ID | Problema | Ação | Prior. | Tipo |
|----|----------|------|--------|------|
| 1.2.1 | Todos os × viram İ, todos os ∼ viram í etc. em todo o MS | Usar exclusivamente modo matemático: `$5\times10^{-6}$`, `$\sim$50`, `$r\in\{4,10,12,14,16\}$` | 🔴 | `TEX` |
| 1.2.2 | Pacotes de fonte | Garantir `\usepackage[T1]{fontenc}` + `lmodern` no preâmbulo; zero caracteres Unicode colados fora de modo matemático | 🔴 | `TEX` |
| 1.2.3 | "5İ10^6" em Table 7 | Corrigir para `$5\times10^{-6}$`; varrer o .tex inteiro com grep por caracteres não-ASCII fora de comentários | 🔴 | `TEX` |

### 1.3 — Equações reescritas (R2.2)

| ID | Equação | Problema | Ação | Prior. | Tipo |
|----|---------|----------|------|--------|------|
| 1.3.1 | Eq. 1 — Retenção R(t) | "Retention.t /" garbled; somatório malformado | Reescrever: `R(t) = \frac{1}{|\mathcal{K}_0|}\sum_{q\in\mathcal{K}_0}\mathbb{1}[\mathrm{match}(\hat{a}_t(q),\mathcal{A}(q))]` | 🔴 | `TEX` |
| 1.3.2 | Eq. 2 — Effective rank | Falta sinal negativo e somatório; normalização matematicamente errada | Reescrever: `p_i=\sigma_i/\sum_j\sigma_j`, `\mathrm{erank}=\exp(-\sum_i p_i\log p_i)` | 🔴 | `TEX` |
| 1.3.3 | Eq. 3 — Drift | "mean absolute" vs "L2 norm" — inconsistente com código (ver A6) | Corrigir para a definição real do código; definir ΔW = (α/r)BA explicitamente | 🔴 | `TEX` |
| 1.3.4 | Eq. 6 — SDI-3 | Sinais, log-ratios e ΔI inconsistentes; variáveis não definidas | Reescrever completo com todas as variáveis: L̄, D₁, I(t), ν(·) — ver trechos prontos em §5.2 do plano | 🔴 | `TEX` |

### 1.4 — Tabela de notação e abreviaturas (R2.1)

| ID | Problema | Ação | Prior. | Tipo |
|----|----------|------|--------|------|
| 1.4.1 | ETP não definido explicitamente; aparece na Fig. 1 sem definição | Definir na primeira ocorrência no texto: "effective training pressure (ETP)"; adicionar à tabela de notação | 🟠 | `TEX` |
| 1.4.2 | MTLD não expandido | Expandir: "Measure of Textual Lexical Diversity (MTLD)" | 🟠 | `TEX` |
| 1.4.3 | KL, JS, coverage na Fig. 1 sem definição | Adicionar na legenda: "KL: Kullback–Leibler divergence; JS: Jensen–Shannon divergence; coverage: fraction of unique n-grams" | 🟡 | `TEX` |
| 1.4.4 | bf16, SVD, TCE sem expansão consistente | Expandir em primeira ocorrência: "bfloat16 (bf16)", "singular value decomposition (SVD)", "token-coverage efficiency (TCE)" | 🟡 | `TEX` |
| 1.4.5 | "Homeo." na Table 2 sem definição | Remover abreviação ou adicionar nota de tabela: "Homeo. = Homeostatic" | 🟡 | `TEX` |
| 1.4.6 | K0 usado como conjunto e como métrica | Separar símbolos: 𝒦₀ para o conjunto, |𝒦₀| para seu tamanho, R(t) para retenção; revisar todas as ocorrências | 🟠 | `TEX` |
| 1.4.7 | BA_F, θ_i^(t), θ_i^(0) não definidos consistentemente | Definir: θ⁽⁰⁾ pesos pré-treino, θ⁽ᵗ⁾ pesos na geração t, ΔW = θ⁽ᵗ⁾ − θ⁽⁰⁾ = (α/r)BA | 🟠 | `TEX` |
| 1.4.8 | "r E 4,10,12,14,16" garbled — encoding | Corrigir todos os conjuntos: `$r\in\{4,10,12,14,16\}$` | 🟠 | `TEX` |
| 1.4.9 | T, D1_T, D10, ΔI, Instability(1), MeanLen_T em Eq. 6 não definidos | Adicionar definições formais antes de Eq. 6 | 🟠 | `TEX` |
| 1.4.10 | σ_i: singular value E singular value normalizada — dois significados | Introduzir p_i = σ_i/Σσ_j e usar p_i onde normalizado | 🟠 | `TEX` |
| 1.4.11 | Criar Tabela de Nomenclatura | Nova Tabela 1 com todos os símbolos e definições | 🟠 | `TEX` |

### 1.5 — Definição formal de regimes (resolve 1.1.2 e 1.1.3)

Introduzir duas fronteiras com critério quantitativo explícito:

- **θ_H** (homeostático → bounded): R(10) ≥ 90% **e** inclinação Gen5→Gen10 ≥ −0,5 pp/gen
- **θ_D** (bounded → degradativo): inclinação Gen5→Gen10 < −0,5 pp/gen (ou limite superior do IC 95% da regressão Gen2→10 abaixo de 0 — mais robusto)

Resultado no Qwen: θ_H entre r=64 e r=128 (erank 30–50); θ_D entre r=128 e r=256 (erank 50–88).
r=128 → "above θ_H, below θ_D" = "distributionally degraded, factually bounded"
r=256 → "the lowest-pressure degradative configuration tested, adjacent to θ_D"

Atenção: E2B r=16 (inclinação −0,52) fica no limite — reportar como "bounded/early-degradative" com IC.

### 1.6 — Abstract: substituições obrigatórias

| Texto atual (aproximado) | Substituir por |
|---|---|
| "three to five independent seeds per condition" | "headline comparisons replicated with three to five independent seeds; supporting ablations single-seed and labelled as such" |
| "a sharp regime transition" | "an abrupt, threshold-like transition within the tested grid" |
| "effective rank 3–6 on Gemma" | "between effective ranks ∼3 and ∼6 on Gemma 3 1B" |
| trecho sobre 5% de remoção | "…restoration of near-homeostatic retention through ∼5% reduction in synthetic exposure in the lowest-pressure degradative Qwen configuration; this did not transfer to Gemma 3 at the tested magnitude" |

---

## PARTE 2 — Rigor estatístico (reanálise dos dados existentes)

### 2.1 — Estatísticas formais a adicionar (R2.4, implícito em R1.Q1)

Estatísticas já calculadas com os dados existentes:

**Headline — Gen10, Welch t / Newcombe CI:**

| Comparação | Δ (pp) | IC 95% (Newcombe) | Welch p | Hedges g | Permutação |
|---|---|---|---|---|---|
| Qwen r=16 vs r=256 | +18,4 | [12,8; 24,2] | 0,007 | 7,8 | p=0,10 (mín. n=3) |
| Qwen r=16 vs FFT 1e-6 | +5,6 | [1,5; 10,0] | 0,006 | 8,5 | p=0,10 (mín.) |
| Gemma 3 r=4 vs r=16 | +37,8 | [30,5; 44,7] | 3×10⁻⁶ | 13,3 | p=0,008 (mín. n=5) |
| Qwen C3 vs C1 | +9,0 | [1,1; 19,2] | 0,007* | — | — |
| Qwen C5 vs C1 | +9,4 | [1,6; 19,6] | 0,002* | — | — |
| C3 vs C5 | −0,4 | [−5,4; 4,5] | 0,65 | — | 1,0 |

*teste t de uma amostra contra C1 (N=1) — fraco, reforça a necessidade do A10.

**Tendência no sweep de rank (Gen10):** logit(p) = 5,97 − 1,04·ln(erank), p = 6×10⁻⁴.

**Incerteza de um único run (Wilson 95%):** 70/78 → [81,1; 94,7] (largura 13,7 pp); 36/46 → [64,4; 87,7] (23,3 pp). Isso justifica quantitativamente por que ablações single-seed são "supportive only".

| ID | Ação | Prior. | Tipo |
|----|------|--------|------|
| 2.1.1 | Adicionar GLMM logístico item-level: `correct ~ condition + (1|item) + (1|seed)`, com IC por bootstrap estratificado por item (statsmodels ou lme4) | 🟠 | `EXP` + `TEX` |
| 2.1.2 | Reportar média ± SD para todas as condições multi-seed | 🟠 | `TEX` |
| 2.1.3 | Adicionar coluna "N seeds" em todas as tabelas de resultados | 🟠 | `TEX` |
| 2.1.4 | Declarar explicitamente p mínimo de permutação (0,10 para n=3; 0,008 para n=5) | 🟠 | `TEX` |
| 2.1.5 | Wilson 95% CI para cada run single-seed; rotular como "supportive" | 🟠 | `TEX` |
| 2.1.6 | Tendência logística no sweep de rank: reportar slope, p-value e figura | 🟡 | `TEX` |

### 2.2 — Ablação de topologia (full-linear vs attention-only)

O dado de full-linear r=16 (erank 2.262, retenção 87,3%) ≈ attention r=128 (erank 2.809, 88,6%) está nos dados mas não no artigo. Acrescentar — fortalece a ablação de que erank é o preditor, não contagem de parâmetros.

| ID | Ação | Prior. | Tipo |
|----|------|--------|------|
| 2.2.1 | Adicionar ponto full-linear r=16 na tabela de ablação modular | 🟡 | `TEX` |

---

## PARTE 3 — ETP quantitativo e generalização (experimentos novos)

### 3.1 — Índice operacional Π = erank·η (R1.Q1, R2.4)

GLM binomial ajustado na matriz 3×3 rank×LR (Gen5):
`logit(p) = −3,20 − 0,668·ln(erank) − 0,697·ln(η)` (ambos p < 0,01; interação LRT p = 0,33, não necessária)

A razão β₂/β₁ ≈ 1,04 ≈ 1 → a retenção depende aproximadamente de um único escalar **Π = erank·η**.

Ordenando as 9 células por Π: retenção perfeitamente monotônica. Leave-one-cell-out MAE = 2,3 pp. Maior discrepância: célula r=256/2e-5 (−7,4 pp) → saturação.

**Como apresentar sem exagero:**
- Chamar de "a candidate operational pressure index", ajustado em 9 células, um seed, Gen5
- Calcular IC do expoente por bootstrap
- Declarar os limites: a exposição não entra em Π de forma suave (5% menos → +9 pp não é suave em ln); slopes diferem entre backbones (Qwen ≈ −1,0; E2B ≈ −0,95; Gemma 3 ≈ −2,4) → probe por backbone necessário

| ID | Ação | Prior. | Tipo |
|----|------|--------|------|
| 3.1.1 | Adicionar nova §3.5.3 com a definição de Π e o ajuste do GLM | 🟠 | `TEX` |
| 3.1.2 | Adicionar nova §4.3.2 com o resultado prospectivo | 🟠 | `TEX` + `EXP` |
| 3.1.3 | Commit datado das previsões prospectivas antes de rodar os experimentos | 🔴 | `INFRA` |

**Protocolo de calibração para backbone novo:**
1. Probe barato: 3 ranks × 3 gerações com LR fixo (~1 h)
2. Ajustar intercepto e inclinação do backbone
3. Prever Π* em que R(10) cruza 90%
4. Validar com 1–2 runs de 10 gerações

**Previsões pré-registradas (commit antes de rodar):**
- r=128 / η=5e-6 → ~94%
- r=128 / η=2e-5 → ~85%
- r=32 / η=2e-5 → ~92%

### 3.2 — Experimentos novos: tabela de prioridades

| Prior. | Experimento | Responde a | Custo GPU |
|--------|-------------|-----------|-----------|
| **P0** | Reavaliar saídas/adapters salvos com EM estrito e contains unidirecional + conjunto de 1.000 itens (K0 ≈ 390 Qwen) | R1.Q3, A9 | Poucas horas (sem treino) |
| **P0** | Controles da C1 (A10): C1 pelo pipeline de intervenção + C5 com passos igualados, 2–3 seeds, Gen5 | R1.Q4, A10 | ~4 h |
| **P1** | LoRA bf16 (sem quantização), r=16 e r=256, 3 seeds, 10 gerações | R1.Q2, Limitação §6 | ~9 h |
| **P1** | Dose-resposta de exposição: Gemma 3 r=10 × {0, 5, 10, 25%} + Qwen r=256 × {10, 25%}, 3 seeds, Gen5 | R1.Q4 | ~8 h |
| **P1** | Teste prospectivo pré-registrado do índice Π (3–4 células fora do ajuste, previsão commitada antes) | R1.Q1, R2.4 | ~3 h |
| **P2** | Segundo dataset: PopQA ou NQ-open + HotpotQA closed-book, Qwen r=16/128/256 | R1.Q3 | ~15–20 h |
| **P2** | Grade mais densa perto do limiar: Qwen r ∈ {96, 160, 192}, Gemma 3 r ∈ {6, 8} | R2.4 ("sharp") | ~8 h |
| **P2** | Fatorial de ordem dos dados: seed de inicialização × seed de ordem, r=256 | R1.Q2 | ~4 h |
| **P3** | 4º backbone: Llama-3.2-1B-Instruct, probe curto + previsão + 10 gerações | R1.Q1 (backbone não visto) | ~10 h |

**Total P0+P1:** ~24 h de GPU. P2 adiciona ~30–32 h. P3 opcional mais ~10 h.
**Mínimo defensável:** P0 + P1.
**Para P2/P3 não rodados:** escrever "acknowledged + future work" com honestidade.

---

## PARTE D — Discordâncias e cautelas (revisão crítica do plano anterior)

> Esta seção documenta os pontos onde a análise anterior estava errada ou excessivamente otimista. Ignorar esses pontos introduziria erros piores do que os que estamos corrigindo.

### D1 — Arquitetura do E2B: o manuscrito estava certo 🔴

**O arquivo de dados consolidado estava errado**, não o manuscrito.

- `config.json` do `google/gemma-4-E2B-it`: `hidden_size=1536`, 35 camadas, 8 attention heads, 1 KV head
- O valor 2048 é do Gemma 2 2B — confusão de modelo
- O mesmo vale para Gemma 3 1B: o manuscrito diz 4 heads/1 KV head, o que confere com o config; o arquivo de dados diz 8
- **A Tab. 11 não muda.** Se o texto disser "corrigimos os valores e a Tab. 11", vai introduzir um erro num item que estava certo
- **Ação:** Confirmar no `config.json` real do HF Hub (com commit hash), depois remover os comentários [v4] A8 do .tex se os valores estiverem corretos
- **Detalhe adicional:** O E2B compartilha KV cache em ~20 das 35 camadas. Imprimir a lista de módulos treináveis e verificar o número real de matrizes adaptadas — isso afeta o erank agregado do E2B

### D2 — A "curva-mestra universal" (R² = 0,921) não se sustenta 🔴

**Não incluir esta análise no manuscrito.** Três problemas fatais:

1. **É circular:** o `e_crit` de cada backbone é ajustado nos mesmos pontos que depois "colapsam" na curva. Colapso bom é esperado por construção
2. **E2B R² = 1,000 por saturação:** Hill de 3–4 parâmetros sobre 3 pontos não é identificável. Um revisor de estatística percebe isso imediatamente
3. **Contradição interna:** o texto diz "geometria universal" mas usa `h=2,75` no Gemma contra `h=1,09` no Qwen (inclinação 2,5× maior). Inclinações diferentes = geometria não universal. A regressão independente confirma: slope ≈ −1,0 no Qwen vs ≈ −2,4 no Gemma 3

**Substituição correta:** apresentar como calibração por backbone com dois parâmetros livres (localização e inclinação). Resultado honesto: "a forma é qualitativamente comum; localização e inclinação dependem do backbone e precisam ser calibradas individualmente." O protocolo de 3 pontos continua válido com no máximo 2 parâmetros.

### D3 — Bateria estatística com falhas de validade 🟠

Os seguintes testes têm problemas que um revisor estatístico detecta:

| Teste | Problema | O que fazer |
|-------|----------|-------------|
| Segmentada vs linear (ΔAIC = −12,08, breakpoint 42,55) | Com n=6 pontos e k=5 parâmetros, AICc é indefinido (divide por n−k−1=0). ΔAIC com 6 pontos não tem valor inferencial. Breakpoint e e_crit ajustados nos mesmos 6 pontos = não são evidências independentes | Não usar ΔAIC. Descrever qualitativamente a transição e quantificar com a grade mais densa quando disponível |
| Cochran-Armitage (Qwen p=10⁻⁶, Gemma p=10⁻⁶) | (i) Mistura Gen5 com Gen10. (ii) Mesmos itens K0 se repetem entre condições → observações não independentes → p anticonservador. No Gemma ainda inclui r=2 e r=256 contados sobre K0=47 | Substituir por GLMM item-level |
| McNemar r=256 (19 vs 4) | Os 19 e 4 são eventos somados ao longo de gerações, com itens que podem se repetir. K0 por definição "todos corretos na Gen0" → comparação Gen0 vs Gen t não admite W→C, tornando o teste degenerado | Não usar. Descrever transições item-level descritivamente |
| Mann-Kendall / OLS −2,00 pp/ger | Inclui Gen0 (=100% por definição), misturando custo de adaptação com degradação. Inclinação pós-adaptação real: −1,0 pp/ger | Rodar com Gen1–10 ou Gen2–10 |
| Mann-Whitney Gemma p=0,0109 | É a aproximação normal. O valor exato é p=0,0079 = mínimo possível com 5+5 | Reportar o exato, declarar que é o mínimo possível |
| Fisher C1 vs C3 p=0,14 | Comparação de contagens agrupadas; itens K0 se repetem entre seeds | Usar GLMM item-level como teste principal |
| R² = 0,907 sobre "15 condições" | Junta varredura de rank (Gen10) com matriz (Gen5); r=16/64/256 com LR 1e-5 aparecem em dois horizontes | Ajustar só dentro de um mesmo horizonte |

**O que manter:** GLM binomial (coeficientes consistentes), testes exatos com p mínimo declarado, ICs de Newcombe e bootstrap, GLMM por item como teste principal.

### D4 — Redação sobre interação ("absorbed by construction") está errada 🟠

O GLM já estava em escala log. O teste de interação nessa escala é o teste de desvio da combinação multiplicativa. Portanto p=0,33 significa "não há evidência de desvio do produto" — não que a interação foi "absorvida por construção".

- Com 9 células e 1 seed, o poder é baixo. Dizer "not detected", não "not required"
- No leave-one-out, o modelo com interação teve MAE menor (1,49 vs 2,32 pp), puxado pela célula extrema (r=256, LR=2e-5, erro de −7,4 pp). Isso sugere saturação e deve ser reportado

**Texto correto:** ver Seção E (textos prontos), item E.1.

### D5 — A1 (decodificação): as duas versões podem coexistir 🟠

O texto anterior afirmou que "tudo é guloso" — mas o manuscrito descreve a geração sintética (temp 0,7) e o arquivo de dados descreve a avaliação (gulosa, temp 0, 20 tokens). São protocolos diferentes para etapas diferentes, não contraditórios.

O argumento "±0,0% nas Gen1/Gen2 prova decodificação determinística" também não se sustenta: contagens iguais não implicam os mesmos itens.

**Ação:** Verificar no código as duas etapas separadamente. Se a geração sintética também for gulosa, isso muda a interpretação das métricas de diversidade e a resposta a R1.Q2.

### D6 — Critérios de regime circulares se misturar SDI-3 🟠

"Homeostático = retenção > 90% e SDI-3 < 0,3; Bounded = SDI-3 > 1,0" mistura critério factual com distribucional e parece ajustado nos dados:
- Qwen r=256 (degradativo) tem SDI-3 = 0,437
- E2B não tem SDI calculado
- O SDI-3 mais alto está no r=128 (verbosidade/filler), não no r=256 (deriva elaborativa)

**Manter:** regimes definidos **só** por retenção (nível e inclinação pós-adaptação). SDI-3 fica como descritor separado, não como critério de validação. A leitura correta é que SDI capta verbosidade/filler e não capta deriva elaborativa — isso é um resultado interessante sobre a limitação da métrica.

### D7 — R1.Q4: argumento "e/e_crit = 2,1 vs 2,5" não se sustenta 🟠

A diferença entre e/e_crit = 2,1 (Qwen) e 2,5 (Gemma) é pequena, e os ICs do e_crit são largos. Os intervalos se sobrepõem.

**Argumento mais forte:** o Gemma r=16 não é a configuração degradativa mais próxima do limiar. A mais próxima é r=10. O teste de exposição foi feito numa posição não equivalente (inclinação −2,5 vs −1,0 pp/ger; 69% vs 83% na Gen5).

**Ação:** Dose de exposição no Gemma **r=10** (0/5/10/25%), não apenas r=16.

### D8 — Pontos menores 🟡

- **Gemma r=2 e r=256 "a custo 0 h":** só adicionar depois de recontar sobre K0=46. Os valores 97,9% e 70,2% vêm de K0=47. E r=256 (70,2%) fica quase empatado com r=16 (71,7%) — pode abrir questionamento sobre não-monotonicidade
- **Validação prospectiva calibrada em Gen1–2:** arriscado. Na Gen2, Qwen r=128 e r=256 são indistinguíveis (88,6% vs 89,9%). Probe deve ir até Gen5 no mínimo
- **Abstract:** não iniciar com "curva universal" (ver D2). Citar Π = erank × LR como resultado secundário

---

## PARTE E — Textos prontos para a carta de resposta

> Substituem os trechos problemáticos identificados nas Partes 3 e D. Colar diretamente no `response-to-reviewers.tex`.

### E.1 — Contribuição #3 (manuscrito, §1 ou §6)

```
(3) a rank × learning-rate experiment showing that update capacity and
perturbation magnitude combine approximately multiplicatively: a binomial
model in log(erank) and log(LR) yields nearly equal coefficients
(ratio ≈ 1.04), so that retention across the nine tested cells is ordered
by the single product erank × LR, with no detectable departure from
multiplicativity (interaction LRT p = 0.33; nine single-seed cells,
limited power).
```

### E.2 — Interação rank × LR (resposta ao R2.4)

```
We thank the reviewer for prompting a formal test. A likelihood-ratio test
of an interaction term in a binomial model on log(erank) and log(LR) was
not significant (p = 0.33). Because both predictors are on a log scale,
this is a test of departure from a multiplicative combination; we therefore
replaced the claim that the axes "interact" with the more precise,
quantitative statement that they combine approximately multiplicatively
(coefficient ratio 1.04). Given nine single-seed cells, we describe any
residual interaction as "not detected" rather than absent, and we note that
the largest residual occurs at the highest-pressure cell (r = 256,
LR = 2×10⁻⁵), consistent with saturation.
```

### E.3 — Normalização cross-architecture (resposta ao R2.4)

```
We agree that reporting only a negative result was unsatisfying.
Normalisation by architectural quantities fails, so we now propose
empirical, per-backbone calibration: a two-parameter logistic (location
and slope in log effective rank) fitted to a short rank probe. Location
differs by roughly an order of magnitude and slope by a factor of ~2.4
between Qwen 2.5 1.5B and Gemma 3 1B. The qualitative form of the
dose–response is shared, but neither parameter is transferable, so both
must be calibrated for each backbone. Gemma 4 E2B (three single-seed ranks)
is consistent with this but cannot identify both parameters independently,
and we report it as such. We describe the calibration protocol in §X
[and test it prospectively on an unseen backbone].
```

### E.4 — "Sharp" → "abrupt within the tested grid" (resposta ao R2.4)

```
We agree. "Sharp" has been replaced by "abrupt within the tested grid".
We now report the change in retention loss per doubling of effective rank
inside versus across the transition interval, and the transition interval
for each backbone. We deliberately avoid claiming a precise breakpoint,
because six rank levels cannot support model selection between linear and
segmented forms. [A denser grid (r ∈ {96, 160, 192}) narrows the Qwen
interval to X–Y.]
```

### E.5 — Gemma 4 E2B (resposta ao R2.4 / R2.5)

```
The backbone is google/gemma-4-E2B-it, distinct from Gemma 3n E2B. Its
technical report (Gemma Team, arXiv:2607.02770) appeared after our
submission, so our footnote stating that none existed is obsolete and has
been replaced by a formal citation together with the model card and revision
hash. We re-verified all architectural values against the released
config.json (hidden size 1536, 35 layers, 8 query heads, 1 key–value head),
which match those reported in the submitted manuscript. We additionally now
report the exact number of adapted modules, since this architecture shares
key–value projections across layers.
```

### E.6 — R1.Q4: por que 5% estabiliza Qwen mas não Gemma 3

```
The two configurations were not at equivalent positions relative to their
boundaries. Qwen r = 256 is the lowest-pressure degradative configuration
tested (post-adaptation slope ≈ −1.0 pp/generation; 83% at Gen5), whereas
Gemma 3 r = 16 lies deep in the degradative regime (≈ −2.5 pp/generation;
69% at Gen5); the Gemma 3 configuration closest to its boundary is r = 10.
We therefore ran an exposure dose–response (0/5/10/25% removal, three
seeds) at Gemma 3 r = 10 [results]. We now scope the claim as sensitivity
to marginal exposure near the degradative boundary.
```

### E.7 — Estatística: método principal (resposta ao R2.4)

```
Primary inference uses item-level mixed-effects logistic regression (random
intercepts for item and seed), because the same K₀ items recur across
generations and conditions and pooled-count tests would be anticonservative.
We additionally report Newcombe and item-stratified bootstrap confidence
intervals, Hedges' g, and exact permutation tests with the minimum
attainable p-value disclosed (0.10 for 3 vs 3; 0.008 for 5 vs 5). Trends
within runs are estimated on Gen1–Gen10, excluding the definitional Gen0
value.
```

---

## PARTE F — Prioridades revisadas de experimentos

> Combina os dois planos anteriores, incorporando as discordâncias da Parte D.

| # | Ação | Custo aprox. | Responde a |
|---|------|-------------|-----------|
| **0** | Verificar no código: decodificação (geração E avaliação separadamente), K0 por backbone, definição de drift, configs dos backbones no HF Hub com hash, lista de módulos treináveis no E2B, mapa de hardware por experimento | 1 dia | A2–A6, D1, D5 |
| **1** | C1 com N=3: reaproveitar os 3 runs de r=256 Gen5 (recalculados sobre K0=78) + 1–2 seeds pelo pipeline de intervenção com 0% de remoção | ~2 h | A10, R1.Q4 |
| **2** | Reavaliação com EM estrito e contains unidirecional + avaliação com 1.000 itens (sem treinar) | Poucas horas | A9, R1.Q3 |
| **3** | Dose de exposição no Gemma **r=10** (0/5/10/25%) + Qwen r=256 com 10/25%, 3 seeds, Gen5 | ~6 h | R1.Q4, D7 |
| **4** | LoRA bf16 vs QLoRA (r=16 e r=256, 3 seeds, 10 ger) + fatorial de ordem dos dados (seed init × seed ordem, r=256) | ~4 h | R1.Q2 |
| **5** | FFT no Gemma com 2 seeds extras (LR 5e-6 e 1e-5) | ~2 h | R1.Q3, 1.1.6 |
| **6** | Previsão pré-registrada: 3–4 células rank×LR fora do ajuste (commit datado antes de rodar); 4º backbone com probe até Gen5 | ~3–10 h | R1.Q1, R2.4 |
| **7** | 2º dataset (PopQA/NQ-open) + grade mais densa perto do limiar (Qwen r∈{96,160,192}) | Se houver tempo | R1.Q3, R2.4 |

**Mínimo defensável:** itens 0–4. Itens 5–7 se sobrar tempo.

---

### 4.1 — Erros confirmados a corrigir

**Citações confirmadas (verificadas independentemente):**

| Ref | Correção confirmada |
|-----|-------------------|
| **[7] Keisha et al.** | NeurIPS 2025 Workshop on Evaluating the Evolving LLM Lifecycle — citar como workshop paper, não como preprint sem venue |
| **[11]** | ICLR 2026 (Yi, Liu, Cheng, Xu) — atualizar venue |
| **[12]** | arXiv:2509.08972 (Zibakhsh Shabgahi et al.); versão publicada em npj Artificial Intelligence (2026) — usar DOI da versão publicada |
| **[32]** | Rathore, Kumar, Bansal, Moitra — AACL-IJCNLP 2025 — corrigir ano e venue |
| **[8]** | *Strong Model Collapse* = arXiv:2410.04840, ICLR 2025 (o 2402.07712 é outro artigo) — corrigir arXiv ID |
| **[16]** | *Collapse or Thrive?* = Kazdan, Schaeffer, Dey, Gerstgrasser, Rafailov, Donoho, Koyejo — corrigir autores |
| **[31]** | Soutif-Cormerais, Magistri, van de Weijer, Bagdanov — CoLLAs 2024 — corrigir autores e venue |
| **[18]** | *A Tale of Tails* = Dohmatob, Feng, Yang, Charton, Kempe — ICML 2024 — completar autores e venue |
| **Gemma 4 E2B** | Gemma Team, *Gemma 4 Technical Report*, arXiv:2607.02770 (2026) + model card HF com hash |
| **[33]** | CURLoRA arXiv:2408.14572 — manter, está certo |

> ⚠️ **Aviso:** Se dizer ao R2 que "normalizou todas as referências" e ele encontrar [8], [16], [31] ou [18] ainda erradas, perde credibilidade. Verificar todas antes de submeter.

### 4.2 — Itens a verificar ainda

| Ref | Suspeita |
|-----|---------|
| **[19] Seddik** | Verificar se foi para COLM 2024 |
| **[24] Feng et al.** | Possivelmente ICLR 2025 ("Beyond Model Collapse…") |

### 4.3 — Formatação geral

- Estilo Elsevier numerado: venue, volume e páginas obrigatórios onde disponíveis
- Preferir versão publicada ao arXiv quando existir

---

## PARTE 5 — Reprodutibilidade e repositório (R1.Q5)

| ID | Ação | Prior. | Tipo |
|----|------|--------|------|
| 5.1 | Criar/completar repositório GitHub com: código de treino/geração/avaliação, YAML configs, lista de seeds, prompts TriviaQA verbatim (incluindo C2), datasets sintéticos S_t (JSONL), outputs por item, adapters headline no HF Hub, environment (requirements pinado, CUDA/driver, Dockerfile) | 🟠 | `INFRA` |
| 5.2 | Criar script único que regenera todas as tabelas e figuras a partir dos raw outputs (resolve A5) | 🔴 | `INFRA` |
| 5.3 | Arquivar no Zenodo e obter DOI | 🟠 | `INFRA` |
| 5.4 | Adicionar Data Availability statement no MS com URL do repositório e DOI Zenodo | 🟠 | `TEX` |
| 5.5 | FFT checkpoints: muito grandes para hospedar inteiro — liberar checkpoints da última geração + receita exata no Apêndice A | 🟡 | `INFRA` + `TEX` |

---

## PARTE 6 — Outros itens obrigatórios (Editor + checklist)

| ID | Problema | Ação | Prior. | Tipo |
|----|----------|------|--------|------|
| 6.1 | Cover letter endereçada à EAAI | Refazer completamente para KBS, com resposta ponto a ponto (ver A1) | 🔴 | `INFRA` |
| 6.2 | Language editing obrigatório (instrução explícita do editor) | Enviar MS para Elsevier Author Services até ~12/10 (leva 5–7 dias úteis) | 🟠 | `INFRA` |
| 6.3 | Highlights: duas versões diferentes em circulação ("three backbone families" vs outra) | Unificar; ≤85 caracteres cada; atualizar com novos resultados se necessário | 🟠 | `INFRA` |
| 6.4 | Cabeçalho "First Author et al." e ORCID vazio | Preencher (KBS não é double-blind; URL do repositório pode ir no Apêndice A) | 🟡 | `TEX` |
| 6.5 | Frase quebrada antes da Fig. 5 ("Having established… Figure 5:") | Corrigir | 🟡 | `TEX` |
| 6.6 | Figuras em PDF no .tex — Elsevier exige 300 dpi PNG/TIFF | Converter todas para PNG 300 dpi; atualizar caminhos no .tex | 🟠 | `TEX` |

---

## Cronograma de execução (21 dias)

```
Semana 1 — 30/09–06/10: forma + dados (edição pura + lançar experimentos)
  Dia 30/09–01/10:
    [ ] A1 — Refazer cover letter para KBS
    [ ] 4.1 — Corrigir erros confirmados no .bib (ref [12], [32], Gemma 4)
    [ ] 4.2 — Verificar refs suspeitas no Google Scholar/DBLP
    [ ] 3.1.3 — Commit datado das previsões prospectivas antes de qualquer experimento
    [ ] Lançar P0 e P1 na fila de GPU (Athena)

  Dia 02/10–04/10:
    [ ] 1.2 — Corrigir encoding em todo o .tex (grep por não-ASCII)
    [ ] 1.3 — Reescrever Eq. 1–6
    [ ] A6 — Conferir definição real de drift no código; corrigir Eq. 3
    [ ] A8 — Copiar arquitetura do config.json; corrigir §3.3 e Tab. 11

  Dia 05/10–06/10:
    [ ] 1.1 — Corrigir todas as inconsistências factuais (5.1–5.7)
    [ ] 1.4 — Criar Tabela de Nomenclatura; expandir todas as abreviaturas
    [ ] 1.5 — Definir θ_H e θ_D; reescrever classificação de r=128 e r=256
    [ ] A2, A3 — Hardware e avaliação gulosa no §3.3/3.2

Semana 2 — 07/10–13/10: estatísticas + experimentos + reescrita
  Dia 07/10–09/10:
    [ ] 2.1 — Adicionar GLMM e estatísticas formais
    [ ] A9 — Recalcular com EM estrito e contains unidirecional
    [ ] A5 — Script de tabelas com K0 auditado
    [ ] A4 — Documentar discrepância seed 15; reportar ambos os valores

  Dia 10/10–12/10:
    [ ] Incorporar resultados dos experimentos P0 e P1
    [ ] 3.1 — Adicionar §3.5.3 (Π) e §4.3.2 (teste prospectivo)
    [ ] A7 — Corrigir taxas de degradação (inclinação pós-adaptação)
    [ ] Reescrever §3–6 com todas as mudanças

  Dia 12/10 (deadline interno):
    [ ] 6.2 — Enviar para Language Editing (Elsevier Author Services)

Semana 3 — 14/10–19/10: carta de resposta + submissão
  Dia 14/10–16/10:
    [ ] Incorporar language editing
    [ ] Preencher response-to-reviewers.tex completo
    [ ] 5.1–5.3 — Repositório GitHub + Zenodo DOI

  Dia 17/10–19/10:
    [ ] Gerar PDFs highlighted + clean (.\build.ps1)
    [ ] Converter carta de resposta para Word
    [ ] 6.3–6.6 — Highlights, cabeçalho, figuras PNG
    [ ] Revisão final de todos os arquivos de submissão
    [ ] Submeter até 19/10 (folga de 1 dia)
```

---

## Checklist de entrega (20 out)

**Verificações antes de editar o .tex:**
- [ ] Confirmar config.json do E2B e Gemma 3 no HF Hub (com hash) — não mudar Tab. 11 se .tex estiver certo (D1)
- [ ] Confirmar decodificação no código: geração sintética (temp?) vs avaliação K0 (greedy?) (D5)
- [ ] Confirmar definição de drift no código: mean absolute ou L2? inclui embeddings? (A6)
- [ ] Imprimir lista de módulos treináveis no E2B — verificar KV sharing (D1)
- [ ] Recalcular 3 runs de r=256 Gen5 sobre K0=78 para usar como C1 com N=3 (item F.1)

**Manuscrito:**
- [ ] `manuscript-anonymous.tex` revisado, compilando sem erros, figuras em PNG 300 dpi
- [ ] `cas-refs.bib` corrigido: [7] NeurIPS WS, [8] arXiv:2410.04840, [11] ICLR 2026, [12] npj AI, [16] autores corretos, [18] completo, [31] Soutif-Cormerais, [32] AACL 2025, Gemma 4 arXiv:2607.02770
- [ ] PDF versão limpa
- [ ] PDF versão marcada (alterações em azul via `\chg{}`)
- [ ] Curva-mestra universal **removida** ou substituída por calibração por backbone (D2)
- [ ] Testes inválidos **removidos**: McNemar de transições, Cochran-Armitage misto, ΔAIC com n=6 (D3)
- [ ] Interação reformulada: "approximately multiplicative, not detected, limited power" (D4)
- [ ] Critérios de regime: só retenção (nível + inclinação pós-adaptação). SDI-3 como descritor separado (D6)

**Carta de resposta:**
- [ ] `response-HIGHLIGHTED.pdf` (via `build.ps1`)
- [ ] `response-CLEAN.pdf` (via `build.ps1`)
- [ ] `response-to-reviewers.docx` (convertido para Word)
- [ ] Textos da Seção E incorporados nas respostas relevantes

**Documentos obrigatórios em Word:**
- [ ] `cover-letter.docx` — nova versão endereçada à KBS
- [ ] `highlights.docx` — versão unificada (≤85 char cada); não mencionar "curva universal"
- [ ] `credit-author-statement.docx`
- [ ] `declaration-of-competing-interests.docx`
- [ ] `title-page.docx` — preencher ORCID
- [ ] Certificado do Language Editing (Elsevier Author Services)

**Repositório:**
- [ ] GitHub: código, configs, seeds, prompts TriviaQA, outputs, environment
- [ ] Zenodo com DOI
- [ ] Adapters headline no HF Hub
- [ ] Data Availability statement no MS

---

## Próximos passos imediatos

Posso executar qualquer um destes agora:

1. **(a) Reescrever §3.5 e §4.5 completos em LaTeX** — com Π, GLM, protocolo de calibração e resultado prospectivo
2. **(b) Script Python de tabelas** — regenera todas as tabelas a partir dos `results.json` com K0 auditado + estatísticas formais (GLMM, bootstrap CI, Wilson)
3. **(c) Arquivo de pré-registro** — commit datado com previsões prospectivas de Π para as 3–4 células a rodar
4. **(d) Corrigir o .tex agora** — começar pela Parte 1 (encoding, equações, inconsistências) que é tudo edição pura

Por onde quer começar?
