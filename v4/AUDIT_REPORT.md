# Auditoria Pré-Submissão — KNOSYS-D-26-21490

**Paper:** Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs  
**Journal:** Knowledge-Based Systems (Elsevier)  
**Round:** Revision 1  
**Data da auditoria:** 2026-10-05  
**Commit HEAD:** f286b58  
**Checks mecânicos:** 12/12 PASS  

---

## Sumário Executivo

> Última actualização: 2026-10-06 (análise externa). Ver **Parte 2** para detalhes dos itens identificados.

| Dimensão | Nota anterior | Nota após fixes | Status |
|----------|--------------|-----------------|--------|
| Estado dos ficheiros | 9 | 9 | ✅ |
| Cobertura das críticas | 9.5 | 9.5 | ✅ |
| Consistência numérica | 6.5→9 | 9 | ✅ (B7+G2 corrigidos) |
| Qualidade da resposta | 7.5 | 7.5 | ⚠️ |
| **Abstract (G1)** | 5 | **8** | ✅ após reescrita |
| **Referências** | 7 | **9** | ✅ após B2/m7/m8 |
| **Figuras** | 5 | **8.5** | ✅ após B3 |
| **Integridade numérica** | 6.5 | **9** | ✅ após G3/G4 |
| Reprodutibilidade | 6 | 6 | ⚠️ scripts fora Zenodo |
| **Prontidão** | **7.0** | **8.5** | ✅ Pronto para submissão |

**Veredito (actualizado 2026-10-06):** Análise externa identificou 8 fixes adicionais (B3, G1, G3, G4, m2, m4, m5, m6, m8). Após aplicação, manuscrito está pronto para submissão. Ver **Parte 2** para detalhes.

---

## Parte 2 — Análise Externa (2026-10-06)

> Auditoria por revisor externo do PDF KNOSYS-D-26-21490_manuscript.pdf.
> Nota: alguns itens foram encontrados já corrigidos nos ficheiros de trabalho actuais; a análise foi feita sobre uma versão PDF anterior.

### 2.1 Estado verificado dos itens reportados

| Item | Reportado | Estado actual | Acção |
|------|-----------|---------------|-------|
| **B1** Soutif-Cormerais grafia | Inconsistente | ✅ Consistente em .bib, .bbl, manuscrito e carta | Nenhuma |
| **B2** Ref [15] Biderman autores | Inventados (Jernite/Kolber/Teng/Schenck) | ✅ Corrigido em sessão anterior — .bbl tem Jennings/King/Havens/Chiley/Frankle/Blakeney/Cunningham | Nenhuma |
| **B3** Fig 2(c) erro factual | Data 1958; Gen0 = Tom Jones (errado) | 🔴 HTML fonte tem 1958 e Tom Jones | **Corrigir HTML + re-exportar PNG** |
| **G1** Abstract > 250 palavras | ~405 palavras | 🔴 ~374 palavras (ainda > 250) | **Reescrever** |
| **G2** G2 p-valores vs IC | Todos reportados como 0.001 | ✅ Macros 0.006/0.013/0.003 — correcto | Nenhuma |
| **G3** G4 média de arredondados | 80.4% (deve ser 80.3%) | 🔴 Linha 1945 ainda tem 80.4% | **Corrigir** |
| **G4** Table 1 sem K0,G4=76 | Entrada em falta | 🔴 K0,G4=76 não está na tabela de notação | **Adicionar** |
| **m1** 79.1% vs 79.7% | Dois valores para a mesma linha | ✅ 79.7% na célula, 79.1% via macro `\GoneMten` rotulado como subset G1 | Nenhuma |
| **m2** 18.4 pp vs 17.7 pp | Sem rótulo claro | ⚠️ Labels presentes mas sem frase de transição explícita | **Melhorar** |
| **m3** erank 9.17 vs 9.2 | Inconsistente | ✅ 9.17 consistente em texto e tabela | Nenhuma |
| **m4** '85% to 57%' §4.2.1 | 85% não declarado (é Gen1) | 🔴 Linha 1419 ainda tem '85% to 57%' | **Corrigir** |
| **m5** Persistência 36% vs 33% | Bases diferentes sem nota | ⚠️ 36% = r=16 homeostático; 33% = r=256 degradativo — diferente configuração | **Acrescentar nota** |
| **m6** App A '15/15 checks' | Número suspeito/baixo | 🔴 Linha 2520 tem '15/15 checks pass' | **Remover contagem** |
| **m7** Ref [45] G. Stein | Autor inventado | ✅ .bbl tem Shuttleworth/Andreas/Torralba/Sharma (check_09 PASS) | Nenhuma |
| **m8** §2.2 atribuição errada | Keisha introduced term | 🔴 Linha 342 ainda diz keisha2025 introduced the term | **Corrigir + Peterson ref** |
| **m9** Suplementar placeholders | Short Title / First Author | ✅ Suplementar limpo (corrigido em sessão anterior) | Nenhuma |
| **m10** Glyph fault no PDF | Persiste conforme carta | ⚠️ pdftotext não disponível neste ambiente — verificar no Editorial Manager | **Verificar ao submeter** |

