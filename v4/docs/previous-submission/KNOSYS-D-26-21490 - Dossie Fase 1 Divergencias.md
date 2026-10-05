# Dossiê Fase 1 — Auditoria de Divergências Carta ↔ Manuscrito
## KNOSYS-D-26-21490 | 2026-10-05

> **Status:** 22 divergências documentadas. Aguardando D1, D2, D4 e 4 verificações locais para fechar esta fase e iniciar patches.

---

## 1. Painel de veredictos

| ID | Tema | Veredicto | Decisão | Prioridade |
|---|---|---|---|---|
| **C1** | Figura 1 (ETP, KL/JS/coverage, exposure) | ❌ Divergência confirmada | A | 🔴 |
| **C2** | Codificação de caracteres | ❌ Divergência ampla e confirmada | A | 🔴 |
| **C3** | Notação $K_0$ / $\sigma_i$ | ❌ A crítica do revisor permanece no texto | A | 🔴 |
| **C4** | r=128 "above-threshold" | ⚠️ Parcial (§4.4.3 ok; §4 e §5.3 não) | A | 🟠 |
| **C5** | "boundary configuration" | ⚠️ Parcial (§3.4 e §4.5 ok; §5.4 não) | A | 🟠 |
| **C6** | Contagem de sementes | ⚠️ Abstract ok, Contribuição 1 não; citação da carta não é literal | A+B | 🔴 |
| **C7** | FFT Gemma 3 "confirming" | ⚠️ Abstract e §4.3.3 ok, Contribuição 2 não | A | 🟠 |
| **C8** | "Homeo." | ❌ Local errado (é Fig. 5, não Tab. 2) + "Degrad." também | A+B | 🟠 |
| **C9** | Controle de quantização | ❌ Baseline e número errados na carta | B | 🔴 |
| **C10** | G5 "2 de 3" | ❌ Confunde ordenação com classificação | B | 🟠 |
| **C11** | Conteúdo do pacote | ❌ Carta contradiz o Apêndice A | A+B | 🟠 |
| **C12** | Protocolo prospectivo na §6 | ❌ Não existe no manuscrito | A | 🔴 |
| **C13** | Shumailov "added" | ❌ Já era [6] na submissão original | B | 🟡 |
| **C14–C15** | Remissões de seção/tabela | ❌ 11 remissões erradas | B | 🔴 |
| **C16** | Números de linha | ❌ O PDF não tem numeração | A ou B | 🔴 |
| **C17** | Números canônicos | ✅ B7/G2 conferem · ⚠️ "112" não verificável | — | 🟠 |
| **C18** | "Degrad." na Tabela 4 | ❌ Novo achado | A | 🟠 |
| **C19** | "no other rendering failure" | ❌ Novo achado — frase perigosa | B | 🔴 |
| **C20** | DOI truncado no Apêndice A | ❌ Novo achado | A | 🟠 |
| **C21** | C1–C5 vs. C2–C5 vs. C3/C5 | ❌ Novo achado — incoerência interna da carta | B | 🟠 |
| **C22** | "all headline comparisons" | ❌ Novo achado — overclaim | B | 🔴 |

---

## 2. Grupo A — Figura 1, renderização e a frase mais arriscada da carta

### C1 · Figura 1 não foi refeita 🔴

**A carta afirma:** "We removed 'ETP' from Figure 1 … removed KL/JS/coverage from Figure 1 … the revised caption describes only quantities that are measured."

**O PDF revisado mostra (p. 8):**
- Painel 6: *ETP threshold identification*
- Painel 4: *Distribution shift — KL, JS, coverage*
- Painel 3: *Exposure — 100% → ~95% synthetic*
- Legenda: *pressure manipulation along five axes*

**Risco:** três afirmações falsas verificáveis em uma única figura, e o revisor citou essa figura nominalmente em dois bullets.

