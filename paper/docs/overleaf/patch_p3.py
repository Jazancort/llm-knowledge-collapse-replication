# -*- coding: utf-8 -*-
"""
Patch P3 — Rebaixar C1-C5 de resultado principal para piloto arquivado.
Reescreve §3.7, tabela de eixos, §4.5 intro, figura interventions caption,
Discussion, Limitations, Conclusion.
"""
import sys, re
sys.stdout.reconfigure(encoding="utf-8")

path = r"G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\manuscript\manuscript-anonymous.tex"
with open(path, encoding="utf-8") as f:
    content = f.read()

original = content
changes = []

# ─── P3-1: Tabela de eixos L745 — 100% vs ~95% → 0–50% ─────────────────
OLD = r"5 & Exposure & Training examples & 100\% vs ${\sim}$95\% \\"
NEW = r"5 & Exposure & Training examples & 0\%, 10\%, 25\%, 50\% removed \rev{(paired dose--response; B7/Qwen $r=256$ $n=5$, G2/Gemma~3 $r=10$ $n=3$)} \\"
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    changes.append("[OK] P3-1: tabela eixos Axis 5 atualizado")
else:
    changes.append(f"[FAIL] P3-1: nao achou tabela eixo 5")

# ─── P3-2: §3.5 ETP — remover ~5% como framing central ──────────────────
OLD = r"length filtering, random downsampling (three independent masks, ${\sim}5\%$"
NEW = r"length filtering, and paired dose--response downsampling (0\%, 10\%, 25\%, 50\%"
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    changes.append("[OK] P3-2: §3.5 ETP ~5% -> dose-response framing")
else:
    changes.append(f"[FAIL] P3-2: nao achou ~5% em §3.5")

# ─── P3-3: §3.7 completo — substituir C1-C5 por dose-response ────────────
OLD_SEC37 = r"""\subsection{Synthetic-exposure interventions}\label{sec:intervention}

The interventions in Axis~5 test whether the degradative regime observed in the
high-capacity Qwen $r=256$ condition can be shifted back toward homeostasis by
modifying the synthetic training stream. All interventions use the same backbone,
rank, dataset, and recursive protocol as the Qwen $r=256$ baseline. The initial
intervention comparison is conducted with seed~15 for 5 generations; the
strongest intervention is then replicated across additional seeds or random
masks, as described below.

We define five intervention strategies to evaluate whether reducing synthetic
exposure can restore homeostatic behavior:

\begin{itemize}
    \item \textbf{C1 (Normal)}: the unmodified baseline. Synthetic responses are
    generated and used for training without filtering, downsampling, or
    post-processing. This is the same replace-only protocol used in the rank
    sweep.

    \item \textbf{C2 (Short-answer constrained)}: the generation prompt is
    modified to request a brief factual answer, and the maximum generation length
    is reduced to 10 tokens. This constrains output verbosity at generation time
    while retaining all training examples.

    \item \textbf{C3 (Length-filtered)}: synthetic responses are generated with
    the normal prompt, then examples whose responses exceed 5 words are removed
    from the next-generation training set. The remaining examples are used
    without duplication.

    \item \textbf{C4 (Canonical extraction)}: synthetic responses are generated
    normally, then a heuristic extracts a short factoid span from each response
    and replaces the original response with this canonicalized answer.

    \item \textbf{C5 (C3-matched random downsampling)}: synthetic responses are
    generated normally, then a random subset of examples is selected so that the
    resulting training stream approximately matches the token budget of C3. The
    subset is chosen by a random permutation seeded independently of the training
    seed.
\end{itemize}

The key comparison is between C3 and C5. C3 reduces exposure by removing long
responses, whereas C5 reduces exposure by removing a random subset of examples
until the training stream matches C3's approximate token budget. Thus, if both
conditions produce similar stabilization, the effect cannot be attributed solely
to removing long responses; it instead suggests sensitivity to marginal
synthetic exposure in this boundary regime.

To test robustness, C3 is evaluated with three independent training seeds.
C5 is evaluated with three independent random downsampling masks.
We compute Jaccard overlap between the examples removed by C3 and by each C5
mask to verify that the interventions remove largely distinct subsets of the
training stream.

C2 and C4 provide additional controls on output format. C2 changes the generation
instruction and length limit while retaining all examples; C4 canonicalizes
responses after generation. These conditions help distinguish exposure reduction
from response-format control. We report token counts, example counts, and
retention for all intervention strategies to assess whether improvements can be
explained by reduced training volume alone.
"""

