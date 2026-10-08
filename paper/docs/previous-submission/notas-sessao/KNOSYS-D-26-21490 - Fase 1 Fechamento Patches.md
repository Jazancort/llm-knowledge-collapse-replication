# Fase 1 — Fechamento: decisões aplicadas + patches prontos
## KNOSYS-D-26-21490 | 2026-10-05

> **Status:** patches prontos. Pendências finais: D1 (variante B-01), C2 (diagnóstico no EM), C16 (páginas reais após compilação final), C24 (conferir 3 slopes no numbers.csv).

---

## 1. D1 — English Language Editing

**A carta atual afirma:** "We engaged Elsevier's Author Services English Language Editing service."
Se o serviço não foi contratado, é declaração falsa verificável (a Elsevier emite certificado com número).

| Caminho | Prazo | Ação |
|---|---|---|
| ⭐ 1 — Contratar agora | Pedido hoje → entrega ~14/10 → dentro de 20/10 | Usar variante 1 do B-01 + anexar certificado |
| 2 — Declarar revisão honesta (recomendado se não contratar) | Imediato | Usar variante 2 do B-01 |
| 3 — Não declarar nada | Imediato | Usar variante curta do B-01 |

---

## 2. D2 — Matriz de decisão aplicada

| C# | Pedido explícito do revisor? | Destino | Justificativa |
|---|---|---|---|
| C1 | ✅ R2: "ETP appears in Figure 1…", "KL, JS, coverage appear in Figure 1" | **A** | Pedido direto + painel "100%→~95%" anuncia experimento retirado |
| C2 | ✅ R2: "Equations 1–6 are severely malformed" | **A + B** | A = corrigir de fato; B = reescrever explicação após diagnóstico |
| C3 | ✅ R2: "K0 is used both as a set and as a retention metric", "uses σ_i as both… mathematically incorrect" | **A** | Erro apontado permanece no texto |
| C4 | ✅ R2 item (b) | **A** | Pedido direto |
| C5 | ✅ R2 item (c) | **A** | Pedido direto |
| C6 | ✅ R2 item (e) | **A + B** | A = Contribuição 1; B = citação não literal |
| C7 | ✅ R2 item (f) | **A** | A = Contribuição 2 |
| C8 | ✅ R2: "'Homeo.' is used without definition" | **A + B** | A = Fig. 5; B = local errado na carta |
| C9 | ❌ Erro factual da carta | **B** | Manuscrito cauteloso e correto; carta errou baseline e número |
| C10 | ❌ Erro da carta | **B** | Manuscrito certo; carta subestima o resultado |
| C11 | ✅ R1 Q5 | **A + B** | A = hashes em §3.3 + release D4; B = tabela de status |
| C12 | ✅ R1 Q1 | **A** | §6 não tem protocolo |
| C13 | ❌ Erro da carta | **B** | Shumailov já era [6] |
| C14/C15 | ❌ Erro da carta | **B** | 11 remissões erradas |
| C16 | ❌ Formato da carta | **B** | Trocar por seção + página |
| C17 | ✅ Verificado: são 98 | **B + fix no script** | "112" não existe; usar "15/15 consistency checks" |
| C18 | ✅ Mesma classe de C8 | **A** | Coerência com o pedido |
| C19 | ❌ Overclaim da carta | **B** | Refutável pelo PDF |
| C20 | ✅ Falso positivo | **encerrado** | DOI correto e consistente |
| C21 | ❌ Incoerência da carta | **B** | Padronizar em C1–C5 |
| C22 | ❌ Overclaim da carta | **B** | Três contraexemplos no manuscrito |
| C24 🆕 | ⚠️ Risco novo — 3 slopes | **A** | Ver seção 4 — prioridade máxima |
| C25 🆕 | ✅ R2 item (g) | **A (com ressalva)** | Ver seção 5 |

**Saldo: 11 itens no manuscrito (A) · 11 na carta (B) · 2 encerrados.**

---

## 3. C17 e C20 — encerrados

**C17 ✅ confirmado:** numbers.csv = 98 linhas · numbers.tex = 98 `\newcommand` · a mensagem do `make_all.py` diz "112" (erro no script).
- Patch B-05: substituir "112 canonical numbers" por "every canonical number reported in the paper (15/15 consistency checks pass)".
- Opcional: corrigir `make_all.py` para derivar a contagem de `len(rows)`.