**Ação (A) — quatro correções:**
1. `ETP threshold identification` → `Pressure–regime mapping and threshold localisation`
2. Remover `Distribution shift — KL, JS, coverage`; substituir por `Distribution shift — Distinct-n, MTLD, stopword ratio` (métricas efetivamente computadas em §3.6/§4.4)
3. `Exposure — 100% → ~95% synthetic` → `Exposure — 0 / 10 / 25 / 50% removal` (**⚠️ mais grave:** a figura ainda anuncia o experimento retirado por inconsistência de pipeline)
4. Harmonizar "five axes" entre legenda e diagrama

---

### C2 · A falha de renderização não foi corrigida 🔴

**A carta afirma:** "The revised submission uses the lmodern package with T1 encoding throughout, which eliminates all rendering artefacts."

**O PDF revisado mostra artefatos em 11 locais distintos:**

| Local | Ocorrência |
|---|---|
| Highlights | `differ í10İ`, `erank í3–6 vs í50–88` |
| Abstract | `rank İ learning-rate`, `3İ3 grid`, `slope *0.15 pp/generation` |
| §3.1 | `t Ë ˆ1`, `ğ`, `T'`, `S_{t*1}`, `learning rate 10*5` |
| §3.4 | `r Ë ˆ4, 10, 12, 14, 16'`, `5İ10*6`, `2İ10*5` |
| Eq. 1 | `R.t/ = ˆq Ë K0 : q correct at gen. t'/K0` |
| Eq. 2 | `erank.BA/ = exp* i σilog σi` |
| Eq. 3 | `d.t/ = 1/θ i θ.t/i * θ.0/i` |
| §4.1 | `*1.20 pp per generation`, `79.72˜` |
| Tabela 1 | `⊙ F`, `erank.∆W/ ⊙ .η˙10*5/` |
| Tabela 2 | `10*6–2İ10*5` |
| Tabelas 8, 9 | `5İ10*6`, `2İ10*5`, `0.42 (BAF)` |

**Diagnóstico provável:** não é falta de lmodern + T1. O padrão (`.` no lugar de parênteses, `*` no lugar de menos, `İ/˜` no lugar de `×/%`) é típico de substituição de glifos na conversão de PDF. Hipóteses em ordem de probabilidade: (i) template elsarticle/cas-dc com fonte que não embute glifos matemáticos; (ii) re-destilação pelo Editorial Manager; (iii) caracteres Unicode colados diretamente no fonte (`×`, `≈`, `−`, `∈`) em vez dos comandos LaTeX.

**Ação (A), nesta ordem:**
1. `grep` por Unicode cru no fonte (bloco Cursor, seção 7)
2. Compilar com embedação de fontes: `\pdfinclusioncopyfonts=1` ou gerar com `lualatex`
3. Validar com `pdffonts arquivo.pdf` → nenhuma fonte deve aparecer sem `emb=yes`
4. Fazer upload no Editorial Manager e baixar o PDF gerado por ele — a falha original só se manifestou nessa etapa

**Ação (B):** reescrever a explicação técnica da carta somente depois do passo 4, e remover a especulação não verificada (ver C19).

---

### C19 · A frase mais perigosa da carta 🔴 (novo)

**Texto atual (R2.2, Author action):** "…and verified that no other table or equation contains a similar rendering failure in the revised submission."

**Problema:** é uma afirmação de verificação exaustiva que o PDF atual refuta em 11 locais. Se o revisor abrir o PDF e ver `3İ3` no próprio Abstract, a credibilidade de toda a carta cai.

**Ação (B) — deletar a frase até que Q4 passe. Substituir por:**

> "We additionally ran an automated glyph audit over the compiled PDF, checking every equation, table cell, and caption against the source; the audit script and its output are included in the replication package."

O mesmo raciocínio se aplica a "while the source was syntactically correct" — manter só se confirmado no `.tex`.

---

## 3. Grupo B — Notação: a crítica central do Revisor #2 ainda está no texto