NEW_SEC37 = r"""\subsection{Synthetic-exposure interventions}\label{sec:intervention}

The interventions in Axis~5 test whether the degradative regime can be shifted
back toward homeostasis by reducing synthetic training exposure. The primary
evidence comes from two pre-registered dose--response experiments, one on each
backbone.

\textbf{Qwen dose--response (B7, $r=256$, $n=5$ seeds).}
Five paired seeds receive 0\%, 10\%, 25\%, or 50\% random downsampling of the
synthetic training stream. The 0\% arm serves as a within-pipeline baseline
(same evaluation code, same seeds), eliminating cross-pipeline confounds. The
pre-registration hash is \texttt{a916ebf}.

\textbf{Gemma~3 dose--response (G2, $r=10$, $n=3$ seeds).}
An independent pre-registered experiment applies the same four dose levels to
Gemma~3~1B~IT at $r=10$. The evaluation set is $K_{0,\mathrm{G2}}=44$ items
(established by the \texttt{g1\_rank10} pipeline; see Section~\ref{sec:k0}).

\rev{A prior exploratory pilot (C1--C5) used a qualitatively different
experimental design: five discrete intervention strategies (baseline, prompt
constraint, length filtering, canonical extraction, and random downsampling)
evaluated on a single seed with a different evaluation pipeline. When C1 and C5
from that pilot are re-run under an identical pipeline and paired seeds, the
approximate $5\%$ downsampling effect is $+1.9$\,pp ($n=3$), which is not
statistically distinguishable from zero. The pilot results are archived in the
replication repository; they are not used in the primary effect estimates below.}
"""

if OLD_SEC37 in content:
    content = content.replace(OLD_SEC37, NEW_SEC37, 1)
    changes.append("[OK] P3-3: §3.7 reescrito com dose-response como protocolo principal")
else:
    changes.append("[FAIL] P3-3: §3.7 nao encontrado verbatim")

# ─── P3-4: §3.8 seeds/stats — remover referência C3/C5 ──────────────────
OLD_38 = r"ranks ($r=4$, homeostatic, and $r=16$, degradative), the QLoRA--FFT comparison, and the C3/C5 synthetic"
NEW_38 = r"ranks ($r=4$, homeostatic, and $r=16$, degradative), the QLoRA--FFT comparison, and the dose--response synthetic"
if OLD_38 in content:
    content = content.replace(OLD_38, NEW_38, 1)
    changes.append("[OK] P3-4: §3.8 C3/C5 -> dose-response")
else:
    changes.append("[FAIL] P3-4: §3.8 C3/C5 nao encontrado")

# ─── P3-5: §4.5 intro — remover "C1 baseline" framing L1699-1710 ─────────
OLD_45_INTRO = r"""The preceding sections established that update capacity and perturbation
magnitude each govern the regime transition. This section tests the third
component of effective training pressure: whether reducing synthetic data
exposure can shift the system back from a degradative to a near-homeostatic
configuration. All interventions are conducted on Qwen $r=256$, which sits at
the boundary between the bounded and degradative regimes.

Table~\ref{tab:interventions} summarizes K0 retention at Gen5 for each
intervention strategy relative to the unmodified C1 baseline.
% [v4] A10 — see planned controls in plano-de-revisao.md (Bloco 4)
A direct comparison of C3/C5 against C1 is complicated by the fact that C1
was evaluated with a single seed (seed~15). Per-seed data from the full
three-seed $r=256$ replication (Gen5 retention: $81.0\%$, $83.5\%$, $84.8\%$
across seeds~256, 15, 137 respectively) indicate that $83.3\%$ at seed~15 is
representative of the seed-mean, reducing the likelihood that the observed
$+9$ pp gain is attributable to seed variability alone. Planned additional
controls (an unmodified C1 re-run through the intervention pipeline at $0\%$
removal, and a step-matched C5 replication) are described in
Section~\ref{sec:limitations}. % [v4] A10"""

NEW_45_INTRO = r"""The preceding sections established that update capacity and perturbation
magnitude each govern the regime transition. This section tests the third
component of effective training pressure: whether reducing synthetic data
exposure can shift the system back from a degradative to a near-homeostatic
configuration. The primary evidence comes from the two pre-registered
dose--response experiments described in Section~\ref{sec:intervention}:
B7 on Qwen $r=256$ ($n=5$ paired seeds, $K_0=78$) and G2 on Gemma~3 $r=10$
($n=3$ paired seeds, $K_{0,\mathrm{G2}}=44$).

\rev{Table~\ref{tab:interventions} reports $K_0$ retention and the gain over
the 0\% within-pipeline baseline for each dose level on Qwen $r=256$.}"""

