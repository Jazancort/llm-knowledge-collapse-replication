# Plano de Revisão — KNOSYS-D-26-21490
<!-- ÚLTIMA ATUALIZAÇÃO: 2026-10-02T10:18 UTC-3 -->
**Knowledge-Based Systems (Elsevier) · Major Revision**
Prazo da revista: 20/10/2026 (ter) · Meta interna: 19/10 (seg) · Hoje: 02/10 (sex)

---

## Regras do plano

1. Toda tarefa aponta para um comentário (R1.Qx / R2.x / Editor) ou para um erro encontrado. O que não aponta para nada fica fora.
2. Nenhum experimento novo é lançado depois de 04/10 (dom). Depois disso, só reexecução de run que falhar.
3. Todo número do manuscrito sai de um script (`make_all.py`), nunca de digitação à mão.
4. Todo patch de código vai para commit antes de rodar; o hash fica gravado em cada `results.json`.

---

## Decisões já tomadas (não reabrir)

| Decisão | Consequência |
|---|---|
| Título fica como está | — |
| +9 pp de exposição retirado; substituído pela dose-resposta pré-registrada (Bloco 7) | Abstract, highlights, Contribuição 5 e §4.5 reescritos |
| Mecanismo da exposição (steps vs. composição) não afirmado | Uma frase nas limitações |
| C2–C4 saem do texto principal | Apêndice "original-pipeline, for transparency" |
| Π = erank·η é "índice operacional candidato", não lei universal | Sem "curva-mestra" nem Π com N_steps |
| Gemma 4 E2B: 1 seed, evidência de apoio | Com citação e arquitetura conferida |
| "sharp" → "abrupt within the tested grid" | Sem breakpoint segmentado nem ΔAIC |
| Dataset adicional → future work | Justificativa: custo computacional proibitivo para um backbone novo a 10 gerações dentro do prazo |

---

## Fora do escopo desta revisão (→ future work / Paper 2)

- Mecanismo da exposição (steps vs. composição dos dados)
- Análise de "atrator" e Jaccard dos itens a 89.7%
- Π com N_steps
- 4º backbone
- Segundo dataset (multi-hop, respostas longas) — custo computacional inviável no prazo
- Bisseção completa do pipeline antigo
- C2/C3 no pipeline g1
- Modelos de 7B ou mais
- Horizonte além de 10 gerações

---

## Correções de análise do Bloco 7 (aplicar antes de escrever)

O arquivo `resultados-bloco7.md` contém afirmações mais fortes do que os dados permitem. As correções abaixo são obrigatórias antes de escrever §4.5.

| Afirmação errada | Correção |
|---|---|
| "Monotonia confirmada em todos os 5 seeds" | Falso. Seeds 42 e 137 têm 91.0%→88.5%→89.7% (dose 10→25→50%). Monotonia vale para as médias, não por seed. |
| "Dose-resposta na Gen5" | Na Gen5 há salto + platô; inclinação com intercepto p=0.58. A graduação aparece só na Gen10. |
| "Π ∝ erank·η·N_steps consistente com os dados" | Só no ponto de 50%. O modelo prevê 84.9% (dose=10%) e 86.5% (dose=25%); observado foi 89.0% e 89.2%. Doses pequenas têm efeito bem maior que o modelo prevê. |
| "7b: efeito é principalmente de steps" | Inconclusivo. N=3, ICs de [-6,+12] e [-14,+7]. Além disso, igualar steps com 75% dos dados faz cada exemplo ser visto ~2.7x em vez de 2 — repetição e composição confundidas. |
| "Dose=5% prevê +0.5 pp, consistente com +1.9" | Contradiz o próprio modelo (erra para cima nas doses baixas). C5 do Bloco 6 precisa ser do mesmo commit para entrar na série. |
| "Dose=50%: atrator estável, homeostase real" | 89.7% = 70/78 itens nos 5 seeds → sugere os mesmos 8 itens sendo perdidos, não homeostase. Verificar via Jaccard (sem GPU). Análise fica no Paper 2. |
| "Benefício cresce ao longo das gerações" | Vale para 25% e 50%. Com dose=10%, inclinação é -1.48 pp/gen vs -0.96 do dose=0%. A redução pequena adia, não interrompe. |