### C3 · $K_0$ e $\sigma_i$ 🔴

O Revisor #2 escreveu:
> "K0 is used both as a set of questions and as a retention metric."
> "The effective-rank formula uses σ_i as both singular values and normalized singular values. The normalization condition is mathematically incorrect as written."

**O PDF revisado mantém exatamente as duas falhas:**

| Local | Texto atual |
|---|---|
| Tabela 1 | `K0 — Set of items in Q answered correctly at generation 0; K0 (also written n0) denotes its cardinality` |
| Tabela 1 | `σi = σi˙ j σj — Normalised singular weight` |
| Eq. 1 | denominador é `K0`, não `|K0|` |
| Eq. 2, texto | `where σi = σi˙ j σj are the normalized singular values` |

**Ação (A) — texto pronto para a Tabela 1:**

```latex
$\mathcal{K}_0$ & Set of held-out items answered correctly at generation~0
                  (the baseline-correct set) \\
$|\mathcal{K}_0|$ & Cardinality of $\mathcal{K}_0$; protocol-specific:
                  78 (Qwen), 46 (Gemma~3 rank sweep),
                  44 (Gemma~3 G2 dose), 76 (Gemma~4 E2B) \\
$R(t)$ & Factual retention at generation~$t$: fraction of
         $\mathcal{K}_0$ items still correct \\
$\sigma_i$ & $i$-th singular value of $\Delta W$ \\
$p_i = \sigma_i/\sum_j \sigma_j$ & Normalised singular weight,
         with $p_i \ge 0$ and $\sum_i p_i = 1$ \\
$\mathrm{erank}(\Delta W)$ & Effective rank:
         $\exp\!\left(-\sum_i p_i \log p_i\right)$ \\
```

**Equações 1–3 corrigidas:**

```latex
R(t) = \frac{\bigl|\{\, q \in \mathcal{K}_0 :
        q \text{ answered correctly at generation } t \,\}\bigr|}
       {|\mathcal{K}_0|}

\mathrm{erank}(BA) = \exp\!\left(-\sum_i p_i \log p_i\right),
  \qquad p_i = \frac{\sigma_i}{\sum_j \sigma_j}

d(t) = \frac{1}{|\theta|}\sum_i \bigl|\theta_i^{(t)} - \theta_i^{(0)}\bigr|
```

A troca de $\hat\sigma_i$ por $p_i$ é deliberada: é a notação que o próprio revisor propôs. Adotá-la literalmente é o movimento mais persuasivo disponível.

---

### C18 · "Degrad." na Tabela 4 🟠 (novo)

A Tabela 4 do manuscrito revisado traz `256* 34.9M 10 79.1% 87.57 3 Degrad.` — mesma classe de problema que o revisor apontou para "Homeo.". Expandir para `Degradative` e verificar as legendas das Figs. 4, 5 e 11.

---

### C8 · "Homeo." está no lugar errado 🟠

**A carta diz:** "expanded 'Homeo.' throughout Table 2" e "in all four occurrences in Table 2".

**Mas:**
- A Tabela 2 do manuscrito revisado é "Experimental axes and their corresponding pressure components" — não contém "Homeo."
- O termo aparece na legenda/eixo da Figura 5 (`Homeo.`, `Bounded`, `Degrad.`)

O revisor citou "Table 2" com base na numeração da submissão original — o que leva ao item mais estrutural desta fase.

---

## 4. Grupo C — Numeração original vs. revisada (causa-raiz de C14–C15)

A carta mistura as duas numerações sem avisar.

### Tabela de remissões erradas