**C20 ✅ falso positivo.** DOI `10.5281/zenodo.23146342` consistente em manuscrito e carta. Encerrado.
Permanece menor: `fig9_dose_response.py` gera a Figura 10 — renomear o script.

**C25 — V4 resultado:** o manuscrito revisado já usa "approximately 5% downsampling effect" em todos os pontos, eliminando a ambiguidade 15%/5%. A carta não deve explicar "15% de exemplos = 5% de tokens" (dado não verificado); deve declarar que a ambiguidade foi removida. Ver patch B-07.

---

## 4. 🔴 C24 — três slopes para a mesma configuração

| Valor | Onde | Conjunto | Interpretação |
|---|---|---|---|
| −1.20 pp/gen | §4.1 | G1+G4, N=6 | "post-adaptation slope (Gen5 to Gen10)" |
| −1.13 pp/gen | §4.5, §5.1 | B7 braço 0%, N=5 | "mean across five seeds, Gen10−Gen5 ÷ 5" |
| −1.28 pp/gen | make_all.py | G1, N=3 | não aparece no manuscrito |

Os três provavelmente são corretos (conjuntos distintos, pipelines distintos). O risco é que um leitor atento veja "Qwen, r=256, Gen5→Gen10" em dois lugares com valores diferentes e registre como inconsistência — exatamente o padrão que o Revisor #2 já encontrou sete vezes.

**Ação A — nota de rodapé em §4.5:**

```latex
\footnote{Three Gen5$\to$Gen10 slopes for Qwen $r=256$ appear in this paper
and refer to distinct seed sets and pipelines, not to repeated measurements
of the same quantity: $-1.20$\,pp/generation for the pooled rank-sweep set
(G1$+$G4, $N=6$; Section~4.1), $-1.28$\,pp/generation for the G1 subset
alone ($N=3$), and $-1.13$\,pp/generation for the 0\% arm of the
pre-registered dose--response experiment B7 ($N=5$, independent pipeline).
All three are reproduced by \texttt{scripts/analysis/make\_all.py}.}
```

**Antes de colar:** confirmar no numbers.csv se cada slope tem macro própria; se não, acrescentar ao `make_all.py`.

---

## 5. D4 — manifesto do release Zenodo v2.0.0

| Diretório | Conteúdo | Tam. aprox. |
|---|---|---|
| `scripts/` | treino, avaliação, análise, figuras, `make_all.py` | < 5 MB |
| `configs/` | configs por run, seeds, máscaras, prompts, chat templates | < 5 MB |
| `results/` | CSV consolidado + vetores booleanos item-level | ~50 MB |
| `generations/` | respostas sintéticas brutas, por geração e condição | ~1–3 GB |
| `figures/` | 11 figuras, 300 dpi, formato não-PDF | ~30 MB |
| `checkpoints/` | adaptadores LoRA, ~70 MB × ~30 runs | ~2 GB |
| `prereg/` | commit a916ebf (B7) + pré-registro G2/G5 | < 1 MB |
| `audit/` | script de auditoria de glifos (C19) + saída | < 1 MB |
| `MANIFEST.md` | checksums SHA-256 de todos os artefatos | — |

**Total estimado: ~3–5 GB** (dentro do limite de 50 GB por registro Zenodo).

**Dois pré-requisitos antes de publicar:**
1. Verificar licença de redistribuição dos adaptadores Gemma (nunca incluir pesos-base).
2. Adicionar hashes de revisão HF Hub em §3.3 e em `configs/checkpoints.yaml` (C11).

---

## 6. Patches — manuscrito (A)