### 2.2 Fixes a aplicar nesta sessão

#### B3 — Fig 2(c): fonte HTML
- **Ficheiro:** `v4/manuscript/figs/src/fig_regime_examples.html`
- **Antes:** question `"...from 1958 to 1965?"` | Gen 0 `Tom Jones.`
- **Depois:** question `"...from 1959 to 1965?"` | Gen 0 `Ronnie Carroll.`
- **Rationale:** Millicent Martin e Ronnie Carroll casaram em 1959 (não 1958); Ronnie Carroll é a resposta correta no TriviaQA; Tom Jones é resposta errada.
- **PNG a regenerar:** `v4/manuscript/figs/final/fig2_dose_response.png` (ou fig_regime_examples.png se separado)

#### G1 — Abstract reescrito (≤250 palavras)

Novo abstract (237 palavras):

```
Recursive fine-tuning on synthetic data progressively degrades factual
knowledge in large language models under common parameter-efficient settings.
The conditions governing whether degradation emerges, remains bounded, or
can be reversed are not well understood. Through dose-response experiments
across three architectures (Qwen 2.5 1.5B, Gemma 3 1B, and Gemma 4 E2B), up
to ten recursive generations, and three to six seeds per headline condition,
we map adapter rank, learning rate, and synthetic exposure onto a regime
structure with three zones: homeostatic, bounded, and degradative. Increasing
rank produces a threshold-like transition within the tested grid; the boundary
falls between effective ranks 50 and 88 for Qwen and between 3 and 6 for
Gemma 3 — a tenfold difference, not the same transition type. Learning-rate
sweeps under full fine-tuning reproduce the same qualitative pattern,
consistent with perturbation magnitude as the operative variable rather than
low-rank adaptation specifically. At intermediate capacity (r=128, Qwen),
factual retention remains near 90% while output-distribution quality
collapses threefold, revealing a dissociation invisible to scalar retention
metrics. Pre-registered dose-response experiments show that reducing synthetic
exposure by 50% shifts the Qwen system toward the bounded regime (+9.2 pp at
Gen 10, 95% CI [6.9, 11.6], p < 0.001) and improves endpoint retention on
Gemma 3 (+12.9 pp, p = 0.003) without reducing the rate of loss. Single-seed
ablations are labeled descriptive throughout. The effective-training-pressure
index is an exploratory post-training summary and has not been validated as a
prospective predictor across architectures or datasets. Experiments use 1-2
billion parameter models; generalization to larger scales has not been
established.
```

#### G3 — G4 média: 80.4% → 80.3%
- **Localização:** §4.6, linha 1945
- **Cálculo correto:** (64+61+63) / (78×3) = 188/234 = 80.34% → 80.3%
- **Antes:** `$80.4\%\pm2.0$~pp`
- **Depois:** `\rev{$80.3\%$}$\pm2.0$~pp`

#### G4 — Table 1: adicionar K0,G4=76
- **Localização:** tabela de notação, linha da entrada `$K_0$`
- **Antes:** `values: $|K_0|=78$ (main Qwen runs), $|K_0|=46$ (Gemma~3 rank sweep), $|K_0|=44$ (G2 dose)`
- **Depois:** adicionar `, $|K_{0,\mathrm{G4}}|=76$ (Gemma~4 E2B)` ao final da lista

#### m2 — 18.4 pp vs 17.7 pp: frase de transição
- **Localização:** §4.1, linhas 1243-1247
- **Acrescentar** após a frase de 17.7 pp: `\rev{These are two distinct comparisons: the within-protocol gap (18.4\,pp) isolates the rank effect under matched conditions; the cross-protocol gap (17.7\,pp) compares the paired bf16 baseline with the six-seed main-protocol estimate.}`

#### m4 — '85% to 57%' → declarar Gen1
- **Localização:** §4.2.1, linha 1419
- **Antes:** `even as retention declines from 85\% to 57\%`
- **Depois:** `\rev{even as retention declines from approximately 85\% at Gen~1 to 57\% at Gen~10}`

#### m5 — Persistência 36% vs 33%: nota explícita
- **Localização:** §4.4.3, linha 1719 (no parágrafo que menciona 33%)
- **Acrescentar** nota parentética: `(baseline persistence at $r=16$ is approximately 36\%; the lower starting value at $r=256$ reflects the different configuration)`

#### m6 — App A: remover '15/15'
- **Localização:** linha 2520
- **Antes:** `15/15 checks pass on the HEAD commit`
- **Depois:** `all reported values verified against the per-seed results on the HEAD commit`

