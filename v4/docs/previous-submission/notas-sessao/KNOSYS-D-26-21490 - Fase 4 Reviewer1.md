# Fase 4 — Correções Críticas + Revisor #1
## KNOSYS-D-26-21490 | 2026-10-05

> **Status:** R1-1, R1-2, R1-3, R1-5 prontos. R1-4 bloqueado até C24 ser resolvido. B-06c pronto mas condicionado ao teste no EM.

---

## Correção 1 — 🔴 C24: o problema não é o slope, é o braço 0% inteiro

### O diagnóstico

Os dados B7 hardcoded em `make_all.py` L86-96 divergem do manuscrito **somente na linha-base**:

| Dose | Gen10 script | Gen10 manuscrito | Status |
|---|---|---|---|
| **0%** | **79.14%** | **79.7%** | ❌ |
| 10% | 81.56% | 81.5% | ✅ |
| 25% | 84.62% | 84.6% | ✅ |
| 50% | 88.98% | 89.0% | ✅ |

Consequência nos Δ Gen10 calculados contra a linha-base:

| Dose | Δ manuscrito | Δ com dados do script |
|---|---|---|
| 10% | +1.8 pp | +2.4 pp |
| 25% | +4.9 pp | +5.5 pp |
| 50% | +9.2 pp | +9.8 pp |

E Δ Gen5 sobe ~1.44 pp em todas as doses: +3.6/+3.8/+4.4 → +5.0/+5.2/+5.8.

Esses são os números da conversa inicial que foram descartados como "confusão de conjuntos" na Fase 1. Não era confusão — são duas análises do B7 com dados divergentes no braço 0%.

### O que isso significa para o hardcode B7_SLOPE0 = −1.13

O hardcode **resolve o sintoma e esconde a causa**. O script emite `\BsevenSlopeZero = -1.13` como se fosse auditável, mas os 8 números que dependem do braço 0% (4 Δ Gen5 + 4 Δ Gen10) saem errados. A promessa "reproduces all canonical numbers" falha exatamente no experimento central de R1.4.

### Patch B-05b — substitui B-05 da Fase 1

```latex
% DE:
% "reproduces every canonical number reported in the paper
%  (15/15 consistency checks pass)"

% PARA (usar até C24 ser resolvido):
"regenerates the aggregated results, tables, and figures reported in
 the paper from the archived per-seed data, and reports a set of
 internal consistency checks on the values it produces"
```

### Decisões possíveis após localizar a fonte dos dados canônicos

| Decisão | Consequência |
|---|---|
| **A** O manuscrito está certo → corrigir os dados em `make_all.py` | Tabela 10 e todos os Δ permanecem |
| **B** O script está certo → corrigir a Tabela 10 | Δ Gen10 50% vira +9.8 pp; Δ Gen5 viram +5.0/+5.2/+5.8; slope 0% vira −0.96; Abstract, §4.5, §5.1, §5.4, Conclusão e Highlights mudam |
| **C** Nenhum dos dois é rastreável | Rerodar o braço 0% |

### Diagnóstico para rodar agora

```python
import csv, glob, os
base = r"...\v4"

# 1. Procurar 85.4 e 79.7 em qualquer resultado
for f in glob.glob(base + r"\**\*.csv", recursive=True) + \
         glob.glob(base + r"\**\*.json", recursive=True):
    try:
        txt = open(f, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    if "85.4" in txt and "79.7" in txt:
        print("CANDIDATO:", f)

# 2. Procurar o script que gerou a Tabela 10
for f in glob.glob(base + r"\**\*.py", recursive=True) + \
         glob.glob(base + r"\**\*.ipynb", recursive=True):
    txt = open(f, encoding="utf-8", errors="replace").read()
    if "85.4" in txt or "table10" in txt.lower() or "tab:dose" in txt.lower():
        print("SCRIPT CANDIDATO:", f)
```

> **Observação:** 85.4% de 78 = 66.6 → provavelmente 67/78 = 85.9 ou 66/78 = 84.6. Os valores 85.4 e 79.7 são médias de contagens por semente. Procurar as contagens raw por semente compatíveis com IC [6.9, 11.6] via engenharia reversa.

### Ações bloqueadas até C24 ser resolvido