**O que os dados sustentam (use estas frases):**

Gen5 — Δ médio por dose (n=5 seeds):
- dose=10%: +5.0 pp (95% CI [+3.2, +6.9], t-pareado p=0.002)
- dose=25%: +5.3 pp (95% CI [+1.8, +8.8], t-pareado p=0.014)
- dose=50%: +5.7 pp (95% CI [+3.4, +8.1], t-pareado p=0.002)
- Wilcoxon: p=0.0625 (mínimo possível com n=5) — declarar explicitamente.

Gen10 — resultado mais forte:
- dose=10%: +2.4 pp (CI [-1.9, +6.8], p=0.20, n.s.), inclinação -1.48 pp/gen
- dose=25%: +5.5 pp (CI [+0.4, +10.5], p=0.039), inclinação -0.92
- dose=50%: +9.8 pp (CI [+6.9, +12.8], p=0.0008), inclinação -0.14 → bounded
- Regressão Δ_Gen10 em -ln(1-f): inclinação 12.3 (p=0.003)

Previsão pré-registrada confirmada (7c):
- Gen5: 89.7% vs 90.2% (Δ=+0.5 pp)
- Gen10: 88.5% vs 88.1% (Δ=+0.4 pp, IC 90% [-0.8, +1.6], TOST n=3)

---

## FASE 0 — Verificações que destravam o texto (02–03/10, sem GPU)

Gerar `docs/revision/verificacoes.md` com uma linha por verificação. Pronto quando todas as 10 linhas estão preenchidas e commitadas.

- [ ] **V1** — Decodificação: separar parâmetros de geração sintética vs avaliação
  - Como: `grep -n "temperature|top_p|do_sample|max_new_tokens" scripts/g1_rank_ablation.py scripts/core/*.py`
  - Output: valores de cada etapa, separados

- [ ] **V2** — Auditoria do K0 (79→78 Qwen, 47→46 Gemma 3)
  - Como: comparar `k0_indices` antigo e novo; identificar o item removido
  - Output: ID do item, motivo, frase pronta para §3.2

- [ ] **V3** — Mapa de hardware
  - Como: logs de `nvidia-smi` e `hostname` nos runs
  - Output: tabela experimento → máquina (RTX 3070 local / Athena RTX 4000 Ada / RTX 5000 Ada)

- [ ] **V4** — Seed 15, r=16: 75/78 vs 76/78
  - Como: comparar commit, kernels, config dos dois runs
  - Output: explicação (não-determinismo ou versão) + frase para o texto

- [ ] **V5** — Definição exata de drift e ‖BA‖_F
  - Como: ler a função no código
  - Output: fórmula exata (média absoluta ou L2, por matriz ou somada, com/sem α/r)

- [ ] **V6** — Arquitetura dos 3 backbones
  - Como: `config.json` com hash da revisão do HF
  - Output: tabela d, layers, heads, KV heads (E2B esperado: 1536/35/8/1)

- [ ] **V7** — Módulos adaptados no E2B (KV compartilhado)
  - Como: `model.print_trainable_parameters()` + lista de módulos LoRA
  - Output: número real de matrizes adaptadas

- [ ] **V8** — Índice da Gen5 nos JSONs
  - Como: confirmar campo `gen` em `data[4]` e `data[5]`
  - Output: convenção única usada em todos os scripts

- [ ] **V9** — Origem do C1 e C3/C5 originais (erro de pipeline)
  - Como: diff dos parâmetros entre `c5_replicate_masks.py` e `g1_rank_ablation.py`
  - Output: lista das diferenças (vai para a carta)