| Na carta | O revisor se referia a… | No manuscrito revisado é… |
|---|---|---|
| "Table 7" (5×10^6) | Tabela 7 original | Tabela 9 (rank × LR) |
| "Table 4" (Gemma 3 ranks) | Tabela 4 original | Tabela 6 |
| "Table 2" (regimes r=128/256) | Tabela 2 original | Tabela 4 |
| "Table 2 (tab:controls)" | — | Tabela 3 |
| "Table 6" (normalizações) | — | Tabela 13 |
| "§4.4" (G5) | — | §4.6 |
| "§4.2" (G3 pareado Qwen) | — | §4.1 |
| "§4.3.1" (Gemma 3) | — | §4.2.1 |
| "§3.6" ($K_0$) | — | §3.2 |
| "§3.1" (protocolo de avaliação) | — | §3.2 |
| "§A.1" | — | Apêndice A (não há A.1) |

**Convenção recomendada:**
- No `\rquote` (fala do revisor): preservar a numeração original, sem alterar.
- No `Author response / Author action`: usar a numeração revisada e declarar o mapeamento na primeira ocorrência — ex.: "Table 7 of the original submission (now Table 9)".

---

### C16 · Os números de linha não existem 🔴

A carta cita `l. 72`, `ll. 2094–2100`, `ll. 692–698`, `ll. 1265, 1277–1280` e ~20 outros intervalos. O PDF revisado não tem numeração de linhas.

**Duas saídas:**
- **(A)** Adicionar `\usepackage{lineno}\linenumbers` ao manuscrito destacado e reconferir todos os intervalos depois da compilação final.
- **(B)** Trocar tudo por Section + page (ex.: "Section 4.6, p. 17").

**Recomendação: B** — robusto a reedições e o prazo é 20/10.

---

## 5. Grupo D — Erros factuais sobre os próprios experimentos

### C9 · Controle de quantização 🔴

**A carta afirma:**
> "At r=16, bf16 achieves Gen10 = 97.4% (76/78 per seed), while the original NF4 single-seed result was 96.2% (75/78) … At r=256, bf16 achieves Gen10 = 79.1%, within 0.0 pp of the NF4 G1+G4 mean. Quantization is therefore not the primary driver."

**Três erros:**
1. **Baseline errado em r=16.** O comparador NF4 de três sementes é 97,4% (§4.3.1), não o valor single-seed de 96,2% (§4.1). Com o baseline certo, a diferença é +0,00 pp.
2. **Número errado em r=256.** A média G1+G4 é 79,72% (§4.1, §4.6), não 79,1%. O 79,1% é a média G1 isolada. "Within 0.0 pp of the G1+G4 mean" é falso; o fato real é que bf16 reproduziu as contagens por semente de G1 ([61, 63, 61]/78) exatamente.
3. **Conclusão mais forte que a do manuscrito.** §4.6 diz: "a causal conclusion about quantization awaits full provenance audit." Contagens idênticas entre NF4 e bf16 são estatisticamente improváveis e sugerem reuso de artefato — exatamente o que a auditoria pendente investiga.

**Ação (B) — parágrafo pronto:**

> For quantization: all primary QLoRA experiments load the base model in 4-bit NormalFloat (NF4) with adapters trained in bfloat16. Ablation G3 re-runs the identical protocol in bf16 with no base-weight quantization, using three matched seeds (15/137/256) at each of $r=16$ and $r=256$. At $r=16$, bf16 returns Gen10 = 97.4% (76/78 in every seed), identical to the three-seed NF4 value reported in Section 4.3.1. At $r=256$, bf16 returns the same per-seed item counts as the NF4 G1 set ([61, 63, 61]/78; 79.1%). The regime classification is therefore invariant to precision at both ranks. We deliberately state this as agreement between classifications rather than as a causal conclusion about quantization: because the per-seed counts coincide exactly, we are completing a run-level provenance and item-level audit before interpreting that agreement as evidence that quantization has no effect (Section 4.6). The audit outcome will be reported in the final version.

---

### C10 · G5: ordenação ≠ classificação 🟠

**A carta afirma:** "retention was ordered in the expected direction for 2 of 3 pre-specified configurations."

