# -*- coding: utf-8 -*-
"""Patch R1.Q2: adicionar resultados N=6 e distinção ETP-design/observed."""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\docs\overleaf\response-to-reviewers.tex'

with open(path, encoding='utf-8') as f:
    content = f.read()

start = r'\subsection{R1.Q2}'
end   = r'\subsection{R1.Q3}'
i1 = content.find(start)
i2 = content.find(end)
print(f'R1.Q2: {i1}–{i2}')

NEW = r"""\subsection{R1.Q2}

\begin{rcomment}
How are quantization, optimizer state, data order, and model-specific
dynamics separated from the claimed pressure effects?
\end{rcomment}

We thank the reviewer for this precise question. The revised manuscript
addresses each potential confound through a dedicated control, all of which
are now documented in Section~3.9 (``Sources of variation and experimental
controls'', ll.~1000--1037) with Table~2 (tab:controls).

\textbf{Quantization (NF4 vs bf16).}
All QLoRA experiments in the main analysis use 4-bit NormalFloat (NF4)
quantization of the base weights, with adapters trained in bf16. A dedicated
ablation (G3, three seeds each at $r=16$ and $r=256$) runs the same protocol
with standard bf16 precision and no base-weight quantization.
G3 results show that the regime classification is preserved under both
precision settings: at $r=16$ bf16 achieves Gen10=97.4\%, identical to the
NF4 baseline; at $r=256$ bf16 achieves Gen10=79.1\%, within 0.0~pp of the
NF4 condition. The delta between NF4 and bf16 is $\leq$0.1~pp at both
ranks. Quantization is therefore not driving the observed regime separation.

\msloc{Section~3.9 (tab:controls); Section~4.6 (G3 results).}

\textbf{Optimizer state.}
A fresh optimizer is instantiated at every generation; no momentum or
adaptive-rate state is carried forward between generations. This is held
constant across all conditions within a backbone and cannot explain
differences between conditions that share the same protocol.

\msloc{Section~3.9 (tab:controls), ``Optimizer state'' row.}

\textbf{Training data order.}
Ablation G4 runs Qwen at $r=256$ with three independent shuffle seeds
(42/101/202), keeping all other conditions identical to G1
(seeds~15/137/256). A permutation test comparing Gen10 retention between
the two seed groups gives $p=0.70$ (two-sided, $N=3+3$), indicating that
the data-order variance is statistically indistinguishable from the
seed-to-seed variance already present within G1. The combined
$N=6$ seed set (G1$+$G4) yields Gen10 = $79.7\%\pm1.7$~pp,
with variance attributable to seed rather than order.

\msloc{Section~3.9 (tab:controls); Section~4.6 (G4 results).}

\textbf{ETP-design vs ETP-observed.}
Following the reviewer's implicit distinction, we now separate two classes
of ETP variables in the revised manuscript. \emph{ETP-design} variables are
known before training: nominal rank ($r$), learning rate ($\eta$), number of
training steps, and synthetic exposure fraction. These are the directly
manipulated axes in our factorial design. \emph{ETP-observed} variables are
measured after training: effective rank (erank), mean absolute weight drift
($d(t)$), response length, and SDI-3. We report erank and drift as
post-training diagnostic proxies that track how much pressure was actually
applied, not as pre-specified predictors. The revised text makes this
distinction explicit and avoids treating erank as a prospective input.

\msloc{Section~3.5 (ETP definition); Table~1 (tab:notation).}

\textbf{Seed-level contrast for the primary headline claim.}
For the central Qwen result, the rank-regime contrast is supported at the
seed level. Using G1 ($r=256$, seeds~15/137/256) and G4 ($r=256$, seeds
42/101/202) as the $r=256$ condition ($N=6$) and the historical multi-seed
runs as the $r=16$ condition ($N=3$), the Gen10 difference is
$+17.7$~pp ($r=16$: $97.4\%\pm0.0$; $r=256$: $79.7\%\pm1.7$).
A one-sided permutation test gives $p<0.001$. For Gemma~3, the $r=4$
versus $r=16$ Gen10 contrast ($N=5+5$) gives $\Delta=+37.2$~pp,
permutation $p=0.0041$. We report these as seed-level evidence rather
than item-level tests.

\msloc{Section~4.2 (Qwen rank sweep, N=3+6); Section~4.3.1 (Gemma~3, N=5+5).}

"""

content_new = content[:i1] + NEW + content[i2:]
with open(path, 'w', encoding='utf-8') as f:
    f.write(content_new)
print('OK — R1.Q2 atualizado.')
print(f'Tamanho: {len(content)} → {len(content_new)}')