- [ ] **V10** — Métricas KL/JS/coverage da Fig. 1
  - Como: verificar se aparecem em algum resultado
  - Output: se não aparecem, remover da figura

---

## FASE 1 — Fila de GPU (02–04/10)

Script único: `run_revisao_final.sh` com `set -euo pipefail`, 1 log por run, linha em `runs_index.csv` ao fim de cada run.

**Pré-registro obrigatório antes de lançar:** commit de `prereg_revisao_final.md` com hipóteses de G2, G3, G5 (G5 já tem ee0aecc9).

| # | ID | Experimento | Responde a | Runs | Custo est. |
|---|---|---|---|---|---|
| 1 | **G1** | Qwen r=256, dose=0%, seeds 15/137/256, commit 5805579, 10 gen | Consistência Bloco 7 (R1.Q4) | 3 | ~3h |
| 2 | **G2** | Gemma 3 r=10, doses 0/10/25/50%, seeds 15/137/256, 10 gen | R1.Q4 (generaliza?) | 12 | ~5h |
| 3 | **G3** | LoRA bf16 sem quantização, Qwen r=16 e r=256, 3 seeds, 10 gen | R1.Q2 (quantização) | 6 | ~7h |
| 4 | **G4** | Ordem dos dados: Qwen r=256, seed init fixo=15, 3 seeds shuffle, 5 gen | R1.Q2 (ordem) | 3 | ~2h |
| 5 | **G5** | Π prospectivo no pipeline g1: 3 células pré-registradas (ee0aecc9), 5 gen | R1.Q1 (prospectivo limpo) | 3 | ~1.5h |
| 6 | **G6** *(opcional)* | FFT Gemma 3, LR 5e-6 e 1e-5, +2 seeds, 5 gen | R2.3 item 6 | 4 | ~2h |

**Total:** ~18.5h obrigatórias + 2h opcionais.

**Corte se o tempo apertar:** G6 → G4 → reduzir G3 para 2 seeds.

**Instruções para o agente:**
- Usar só `g1_rank_ablation.py` com patch 5805579
- Gravar em cada `results.json`: commit, dose, tokens, exemplos, steps, rank, LR, quantização, seed_init, seed_shuffle
- Nomes únicos: `rev_{exp}_{backbone}_r{r}_s{seed}_{var}`
- Ao fim de cada run: gravar linha em `runs_index.csv`

Pronto quando: todos os runs obrigatórios terminam sem FAIL e estão no `runs_index.csv`.

---

## FASE 2 — Análises (03–08/10, CPU, em paralelo com GPU)

Script único: `analysis/make_all.py` — lê `results.json`, gera todas as tabelas (CSV + LaTeX) e figuras. Nenhum número entra no .tex de outra forma.

- [ ] **A1** — Regenerar todas as tabelas com K0 auditado (78/46/76) → Tabelas 2–8 novas (R2.3, consistência)

- [ ] **A2** — GLMM por item: `correct ~ condição + (1|item) + (1|seed)` nas comparações principais:
  - r=16 vs r=256
  - Gemma r=4 vs r=16
  - QLoRA vs FFT
  - Bloco 7 + G1 (análise primária pré-registrada: `correct ~ log(1-f) + (1|item) + (1|seed)`)
  - G2 (Gemma r=10, mesma fórmula)
  - Output: Tabela S1 com coeficientes, p unilateral, AIC

- [ ] **A3** — IC de Newcombe, Hedges g, permutação exata (com p mínimo declarado), Wilson para runs de 1 seed → Tabela suplementar S1 (R2.4)

- [ ] **A4** — Inclinação pós-adaptação (Gen2–10 ou Gen5–10) com IC → classificação de regime; coluna "slope" nas tabelas (R2.3 r=128/r=256)

- [ ] **A5** — GLM rank×LR: coeficientes, razão, LRT da interação, LOO; Π prospectivo (G5): MAE do Π vs modelos só-rank e só-LR → Tabela 7 nova + parágrafo (R1.Q1, R2.4)