- Nota de rodapé A-11 (afirma que os 3 slopes são reproduzidos pelo script)
- R1-4 (usa `\BsevenSlopeZero`, `\BsevenSlopeFifty`, `\GtwoDeltatenFifty`)
- Promessa de reprodutibilidade integral em R1-5 (usar B-05b enquanto isso)

---

## Correção 2 — C2: diagnóstico final corrigido

### Resultado verificado

- `pdffonts`: todas as 30 fontes com `emb=yes, sub=yes, uni=yes`
- Hipótese "XeLaTeX + T1/lmodern sem ToUnicode" está **refutada**
- Fonte LaTeX: 0 Unicode cru problemático (1 `←` em comentário, inócuo)
- **Causa real: re-destilação pelo Editorial Manager** não preserva Unicode maps de fontes Type 1C Custom

### Mitigação prática

```latex
% Camada 1: compilar com LuaLaTeX + fontes OpenType
\usepackage{fontspec}
\setmainfont{Latin Modern Roman}[Ligatures=TeX]
\usepackage{unicode-math}
\setmathfont{Latin Modern Math}
% lualatex → bibtex → lualatex → lualatex
% pdffonts deve mostrar "CID TrueType" ou "CID Type 0C", não "Type 1C Custom"
```

```bash
# Camada 2: pré-destilar antes de subir
gs -dPDFA=2 -dBATCH -dNOPAUSE -dNOOUTERSAVE \
   -sColorConversionStrategy=UseDeviceIndependentColor \
   -sDEVICE=pdfwrite -dPDFACompatibilityPolicy=1 \
   -sOutputFile=manuscript-submit.pdf manuscript.pdf

pdffonts manuscript-submit.pdf      # conferir uni=yes
pdftotext manuscript-submit.pdf - | rg 'í|İ|Ë|ˆ|˜|⊙'
```

### B-06c — substitui B-06b (condicionado ao teste no EM)

```latex
The reviewer is correct that Equations~1--6 and several table cells were
unreadable in the submitted PDF, and we apologise for it. Rather than
re-render the document and hope for a different outcome, we traced the
fault. Two audits establish where it does \emph{not} originate. First,
an automated scan of the complete LaTeX source returns a single
non-ASCII character, inside a comment: no mathematical symbol is
encoded as raw Unicode, and the source is syntactically correct as
submitted. Second, \texttt{pdffonts} confirms that every font in our
locally compiled PDF is embedded with a complete \texttt{ToUnicode}
mapping, and text extraction from that file reproduces the equations
correctly.

The corruption is therefore introduced when the submission system
re-processes the uploaded file. The embedded fonts use a custom
encoding, and the re-distillation step does not preserve their Unicode
mappings; minus signs, multiplication signs, set-membership symbols,
and percent signs are drawn correctly on the page but map to unrelated
code points on extraction. This accounts for the specific form of the
corruption the reviewer observed (\texttt{Retention.t /},
\texttt{5İ10\^{}6}, \texttt{r~E~4,10,12,14,16}) rather than missing
or blank glyphs.

For this revision we have changed the font pipeline so that the
document no longer relies on custom-encoded subsets, and we verified
the result at the point where the fault appears: the file was uploaded,
the system-generated PDF was retrieved, and its extracted text was
compared against the LaTeX source equation by equation, table cell by
table cell. The audit script and its output are included in the
replication package. Independently of the encoding, Equations~1, 2,
and 3 were rewritten with explicit notation consistent with Table~1,
and all garbled set expressions are now proper set notation.
```

> ⚠️ O terceiro parágrafo afirma que o teste no EM foi feito. **Não colar antes de fazê-lo.** Se o teste não for possível antes do prazo, substituir por: "and we will verify the system-generated PDF at upload; should any residual artefact remain, we ask the Editor to let us supply a pre-flattened file."

---

## FASE 4 — Revisor #1 (R1-1 a R1-5)

> R1-0 (avaliação geral) foi entregue na Fase 2. Padrão E2: comentário embutido + resposta argumentada + ação com citação literal + localização por seção e página.

---

### R1-1 · Calibração prospectiva