**§4.6 mostra:**
- Baixa pressão: 96,20% → Homeostatic ✔
- Intermediária: 89,70% → Bounded ✔
- Alta pressão: 85,90% → Bounded (previsto Degradative ✗)

A ordenação 96,2 > 89,7 > 85,9 saiu **correta nas três células**. O que falhou foi uma **classificação de regime**. A carta subestima o próprio resultado e contradiz o manuscrito.

**Ação (B) — frase pronta:**

> The pre-registered G5 probe (three single-seed cells on Qwen) provides limited exploratory evidence: Gen5 retention was ordered in the predicted direction across all three cells (96.2%, 89.7%, and 85.9% for the low-, intermediate-, and high-pressure cells), but one of the three pre-specified regime classifications was not met — the high-pressure cell was predicted Degradative and returned Bounded. No $\Pi$ threshold is reported for G5, because the pre-specification fixed nominal rank and learning rate rather than a threshold on $\Pi$; nor does G5 test an unseen backbone or dataset.

---

### C17 · Números canônicos ⚠️

**Confere ✅** — B7 (Tabela 10: +3,6/+3,8/+4,4 pp em Gen5; +1,8/+4,9/+9,2 pp em Gen10) e G2 (+9,8/+11,4/+12,9 pp) batem entre carta e manuscrito.

**Pendente ⚠️:**
- A carta diz "reproduces all 112 canonical numbers (15/15 checks pass)"; o Apêndice A diz apenas "reproduces all canonical numbers reported in this paper (15/15 consistency checks pass)". O "112" não existe no manuscrito. **Verificar na saída de `make_all.py`** e harmonizar os dois textos.
- As macros `\BsevenSlopeFifty`, `\GtwoDeltatenFifty`, `\GtwoPtenFifty`, `\GtwoCItenLoFifty`, `\GtwoCItenHiFifty` precisam ser expandidas e conferidas: esperado −0,15 / +12,9 / 0,001 / 9,70 / 16,10.

---

### C22 · "all headline comparisons" 🔴 (novo)

**Capa da carta, item (3):** "seed-level exact permutation tests and paired t-tests with 95% confidence intervals for all headline comparisons."

**Contraexemplos no próprio manuscrito:**
- Qwen r=16 vs. r=256 (G3): sign test, p = 0,25 — não é teste de permutação
- QLoRA vs. FFT (§4.3.1): nenhum teste reportado, apenas "ranges do not overlap"
- Gemma 4 E2B: semente única, sem teste

**Ação (B):**

> "(3) seed-level inferential statistics for every comparison in which independent training runs are available: exact permutation and sign-flip tests for the rank contrasts (G3 on Qwen; anchor ranks on Gemma 3) and paired $t$-tests with 95% confidence intervals for all dose levels of the two pre-registered dose–response experiments (B7, G2); comparisons that remain single-seed or non-exchangeable are reported as descriptive and labelled as such."

---

## 6. Grupo E — Reprodutibilidade e coerência interna

### C11 · O pacote se contradiz 🟠

| Fonte | Afirmação |
|---|---|
| Carta (response) | "per-generation retention counts and boolean correctness vectors included in the consolidated CSV" |
| Carta (action) | "The package does not contain raw token-level predictions" |
| Apêndice A | "This snapshot contains the initial experimental scripts, raw outputs, aggregated per-seed per-generation results…" |

Além disso, a carta promete "exact model checkpoint identifiers and revisions" remetendo a §3.3 — mas §3.3 lista apenas nomes de modelos, sem hashes de revisão.

**Ação (A+B), após decisão D4 — tabela de status:**