- [ ] **A6** — Calibração por backbone: logística de 2 parâmetros (localização e inclinação) em ln(erank) → Tabela 11 revisada + texto (R2.4)

- [ ] **A7** — Bloco 7 + G1: análise primária pré-registrada + Δ pareados (Gen5 e Gen10) + equivalência com LR → Tabela 8 nova + Figura 9 nova (R1.Q4)

- [ ] **A8** — G2 (Gemma r=10): mesma análise do A7 → painel adicional na Fig. 9 (R1.Q4)

- [ ] **A9** — G3 (bf16 vs NF4) e G4 (ordem dos dados): diferença por seed + decomposição de variância → Tabela nova na §4.6 (R1.Q2)

- [ ] **A10** — Reavaliação com EM estrito e `contains` unidirecional sobre saídas já salvas → checar viés de verbosidade → Tabela suplementar S2 (R1.Q3)

- [ ] **A11** — SDI-3 de todas as configurações (nota: capta filler, não deriva elaborativa) → Tabela 12 (R2.1 / Eq. 6)

- [ ] **A12** — Controle G1 vs G2 (sintético vs real) + CKA, dados M2 existentes → §4.6 (R1.Q2)

Pronto quando: `make_all.py` roda do zero e reproduz todas as tabelas; nenhum número do .tex fica fora dele.

---

## FASE 3 — Correções do Revisor 2 (03–07/10, sem GPU, começar já)

### 3.1 Encoding e renderização (R2.1, R2.2)

- [ ] Adicionar `\usepackage[T1]{fontenc}` + `lmodern`; remover todo Unicode colado no texto (×, ≈, ∈, −)
- [ ] Toda notação em modo matemático: `$5\times10^{-6}$`, `$\sim$5\%`, `$r\in\{4,10,12,14,16\}$`
- [ ] Rodar `pdffonts` no PDF: nenhuma fonte Type 3, todas embutidas
- [ ] Após upload, abrir o PDF gerado pelo Editorial Manager e conferir cada equação

### 3.2 Tabela de nomenclatura (R2.1)

Todos os símbolos definidos formalmente, em ordem de aparição:

| Símbolo | Definição |
|---|---|
| 𝒦₀ | conjunto de K₀ perguntas de avaliação |
| \|𝒦₀\| = K₀ | cardinalidade do conjunto |
| R(t) | retenção factual na geração t: \|{i ∈ 𝒦₀ : acerto}\| / K₀ |
| erank | effective rank: exp(−Σ pᵢ log pᵢ), com pᵢ = σᵢ / Σσⱼ |
| pᵢ | peso espectral normalizado |
| σᵢ | i-ésimo valor singular de ΔW |
| ΔW = (α/r)BA | matriz de atualização LoRA |
| ‖·‖_F | norma de Frobenius |
| θ⁽⁰⁾ | pesos do backbone pré-treinado |
| θ⁽ᵗ⁾ | pesos adaptados na geração t |
| d(t) | drift: (definição exata da V5) |
| CE(t) | cross-entropy média na geração t |
| Persist(t) | taxa de persistência de padrões geração a geração |
| I(t) | índice de itemização (variações únicas) |
| L̄(t) | comprimento médio das respostas sintéticas |
| D₁ | diversidade tipo 1 (exponencial de entropia) |
| T | horizonte temporal (T=10 gerações) |
| SDI-3 | índice de diversidade sintética (D₁, I(t), L̄(t)) |
| η | learning rate |
| Π | índice de pressão operacional: erank · η |
| f | fração de exemplos removidos (dose de exposição) |
| θ_H | limiar homeostático (R ≥ θ_H → regime homeostático) |
| θ_D | limiar degradativo (R ≤ θ_D → regime degradativo) |

Siglas por extenso na primeira ocorrência: ETP, LoRA, QLoRA, NF4, bf16, FFT, SVD, TCE, MTLD, CKA, EM.

### 3.3 Equações 1–6 reescritas (R2.2)