```latex
\rconcern{Reviewer \#1, Concern \#1}{Quantitative calibration and
prospective testing}{How can effective training pressure be
quantitatively calibrated and prospectively tested on an unseen
backbone or dataset?}

\arhead{Author response:}
We cannot answer this question affirmatively from the present
experiments, and the revision says so rather than arguing around it. No
transferable scalar predictor is derived, and no prospective threshold
is established for an unseen backbone or dataset. Three things changed
instead.

First, the framework is reframed. Effective training pressure is now
introduced as an organising framework for three independently
manipulated variables, not as a predictor, and the manuscript
distinguishes the variables that are fixed before training from the
quantities measured after it. The operational index
$\Pi = \mathrm{erank}(\Delta W)\cdot(\eta/10^{-5})$ is labelled an
exploratory post-training summary at every occurrence, and is never used
as a decision rule.

Second, we state what a prospective test would require, concretely
enough to be executed. A calibration rule and an outcome criterion must
be fixed before the held-out backbone is examined; configurations must
be selected on both sides of the predicted boundary; and they must be
evaluated without refitting the rule to the observed outcomes. Section~6
now specifies this as a five-step protocol, together with its
approximate cost, so that it is a target rather than an aspiration.

Third, we report the one prospective element the study does contain,
without inflating it. The pre-registered G5 probe fixed three
rank$\times$learning-rate cells on Qwen before execution. Gen5 retention
came out in the predicted order across all three cells (96.2\,\%,
89.7\,\%, 85.9\,\%), but one of the three pre-specified regime
classifications was not met: the high-pressure cell was predicted
Degradative and returned Bounded. No $\Pi$ threshold is reported for G5,
because the pre-specification fixed nominal rank and learning rate rather
than a threshold on $\Pi$. G5 also does not test an unseen backbone or
dataset. Prospective calibration remains future work, and is now listed
as such.

\arhead{Author action:}
\begin{enumerate}[leftmargin=1.4em,itemsep=0.3em]
\item Section~3.5 (p.~8) was rewritten to introduce the framework
      without predictive claims, and to separate the two classes of
      variable: \newtext{We distinguish ETP-design variables, which are
      fixed before training and directly manipulated in our factorial
      design (nominal adapter rank $r$, learning rate $\eta$, number of
      training steps, and synthetic-data dose fraction), from
      ETP-observed variables, which are measured after training as
      diagnostic proxies.} The index is qualified in the same
      subsection: \newtext{This is an exploratory post-training summary
      and is not used as a validated quantitative threshold.}
\item Section~6 (p.~22) gained an explicit five-step calibration
      protocol, closing with: \newtext{the present study performed
      neither the pre-specification nor the held-out evaluation on an
      unseen backbone, nor the cross-dataset variant of the same design.}
\item Section~4.6 (p.~17) reports G5 with the classification outcome
      stated plainly: \newtext{One of the three pre-specified regime
      classifications was not met; G5 is therefore exploratory evidence
      for the ordering, not a confirmatory test of the full
      classification scheme.}
\end{enumerate}

\msloc{§3.5, p.~8; §4.6, p.~17; §6, p.~22; Table~1, p.~25.}
```

---

### R1-2 · Separação de confusores

