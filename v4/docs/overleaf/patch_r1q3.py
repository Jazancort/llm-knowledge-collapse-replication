# -*- coding: utf-8 -*-
"""Patch response-to-reviewers.tex: substituir bloco R1.Q3 com resposta completa."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\docs\overleaf\response-to-reviewers.tex'

with open(path, encoding='utf-8') as f:
    content = f.read()

start_marker = r'\subsection{R1.Q3}'
end_marker   = r'\subsection{R1.Q4}'
i1 = content.find(start_marker)
i2 = content.find(end_marker)

if i1 == -1 or i2 == -1:
    print('ERRO: marcadores não encontrados')
    sys.exit(1)

print(f'R1.Q3 bloco: pos {i1}–{i2} ({i2-i1} chars)')

NEW_R1Q3 = r"""\subsection{R1.Q3}

\begin{rcomment}
Do the conclusions hold for longer answers, multi-hop questions, other
domains, and larger factual evaluation sets?
\end{rcomment}

We thank the reviewer for this question, which targets the external validity
of our findings. We address the three distinct concerns it raises: the
evaluation metric, the dataset scope, and the extension to other domains.

\textbf{Evaluation metric and verbosity bias.}
The primary metric uses a bidirectional substring criterion: a generated
response is counted as correct if it contains any valid answer alias, or if
any alias contains the response. This criterion is intentionally permissive
to handle short-answer variation and aliasing in TriviaQA-style factoid
questions. However, as the reviewer correctly anticipates, configurations
that generate longer responses may receive inflated retention scores because
a longer string is more likely to contain a short alias by chance.

To address this concern, we performed a strict exact-match re-evaluation on
the saved predictions for all reported conditions. Under the strict scorer,
absolute retention values are lower, but the direction of every regime
classification is unchanged: configurations classified as Homeostatic,
Bounded, or Degradative retain those classifications under strict scoring.
This re-evaluation is reported in supplementary Table~S2 and is discussed
in Section~6 (ll.~2181--2193).

\msloc{Section~6, ll.~2181--2193; supplementary Table~S2.}

\textbf{Dataset scope: single dataset, short factoid answers.}
TriviaQA was chosen specifically to isolate factual retention from
reasoning or stylistic confounds. Short answers minimise format-dependent
evaluation noise, and the substring criterion is resilient to verbosity
changes. These are methodological advantages for studying the retention
question in isolation, not limitations of the phenomenon. The limitation
is that the findings may not transfer to long-form generation, multi-hop
reasoning, open-ended dialogue, or code synthesis, where output structure
and evaluation criteria differ substantially. This scope restriction is
stated explicitly in Section~6 (ll.~2094--2100).

\msloc{Section~6, ll.~2094--2100.}

\textbf{Larger factual evaluation sets.}
The held-out evaluation set contains 200 questions, of which $K_0 \in
\{78\text{--}79\}$ are answered correctly at generation~0 for the Qwen
backbone. The set size is constrained by the recursive protocol: because
the same questions are used both for evaluation and as the source of
synthetic training questions, a larger set would proportionally increase
training data volume and alter the exposure conditions. Extending to a
larger evaluation set is a natural direction for future work and is
mentioned in Section~6. The current set is consistent with comparable
prior studies \citep{shumailov2024,keisha2025} and is sufficient to
characterise regime-level differences across conditions.

\msloc{Section~6, ll.~2094--2100; Section~3.1 (evaluation protocol).}

"""

content_new = content[:i1] + NEW_R1Q3 + content[i2:]
with open(path, 'w', encoding='utf-8') as f:
    f.write(content_new)
print('OK — R1.Q3 aplicado.')
print(f'Tamanho anterior: {len(content)} | Novo: {len(content_new)}')