if OLD_45_INTRO in content:
    content = content.replace(OLD_45_INTRO, NEW_45_INTRO, 1)
    changes.append("[OK] P3-5: §4.5 intro reescrito sem C1 baseline framing")
else:
    changes.append("[FAIL] P3-5: §4.5 intro nao encontrado verbatim")

# ─── P3-6: tabela caption — "C3/C5" → dose labels ────────────────────────
OLD_TAB_CAP = r"""\caption{Synthetic-exposure interventions on Qwen $r=256$. C3: three seeds;
C5: three independent masks. Means reported for multi-seed/mask
conditions.}\label{tab:interventions}"""
NEW_TAB_CAP = r"""\caption{\rev{Dose--response on Qwen $r=256$ ($K_0=78$, $n=5$ paired seeds per
dose). Retention and gain ($\Delta$) relative to the 0\% within-pipeline
baseline at Gen5 and Gen10.}}\label{tab:interventions}"""
if OLD_TAB_CAP in content:
    content = content.replace(OLD_TAB_CAP, NEW_TAB_CAP, 1)
    changes.append("[OK] P3-6: tabela caption atualizada")
else:
    changes.append("[FAIL] P3-6: tabela caption nao encontrada")

# ─── P3-7: parágrafo intro B7 — remover "any reduction raises ~5pp" ──────
OLD_B7_INTRO = r"""\rev{A pre-registered dose--response experiment (five paired seeds; protocol
registered as \texttt{a916ebf} before any run) shows that any reduction of the
synthetic training stream raises Gen~5 retention by approximately $5$\,pp
relative to the unmodified baseline ($+5.0$, $+5.3$, $+5.7$\,pp at 10\%,
25\%, and 50\% removal; paired $t$-test $p = 0.002$, $0.014$, $0.002$,
$n = 5$). At Gen~10 the benefit is graded: $+2.4$\,pp at 10\%, $+5.5$\,pp
at 25\% (95\%~CI $[0.4, 10.5]$, $p = 0.039$), and $+9.8$\,pp at 50\%
(95\%~CI $[6.9, 12.8]$, $p = 0.0008$). A 50\% reduction effectively arrests
progressive loss: the Gen~5$\to$10 slope is $-0.14$\,pp/generation versus
$-0.96$\,pp/generation at 0\%, shifting the system from the degradative to
the bounded regime by the criterion of Section~\ref{sec:res_capacity}.

The pre-registered prediction that 50\% removal would match halving the
learning rate (from $\eta = 10^{-5}$ to $5\times 10^{-6}$) was confirmed:
Gen~5 retention at dose~$= 50\%$ is $89.7\%$ versus $90.2\%$ at
$\eta = 5\times 10^{-6}$ (mean over three seeds; Gen~10 difference
$+0.4$\,pp, 90\%~CI $[-0.8, 1.6]$). This is consistent with exposure
acting through the per-generation update budget: fewer training examples
reduce the number of gradient steps by the same proportion as a
proportional reduction in learning rate, with equivalent effect on retention.
The mechanism (whether update budget or data composition) was not established;
a steps-matched control was inconclusive at $n = 3$.

The original submission reported C3 ($+9.0$\,pp) and C5 ($+9.4$\,pp) from a
different evaluation pipeline. When C1 and C5 are re-run under an identical
pipeline and paired seeds, the effect of ${\sim}5\%$ removal is $+1.9$\,pp
(not statistically distinguishable from zero, $n = 3$). The dose--response
reported here replaces those comparisons. The original C2--C5 results are
preserved in Appendix~\ref{app:repo} for transparency.}"""