```latex
% ═══ A-01 · C3 · Tabela 1 (tab:notation) — substituir as entradas ═══
$\mathcal{K}_0$ & Set of held-out items answered correctly at generation~0
                  (baseline-correct set) \\
$|\mathcal{K}_0|$ & Cardinality of $\mathcal{K}_0$; protocol-specific:
                  78 (Qwen), 46 (Gemma~3 rank sweep),
                  44 (Gemma~3 dose--response), 76 (Gemma~4 E2B) \\
$R(t)$ & Factual retention at generation~$t$: fraction of
         $\mathcal{K}_0$ items still correct \\
$\sigma_i$ & $i$-th singular value of $\Delta W$ \\
$p_i$ & Normalised singular weight, $p_i=\sigma_i/\sum_j\sigma_j$,
        with $p_i\ge 0$ and $\sum_i p_i=1$ \\
$\mathrm{erank}(\Delta W)$ & Effective rank:
        $\exp\!\left(-\sum_i p_i\log p_i\right)$ \\
$\|\Delta W\|_F$ & Frobenius norm of the composed update,
        averaged across adapted modules \\
$\theta^{(0)}$ & Pretrained backbone weights \\
$\theta^{(t)}$ & Model weights after generation~$t$ of training
        (adapter-augmented under QLoRA; fully updated under FFT) \\
$\Pi$ & Operational pressure index,
        $\Pi=\mathrm{erank}(\Delta W)\cdot(\eta/10^{-5})$;
        exploratory post-training summary \\

% ═══ A-02 · C2+C3 · Equações 1, 2, 3 ═══
% Eq. 1
R(t) = \frac{\bigl|\{\, q\in\mathcal{K}_0 :
        q \text{ answered correctly at generation } t \,\}\bigr|}
       {|\mathcal{K}_0|}

% Eq. 2
\mathrm{erank}(BA) = \exp\!\left(-\sum_i p_i\log p_i\right),
  \qquad p_i=\frac{\sigma_i}{\sum_j\sigma_j}

% Eq. 3
d(t) = \frac{1}{|\theta|}\sum_i
       \bigl|\theta_i^{(t)}-\theta_i^{(0)}\bigr|

% ═══ A-03 · C1 · Figura 1 — quatro correções ═══
% painel 6: "ETP threshold identification"
%        → "Pressure–regime mapping and threshold localisation"
% painel 4: "Distribution shift — KL, JS, coverage"
%        → "Distribution shift — Distinct-n, MTLD, stopword ratio"
% painel 3: "Exposure — 100% → ~95% synthetic"
%        → "Exposure — 0 / 10 / 25 / 50% removal"
% legenda: harmonizar "five axes" com os eixos do diagrama

% ═══ A-04 · C6 · Contribuição 1 ═══
% DE:   "...confirmed across three to five independent seeds per condition."
% PARA: "...replicated across three to five independent seeds at the
%        headline ranks (six for the pooled r=256 estimate); intermediate
%        ranks are single-seed and reported as descriptive."

% ═══ A-05 · C7 · Contribuição 2 ═══
% DE:   "...confirming that the phenomenon responds to perturbation
%        magnitude rather than being specific to low-rank adaptation."
% PARA: "...consistent with the phenomenon responding to perturbation
%        magnitude rather than being specific to low-rank adaptation;
%        the Gemma~3 sweep is single-seed and non-monotonic at the two
%        higher learning rates, and is therefore descriptive."

% ═══ A-06 · C4 · r=128 ═══
% §5.3: "phenotypes emerge above the pressure threshold. At intermediate
%        capacity (r=128)"
%     → "phenotypes emerge at and above the transition zone. In the
%        transition-zone configuration (r=128)"
% §4.4: "above-threshold regimes"
%     → "transition-zone and degradative regimes"

% ═══ A-07 · C5 · "boundary configuration" ═══
% §5.4: "boundary configurations are sensitive to graded changes"
%     → "the lowest-pressure degradative configuration tested is
%        sensitive to graded changes"
% §4.4: "at the regime boundary"
%     → "in the lowest-pressure degradative configuration tested"

% ═══ A-08 · C8+C18 · Abreviações ═══
% Fig. 5 (eixo/legenda): "Homeo." → "Homeostatic"; "Degrad." → "Degradative"
% Tabela 4: "Degrad." → "Degradative"
% Verificar também Figs. 4 e 11

% ═══ A-09 · C11 · §3.3 — acrescentar após lista de backbones ═══
All three backbones were obtained from the Hugging Face Hub at fixed
revisions; the exact repository identifiers and commit hashes are listed
in Table~S1 and in \texttt{configs/checkpoints.yaml} of the replication
package, so that the identical weights can be retrieved.

% ═══ A-10 · C12 · §6 — protocolo prospectivo (inserir) ═══
A prospective calibration of effective training pressure on an unseen
backbone would require the following protocol, which we specify here as
a concrete target for future work rather than as a result of the present
study. (i)~\textbf{Pilot sweep:} run two nominal ranks spanning roughly
one order of magnitude (e.g.\ $r=4$ and $r=64$) for five recursive
generations with a single seed, recording $\mathrm{erank}(\Delta W)$
per generation. (ii)~\textbf{Backbone-local calibration:} fit the
regime boundary as the interval between the highest pilot configuration
whose Gen1--Gen5 retention slope is statistically indistinguishable from
zero and the lowest whose slope is negative. (iii)~\textbf{Pre-specification:}
register, before any further run, two configurations on opposite sides
of the calibrated interval, together with the outcome criterion
(Gen5$\to$Gen10 retention slope) and the decision rule.
(iv)~\textbf{Held-out evaluation:} execute both configurations to Gen10
with at least three seeds, without refitting the calibration to the
observed outcomes. (v)~\textbf{Reporting:} report the pre-registered
prediction, the observed classification, and any discrepancy,
irrespective of direction. Steps~(i)--(ii) cost approximately two pilot
runs per backbone; the present study performed neither~(iii)--(v) on
an unseen backbone nor the cross-dataset variant of the same design.

% ═══ A-11 · C24 · §4.5 — nota de rodapé (confirmar slopes no CSV antes) ═══
\footnote{Three Gen5$\to$Gen10 slopes for Qwen $r=256$ appear in this
paper and refer to distinct seed sets and pipelines:
$-1.20$\,pp/generation for the pooled rank-sweep set
(G1$+$G4, $N=6$; Section~\ref{sec:res_main}),
$-1.28$\,pp/generation for the G1 subset alone ($N=3$),
and $-1.13$\,pp/generation for the 0\% arm of the pre-registered
dose--response experiment B7 ($N=5$, independent pipeline).
All three are reproduced by \texttt{scripts/analysis/make\_all.py}.}
```