- [ ] **Eq. 1:** R(t) com o conjunto 𝒦₀ e o indicador de acerto
- [ ] **Eq. 2:** pᵢ = σᵢ / Σσⱼ e erank = exp(−Σ pᵢ log pᵢ)
- [ ] **Eq. 3:** fórmula real do drift (resultado da V5)
- [ ] **Eq. 4:** CE(t) com todos os símbolos definidos
- [ ] **Eq. 5:** Persist(t) com todos os símbolos definidos
- [ ] **Eq. 6:** SDI-3 com T=10, D₁ e I(t) definidos

### 3.4 Inconsistências (R2.3)

- [ ] "~50" no lugar de "150" (era render do til)
- [ ] Dois limiares θ_H e θ_D com critério numérico; r=128 fica "acima de θ_H e abaixo de θ_D"
- [ ] r=256 → "lowest-pressure degradative configuration tested", não "boundary"
- [ ] Gemma 3: r ≥ 10 (§5.2)
- [ ] Abstract: "headline comparisons replicated with 3–5 seeds; supporting ablations single-seed"
- [ ] FFT no Gemma 3: "consistent with", não "confirms" (ou números novos do G6)
- [ ] "~5%" no lugar de "15°"; contagens exatas de tokens e exemplos
- [ ] Coluna "N seeds" em todas as tabelas; "Homeo." escrito por extenso

### 3.5 Referências (R2.5)

| Ref | Correção |
|---|---|
| [7] Keisha | NeurIPS 2025 Workshop on Evaluating the Evolving LLM Lifecycle; rotular como workshop |
| [8] Strong Model Collapse | arXiv:2410.04840, ICLR 2025 |
| [11] Yi et al. | ICLR 2026; autores Yi, Liu, Cheng, Xu |
| [12] ForTIFAI | arXiv:2509.08972 (2025) + versão npj AI se confirmada |
| [16] Collapse or Thrive | Kazdan, Schaeffer, Dey, Gerstgrasser, Rafailov, Donoho, Koyejo |
| [18] | Título completo "A Tale of Tails…", ICML 2024 |
| [31] | Soutif-Cormerais, Magistri, van de Weijer, Bagdanov |
| [32] | Rathore, Kumar, Bansal, Moitra, AACL-IJCNLP 2025 |
| Novo | Gemma Team, Gemma 4 Technical Report, arXiv:2607.02770 + model card com hash |
| Todas | Estilo elsarticle-num; versão publicada quando existir; conferir no DBLP/Scholar |

Pronto quando: checklist fechado e PDF compila sem nenhum glifo estranho.

---

## FASE 4 — Reescrita do manuscrito (05–10/10)

### Textos prontos para uso direto

**Contribuição (5) — nova:**

> (5) a pre-registered exposure dose–response on the Qwen degradative configuration (r = 256; five paired seeds): any reduction of the synthetic training stream (10–50%) raises Gen5 retention by ≈5 pp, and at Gen10 the benefit is graded (+2.4, +5.5, +9.8 pp at 10/25/50%). A 50% reduction effectively arrests progressive loss (Gen5→Gen10 slope −0.14 vs −0.96 pp/generation) and is equivalent, as predicted before the runs, to halving the learning rate (Gen10 difference +0.4 pp, 90% CI [−0.8, 1.6]). This is consistent with exposure acting through the per-generation update budget.

**Abstract item (5) — novo:**

> …and (5) a pre-registered dose–response showing that reducing synthetic exposure shifts the system toward bounded retention, with a 50% reduction arresting progressive degradation and matching the effect of halving the learning rate.

**Highlight (≤85 caracteres):**

> Halving synthetic exposure arrests recursive degradation, like halving the LR (78 caracteres)

**Limitações — trecho sobre exposição:**

> The mechanism through which exposure reduction acts — whether via the per-generation update budget or via data composition — was not established; the steps-matched control (G2b) was inconclusive at n = 3. The effect was tested on a single backbone and configuration.