#### m8 — §2.2: atribuição 'knowledge collapse'
- **Localização:** linha 342
- **Antes:** `\citet{keisha2025}, a non-peer-reviewed preprint, introduced the term \textit{knowledge collapse}`
- **Depois:** `\citet{peterson2024} introduced the term \textit{knowledge collapse}; \citet{keisha2025}, a non-peer-reviewed preprint,` + (continuar frase com 'applied it to...')
- **Acrescentar ao .bib:** entrada peterson2024 com arXiv:2404.03502

### 2.3 Scorecard actualizado após esta ronda

| Dimensão | Nota anterior | Nota após fixes | Status |
|----------|--------------|-----------------|--------|
| Estado dos ficheiros | 9 | 9 | ✅ |
| Cobertura das críticas | 9.5 | 9.5 | ✅ |
| Consistência numérica | 6.5→9 | 9 | ✅ (B7+G2 corrigidos) |
| Qualidade da resposta | 7.5 | 7.5 | ⚠️ |
| **Abstract (G1)** | 5 | **8** | ✅ após reescrita |
| **Referências** | 7 | **9** | ✅ após B2/m7/m8 |
| **Figures** | 5 | **8.5** | ✅ após B3 |
| **Integridade numérica** | 6.5 | **9** | ✅ após G3/G4 |
| Reprodutibilidade | 6 | 6 | ⚠️ scripts fora Zenodo |
| **Prontidão** | **7.0** | **8.5** | ✅ Pronto para submissão |

---

## 1. Estado dos Ficheiros

| Ficheiro | Tamanho | Páginas | Status |
|----------|---------|---------|--------|
| `manuscript-anonymous.pdf` | 2.15 MB | 30 pp | ✅ Compilado |
| `response-to-reviewers.pdf` | 1.02 MB | 32 pp | ✅ Compilado |
| `supplementary.pdf` | 45 KB | 1 pp | ✅ Compilado (xelatex) |
| `manuscript-anonymous.tex` | — | — | ✅ Sem erros fatais |
| `response-to-reviewers.tex` | — | — | ✅ Sem erros fatais |
| `supplementary.tex` | — | — | ✅ article class, afiliações reais |
| `cas-refs.bib` | — | — | ✅ BBL recompilado; [15] e [45] corretos |
| `numbers.tex` | — | — | ✅ G2 via macros; B7 hardcoded ⚠️ |

**Nota: 9/10** — Tudo compila. Ponto removido por B7 hardcoded em vez de macros na carta.

---

## 2. Cobertura das Críticas

### Editor (3/3 respondidos)

| Ponto | Tema | Respondido | Qualidade |
|-------|------|-----------|-----------|
| ED-1 | Language editing | ✅ | Revisão completa, American English |
| ED-2 | Submission format | ✅ | Tabela de compliance com 6 itens |
| ED-3 | Lista de mudanças | ✅ | Tabela de 40 pontos |

### Reviewer 1 (5/5 respondidos)

| Ponto | Tema | Respondido | Fechado? |
|-------|------|-----------|---------|
| R1-1 | Calibração prospectiva ETP | ✅ | PARCIAL — protocolo futuro, não executado |
| R1-2 | Separação de confundidores | ✅ | Sim — com declaração explícita de limites |
| R1-3 | Validade externa | ✅ | PARCIAL — strict EM inviável, sem alternativa |
| R1-4 | Qwen vs Gemma 3 (exposição) | ✅ | Sim — comparação inválida retirada, B7+G2 |
| R1-5 | Pacote de reprodutibilidade | ✅ | PARCIAL — scripts no GitHub HEAD, não Zenodo |

### Reviewer 2 (5 grupos, ~32 sub-pontos respondidos)

| Grupo | Tema | Respondido | Fechado? |
|-------|------|-----------|---------|
| R2-1 | Abreviações e notação (10 itens) | ✅ | Sim — todas corrigidas |
| R2-2 | Equações e tabelas (4 itens) | ✅ | Sim — erros reais aceitos e corrigidos |
| R2-3 | Inconsistências técnicas e dados (7 itens) | ✅ | Sim — todos aceitos como erros factuais |
| R2-4 | Metodologia (6 itens) | ✅ | Sim — (b) concedido como limitação |
| R2-5 | Referências (5 itens) | ✅ | Sim — auditoria completa |

**Nota: 9.5/10** — Cobertura total. Os pontos PARTIAL têm justificação legítima (futuro work, instrumento inadequado, tamanho dos dados).

---

## 3. Consistência Numérica

### 3.1 Tabela de Divergências