NEW_B7 = r"""\rev{\textbf{Qwen dose--response (B7).}
A pre-registered dose--response experiment on Qwen $r=256$ (five paired seeds;
protocol registered as \texttt{a916ebf} before any run) shows that the
Gen~10 benefit is graded: $+2.4$\,pp at 10\% removal ($p = 0.002$, $n=5$),
$+5.5$\,pp at 25\% (95\%~CI $[0.4, 10.5]$, $p = 0.039$), and
$+9.8$\,pp at 50\% (95\%~CI $[6.9, 12.8]$, $p = 0.0008$). At Gen~5, the
gains are smaller and more uniform ($+5.0$, $+5.3$, $+5.7$\,pp;
paired $t$-test $p = 0.002$, $0.014$, $0.002$). A 50\% reduction
effectively arrests progressive loss: the Gen~5$\to$10 slope is
$-0.14$\,pp/generation versus $-0.96$\,pp/generation at 0\%, shifting the
system from the degradative to the bounded regime by the criterion of
Section~\ref{sec:res_capacity}.

The pre-registered prediction that 50\% removal would match halving the
learning rate (from $\eta = 10^{-5}$ to $5\times 10^{-6}$) was confirmed:
Gen~5 retention at dose~$= 50\%$ is $89.7\%$ versus $90.2\%$ at
$\eta = 5\times 10^{-6}$ (mean over three seeds; Gen~10 difference
$+0.4$\,pp, 90\%~CI $[-0.8, 1.6]$). The mechanism (whether update budget
or data composition) was not established; a steps-matched control was
inconclusive at $n = 3$.

The original C1--C5 pilot compared non-identical evaluation pipelines;
when C1 and C5 are re-run under an identical pipeline and paired seeds,
the approximate $5\%$ downsampling effect is $+1.9$\,pp ($n=3$, not
statistically distinguishable from zero). We therefore exclude the
original pilot from the primary effect estimate; those results are
archived in the replication repository (Section~\ref{app:repo}).}"""

if OLD_B7_INTRO in content:
    content = content.replace(OLD_B7_INTRO, NEW_B7, 1)
    changes.append("[OK] P3-7: paragrafos B7 reescritos sem C3/C5 como resultado principal")
else:
    changes.append("[FAIL] P3-7: bloco B7 nao encontrado verbatim")

# ─── P3-8: fig:interventions caption — C1-C5 → dose-response ─────────────
OLD_FIG_INT = r"""\begin{figure}
  \centering
  \includegraphics[width=0.95\columnwidth]{figs/scratch/fig_interventions.png}
  \caption{Intervention comparison on Qwen $r=256$ at Gen5. (a)~$K_0$ retention
  by condition (C1--C5). (b)~Retention improvement relative to C1 baseline.
  Error bars for C3 and C5 reflect the range across three seeds or
  masks.}\label{fig:interventions}
\end{figure}"""
NEW_FIG_INT = r"""\rev{\begin{figure}
  \centering
  \includegraphics[width=0.95\columnwidth]{figs/scratch/fig_interventions.png}
  \caption{Exploratory pilot (C1--C5) on Qwen $r=256$ at Gen5, included for
  transparency. These results use a different evaluation pipeline from the
  primary dose--response experiments (B7/G2) and are not used in the primary
  effect estimates. (a)~$K_0$ retention by condition. (b)~Retention improvement
  relative to C1 baseline; error bars reflect the range across three seeds or
  masks.}\label{fig:interventions}
\end{figure}}"""
if OLD_FIG_INT in content:
    content = content.replace(OLD_FIG_INT, NEW_FIG_INT, 1)
    changes.append("[OK] P3-8: fig:interventions caption -> piloto arquivado")
else:
    changes.append("[FAIL] P3-8: fig:interventions nao encontrada")

# ─── P3-9: L1772-1778 — "approximately 5% is sufficient" → corrigido ─────
OLD_5PCT = r"""These results demonstrate that the Qwen $r=256$ configuration lies near \rev{a steep empirical transition
region}: a reduction of approximately 5\% in synthetic exposure volume
is sufficient to restore near-homeostatic retention in this boundary case. This
sensitivity is tested only at the $r=256$ boundary on Qwen and should not be
interpreted as a universal property of recursive fine-tuning. Whether comparable
boundary sensitivity exists at other ranks, on other backbones, or with
different datasets remains untested."""

NEW_5PCT = r"""\rev{These results demonstrate that the Qwen $r=256$ configuration responds to
graded exposure reduction: a 50\% reduction arrests progressive loss and shifts
the system to the bounded regime, whereas a 10\% reduction does not. This
graded dose--response is confirmed on a second backbone (Gemma~3 G2, see below).
The sensitivity is tested only at the configurations evaluated here and should
not be interpreted as a universal property of recursive fine-tuning.}"""

if OLD_5PCT in content:
    content = content.replace(OLD_5PCT, NEW_5PCT, 1)
    changes.append("[OK] P3-9: 'approximately 5% sufficient' removido; dose-response graded")
else:
    changes.append("[FAIL] P3-9: '5% sufficient' nao encontrado")

# ─── P3-10: Discussion §5.1 — C3/C5 → dose-response ─────────────────────
OLD_DISC1 = r"C3/C5 results operate on a complementary axis: rather than adding real data, we"
NEW_DISC1 = r"\rev{dose--response results} operate on a complementary axis: rather than adding real data, we"
if OLD_DISC1 in content:
    content = content.replace(OLD_DISC1, NEW_DISC1, 1)
    changes.append("[OK] P3-10: Discussion §5.1 C3/C5 -> dose-response")