```latex
\rconcern{Reviewer \#1, Concern \#2}{Separating quantization, optimizer
state, data order, and model-specific dynamics}{How are quantization,
optimizer state, data order, and model-specific dynamics separated from
the claimed pressure effects?}

\arhead{Author response:}
Each of the four sources is now mapped to a specific control, and the
inventory is given as a table rather than left implicit in the text
(Table~3, p.~26).

\emph{Quantization.} Ablation G3 re-runs the identical protocol in bf16
with no base-weight quantization, using three matched seeds at each of
$r=16$ and $r=256$. At $r=16$, bf16 returns Gen10 $=$ 97.4\,\% (76/78
in every seed), identical to the three-seed NF4 value in Section~4.3.1.
At $r=256$, bf16 returns the same per-seed item counts as the NF4 G1
set ([61,\,63,\,61]/78). The regime classification is invariant to
precision at both ranks. We state this as agreement between
classifications rather than as a causal conclusion: because the
per-seed counts coincide exactly, we are completing a provenance audit
before interpreting that agreement as evidence that quantization has no
effect.

\emph{Optimizer state.} A fresh optimizer is instantiated at every
generation; no momentum or adaptive-rate state is carried across
generations. This is held constant in every condition.

\emph{Data order.} Ablation G4 replicates Qwen $r=256$ with three
independent shuffle seeds (42/101/202). A bilateral permutation test
against G1 gives $p=0.70$. Because G4 varies seed and data order
together, this does not isolate ordering; it establishes that the
combined variance is indistinguishable from the seed-to-seed variance
already present in G1. Pooling yields the six-seed Gen10 estimate of
79.7\,\%\,$\pm$\,1.7\,pp.

\emph{Model-specific dynamics.} This is the one source we cannot
eliminate, and the revision treats it as a finding. The regime boundary
is backbone-dependent by roughly an order of magnitude, and five
architectural normalisations (by hidden dimension, its square root,
layer count, attention heads, and key--value heads) all fail to align
the thresholds (Table~13, p.~28).

The reviewer's question also prompted a distinction left implicit: effective
rank and weight drift are not available before training and cannot serve
as pre-specified predictors; they are post-hoc diagnostics. The revision
separates them from the design variables throughout.

Finally, the 17.7\,pp gap between the three-seed $r=16$ condition and
the six-seed $r=256$ estimate is descriptive, because the two groups
differ in rank, precision protocol, and seed assignment. The clean
contrast is G3 paired design --- same seeds, same precision, rank the
only variable --- giving per-seed Gen10 differences of $+15$, $+13$,
$+15$ out of 78 (mean $+18.4$\,pp), exact sign test $p=0.25$ at $N=3$.
We report both, labelled accordingly.

\arhead{Author action:}
\begin{enumerate}[leftmargin=1.4em,itemsep=0.3em]
\item Section~3.9 (p.~10) and Table~3 (p.~26) were added. The optimizer
      entry reads \newtext{Held constant: fresh optimizer at every
      generation (no state carryover)}; the pipeline entry discloses a
      limitation: \newtext{Per-execution commit traceability was not
      systematically recorded; the git log provides version history but
      does not identify the commit used in each individual run.}
\item Section~4.6 (p.~17) reports G3 and G4 with their caveats, G3
      including: \newtext{run-level provenance and item-level outputs are
      audited separately before interpreting this agreement as evidence
      about quantization.}
\item Section~4.1 (p.~10) separates the two Qwen contrasts:
      \newtext{The mean within-protocol gap is 18.4\,pp; with $N=3$
      pairs, the exact two-sided sign test gives $p=0.25$, so this
      result is descriptive rather than confirmatory.}
\item Section~3.5 (p.~8) and Table~1 (p.~25) introduce the
      design/observed distinction; Table~13 (p.~28) retains the five
      failed normalisations as a reported negative result.
\end{enumerate}

\msloc{§3.5, p.~8; §3.9 and Table~3, pp.~10 and 26; §4.1, p.~10;
§4.6, p.~17; Table~13, p.~28.}
```

---

### R1-3 · Validade externa

```latex
\rconcern{Reviewer \#1, Concern \#3}{Longer answers, multi-hop
questions, other domains, larger evaluation sets}{Do the conclusions
hold for longer answers, multi-hop questions, other domains, and larger
factual evaluation sets?}

\arhead{Author response:}
We did not test any of the four extensions, and we do not claim the
conclusions hold for them. What we can do --- and have done --- is
remove the most plausible artefact the question implies, and state the
scope restriction where a reader will encounter it.

The concern that longer answers inflate retention is specific and
testable with the data already collected. Our bidirectional substring
match is permissive by construction: a verbose response is more likely
to contain a short alias by chance. This is not hypothetical: $r=128$
on Qwen produces roughly seven-word answers against roughly two words
at $r=16$. We therefore re-scored every saved prediction under a strict
exact-match criterion. Absolute retention is lower throughout, but the
direction of every regime classification is unchanged. The re-scoring is
in supplementary Table~S2 and discussed in Section~6.

On the remaining three extensions we are explicit. TriviaQA was chosen
to isolate factual retention from reasoning and stylistic confounds.
Short answers minimise format-dependent evaluation noise; the matching
criterion is robust to verbosity changes. The cost is that the findings
may not transfer to long-form generation, multi-hop reasoning,
open-ended dialogue, or code synthesis. This is now the second
limitation in Section~6.

On evaluation-set size, the original submission stated incorrectly that
enlarging the evaluation set would alter the training-data composition.
It would not: the held-out set is disjoint from the 2,000-question
training stream and could be enlarged without touching it. The actual
constraint is computational, and we say so.

\arhead{Author action:}
\begin{enumerate}[leftmargin=1.4em,itemsep=0.3em]
\item Strict exact-match re-scoring performed and reported in
      supplementary Table~S2; outcome stated in Section~6 (p.~23):
      \newtext{the direction of all regime classifications is unchanged,
      but absolute retention levels are lower under the strict scorer.}
\item Section~3.2 (p.~5) states the inflation risk at metric definition:
      \newtext{Configurations that produce longer responses (notably
      $r=128$ on Qwen) may have their retention scores modestly inflated
      relative to a strict exact-match scorer.}
\item Section~6 (p.~21) states the domain restriction:
      \newtext{The findings may not extend to long-form generation,
      open-ended dialogue, code synthesis, or other domains where output
      structure and evaluation criteria differ substantially.}
\item The evaluation-set-size justification was corrected to cite the
      computational constraint, not training-data composition.
\end{enumerate}

\msloc{§3.2, p.~5; §6, pp.~21 and 23; supplementary Table~S2.}
```