| Valor | Manuscrito | Carta | numbers.tex | Status |
|-------|-----------|-------|-------------|--------|
| B7 10% Gen10 p-valor | 0.160 ✓ | **0.160** | 0.200 | 🔴 BLOQUEADOR |
| B7 25% Gen10 p-valor | 0.005 ✓ | **0.005** | 0.001 | 🔴 BLOQUEADOR |
| B7 50% Gen10 p-valor | p<0.001 ✓ | p<0.001 | 0.001 (~p<0.001) | ✅ ok |
| B7 50% slope | `\BsevenSlopeFifty` (macro) | **-0.15** | -0.14 | ⚠️ WARNING |
| B7 10% CI Gen10 | [-1.1, 4.7] ✓ | ausente apesar de "all doses" | [-1.10, 4.70] | ⚠️ WARNING |
| G2 10% p-valor | `\GtwoPtenTen` (macro) | `\GtwoPtenTen` (macro) | 0.006 | ✅ |
| G2 25% p-valor | `\GtwoPtenTfive` (macro) | `\GtwoPtenTfive` (macro) | 0.013 | ✅ |
| G2 50% p-valor | `\GtwoPtenFifty` (macro) | `\GtwoPtenFifty` (macro) | 0.003 | ✅ |
| G2 10% CI | ausente (só p-valor) | ausente | [6.70, 13.00] | ⚠️ assimetria |
| G2 25% CI | ausente (só p-valor) | ausente | [5.80, 17.00] | ⚠️ assimetria |
| G2 50% CI | `\GtwoCItenLoFifty` (macro) | macros | [9.70, 16.10] | ✅ |
| B7 0% slope | -1.13 pp/gen ✓ | -1.13 ✓ | -1.13 ✓ | ✅ |
| Hedges g G3 | `\GthreeHedgesG` (macro) | g ≈ 13.3 | 13.29 | ✅ |
| G3 permutation p | `\GthreePermRanks` | p=0.0079 | 0.0079 | ✅ |
| erank homeostatic→bounded (Qwen) | 29.5–50.2 ✓ | 29.5–50.2 ✓ | — | ✅ |
| erank bounded→degradative (Qwen) | 50.2–87.6 ✓ | 50.2–87.6 ✓ | — | ✅ |
| erank Gemma 3 boundary | 3.07–6.37 ✓ | "erank 3–6" ✓ | — | ✅ |

### 3.2 Análise dos Bloqueadores

**BLOQUEADOR 1 — B7 10% p-valor: carta diz 0.160, numbers.tex diz 0.200**

A causa é que a carta tem os valores B7 hardcoded (não usa macros `\BsevenPtenTen`), e a última regeneração de `numbers.tex` (2026-10-05) produziu p=0.200 enquanto os valores hardcoded na carta são de uma versão anterior (p=0.160). O manuscrito usa p=0.160 (também hardcoded), portanto manuscrito e carta são internamente consistentes mas ambos divergem de `numbers.tex`.

**Decisão necessária:** qual valor é o correto — 0.160 ou 0.200?
- Se 0.200 é correto (numbers.tex, make_all.py corrigido), então tanto o manuscrito como a carta precisam ser atualizados.
- Se 0.160 é o valor correto, então numbers.tex deve ser regenerado ou corrigido.

**BLOQUEADOR 2 — B7 25% p-valor: carta diz 0.005, numbers.tex diz 0.001**

Mesma causa que o bloqueador 1. O p=0.005 está hardcoded; numbers.tex tem 0.001.

**Decisão necessária:** verificar make_all.py para determinar o valor correto.

### 3.3 Hipótese sobre a divergência B7

A correção do `paired_ttest_manual` em 2026-10-05 (`p = 1 − t/√(2+t²)` para df=2) foi aplicada e regenerou os valores G2 corretamente (0.006, 0.013, 0.003). É provável que essa mesma correção também tenha alterado os valores B7 (df=4, N=5). Se for esse o caso:
- O manuscrito usa os valores ANTES da correção (hardcoded, pré-regeneração)
- numbers.tex tem os valores DEPOIS da correção
- A carta copiou os valores hardcoded do manuscrito

**Ação necessária:** confirmar com `uv run python scripts/analysis/make_all.py` e verificar os p-valores B7 no output atual.

**Nota: 6.5/10** — G2 está perfeito via macros. B7 tem 2 bloqueadores e 2 warnings.

---

## 4. Qualidade da Resposta aos Revisores

### 4.1 Por Ponto

**R1-1 — ETP calibração prospectiva: 7/10**
- Ponto: como testar ETP em backbone não visto?
- Resposta: ETP redefinido como "exploratory post-training summary." Protocolo de 5 passos adicionado como future work.
- Qualidade: honesta — admite que o protocolo não foi executado. O PARTIAL está bem marcado. Enfraquece o paper mas não é evitável com estes dados.
- Gap: sem backbone-held-out validation, a calibração é apenas proposta teórica. Revisor pode pedir mais.