| Artefato | Status | Local |
|---|---|---|
| Analysis & figure scripts | ✅ incluído | `scripts/` |
| Consolidated per-seed per-generation CSV | ✅ incluído | `results/` |
| Prompts & chat templates | ✅ incluído | `configs/` |
| Seeds, data-order & downsampling masks | ✅ incluído | `configs/` |
| Base-model checkpoint IDs + revision hashes | ⬜ a adicionar em §3.3 | — |
| Item-level boolean correctness vectors | ⬜ decisão D4 | — |
| Raw token-level generations | ⬜ decisão D4 | — |
| Adapter checkpoints (~70 MB cada, bf16) | 🔸 sob solicitação | — |
| Base-model weights | ❌ não redistribuídos | HF Hub |

---

### C12 · O protocolo prospectivo não existe 🔴

**A carta afirma:** "We added a concrete validation protocol for future prospective calibration in Section 6."

**§6 contém apenas:** "Whether such a formulation can be obtained… remains an open question for future work." Isso é uma frase, não um protocolo.

**Ação (A) — bloco pronto para inserir em §6:**

> A prospective calibration of effective training pressure on an unseen backbone would require the following protocol, which we specify here as a concrete target for future work rather than as a result of the present study. (i) **Pilot sweep:** run two nominal ranks spanning roughly one order of magnitude (e.g. $r=4$ and $r=64$) for five recursive generations with a single seed, recording $\mathrm{erank}(\Delta W)$ per generation. (ii) **Backbone-local calibration:** fit the regime boundary as the interval between the highest pilot configuration whose Gen1–Gen5 retention slope is statistically indistinguishable from zero and the lowest configuration whose slope is negative. (iii) **Pre-specification:** register, before any further run, two configurations placed on opposite sides of the calibrated interval, together with the outcome criterion (Gen5→Gen10 retention slope) and the decision rule. (iv) **Held-out evaluation:** execute both configurations to Gen10 with at least three seeds, without refitting the calibration to the observed outcomes. (v) **Reporting:** report the pre-registered prediction, the observed classification, and any discrepancy, irrespective of direction. Steps (i)–(ii) cost approximately two pilot runs per backbone; the present study performed neither (iii)–(v) on an unseen backbone nor the cross-dataset variant of the same design.

---

### C20 · DOI truncado 🟠 (novo)

**Apêndice A:** `https://doi.org/10.5281/zenodo.23146342` (carta) vs. `DOI: 10.5281/zenodo.2314634` (Apêndice A — truncado e com contagem de dígitos divergente).

**Ação:** verificar o DOI real no Zenodo e padronizar nos dois documentos.

Relacionado: §A diz "Running `python scripts/figures/fig9_dose_response.py` regenerates Figure 10" — nome do script e número da figura não coincidem. Renomear o script ou explicar.

---

### C21 · Qual conjunto foi arquivado? 🟠 (novo)

Três grafias para o mesmo objeto:
- Capa da carta: "replacing the original **C3/C5** comparison"
- R1.4 (action): "archived the original **C2–C5** results"
- Manuscrito §4.5 e §3.7: "the original **C1–C5** pilot"
- R1.4 (msloc): "original **C1–C5** archived"

**Ação (B):** padronizar em **C1–C5** (o piloto completo, incluindo a linha-base C1) em todos os pontos, e descrever o problema uma única vez como "the C1-versus-C3/C5 comparisons".

---

### C13 · Shumailov 🟡

A carta diz "[Shumailov] is added as the primary citation". Ele já era a referência [6] desde §2.1 da submissão original.

**Ação (B):** "…and we have **reinforced** Shumailov et al. [6] (Nature) as the primary peer-reviewed anchor for the model-collapse phenomenon, so that no quantitative claim rests on [7] alone."

---

## 7. Bloco de verificação no Cursor