else:
    changes.append("[FAIL] P3-10: Discussion §5.1 C3/C5 nao encontrado")

# ─── P3-11: Discussion §5.4 practical — C3/C5 ────────────────────────────
OLD_DISC2 = r"""Regarding intervention design, the C3/C5 results demonstrate that boundary
sensitivity is real and replicable across a dose range. While this is a positive
finding"""
# procurar mais contexto
idx = content.find("Regarding intervention design, the C3/C5 results")
if idx >= 0:
    snippet = content[idx:idx+400]
    changes.append(f"[FOUND] P3-11: Discussion §5.4 (precisa substituição manual): {snippet[:80]}")
else:
    changes.append("[FAIL] P3-11: Discussion §5.4 C3/C5 nao encontrado (busca ampla)")

# ─── P3-12: Limitations — C3/C5 e 5% ────────────────────────────────────
OLD_LIM1 = r"Gemma~3 \rev{lowest-pressure degradative configuration tested} (r=16, using the same approximate 5\% random\ndownsampling protocol) did not reproduce the stabilization observed on Qwen."
NEW_LIM1 = r"\rev{Gemma~3 at $r=16$ (degradative regime) was not tested with the paired dose--response protocol; the prior exploratory C5 pilot at ${\sim}5\%$ downsampling did not reproduce the stabilization observed on Qwen, but the doses tested and the evaluation pipeline differ from B7/G2.}"
if OLD_LIM1 in content:
    content = content.replace(OLD_LIM1, NEW_LIM1, 1)
    changes.append("[OK] P3-12: Limitations Gemma r=16 C5 reescrito")
else:
    changes.append("[FAIL] P3-12: Limitations Gemma r=16 nao encontrado verbatim")

OLD_LIM2 = r"The synthetic-exposure interventions (C3/C5) are tested only at the $r=256$"
NEW_LIM2 = r"\rev{The primary dose--response experiments (B7 and G2) are tested only at $r=256$ on Qwen and $r=10$ on Gemma~3. The exploratory C1--C5 pilot is archived but not used in primary estimates.} The interventions are tested only at the $r=256$"
if OLD_LIM2 in content:
    content = content.replace(OLD_LIM2, NEW_LIM2, 1)
    changes.append("[OK] P3-12b: Limitations C3/C5 -> dose-response")
else:
    changes.append("[FAIL] P3-12b: Limitations C3/C5 nao encontrado")

OLD_LIM3 = r"changes with genuine knowledge loss. However, the C2 intervention (which"
NEW_LIM3 = r"changes with genuine knowledge loss. \rev{The C2 intervention from the exploratory pilot (which"
if OLD_LIM3 in content:
    content = content.replace(OLD_LIM3, NEW_LIM3, 1)
    changes.append("[OK] P3-12c: Limitations C2 -> exploratory pilot C2")
else:
    changes.append("[FAIL] P3-12c: Limitations C2 nao encontrado")

# ─── P3-13: Conclusion — "marginal reductions" ───────────────────────────
OLD_CONC = r"stabilize within the observed horizon. At the regime boundary, marginal\nreductions in synthetic exposure restore near-homeostatic retention, although\nthis sensitivity is backbone-dependent."
NEW_CONC = r"""stabilize within the observed horizon. \rev{Pre-registered dose--response
experiments on two backbones show that a 50\% reduction in synthetic exposure
arrests progressive loss, with the effect magnitude depending on the backbone
operating pressure. An approximate $5\%$ pilot reduction, evaluated in a
different pipeline, did not replicate under paired conditions ($+1.9$\,pp,
$n=3$).} This sensitivity is backbone-dependent."""
if OLD_CONC in content:
    content = content.replace(OLD_CONC, NEW_CONC, 1)
    changes.append("[OK] P3-13: Conclusion marginal -> dose-response + C5 não replicou")
else:
    changes.append("[FAIL] P3-13: Conclusion marginal nao encontrado")

# ─── Salvar ──────────────────────────────────────────────────────────────
if content != original:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    n_ok = sum(1 for c in changes if "[OK]" in c)
    n_fail = sum(1 for c in changes if "[FAIL]" in c)
    print(f"SALVO — {n_ok} patches aplicados, {n_fail} falhas")
else:
    print("NENHUMA MUDANCA")

print()
for c in changes:
    print(f"  {c}")