---

### R1-4 · Redução de exposição ⚠️ BLOQUEADO até C24

```latex
% ⚠️ Este item usa \BsevenSlopeZero, \BsevenSlopeFifty, \GtwoDeltatenFifty
% Não congelar antes de resolver a proveniência do braço 0%

\rconcern{Reviewer \#1, Concern \#4}{Why the exposure reduction
stabilises Qwen but not Gemma~3}{Why does the five-percent exposure
reduction stabilize Qwen but not Gemma~3, and does this generalize
across ranks and seeds?}

\arhead{Author response:}
This question led us to audit the provenance of the experiment it refers
to, and the premise of the question did not survive the audit.

\emph{The original result was an artefact.} The submitted manuscript
reported that removing approximately five percent of synthetic training
examples raised retention by $+9.0$ and $+9.4$\,pp in conditions C3 and
C5. On re-examination, C1 and the intervention arms were produced by
different evaluation pipelines. When C1 and C5 are re-run under one
pipeline with paired seeds, the effect of that intervention is
$+1.9$\,pp at $n=3$, not distinguishable from zero. The asymmetry the
reviewer asks about was a comparison between pipelines, not between
backbones. The C1--C5 pilot is archived and excluded from every effect
estimate.

\emph{What replaces it.} Two pre-registered dose--response experiments,
one per backbone, with multiple paired seeds at four dose levels
(0\,\%, 10\,\%, 25\,\%, 50\,\% of training examples removed). The 0\,\%
arm is a within-pipeline baseline, eliminating the class of confound
that produced the original error. On Qwen $r=256$ (five paired seeds;
protocol registered as \texttt{a916ebf}), the Gen~10 benefit is
dose-graded, and at the highest dose the Gen~5$\to$10 slope falls from
\BsevenSlopeZero\,pp/generation to \BsevenSlopeFifty\,pp/generation.
On Gemma~3 $r=10$ (three paired seeds), all three doses raise Gen~10
retention ($+9.8$, $+11.4$, and \GtwoDeltatenFifty\,pp) but the slope
in the 50\,\% arm equals that of the 0\,\% arm within rounding.

\emph{The revised answer.} Under paired evaluation both backbones
respond to exposure reduction, but differently: on Qwen the rate of
progressive loss is attenuated; on Gemma~3 the retention level improves
without a reduction in that rate. We report this asymmetry as an
observation and do not explain it. The steps-matched control was
inconclusive at $n=3$. Generalisation across ranks is untested, and is
now stated as a limitation.

\arhead{Author action:}
\begin{enumerate}[leftmargin=1.4em,itemsep=0.3em]
\item Section~3.7 (p.~9) documents the pilot's exclusion:
      \newtext{When C1 and C5 are re-run under an identical pipeline and
      paired seeds, the approximate 5\,\% downsampling effect is
      $+1.9$\,pp ($n=3$), not statistically distinguishable from zero.
      The pilot results are archived; they are not used in the primary
      effect estimates below.}
\item Section~4.5 (pp.~16--17) was rewritten around the two
      pre-registered experiments, with paired $t$-tests and 95\,\% CIs
      at every dose; Table~10 (p.~27) reports per-dose results.
\item The Gemma~3 asymmetry is stated in Section~4.5 (p.~17):
      \newtext{near-arrest of progressive loss was not observed for G2
      at this dose; the exposure effect manifested as a retention gain,
      not a slope reduction.}
\item Figure~9 (p.~25) retains the pilot for transparency:
      \newtext{These results use a different evaluation pipeline from the
      primary dose--response experiments and are not used in the primary
      effect estimates.}
\item Section~6 (p.~22) states the untested ranks and unresolved
      mechanism: \newtext{The steps-matched control was inconclusive,
      so the relative contribution of each mechanism remains
      unresolved.}
\end{enumerate}

\msloc{§3.7, p.~9; §4.5, pp.~16--17; Table~10, p.~27; Figure~9, p.~25;
§6, pp.~22--23; replication package (C1--C5 archived).}
```

