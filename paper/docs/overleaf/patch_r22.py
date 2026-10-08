# -*- coding: utf-8 -*-
"""Patch response-to-reviewers.tex: substituir bloco R2.2 com resposta completa."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\docs\overleaf\response-to-reviewers.tex'

with open(path, encoding='utf-8') as f:
    content = f.read()

start_marker = r'\subsection{R2.2'
end_marker   = r'\subsection{R2.3'
i1 = content.find(start_marker)
i2 = content.find(end_marker)

if i1 == -1 or i2 == -1:
    print('ERRO: marcadores não encontrados')
    sys.exit(1)

print(f'R2.2 bloco: pos {i1}–{i2} ({i2-i1} chars)')

NEW_R22 = r"""\subsection{R2.2 --- Equations and tables}

\begin{rcomment}
Equations 1--6 are severely malformed in the provided PDF. Eq.~1 uses
``Retention.t /'' instead of a clear function notation and has a garbled
summation over $K_0$.
\end{rcomment}

The malformed rendering was an artefact of the font encoding used in the
original submission: Unicode characters in mathematical mode were not mapped
correctly to the T1 font metric, producing garbled output in the compiled PDF
while the source was syntactically correct. The revised submission uses the
\texttt{lmodern} package with T1 encoding throughout (preamble), which
eliminates the rendering artefact.

Eq.~1 now reads correctly as
\[
  R(t) = \frac{|\{q \in K_0 : q \text{ correct at gen.\ } t\}|}{|K_0|},
\]
using $R(t)$ as the retention symbol, consistent with Table~1 (tab:notation)
and the surrounding prose. The symbol $\mathrm{Retention}(t)$ that appeared in
the original version has been replaced by $R(t)$ throughout Equations~1, 3,
and 5 and the accompanying text.

\msloc{Preamble (lmodern + T1); Eq.~1, l.~595.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
Eq.~2 for effective rank is missing the negative sign and summation.
It should be $\exp\!\bigl(-\sum_i p_i \log p_i\bigr)$,
with $p_i = \sigma_i / \sum_j \sigma_j$.
\end{rcomment}

Corrected. Eq.~2 now reads
\[
  \mathrm{erank}(BA) = \exp\!\left(-\sum_i \hat{\sigma}_i \log \hat{\sigma}_i\right),
\]
where $\hat{\sigma}_i = \sigma_i / \sum_j \sigma_j$ are the normalised singular
values of $BA$. The normalised symbol $\hat{\sigma}_i$ is distinct from the raw
singular value $\sigma_i$, consistent with Table~1. The formula is the
standard effective-rank definition of \citet{roy2007}.

\msloc{Eq.~2, ll.~798--803.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
Eq.~6 for SDI-3 is unclear: signs, log ratios, and the $\Delta I$ term
are not consistently defined.
\end{rcomment}

Eq.~6 now reads
\[
  \mathrm{SDI\text{-}3} =
  \log\frac{\mathrm{MeanLen}_T}{\mathrm{MeanLen}_0}
  + \log\frac{\mathrm{D1}_0}{\mathrm{D1}_T}
  + \Delta I,
\]
with each term defined immediately before the equation and in Table~1:
the first term is positive when mean response length grows over the
evaluation horizon; the second is positive when content efficiency
($\mathrm{D1}$) declines (the numerator and denominator are swapped relative
to the length term, encoding the opposite direction of ``worse''); and
$\Delta I$ is the absolute drop in content efficiency from generation~1 to
generation~$T$. A positive SDI-3 score therefore indicates cumulative
distributional deterioration.

\msloc{Eq.~6, ll.~881--886; Table~1 (tab:notation); prose ll.~870--890.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
What is ``$5 \times 10^6$'' in Table~7? Please check also elsewhere.
\end{rcomment}

The garbled rendering was again a font-encoding artefact. The value in
Table~7 (tab:ranklr) is the learning rate $5 \times 10^{-6}$, not
$5 \times 10^6$. The exponent $-6$ was dropped in the original PDF due to
the same encoding issue. The revised PDF renders the value correctly as
$5 \times 10^{-6}$ throughout (Table~7 header row, l.~1473, and all
inline references). We have verified that no other table or equation
contains a similar rendering failure in the revised submission.

\msloc{Table~7 (tab:ranklr), l.~1473; preamble (lmodern + T1).}

"""

content_new = content[:i1] + NEW_R22 + content[i2:]
with open(path, 'w', encoding='utf-8') as f:
    f.write(content_new)
print('OK — R2.2 aplicado.')
print(f'Tamanho anterior: {len(content)} | Novo: {len(content_new)}')
