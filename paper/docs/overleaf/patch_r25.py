# -*- coding: utf-8 -*-
"""Patch response-to-reviewers.tex: substituir bloco R2.5 com resposta completa."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\docs\overleaf\response-to-reviewers.tex'

with open(path, encoding='utf-8') as f:
    content = f.read()

start_marker = r'\subsection{R2.5'
# R2.5 é o último subsection — vai até o \end{document}
end_marker   = r'\end{document}'
i1 = content.find(start_marker)
i2 = content.rfind(end_marker)

if i1 == -1 or i2 == -1:
    print('ERRO: marcadores não encontrados')
    sys.exit(1)

print(f'R2.5 bloco: pos {i1}–{i2} ({i2-i1} chars)')

NEW_R25 = r"""\subsection{R2.5 --- Format and citations}

We thank the reviewer for auditing the reference list. Each issue has been
corrected as described below.

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
References [12] and [33] share the same arXiv number: arXiv:2408.14572.
\end{rcomment}

In the revised reference list the arXiv number 2408.14572 appears exactly
once, assigned to \citet{fawi2024curlora} (\textit{CURLoRA}, Fawi, 2024).
The duplicate entry that appeared in the submitted version has been removed.
The reference formerly numbered [33] in the submitted PDF was an artefact
of a bibliography management error; it is no longer present.

\msloc{References section (cas-refs.bib), entry \texttt{fawi2024curlora}.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
Reference [32] lists arXiv:2512.15634 with year 2024, which is impossible
if the arXiv ID is from December 2025.
\end{rcomment}

Corrected. The entry \texttt{ding2024ranktrade} (Rathore et al.) now carries
\texttt{year = \{2025\}}, consistent with the December~2025 arXiv submission
date. The paper appeared in the proceedings of AACL-IJCNLP 2025. The
\texttt{year = \{2024\}} in the submitted version was a transcription error
introduced when the preliminary arXiv preprint was first catalogued.

\msloc{References section, entry \texttt{ding2024ranktrade}.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
No citation is provided for Gemma~4 E2B IT, despite it being a central
backbone.
\end{rcomment}

A full citation has been added. The backbone is now cited as
\citet{gemma4_2026} (Gemma Team, 2026, arXiv:2607.02770) at every point
where it is introduced or described, including the experimental setup
(Section~3.3) and the cross-backbone results (Section~4.3). The model
architecture details (hidden dimension, layers, LoRA target modules) are
sourced from the same technical report.

\msloc{Section~3.3; Section~4.3; References entry \texttt{gemma4\_2026}.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
Reference [7] ``Keisha et al.'' is used heavily but appears to be a
preprint with no venue. Its reliability should be clarified.
\end{rcomment}

The entry \texttt{keisha2025} (Keisha et al., 2025) is a non-peer-reviewed
preprint (arXiv:2509.04796). This is now declared explicitly in the
bibliography note and in the text at first citation:
\revised{``\citet{keisha2025} (non-peer-reviewed preprint) report a
complementary observation...''}.
The paper is used for contextual framing only; no quantitative claim in our
manuscript depends exclusively on this source. We have added
\citet{shumailov2024} (published in \textit{Nature}) as the primary citation
for the model-collapse phenomenon wherever both sources were previously cited.

\msloc{First citation of \texttt{keisha2025}; References entry with
\texttt{note = \{arXiv:2509.04796. Non-peer-reviewed preprint\}}.}

% ─────────────────────────────────────────────────────────────────────────────
\begin{rcomment}
Reference formatting is inconsistent: some entries include conference
proceedings, others only arXiv, some lack page numbers or venues.
\end{rcomment}

The reference list has been audited and harmonised. Published works include
their full venue (journal or conference proceedings, volume, pages, DOI
where available). Works that exist only as arXiv preprints are formatted as
\texttt{arXiv preprint arXiv:XXXX.XXXXX} with the submission year. Entries
that had previously been submitted with incomplete venue data -- including
\texttt{ding2024ranktrade}, \texttt{fawi2024curlora}, and
\texttt{zibakhsh2024} -- have been completed. The full revised bibliography
is provided as \texttt{cas-refs.bib} in the submission package.

\msloc{References section (cas-refs.bib), all entries.}

"""

content_new = content[:i1] + NEW_R25 + content[i2:]
with open(path, 'w', encoding='utf-8') as f:
    f.write(content_new)
print('OK — R2.5 aplicado.')
print(f'Tamanho anterior: {len(content)} | Novo: {len(content_new)}')