### Mapa de alterações por seção

| Seção | O que muda | Responde a |
|---|---|---|
| Abstract | Seeds, "abrupt", item (5) novo, Π em uma frase | R2.3, R2.4, R1.Q4 |
| Highlights | 5º bullet novo; unificar as duas versões | Editor |
| Intro: contribuições | #3 → "combinação multiplicativa (razão ≈ 1.04, interação não detectada)"; #5 → dose-resposta pré-registrada | R2.4, R1.Q4 |
| §3.1 | Decodificação de geração e avaliação separadas (V1) | R1.Q5 |
| §3.2 | Auditoria do K0 (V2); 𝒦₀ separado de R(t) | R2.1 |
| §3.3 | Mapa de hardware (V3); configs com fonte (V6); citação Gemma 4; módulos E2B (V7) | R2.4, R1.Q5 |
| §3.5 | Π como índice operacional + protocolo de calibração por probe; definição dos regimes | R1.Q1, R2.4 |
| §3.7 | Desenho novo da exposição (doses, seeds pareados, pré-registro) | R1.Q4 |
| §3.8 | Estatística: GLMM, ICs, testes exatos, horizonte primário, análises secundárias rotuladas | R2.4 |
| §3.9 nova | Tabela "fonte de variação → controle" (otimizador, quantização, ordem, seeds, pipeline) | R1.Q2 |
| §4.1–4.4 | Números regenerados, coluna inclinação, "abrupt", nota V4 | R2.3 |
| §4.3.2 | GLM + Π + resultado prospectivo (G5) vs modelos nulos | R1.Q1 |
| §4.5 reescrita | Dose-resposta Qwen + Gemma r=10 + equiv. LR; nota sobre pipelines; C2–C4 no apêndice | R1.Q4 |
| §4.6 nova | G1 vs G2 (sintético vs real), bf16, ordem dos dados | R1.Q2 |
| §5 | Tirar "5% flips regime"; ajustar Tabela 9; normalização com calibração 2 parâmetros | R2.4 |
| §6 Limitações | Escopo (respostas curtas, 1 dataset, até 2B, 10 gen); mecanismo exposição não estabelecido; E2B 1 seed; EM estrito | R1.Q3 |
| §7 Conclusão | Alinhar com tudo acima | — |
| Apêndice A + Data availability | URL, DOI Zenodo, lista do que foi liberado | R1.Q5 |

Pronto quando: Julio leu o texto inteiro uma vez e todo número no texto bate com `make_all.py`.

---

## FASE 5 — Reprodutibilidade (06–10/10, R1.Q5)

- [ ] Repositório: código, configs YAML de cada run, `runs_index.csv`, lista de seeds e máscaras, prompts e chat templates literais
- [ ] IDs do 𝒦₀ por backbone + item removido na auditoria
- [ ] Datasets sintéticos S_t (JSONL) e saídas de avaliação por item
- [ ] Adapters LoRA dos runs principais no HF Hub; para FFT, só a geração final dos runs principais (declarar)
- [ ] Ambiente: versões fixadas, CUDA/driver, `uv.lock` ou Dockerfile
- [ ] Pré-registros (`a916ebf`, `ee0aecc9`, `prereg_revisao_final.md`) com data e timestamp
- [ ] `make_all.py` + README "reproduce every table in one command"
- [ ] Release no GitHub com DOI do Zenodo

---

## FASE 6 — Figuras e formato (08–11/10, Editor)

- [ ] Todas as figuras em PNG/TIFF a 300 dpi (não PDF), geradas pelo `make_all.py`
- [ ] Fig. 1: ETP por extenso; remover KL/JS/coverage se não reportados (V10); trocar "5% exposure" pela dose-resposta
- [ ] Figs. 3–5 e 7 regeneradas com K0 auditado
- [ ] Fig. 9 nova: dose-resposta (Qwen r=256 + Gemma r=10), Gen5 e Gen10, com IC
- [ ] Corrigir frase quebrada antes da Fig. 5
- [ ] Tabelas e equações editáveis (LaTeX nativo, sem imagem)
- [ ] Cabeçalho "First Author et al." e ORCID preenchidos

