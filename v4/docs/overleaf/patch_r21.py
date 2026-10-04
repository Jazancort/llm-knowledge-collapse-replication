# -*- coding: utf-8 -*-
"""Patch response-to-reviewers.tex: substituir bloco R2.1 com resposta completa."""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\docs\overleaf\response-to-reviewers.tex'

with open(path, encoding='utf-8') as f:
    content = f.read()

# Localizar início e fim do bloco R2.1
start_marker = r'\subsection{R2.1'
end_marker   = r'\subsection{R2.2'
i1 = content.find(start_marker)
i2 = content.find(end_marker)

if i1 == -1 or i2 == -1:
    print('ERRO: marcadores não encontrados')
    sys.exit(1)

print(f'R2.1 começa: {i1}, R2.2 começa: {i2}, bloco: {i2-i1} chars')

NEW_R21 = r"""\subsection{R2.1 --- Abbreviations and notation}

\begin{rcomment}
ETP appears in Figure~1 (``ETP threshold identification'') but is never
explicitly defined as ``effective training pressure.''
\end{rcomment}

We agree. The revised manuscript does not use ``ETP'' as a standalone acronym.
The term is introduced by name at l.~72
(\revised{``which we term effective training pressure''}) and used in full
throughout. Figure~1 (caption ll.~692--698) no longer contains the
abbreviation in isolation.

\msloc{Abstract l.~72; Figure~1 caption ll.~692--698.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
MTLD is introduced as ``a length-robust diversity estimate'' but the
acronym is not expanded.
\end{rcomment}

Corrected. The first occurrence now reads
\revised{``Measure of Textual Lexical Diversity (MTLD)''} followed by the
functional description.

\msloc{l.~875.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
KL, JS, and coverage appear in Figure~1 without definition.
\end{rcomment}

These three quantities were used as conceptual labels for
distribution-comparison diagnostics that are not computed or reported anywhere
in the manuscript. They have been removed from Figure~1 entirely. The revised
caption describes only quantities that are measured and reported: factual
retention, effective rank, and distributional shift (response length, content
efficiency, SDI-3).

\msloc{Figure~1 caption, ll.~692--698.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
bf16, SVD, TCE, QLoRA, and LoRA are used without consistently expanded
forms.
\end{rcomment}

All four acronyms now have explicit parenthetical expansions at first use:
\revised{``full fine-tuning (FFT)''} at l.~75;
\revised{``singular value decomposition (SVD)''} at l.~332;
\revised{``Quantized Low-Rank Adaptation (QLoRA)''} at l.~333.
The term \textit{bf16} (BFloat16) is glossed on first use. TCE does not
appear in the revised manuscript. LoRA was already expanded in the Related
Work section.

\msloc{ll.~75, 332, 333.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
``Homeo.'' is used in Table~2 without definition.
\end{rcomment}

The abbreviation has been expanded to \revised{``Homeostatic''} in all four
occurrences within the rank-sweep results table.

\msloc{Table~2 (tab:rank\_sweep), regime column.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
$K_0$ is used both as a set of questions and as a retention metric.
This dual use is not always clear.
\end{rcomment}

We have added a dedicated notation table (Table~1, ll.~438--445) that
distinguishes the two uses explicitly: $K_0$ denotes the integer cardinality
of the held-out question set answered correctly at generation~0; $R(t) =
K_t/K_0$ denotes the retention ratio at generation~$t$. The symbols $R(t)$,
$d(t)$, and the efficiency numerator have been harmonised throughout
Equations~1--6 and the surrounding prose.

\msloc{Table~1 (tab:notation), ll.~438--445; Equations~1, 3, 5.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
$T$, $D_{1,T}$, $D_{10}$, $\Delta I$, $\mathrm{Instability}(1)$,
$\mathrm{MeanLen}_T$, and related symbols in Eq.~6 are not fully defined.
\end{rcomment}

All symbols in Eq.~6 (SDI-3) and its supporting quantities are now defined in
Table~1 (tab:notation) and in the inline text preceding the equations:
$T$ = number of generations evaluated; $D_{1,T}$ and $D_{10}$ = content
efficiency at generation~1 and generation~10; $\Delta I$ = absolute change in
content efficiency over the evaluation horizon; $\mathrm{Instability}(1)$ =
SDI-3 sub-score at the first generation; $\mathrm{MeanLen}_T$ = mean response
length averaged over all $T$ generations.

\msloc{Table~1 (tab:notation); prose preceding Eq.~6.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
The effective-rank formula uses $\sigma_i$ as both singular values and
normalised singular values. The normalisation condition is mathematically
incorrect as written.
\end{rcomment}

Corrected. Eq.~2 now defines $p_i = \sigma_i / \sum_j \sigma_j$ explicitly,
reserving $\sigma_i$ for the raw singular value throughout. The entropy is
computed over the normalised distribution $\{p_i\}$, consistent with
Table~1.

\msloc{Eq.~2 (erank definition); Table~1 (tab:notation).}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
$\|BA\|_F$, $\theta_i^{(t)}$, $\theta_i^{(0)}$, and related notation in
the drift equation are not consistently defined.
\end{rcomment}

Both quantities are now defined in Table~1 and at first use: $\|BA\|_F$
denotes the Frobenius norm of the LoRA reconstruction matrix, averaged across
adapted modules; $\theta_i^{(t)}$ and $\theta_i^{(0)}$ denote the $i$-th
parameter at generation $t$ and at generation~0. The mean absolute drift $d(t)$
in Eq.~3 is the mean over all $i$ of $|\theta_i^{(t)} - \theta_i^{(0)}|$.

\msloc{Table~1 (tab:notation); Eqs.~3--4 and surrounding prose.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
``$r \in \{4,10,12,14,16\}$'' and ``$r \approx \{10,12,14\}$'' are
garbled in the PDF; they should use clear set notation.
\end{rcomment}

The garbled rendering was a font-encoding artefact in the PDF generated from
the original submission. The revised manuscript uses the \texttt{lmodern}
package with T1 encoding throughout, which resolves all set-notation rendering.
The expressions now compile correctly as $r \in \{4, 10, 12, 14, 16\}$ and
$r \in \{10, 12, 14\}$.

\msloc{Preamble (lmodern + T1); all set-notation instances throughout.}

"""

content_new = content[:i1] + NEW_R21 + content[i2:]
with open(path, 'w', encoding='utf-8') as f:
    f.write(content_new)
print('OK — R2.1 aplicado.')
print(f'Tamanho anterior: {len(content)} | Novo: {len(content_new)}')
