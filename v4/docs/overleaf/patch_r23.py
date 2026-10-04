# -*- coding: utf-8 -*-
"""Patch response-to-reviewers.tex: substituir bloco R2.3 com resposta completa."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\docs\overleaf\response-to-reviewers.tex'

with open(path, encoding='utf-8') as f:
    content = f.read()

start_marker = r'\subsection{R2.3'
end_marker   = r'\subsection{R2.4'
i1 = content.find(start_marker)
i2 = content.find(end_marker)

if i1 == -1 or i2 == -1:
    print('ERRO: marcadores não encontrados')
    sys.exit(1)

print(f'R2.3 bloco: pos {i1}–{i2} ({i2-i1} chars)')

NEW_R23 = r"""\subsection{R2.3 --- Technical and data inconsistencies}

We thank the reviewer for this careful cross-checking of results against tables and
prose. Each inconsistency has been corrected as described below.

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
\textbf{Qwen threshold inconsistency.} Abstract and Section~4.2.3 state
the Qwen boundary is between effective ranks 50--88. Section~5.1 states
Qwen remains outside the degradative regime ``up to effective rank~150.''
This contradicts Table~2, where $r=256$ has effective rank~87.57 and is
classified as degradative.
\end{rcomment}

The phrase ``up to effective rank~150'' has been removed. All threshold
language now uses the form \revised{``an abrupt, threshold-like transition
within the tested grid''} (l.~72, l.~95), which accurately reflects that the
boundary is established empirically between adjacent tested configurations
rather than extrapolated to untested values. The interval 50--88 (effective
ranks of $r=128$ and $r=256$ respectively) is retained as the localization
of the boundary. No claim is made beyond the tested range.

\msloc{Abstract l.~72; Contribution~\#1 l.~95; Section~5.1 (phrase removed).}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
\textbf{$r=128$ classification.} $r=128$ is classified as ``Bounded'' in
Table~2, but Section~4.4.3 calls $r=128$ and $r=256$
``above-threshold configurations.''
\end{rcomment}

The phrase ``above-threshold configurations'' in Section~4.4.3 now refers
only to $r=256$, which Table~2 classifies as Degradative. The term
\revised{``above-threshold''} is used exclusively for configurations in
the Degradative regime. $r=128$ (Bounded) is described as a
\revised{``transition-zone configuration''} where distributional signatures
begin to emerge without producing the full degradative trajectory.

\msloc{Section~4.4.3, ll.~1061, 1570.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
\textbf{$r=256$ boundary claim.} $r=256$ is repeatedly called a
``boundary configuration,'' but Table~2 classifies it as degradative.
The boundary lies between $r=128$ and $r=256$.
\end{rcomment}

Agreed. The five occurrences of ``boundary configuration'' referring to
$r=256$ have been replaced throughout with
\revised{``lowest-pressure degradative configuration tested''}, which
correctly identifies $r=256$ as the degradative anchor while making
explicit that the transition itself is localised between $r=128$ and
$r=256$.

\msloc{ll.~1737, 1915, 2063, 2069, 2159.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
\textbf{Gemma~3 degradative range.} Section~5.2 states ``$r \geq 16$ on
Gemma~3,'' but Table~4 shows $r \in \{10,12,14\}$ already degradative at
Gen~5. The boundary is below $r=10$.
\end{rcomment}

Corrected. Table~4 (tab:gemma3) reports retention of 78.3\,\%, 73.9\,\%,
and 69.6\,\% for $r=10$, 12, and 14 respectively at Gen~5, all classified
as Degradative. The regime boundary is placed at effective ranks between
3 and 6 (between $r=4$, which is Homeostatic, and $r=10$, which is
Degradative). The text now reads \revised{``the Gemma~3 regime boundary
lies between effective ranks 3 and 6, below $r=10$''}, consistent with
Table~4. The phrase ``$r \geq 16$'' has been removed.

\msloc{Section~5.2; Table~4 (tab:gemma3), ll.~1265, 1277--1280.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
\textbf{Abstract overclaim.} ``Three to five independent seeds per
condition'' is not accurate: many conditions are single-seed; only
headline comparisons use multiple seeds.
\end{rcomment}

The abstract now reads \revised{``three to five independent seeds for
headline conditions (single seed for intermediate ablations)''} (l.~69),
which accurately reflects the experimental design. Headline rank levels
($r \in \{16, 256\}$ on Qwen; $r \in \{4, 16\}$ on Gemma~3) use three to
five seeds; intermediate and ablation conditions use a single seed. This
distinction is also stated in the Methods and reported per table via the
added $N$ column.

\msloc{Abstract l.~69.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
\textbf{FFT on Gemma~3: non-monotonic results.} Retention values of
78.3\,\%, 54.3\,\%, and 63.0\,\% for learning rates $10^{-6}$,
$5\times10^{-6}$, and $10^{-5}$ are non-monotonic. The conclusion that
this ``confirms'' the magnitude axis is too strong for a single-seed,
non-monotonic result.
\end{rcomment}

Agreed. The text (l.~1147--1152) now notes explicitly that
\revised{``no rank reversal or non-monotonicity is observed''} in the
primary Qwen rank sweep; for the FFT on Gemma~3, the word ``confirms'' has
been replaced with \revised{``is consistent with''} and the non-monotonic
pattern is acknowledged: the result is treated as supporting evidence at
$n=1$ seed rather than confirmatory.

\msloc{ll.~1147--1149 (Qwen rank sweep prose); FFT Gemma~3 paragraph.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
\textbf{C5 removal percentage.} Section~3.4 mentions ``15\% removal,''
while Section~4.5 reports approximately 5\,\% token reduction.
This discrepancy must be clarified.
\end{rcomment}

The two figures refer to different quantities. The original C5 condition
removed 15\,\% of training \emph{examples} (questions), which reduced the
token count by approximately 5\,\% because responses vary in length. The
revised manuscript clarifies this distinction at both locations. However,
the more substantive resolution is that the original C3/C5 results were
produced by a different evaluation pipeline than C1: when C1 and C5 are
re-run under an identical pipeline with paired seeds, the effect of
${\sim}5\%$ example removal is $+1.9$\,pp (not distinguishable from zero,
$n=3$). The dose--response reported in Section~4.5 (Bloco~7) replaces
those comparisons; the original C2--C5 results are preserved in
Appendix~A for transparency.

\msloc{Section~3.7 (definition of C5 doses); Section~4.5 l.~1708--1713.}

"""

content_new = content[:i1] + NEW_R23 + content[i2:]
with open(path, 'w', encoding='utf-8') as f:
    f.write(content_new)
print('OK — R2.3 aplicado.')
print(f'Tamanho anterior: {len(content)} | Novo: {len(content_new)}')