---

## FASE 7 — Language editing (enviar 12/10)

- [ ] 11/10: versão congelada para envio (sem números pendentes)
- [ ] 12/10: enviar ao Elsevier Language Editing Services
- [ ] Enquanto aguarda: escrever a carta (Fase 8)
- [ ] Ao receber: aplicar as edições sem mexer em números nem em afirmações; guardar o certificado

**Plano B:** se o serviço não devolver até 17/10, submeter com revisão própria cuidadosa e explicar na carta que o certificado vai depois.

---

## FASE 8 — Carta e pacote de submissão (12–18/10)

### Progresso da carta (response-to-reviewers.tex)
**Arquivo:** `v4/docs/overleaf/response-to-reviewers.tex`
**Atualizado:** 2026-10-02

| Comentário | Status | Data |
|---|---|---|
| Editor | ✅ escrito | 02/10 |
| R2.1 — Notação (10 sub-itens) | ✅ escrito | 02/10 |
| R2.2 — Equações 1–6 (4 sub-itens) | ✅ escrito | 02/10 |
| R2.3 — Inconsistências (7 sub-itens) | ✅ escrito | 02/10 |
| R2.4 — Metodologia (6 sub-itens) | ⏳ parcial — aguarda GPU | — |
| R2.5 — Referências (5 sub-itens) | ✅ escrito | 02/10 |
| R1.Q1 — Calibração prospectiva | ⏳ aguarda G5 | — |
| R1.Q2 — Confounds | ✅ escrito (G3/G4 + N=6 permutação p<0.001 + ETP-design/observed) | 04/10 |
| R2.4 — Metodologia (6 sub-itens) | ✅ escrito | 04/10 |

`\msnote{inserir resposta}` restantes no .tex: **2** (04/10 12:38) — R1.Q1 (aguarda G5 completo) + R1.Q5 (aguarda Zenodo DOI)
| R1.Q3 — Escopo métrica | ✅ escrito | 02/10 |
| R1.Q4 — Exposição | ✅ escrito | 02/10 |
| R1.Q5 — Reprodutibilidade | ⏳ aguarda Fase 5 | — |

`\msnote{inserir resposta}` restantes no .tex: **8** (02/10 10:38)

### Padrão de escrita adotado
Modelo: carta IEEE Access (Access-2025-40211, arquivo `docs/previous-submission/`).
Estrutura por resposta:
1. Agradecimento breve (1 frase)
2. Resposta substantiva com evidência específica
3. `\msloc{linha exata}` com localização no manuscrito



### Texto base para a carta (trecho sobre a Contribuição 5)

> In addressing Reviewer 1 (Q4) and Reviewer 2 (statistical rigour), we replicated the unmodified baseline with multiple seeds and found that, in the original submission, the C1 baseline and the C3/C5 interventions had been produced by different code paths [the source of the discrepancy was X]. When re-run under an identical pipeline and paired seeds, a ∼5% reduction yields only +1.9 pp. We have therefore withdrawn the original claim that a ∼5% reduction restores near-homeostatic retention.
>
> We replaced it with a pre-registered experiment (protocol committed as a916ebf before any run): an exposure dose–response at 0/10/25/50% removal with five paired seeds, a learning-rate equivalence test, and a steps-matched control. The pre-registered primary analysis [item-level mixed model, slope p = …] supports the hypothesis that retention increases with exposure reduction. At Gen10, the effect is graded and reaches +9.8 pp at 50% removal (95% CI [6.9, 12.8]). The pre-registered prediction that 50% removal would match halving the learning rate was confirmed. The steps-matched control was inconclusive at n = 3, so we do not claim a specific mechanism [or: an additional post-hoc control indicates…]. All runs are reported, including those inconsistent with the hypothesis. We thank the Reviewer, whose question led directly to this corrected and stronger result.