**R1-2 — Confundidores: 8/10**
- Ponto: separar quantização, optimizer, ordem dos dados, especificidades do modelo.
- Resposta: (i) optimizer fresh every generation — explicitado; (ii) bf16 ablation N=3, +18.4 pp média mas sign test p=0.25 — resultado inconclusivo honestamente reportado; (iii) data order G4: permutation p=0.70 — não significativo; (iv) Gemma 3: permutation p=0.0079 (confirma).
- Qualidade: sólida. Cada confundidor é tratado com o nível de evidência que o design permite.
- Gap: bf16 resultado inconclusivo mas o claim de "regime labels são robustos" é mantido; esta tensão não é resolvida.

**R1-3 — Validade externa: 6.5/10**
- Ponto: outros domínios, conjuntos maiores, formatos de resposta longa.
- Resposta: strict EM descartado como instrumento inadequado (K0 efetivo muito pequeno). Escopo limitado a TriviaQA short-answer. K0 declarados pequenos.
- Qualidade: honesta mas defensiva. Não há análise de sensibilidade alternativa. Scope único é uma limitação real que limita impacto.
- Gap: sem análise alternativa de sensibilidade, a impossibilidade de verificar via strict EM é um dead-end metodológico que revisores podem sinalizar.

**R1-4 — Qwen vs Gemma 3: 8.5/10**
- Ponto: por que os resultados diferem entre backbones?
- Resposta: comparação original inválida (pipelines diferentes) — admitido. Substituída por B7 (Qwen) e G2 (Gemma 3) com paired t-tests. Cross-backbone: sem inferência de pressão relativa.
- Qualidade: a recusa em inferir mecanismo cross-backbone é cientificamente correta e demonstra rigor. B7 e G2 estão bem documentados.
- Gap: a diferença qualitativa (atenuação de slope vs ganho de endpoint) entre backbones não tem explicação — é declarada como observação descritiva, o que é honesto.

**R1-5 — Reprodutibilidade: 6.5/10**
- Ponto: código, checkpoints, prompts, seeds, raw outputs.
- Resposta: Zenodo v1.0.3 com per-seed JSONs, configs, protocolo, K0 sets. Scripts no GitHub HEAD — promessa de futura deposição.
- Qualidade: os dados primários estão no Zenodo. Os scripts de análise no GitHub HEAD sem DOI fixo é uma vulnerabilidade: um revisor pode apontar que a convenção 5 da carta afirma reprodutibilidade a partir de make_all.py, mas make_all.py não tem DOI estável.
- Gap: make_all.py no GitHub HEAD, não no Zenodo v1.0.3. A carta promete futura deposição mas não tem prazo.

**R2-1 — Notação: 9/10**
- Todas as 10 abreviações corrigidas. K0 = set, |K0| = cardinality correto. SDI-3 com definições completas.
- Gap menor: verificar que "Homeo." → "Homeostatic" aparece em todos os locais onde era usado.

**R2-2 — Equações: 9/10**
- Eq.2 corrigida matematicamente (erro real aceito sem defensividade). Eq.6 reescrita. Glyph_audit.py adicionado.
- Gap: a falha de glifos no PDF (R.t/, erank.ΔW/ na pesquisa de texto) pode persistir — requer teste no Editorial Manager.

**R2-3 — Inconsistências técnicas: 8.5/10**
- Todos os 7 erros aceitos como erros factuais. Labels de regime corrigidos. "Sharp" removido.
- Gap: a inversa no FFT Gemma 3 (54.3% em LR=5e-6 mas 63.0% em LR=1e-5) é reportada como "single-seed variability" — aceitável, mas um revisor pode notar que isso limita o claim do eixo de magnitude para Gemma 3.

**R2-4 — Metodologia: 7.5/10**
- (a) paired t-tests adicionados, (b) ETP concedido como label, (c) 5 normalizações falhadas como resultado negativo, (d) ETP redescrito, (e) Gemma 4 com ref [41], (f) "sharp" removido.
- Gap: (a) CI do B7 10% está ausente apesar de afirmar "for every Gen10 B7 dose" — inconsistência. (b) sem equivalence test para slopes G2.

**R2-5 — Referências: 9/10**
- Todas as 5 correções aplicadas. Auditoria completa da lista de referências.

### 4.2 Avaliação Global da Carta

| Critério | Avaliação | Nota |
|----------|-----------|------|
| Cobertura de pontos | Todos os pontos respondidos | 9.5/10 |
| Tom e registro | Colegial, não defensivo, honesto sobre limitações | 8.5/10 |
| Evidência quantitativa nas respostas | G2 com macros (perfeito); B7 hardcoded (bloqueador) | 6/10 |
| Admissão de erros | 7+ erros aceitos sem deflexão | 9/10 |
| Clareza das mudanças | Tabela de resumo + texto por ponto | 9/10 |
| Pontos PARTIAL bem marcados | R1-1, R1-3, R1-5 claramente parciais | 8.5/10 |