```bash
# ── C2: Unicode cru no fonte LaTeX ─────────────────────────────────────
rg -n '[×≈−–—∈≥≤σΔΠηθ]' *.tex | rg -v '^\s*%'
rg -n '[\x{00C0}-\x{024F}]' *.tex        # latin estendido inesperado

# ── C3: notação K0 / sigma ──────────────────────────────────────────────
rg -n 'also written|n_?0|\\sigma_i\s*=\s*\\sigma_i' *.tex
rg -n 'K_0' *.tex | rg -v '\|K_0\||\\mathcal'

# ── C4 / C5: rótulos de regime ──────────────────────────────────────────
rg -n 'above[- ]threshold|boundary configuration|intermediate capacity' *.tex

# ── C6 / C7: contribuições ──────────────────────────────────────────────
rg -n 'per condition|confirming that|three to five' *.tex

# ── C8 / C18: abreviações em tabelas e figuras ──────────────────────────
rg -n 'Homeo\.|Degrad\.' *.tex

# ── O1 (Fase 6, antecipado): overclaims ────────────────────────────────
rg -n 'abrupt|sharp|reversible|restores|evident|demonstrates|confirms' *.tex

# ── C16: numeração de linhas ────────────────────────────────────────────
rg -n 'lineno|linenumbers' *.tex

# ── C2: validação do PDF compilado ──────────────────────────────────────
pdffonts manuscript.pdf | rg -v 'yes'   # deve retornar vazio
pdftotext manuscript.pdf - | rg -n 'í|İ|Ë|ˆ|˜|⊙|ù'
```

**Prompt sugerido para o Cursor (Composer):**

> No arquivo `@manuscript.tex`, localize todas as ocorrências de `above-threshold` e `boundary configuration`. Para cada uma, verifique se o rank referido é 128 ou 256. Se for 128, substitua por `transition-zone configuration`; se for 256, substitua por `lowest-pressure degradative configuration tested`. Não altere ocorrências de `regime boundary` usadas em sentido geral. Liste cada alteração com número de linha antes de aplicar.

---

## 8. O que só você pode fechar

**Verificações locais (4):**
1. `make_all.py` → o número total de valores canônicos é 112?
2. `numbers.tex` → as cinco macros expandem para −0,15 / +12,9 / 0,001 / 9,70 / 16,10?
3. Zenodo → o DOI correto é `10.5281/zenodo.23146342`?
4. Dados brutos de C5 → 15% dos exemplos correspondem a ~5% dos tokens?

**Decisões que destravam a Fase 2 (3 das 7):**
- **D1** — o English Language Editing da Elsevier foi contratado? (impacta a resposta ao Editor)
- **D2** — opção A ou B para cada item? Recomendação: A para C1, C2, C3, C4, C5, C6, C7, C8, C12, C18, C20 · B para C9, C10, C11, C13, C14–C15, C19, C21, C22 · B para C16 (seção + página)
- **D4** — conteúdo do novo release (destrava C11)

---

## 9. Balanço

**14 divergências confirmadas + 5 achados novos (C18–C22).**

As cinco que, isoladamente, podem comprometer a rodada:

| Divergência | Por quê |
|---|---|
| **C2 + C19** | A carta afirma ter corrigido a renderização e tê-la verificado exaustivamente; o PDF exibe o defeito no próprio Abstract |
| **C3** | A crítica matemática mais objetiva do Revisor #2 permanece intacta no texto |
| **C9** | Baseline errado, número errado e conclusão mais forte que a do manuscrito, em cima de contagens idênticas que a auditoria interna ainda questiona |
| **C16** | ~25 localizações inutilizáveis |
| **C22** | "all headline comparisons" é refutável por três contraexemplos do próprio manuscrito |

Nenhuma delas é difícil de resolver — todas são de execução, não de ciência. A carta tem um ativo real que deve ser preservado: **a admissão espontânea do erro de pipeline C1/C5 é o tipo de transparência que editores recompensam.**

---

## Próximo passo

Envie as 4 verificações locais + D1/D2/D4 e os patches prontos serão gerados para colar no manuscrito e na carta. Ou peça o "item 2" (Fase 2 — estrutura e formato) para desenvolvimento em paralelo.