---

### R1-5 · Pacote de reprodução

```latex
\rconcern{Reviewer \#1, Concern \#5}{Code, checkpoints, prompts, seeds,
raw outputs}{What complete code, checkpoints, prompts, seeds, and raw
outputs will support independent reproduction?}

\arhead{Author response:}
The reviewer names five classes of artefact. The original deposit
contained scripts and aggregated results but not item-level outputs or
trained adapters. The deposit has been extended accordingly.

\renewcommand{\arraystretch}{1.2}
\begin{tabular}{@{}L{3.6cm}L{2.2cm}L{7.6cm}@{}}
\toprule
\rowcolor{hdrgray}\textbf{Artefact} & \textbf{Status} &
\textbf{Content} \\
\midrule
Code & Deposited &
Training, synthetic-data generation, evaluation, analysis, and
figure-generation scripts, with the pinned software environment \\
Checkpoints & Deposited &
Base-model repository identifiers with revision hashes (Table~S1) so
that identical weights can be retrieved; trained LoRA adapters for
all reported runs \\
Prompts & Deposited &
Chat templates per backbone, system-message formats that define each
$\mathcal{K}_0$ set, and decoding configurations for generation and
evaluation \\
Seeds & Deposited &
Per-run training seeds, corpus shuffle seed, data-order masks of the G4
control, and downsampling masks of every dose arm \\
Raw outputs & Deposited &
Per-seed per-generation retention counts, item-level boolean correctness
vectors over $\mathcal{K}_0$, and raw synthetic generations for all
reported conditions \\
\bottomrule
\end{tabular}

\medskip\noindent
Two points of transparency. Base-model weights are not redistributed;
revision hashes in Table~S1 are what make the checkpoints reproducible.
Per-execution commit traceability was not systematically recorded during
the original campaign: the repository history is available, but we
cannot identify the exact commit used for each individual run. We state
this in Table~3 rather than leave it to be discovered.

\arhead{Author action:}
\begin{enumerate}[leftmargin=1.4em,itemsep=0.3em]
\item Appendix~A (p.~22) was expanded to enumerate the deposit contents
      by class, to name the scripts that regenerate each table and
      figure, and to state what is \emph{not} included.
\item Section~3.3 (p.~6) now specifies retrieval conditions with
      repository identifiers and revision hashes in supplementary
      Table~S1; hardware description was corrected.
\item Section~3.2 (p.~5) documents the two distinct $\mathcal{K}_0$
      sets on Gemma~3: \newtext{The 44-item set is a strict subset of
      the 46-item set: the two additional items were answered correctly
      under one prompt template but not under the other.}
\item A new version of the replication package was deposited with a
      manifest giving SHA-256 checksums for every artefact.
\end{enumerate}

\msloc{§3.2, p.~5; §3.3, p.~6; Table~3, p.~26; Appendix~A, p.~22;
supplementary Table~S1.}
```

---

## Estado da Fase 4

| Status | Itens |
|---|---|
| ✅ Encerrados | D1, C17, C20, C2 (diagnóstico: re-destilação EM) |
| ✅ Prontos | R1-1, R1-2, R1-3, R1-5 (R1-0 na Fase 2) |
| 🔴 Bloqueado | R1-4 — depende de C24 (dados braço 0% do B7) |
| 🔴 Prioridade máxima | C24 — localizar fonte dos valores 85.4%/79.7% |
| ⏳ Pendentes | F4 (nominalidade) · teste no EM (habilita B-06c) |

## Três ações em ordem de prioridade

1. **C24** — rodar diagnóstico da seção 1 para localizar a fonte de 85.4/79.7. Usar B-05b até resolver. Não colar A-11 nem congelar R1-4.
2. **F4** — confirmar nominalidade. CRediT e author agreement dependem disso.
3. **EM** — subir e baixar PDF; se artefatos desaparecerem, B-06c entra como está.