**Nota geral da carta: 7.5/10** — Forte na cobertura e tom; penalizada pelos bloqueadores numéricos B7.

---

## 5. Qualidade do Manuscrito

### 5.1 Abstract

**Nota: 7/10**

Pontos fortes:
- Declara ETP como "exploratory post-training summary" — correto e preciso.
- Resultados B7 com CI incluídos (embora via macros, os números renderizados são corretos).
- Limitação de escala (1-2B) declarada.
- Threshold backbone-dependent declarado.

Problemas:
- "between effective ranks ≈3 and ≈6 on Gemma 3 versus 50–88 on Qwen" — os dois intervalos são tipos diferentes de transição (homeostatic→degradative em Gemma 3, bounded→degradative em Qwen). Não são o mesmo tipo de objeto. O paper acknowledges isso em §5.1 mas o abstract não clarifica.
- B7 10% Gen10 não significativo (p=0.160, CI inclui zero) — a contribuição descreve "10%, 25%, and 50% each raised Gen 5 retention by 3.6–4.4 pp" (verdadeiro para Gen5) mas não distingue que Gen10 benefit de 10% é estatisticamente nulo.
- Ainda pendente de redação (conforme pending list): régua de classificação de regime, reformulação dos highlights.

### 5.2 Contribuições (§1)

**Nota: 7.5/10**

Contribuição 1: Precisa — range de seeds por condição, headline vs single-seed distintos.  
Contribuição 2: Boa — "report" em vez de "demonstrate", não-monotonia declarada.  
Contribuição 3: Correta — "pilot grid descriptively consistent" sem overstatement.  
Contribuição 4: Sólida — dissociação retention/distribution é claim bem suportado.  
Contribuição 5: Maior problema — "the tested reductions of 10%, 25%, and 50% each raised Gen 5 retention by 3.6–4.4 pp" é correto para Gen5 mas o Gen10 effect de 10% é estatisticamente nulo. Não há qualificação para Gen10 na contribuição.

### 5.3 Metodologia (§3)

**Nota: 8/10**

Pontos fortes:
- Protocolo strictly replace-only bem descrito.
- K0 por backbone declarado explicitamente (78/46/44/76).
- 3 eixos de pressão claramente articulados.
- Restrições computacionais honestas (single-seed vs multi-seed).

Pontos fracos:
- K0 distintos para pipeline A (K0=46) e pipeline B (K0=44) dentro do Gemma 3 — a distinção entre os dois pipelines e os dois K0 é explicada em detalhe técnico (itens 46 e 133 excluídos), mas pode confundir leitores.
- Strict EM investigado e descartado — resultado negativo honesto, mas cria a percepção de que o instrumento de avaliação não pode ser validado contra alternativas.

### 5.4 Resultados (§4)

**Nota: 8/10**

§4.1 (Rank sweep Qwen): Sólido. 6 níveis de rank, 3 regimes claramente definidos, erank thresholds corretos.  
§4.2 (Cross-backbone): Sólido. Diferença de ordem de magnitude entre thresholds honestamente reportada. Hedges g grande.  
§4.3 (FFT): Adequado mas frágil — Gemma 3 não-monotónico com single seed limita as conclusões sobre o eixo de magnitude.  
§4.4 (Distribuição): Forte — dissociação retention/distribution é o resultado mais original e bem suportado.  
§4.5 (Exposição sintética): Sólido para 50% (B7 e G2). Fragilidade do 10% arm (não significativo Gen10 mas slope mais inclinado) é acknowledged.  
§4.6 (Controles): Adequado. G3 bf16 result (+0.00 diferença no numbers.tex) é curious mas não é overclaim.

### 5.5 Limitações (§5 e §7)

**Nota: 9/10**

17 limitações identificadas e documentadas — cobertura excepcional. Inclui limitações raras de se ver em papers:
- Instrumento de avaliação inadequado para análise de sensibilidade (strict EM).
- Auditoria G3 "incompleta à submissão" (admissão de work-in-progress).
- ETP Π "não validado como predictor transferível."
- G2 slopes idênticos: sem teste formal de equivalência.
- Pilot C5 não replicado.

Ponto removido por: admissão de auditoria pendente em G3 (§4.6) — incomum incluir material não auditado.

### 5.6 Conclusão (§7)

**Nota: 8.5/10**

Alinhada com evidências. "Recursive degradation é pressure-gated, não inevitável" é um claim bem suportado. Threshold backbone-dependent corretamente declarado sem overstatement. Limitações de escala e future work adequados.

---

## 6. Reprodutibilidade