### Checklist do pacote

- [ ] Cover letter nova endereçada à KBS (a atual cita a EAAI)
- [ ] Carta de resposta ponto a ponto (R1.Q1–Q5; R2.1–R2.5, cada bullet): comentário → resposta → "Changes: §X, Table Y, p. Z"
- [ ] Parágrafo de transparência sobre os pipelines (C1 vs C5), o pré-registro e o resultado corrigido
- [ ] Manuscrito com mudanças marcadas (azul) + versão limpa
- [ ] Source LaTeX + .bib + figuras
- [ ] Highlights, CRediT, declaração de interesses e author agreement (Word)
- [ ] Certificado do language editing
- [ ] Material suplementar (Tabelas S1, S2; C2–C4 originais)

---

## FASE 9 — Controle de qualidade final (16–19/10)

- [ ] Script de consistência: extrair todos os números do .tex e cruzar com saídas do `make_all.py`
- [ ] Grep de termos proibidos: "sharp", "boundary configuration", "5%… restores", "150", "three to five seeds per condition", "confirms" (FFT Gemma)
- [ ] `pdffonts` + leitura do PDF gerado pelo Editorial Manager
- [ ] Aprovação dos coautores (Carlos André, André de Carvalho, Carlos Francês): enviar 15/10, prazo 17/10
- [ ] 19/10: submeter

---

## Cronograma diário

| Data | Julio | Agente / GPU |
|---|---|---|
| 02/10 sex | Fase 0 (V1–V10); começar Fase 3.1 | Commit pré-registro; lançar G1 → G2 |
| 03/10 sáb | Fase 3.2–3.3 (nomenclatura, equações) | G2 → G3; A1, A10 (CPU) |
| 04/10 dom | Fase 3.4–3.5 (inconsistências, referências) | G3 → G4 → G5 (→ G6). **Fim dos lançamentos** |
| 05/10 seg | Fase 4: abstract, contribuições, §3 | A2–A7 |
| 06/10 ter | Fase 4: §3.5, 3.8, 3.9 | A8, A9, A12; Fase 5 |
| 07/10 qua | Fase 4: §4.1–4.4, §4.3.2 | A11; Fase 5 |
| 08/10 qui | Fase 4: §4.5, §4.6 | Fase 6 (figuras) |
| 09/10 sex | Fase 4: §5, §6, §7, apêndice | Fase 6 |
| 10/10 sáb | Releitura completa; checagem de consistência | Release no Zenodo |
| 11/10 dom | Congelar versão para editing | — |
| 12/10 seg | Enviar ao language editing; começar a carta | — |
| 13–14/10 | Carta ponto a ponto | — |
| 15/10 qua | Enviar pacote aos coautores | — |
| 16–17/10 | Aplicar editing e comentários dos coautores | — |
| 18/10 sáb | Montar pacote em Word e LaTeX final | — |
| 19/10 seg | Fase 9 + submissão | — |
| 20/10 ter | Folga (prazo da revista) | — |

---

## Riscos e respostas

| Risco | Resposta |
|---|---|
| G2: sem efeito de dose no Gemma r=10 | Reportar. Responde R1.Q4 do mesmo jeito: "exposure sensitivity is backbone-dependent". Não rodar mais doses. |
| G3: bf16 muda o regime | Reportar e discutir a quantização como fator de pressão. Não esconder. |
| G5: Π erra a previsão | Reportar o MAE e manter o Π como descritivo. |
| G1 diferente da dose=0% anterior | Usar só G1 na série do Bloco 7 e declarar. |
| Language editing atrasa | Plano B da Fase 7. |
| Coautor demora | Prazo fixo de 17/10, combinado na hora do envio. |
| Novo problema na Fase 0 | Corrigir só se afetar número reportado; o resto vai para as limitações. |

---

*Arquivo: `v4/docs/revision/plano-revisao-final.md`*
*Criado: 2026-10-02*