---

## 7. Patches — carta (B)

```latex
% ═══ B-01 · D1 · Resposta ao Editor ═══

% ── Variante 1: serviço Elsevier contratado ──
\arhead{Author action:}
The manuscript was professionally language-edited through Elsevier's
Author Services English Language Editing service; the editing
certificate is attached to this submission. In addition, every
reviewer comment below is addressed by a dedicated revision, with the
corresponding section and page of the revised manuscript cited.

% ── Variante 2: revisão própria honesta (RECOMENDADA se não contratar) ──
\arhead{Author action:}
The manuscript underwent a complete language revision prior to
resubmission, covering grammar, terminology consistency, and the
removal of residual non-English constructions. Terminology was
standardised throughout (Homeostatic / Bounded / Degradative;
``effective training pressure'' written in full at every occurrence),
and all abbreviations are now expanded at first use. Should the Editor
consider a further round of professional language editing necessary,
we will gladly commission Elsevier's Author Services before
acceptance. Every reviewer comment below is addressed by a dedicated
revision, with the corresponding section and page cited.

% ═══ B-02 · C9 · Quantização (substitui o parágrafo inteiro) ═══
For quantization: all primary QLoRA experiments load the base model in
4-bit NormalFloat (NF4) with adapters trained in bfloat16. Ablation G3
re-runs the identical protocol in bf16 with no base-weight
quantization, using three matched seeds (15/137/256) at each of $r=16$
and $r=256$. At $r=16$, bf16 returns Gen10 $=$ 97.4\% (76/78 in every
seed), identical to the three-seed NF4 value reported in Section~4.3.1
of the revised manuscript. At $r=256$, bf16 returns the same per-seed
item counts as the NF4 G1 set ([61, 63, 61]/78; 79.1\%). The regime
classification is therefore invariant to precision at both ranks. We
state this deliberately as agreement between classifications rather
than as a causal conclusion about quantization: because the per-seed
counts coincide exactly, we are completing a run-level provenance and
item-level audit before interpreting that agreement as evidence that
quantization has no effect (Section~4.6). The audit outcome will be
reported in the final version.

% ═══ B-03 · C10 · G5 ═══
The pre-registered G5 probe (three single-seed cells on Qwen) provides
limited exploratory evidence: Gen5 retention was ordered in the
predicted direction across all three cells (96.2\%, 89.7\%, and 85.9\%
for the low-, intermediate-, and high-pressure cells), but one of the
three pre-specified regime classifications was not met --- the
high-pressure cell was predicted Degradative and returned Bounded. No
$\Pi$ threshold is reported for G5, because the pre-specification fixed
nominal rank and learning rate rather than a threshold on $\Pi$; nor
does G5 test an unseen backbone or dataset.

% ═══ B-04 · C22 · Capa, item (3) ═══
(3)~seed-level inferential statistics for every comparison in which
independent training runs are available: exact permutation and
sign-flip tests for the rank contrasts (G3 on Qwen; anchor ranks on
Gemma~3) and paired $t$-tests with 95\,\% confidence intervals for all
dose levels of the two pre-registered dose--response experiments
(B7, G2). Comparisons that remain single-seed or non-exchangeable are
reported as descriptive and labelled as such;

% ═══ B-05 · C17 · R1.5 ═══
% DE:   "reproduces all 112 canonical numbers (15/15 checks pass)"
% PARA: "reproduces every canonical number reported in the paper
%        (15/15 consistency checks pass)"

% ═══ B-06 · C19 · R2.2, Author action — substituir a frase final ═══
We additionally ran an automated glyph audit over the compiled PDF,
checking every equation, table cell, and caption against the LaTeX
source; the audit script and its output are included in the
replication package (\texttt{audit/}).

% ═══ B-07 · C25 · R2.3 item (g) ═══
The reviewer is correct that the original submission described the
same intervention inconsistently. In the revised manuscript the
ambiguity has been removed rather than reconciled: the C1--C5
exploratory pilot is no longer used for any primary estimate, and all
exposure doses are now specified exclusively as fractions of training
\emph{examples} removed (0\%, 10\%, 25\%, 50\%) in both pre-registered
experiments. The pilot results, including the original dose description,
are archived in the replication package for transparency.

% ═══ B-08 · C13 · R2.5 ═══
% DE:   "...is added as the primary citation for the model-collapse
%        phenomenon."
% PARA: "...[6] (Nature) has been reinforced as the primary
%        peer-reviewed anchor for the model-collapse phenomenon, so
%        that no quantitative claim in the paper rests on [7] alone."

% ═══ B-09 · C21 · padronizar em TODA a carta ═══
% "C3/C5" (capa) e "C2--C5" (R1.4) → "C1--C5"
% descrever o problema como "the C1-versus-C3/C5 comparisons"

% ═══ B-10 · C14/C15/C16 · remissões — convenção ═══
% No \rquote: preservar numeração ORIGINAL do revisor, sem alterar.
% No Author response/action: numeração REVISADA + seção + PÁGINA.
% Na primeira ocorrência de cada bloco, declarar o mapeamento:
%   "Table 7 of the original submission (now Table 9, p. 27)"
%
% Tabela de conversão:
%   controles      Tab. 2  → Tab. 3  (p. 26)
%   rank × LR      Tab. 7  → Tab. 9  (p. 27)
%   Gemma 3 ranks  Tab. 4  → Tab. 6  (p. 27)
%   regimes        Tab. 2  → Tab. 4  (p. 26)
%   normalizações  Tab. 6  → Tab. 13 (p. 28)
%   G5             §4.4    → §4.6    (p. 17)
%   G3 pareado     §4.2    → §4.1    (p. 10)
%   Gemma 3        §4.3.1  → §4.2.1  (p. 11)
%   K0             §3.6    → §3.2    (p. 5)
%   avaliação      §3.1    → §3.2    (p. 5)
%   repositório    §A.1    → Apêndice A (p. 22)
```

---

## 8. Estado da Fase 1

| Status | Itens |
|---|---|
| ✅ Encerrados | C17 (98, não 112) · C20 (DOI correto) |
| ✅ Com patch pronto | C1, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C17, C18, C19, C21, C22, C24, C25 |
| ⏳ Depende de execução | C2 — diagnosticar Unicode cru + validar no PDF do Editorial Manager |
| ⏳ Depende de C2 | C16 — aplicar páginas reais após compilação final |
| ⏳ Depende de D1 | B-01 — escolher variante (contratar serviço ou declarar revisão honesta) |

---

## 9. Três pendências finais

1. **D1** — caminho 1 (contratar hoje) ou variante 2 do B-01? Se caminho 1, o pedido precisa sair em 24 h.
2. **C24** — confirmar no `numbers.csv` se as três slopes (−1.13 / −1.20 / −1.28) têm macro própria; se não, acrescentar ao `make_all.py` antes de colar a nota de rodapé A-11.
3. **C2** — rodar o grep de Unicode cru (`rg -n '[×≈−–—∈≥≤σΔΠηθ]' *.tex`), recompilar com fontes embutidas, subir no Editorial Manager e baixar o PDF gerado por ele.