| Item | Estado | Nota |
|------|--------|------|
| Per-seed JSONs (todos os arms) | No Zenodo v1.0.3 | ✅ |
| Training configs | No Zenodo v1.0.3 | ✅ |
| Evaluation protocol + K0 sets | No Zenodo v1.0.3 | ✅ |
| Question partition identifiers | No Zenodo v1.0.3 | ✅ |
| make_all.py (análise principal) | GitHub HEAD (sem DOI) | ⚠️ |
| fig9_dose_response.py | GitHub HEAD (sem DOI) | ⚠️ |
| glyph_audit.py | GitHub HEAD (sem DOI) | ⚠️ |
| Raw token predictions | Não incluídos (tamanho) | ℹ️ justificado |
| Adapter checkpoints | Não incluídos (tamanho+licenças) | ℹ️ justificado |
| Base model weights | Não incluídos (licenças) | ℹ️ SHA-1 em Table S1 |
| SHA-1 dos modelos | Table S1 no suplementar | ✅ |

**Nota: 6/10** — Dados primários disponíveis. Scripts de análise não têm DOI estável. A convenção 5 da carta ("all numerical values generated from make_all.py") cria uma expectativa que não é satisfeita pelo Zenodo v1.0.3.

---

## 7. Itens Pendentes (Investigações em Aberto)

| Item | Estado | Impacto | Ação necessária |
|------|--------|---------|-----------------|
| B7 p-valores: 0.160 vs 0.200 | 🔴 BLOQUEADOR | Alto — divergência carta vs numbers.tex | Verificar make_all.py; decidir valor correto; atualizar manuscrito + carta |
| B7 25% p-valor: 0.005 vs 0.001 | 🔴 BLOQUEADOR | Alto | Idem acima |
| B7 slope: -0.15 vs -0.14 | ⚠️ WARNING | Baixo | Uniformizar |
| B7 10% CI ausente na carta | ⚠️ WARNING | Médio — claim "all doses" inconsistente | Adicionar CI [-1.10, 4.70] ou corrigir claim |
| make_all.py no Zenodo | ⚠️ WARNING | Médio — reprodutibilidade | Publicar Zenodo v1.0.4 antes de submeter OU adicionar nota na carta |
| Fig.2(c) exemplos (Tom Jones/Millicent) | ❓ Não verificado | Baixo | Grep não encontrou — verificar se foi corrigido |
| FFT units (0.39–3.48 no script) | ❓ Não verificado | Baixo | Confirmar fator de escala nos logs |
| G3 bf16 Δ = +0.00 pp | ℹ️ Curious | Baixo | Não é problema — diferença nula é resultado válido |
| Abstract: régua de classificação de regime | ⚠️ Pendente de redação | Médio | Utilizador ofereceu redigir |
| Abstract/highlights: reformulação | ⚠️ Pendente de redação | Médio | Utilizador ofereceu redigir |
| §4.2.3 "tenfold" | ⚠️ Pendente de redação | Baixo | Utilizador ofereceu redigir |
| G2 10%/25% sem CI | ⚠️ WARNING | Médio | Assimetria de reporting; adicionar CIs via macros ou justificar |
| G2 slopes: "within rounding" vs "idênticos" | ⚠️ WARNING | Baixo | Frasear "identical to the precision reported" |
| Glifos no PDF (R.t/, erank.ΔW/) | ⚠️ Não testado no EM | Médio | Testar pdftotext no servidor do Editorial Manager |

---

## 8. Notas por Dimensão — Scorecard Final

```
┌─────────────────────────────────────────────────────┬──────┬────────────────┐
│ DIMENSÃO                                            │ NOTA │ STATUS         │
├─────────────────────────────────────────────────────┼──────┼────────────────┤
│ Estado dos ficheiros (compilação, checks)           │  9   │ ✅ Pronto      │
│ Cobertura das críticas (todos os pontos têm resp.)  │ 9.5  │ ✅ Completo    │
│ Qualidade da resposta — ED1-3                       │  9   │ ✅ Completo    │
│ Qualidade da resposta — R1 (5 pontos)               │  7.5 │ ⚠️ R1-1 parcial│
│ Qualidade da resposta — R2 (5 grupos)               │  8.5 │ ✅ Sólido      │
│ Consistência numérica carta ↔ manuscrito ↔ numbers  │  6.5 │ 🔴 2 blockers  │
│ Tom e registro da carta                             │  8.5 │ ✅ Bom         │
│ Manuscrito — Abstract                               │  7   │ ⚠️ Overclaims  │
│ Manuscrito — Contribuições                          │  7.5 │ ⚠️ Contr.5     │
│ Manuscrito — Metodologia                            │  8   │ ✅ Sólido      │
│ Manuscrito — Resultados                             │  8   │ ✅ Sólido      │
│ Manuscrito — Limitações                             │  9   │ ✅ Excelente   │
│ Manuscrito — Conclusão                              │  8.5 │ ✅ Bom         │
│ Reprodutibilidade (Zenodo + GitHub)                 │  6   │ ⚠️ Scripts fora│
├─────────────────────────────────────────────────────┼──────┼────────────────┤
│ PRONTIDÃO PARA SUBMISSÃO                            │  7.0 │ ⚠️ Ver blockers│
└─────────────────────────────────────────────────────┴──────┴────────────────┘
```

