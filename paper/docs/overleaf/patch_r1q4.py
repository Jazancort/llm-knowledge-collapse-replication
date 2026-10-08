# -*- coding: utf-8 -*-
"""Patch response-to-reviewers.tex: substituir bloco R1.Q4 com resposta completa."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\docs\overleaf\response-to-reviewers.tex'

with open(path, encoding='utf-8') as f:
    content = f.read()

start_marker = r'\subsection{R1.Q4}'
end_marker   = r'\subsection{R1.Q5}'
i1 = content.find(start_marker)
i2 = content.find(end_marker)

if i1 == -1 or i2 == -1:
    print('ERRO: marcadores não encontrados')
    sys.exit(1)

print(f'R1.Q4 bloco: pos {i1}–{i2} ({i2-i1} chars)')

NEW_R1Q4 = r"""\subsection{R1.Q4}

\begin{rcomment}
Why does the five-percent exposure reduction stabilize Qwen but not
Gemma~3, and does this generalize across ranks and seeds?
\end{rcomment}

We thank the reviewer for this question, which led directly to a
substantially revised and pre-registered experiment. We address three issues
in turn: the correction of the original result, the pre-registered
dose--response, and the mechanism.

\textbf{Correction of the original result.}
The original submission reported that a ${\sim}5\%$ reduction of synthetic
training examples raised retention by $+9.0$ and $+9.4$\,pp for
conditions C3 and C5 respectively. We subsequently identified that C1
(the baseline) and C5 (the intervention) had been produced by different
evaluation pipelines, which differed in the $K_0$ construction procedure
and the data-loading code path. When C1 and C5 are re-run under an
identical pipeline with paired seeds, the effect of ${\sim}5\%$ example
removal is only $+1.9$\,pp (not distinguishable from zero at $n=3$). This
discrepancy is acknowledged explicitly in the revised manuscript (ll.~1708--1713)
and the original C2--C5 results are preserved in Appendix~A for transparency.
We thank the reviewer, whose question prompted the investigation that
uncovered this error.

\textbf{Pre-registered dose--response (Bloco~7).}
To replace the discredited result, we designed and pre-registered a
dose--response experiment (protocol committed as \texttt{a916ebf} before
any run), varying synthetic exposure at 0\%, 10\%, 25\%, and 50\%
removal across five paired seeds on Qwen~2.5~1.5B at $r=256$. The results,
reported in Section~4.5 (ll.~1685--1713), show that:

\begin{itemize}
  \item At Gen~5, any reduction raises retention by approximately
    $5$\,pp: $+5.0$\,pp (10\%, $p=0.002$), $+5.3$\,pp (25\%, $p=0.014$),
    $+5.7$\,pp (50\%, $p=0.002$), $n=5$ seeds each.
  \item At Gen~10, the benefit is dose-graded: $+2.4$\,pp at 10\% ($p$
    n.s.), $+5.5$\,pp at 25\% (95\,\% CI $[0.4, 10.5]$, $p=0.039$), and
    $+9.8$\,pp at 50\% (95\,\% CI $[6.9, 12.8]$, $p=0.0008$).
  \item At 50\% removal the Gen~5$\to$10 slope is $-0.14$\,pp/generation
    versus $-0.96$\,pp/generation at 0\%, shifting the system from the
    Degradative to the Bounded regime.
\end{itemize}

The pre-registered prediction that 50\% removal would match halving the
learning rate (from $\eta = 10^{-5}$ to $5\times10^{-6}$) was
confirmed: Gen~5 retention at dose~$=50\%$ is 89.7\% versus 90.2\% at
$\eta = 5\times10^{-6}$ (mean over three seeds; Gen~10 difference
$+0.4$\,pp, 90\,\% CI $[-0.8, 1.6]$).

\textbf{Mechanism and generalization.}
The mechanism through which exposure reduction acts was not established.
Two candidate explanations are plausible: a reduction in the per-generation
update budget (fewer gradient steps) and a change in data composition (lower
fraction of potentially corrupted synthetic responses). A steps-matched
control (G2b, $n=3$) was inconclusive. The effect was tested on a single
backbone (Qwen) and configuration ($r=256$, Gen~10 horizon); whether it
generalises to other ranks, other backbones, or different datasets is
explicitly listed as a limitation in Section~6 (ll.~2204--2214). The
original reviewer question about Gemma~3 is therefore not yet resolved for
the dose--response setting; the Gemma~3 analysis in the original submission
used the discredited pipeline and is not reported in the revised version.

\msloc{Section~4.5, ll.~1685--1713 (dose--response, pre-registration, LR
equivalence); Section~6, ll.~2204--2214 (mechanism limitation); Appendix~A
(original C2--C5 results).}

"""

content_new = content[:i1] + NEW_R1Q4 + content[i2:]
with open(path, 'w', encoding='utf-8') as f:
    f.write(content_new)
print('OK — R1.Q4 aplicado.')
print(f'Tamanho anterior: {len(content)} | Novo: {len(content_new)}')
