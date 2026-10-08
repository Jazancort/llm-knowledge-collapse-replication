# -*- coding: utf-8 -*-
"""Patch R1.Q1 e R1.Q5 — preencher msnote com texto final."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\docs\overleaf\response-to-reviewers.tex'

with open(path, encoding='utf-8') as f:
    content = f.read()

# ── R1.Q1 ────────────────────────────────────────────────────────────────────
OLD_Q1 = r"""\msnote{inserir resposta}
\msloc{p.~??, ll.~??--??}

\begin{rcomment}
How are quantization, optimizer state, data order, and model-specific"""

NEW_Q1 = r"""We agree that the present experiments do not establish a transferable
scalar ETP predictor or a prospective threshold for an unseen backbone
or dataset. We have revised the manuscript to distinguish controllable
design variables---nominal adapter rank, learning rate, planned training
steps, and synthetic-data dose---from post-training diagnostics,
including effective rank and weight drift. Under the tested protocol,
we identify empirical intervals between adjacent configurations
exhibiting different retention trajectories; these intervals should not
be interpreted as universal numerical thresholds.

A prospective test would require: (i)~specifying a calibration rule and
outcome criterion before examining a held-out backbone or dataset;
(ii)~selecting configurations on both sides of the predicted regime
boundary; and (iii)~evaluating them without refitting that rule to the
held-out outcomes. We have added this as a concrete validation protocol
in Section~\ref{sec:limitations} and state explicitly that such
held-out prospective validation has not been performed in the present
study. Accordingly, we describe effective training pressure as an
\emph{operational experimental framework}, not a validated universal
predictor.

The pre-registered G5 experiment (three cells, one seed) provides
exploratory evidence that the operational regime index correctly
predicts qualitative behavior (homeostatic vs.\ bounded) for
pre-specified configurations on the tested backbone. Prediction of the
exact degradative threshold remains uncalibrated.

\msloc{Section~3.5 (ETP as framework, revised); Section~\ref{sec:limitations}
(prospective calibration protocol); Section~4.4 (G5 prospective results).}

\subsection{R1.Q2}

\begin{rcomment}
How are quantization, optimizer state, data order, and model-specific"""

assert OLD_Q1 in content, "OLD_Q1 not found"
content = content.replace(OLD_Q1, NEW_Q1, 1)
print("R1.Q1 patched OK")

# ── R1.Q5 ────────────────────────────────────────────────────────────────────
OLD_Q5 = r"""\msnote{inserir resposta}
\msloc{p.~??, ll.~??--??}"""

NEW_Q5 = r"""We agree that independent reproduction requires more than aggregate
retention tables. We have expanded the reproducibility section
(Section~\ref{app:repo}) to specify:

\begin{enumerate}
\item the exact model checkpoint identifiers and revisions for all three
  backbones;
\item train and evaluation question IDs, and the baseline-correct
  $K_0$ sets ($|K_0|=78$ for Qwen, $|K_0|=46$ for Gemma~3);
\item prompt and chat templates used for both synthetic data generation
  and deterministic evaluation;
\item distinct decoding settings (sampling parameters for generation,
  \texttt{do\_sample=False} and \texttt{temperature=0} for evaluation);
\item correctness normalization and alias-expansion code;
\item training configurations, software versions, random seeds,
  data-order and downsampling masks;
\item per-generation, item-level predictions and correctness labels; and
\item scripts used to regenerate every table and figure.
\end{enumerate}

We also specify which experiments reset adapters and optimizer states
between generations. The source code, configurations, raw outputs,
analysis scripts, and adapter checkpoints permitted by the applicable
model licenses are available to reviewers via the anonymized repository
link provided in the cover letter, with a permanent DOI to be assigned
upon acceptance. Base-model weights are obtained from their original
distributors and are not redistributed. The revised appendix provides
an artifact manifest mapping every reported figure and table to its
generating data and script.

\msloc{Section~\ref{app:repo} (repository and data access, expanded).}"""

# R1.Q5 msnote appears after \begin{rcomment} block for Q5
# We replace only the LAST occurrence of the msnote+msloc pattern
# (i.e., the one under R1.Q5)
idx = content.rfind(OLD_Q5)
assert idx != -1, "OLD_Q5 not found"
content = content[:idx] + NEW_Q5 + content[idx+len(OLD_Q5):]
print("R1.Q5 patched OK")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

remaining = content.count(r'\msnote{inserir resposta}')
print(f"msnote restantes: {remaining}")
print(f"Tamanho final: {len(content)} chars")