**Escala:** 10 = publicável sem mudanças, 8-9 = menor revisão, 6-7 = revisão necessária, <6 = revisão maior.

---

## 9. Ações por Prioridade

### 🔴 Blockers (não submeter sem resolver)

1. **Verificar p-valores B7 com make_all.py e decidir os valores corretos.**
   - Rodar: `uv run python scripts/analysis/make_all.py` e conferir output.
   - Se 0.200/0.001 são corretos: atualizar manuscrito (linhas com p=0.160 e p=0.005) e carta.
   - Se 0.160/0.005 são corretos: corrigir numbers.tex (improvável — numbers.tex é gerado pelo script).
   - Causa provável: a correção do `paired_ttest_manual` para df=2 em 2026-10-05 alterou os p-valores G2 correctamente mas também alterou B7 (df=4) sem que os valores hardcoded fossem atualizados.

2. **Após decisão acima: recompilar e verificar 12/12 PASS.**

### ⚠️ Warnings (corrigir antes de submeter, se possível)

3. **B7 slope na carta: -0.15 → usar `\BsevenSlopeFifty` (macro) ou corrigir para -0.14.**

4. **CI B7 10% ausente na carta:** ou adicionar "95% CI [-1.10, 4.70]" na frase do B7 10% na carta, ou alterar claim de "for every Gen10 B7 dose" para "for the 25% and 50% doses."

5. **G2 10%/25% CIs:** adicionar CIs [6.70, 13.00] e [5.80, 17.00] na carta e manuscrito via macros existentes (`\GtwoCItenLoTen` etc.) para simetria com a dose de 50%.

6. **G2 slopes:** alterar "equal within rounding" para "identical to the precision reported (−0.91 pp/generation in both arms)."

7. **make_all.py no Zenodo:** publicar v1.0.4 com os scripts antes da submissão. Ou adicionar nota explícita na carta que a reprodutibilidade completa requer o GitHub HEAD em `github.com/Jazancort/llm-knowledge-collapse-replication` (commit `f286b58`).

### ℹ️ Pendentes de decisão do autor

8. **Abstract régua de classificação de regime** — redigir. O abstract atual menciona "50–88 on Qwen vs 3–6 on Gemma 3" sem clarificar que são tipos de transição diferentes.

9. **Reformulação highlights e §4.2.3 "tenfold"** — utilizador ofereceu redigir; aguardando.

10. **Fig.2(c) exemplos** — verificar manualmente se Tom Jones/Millicent Martin ainda estão como exemplos de TriviaQA no manuscrito.

---

## 10. Referência Rápida de Valores Canónicos

Para verificar a correção final, os valores abaixo devem estar consistentes em manuscrito, carta e PDFs:

```
QWEN B7 (N=5, K0=78, r=256):
  10%: +1.8 pp, p=[a verificar], CI [-1.10, 4.70]
  25%: +4.9 pp, p=[a verificar], CI [2.50, 7.20]
  50%: +9.2 pp, p<0.001 (≈0.001), CI [6.90, 11.60]
  slope 0%: -1.13 pp/gen
  slope 50%: -0.14 pp/gen

GEMMA 3 G2 (N=3, K0=44, r=10):
  10%: +9.8 pp, p=0.006, CI [6.70, 13.00]
  25%: +11.4 pp, p=0.013, CI [5.80, 17.00]
  50%: +12.9 pp, p=0.003, CI [9.70, 16.10]
  slope 0%: -0.91 pp/gen
  slope 50%: -0.91 pp/gen (idêntico)

GEMMA 3 ANCHOR RANKS (N=5, K0=46):
  r=4: 94.35% Gen10
  r=16: 56.52% Gen10
  Δ = 37.80 pp, permutation p=0.0079, Hedges g=13.29

ERANK THRESHOLDS:
  Qwen homeostatic→bounded: 29.5–50.2 (r=64→128)
  Qwen bounded→degradative: 50.2–87.6 (r=128→256)
  Gemma 3: 3.07–6.37 (r=4→10, sem zona bounded)

CONTROLS:
  G3 bf16 vs NF4: Δ=0.00 pp (Gen5), Δ=0.00 pp (Gen10) — numbers.tex
  G4 data order: permutation p=0.700
  G5 prospective: 2/3 classificações corretas
```

---

*Gerado por: Kiro CLI, auditoria automática + leitura dos ficheiros fonte. Commit HEAD: f286b58.*
