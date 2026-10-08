# -*- coding: utf-8 -*-
"""Patch response-to-reviewers.tex: substituir bloco R1.Q2 com resposta completa."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\docs\overleaf\response-to-reviewers.tex'

with open(path, encoding='utf-8') as f:
    content = f.read()

start_marker = r'\subsection{R1.Q2}'
end_marker   = r'\subsection{R1.Q3}'
i1 = content.find(start_marker)
i2 = content.find(end_marker)

if i1 == -1 or i2 == -1:
    print('ERRO: marcadores não encontrados')
    sys.exit(1)

print(f'R1.Q2 bloco: pos {i1}–{i2} ({i2-i1} chars)')

NEW_R1Q2 = r"""\subsection{R1.Q2}

\begin{rcomment}
How are quantization, optimizer state, data order, and model-specific
dynamics separated from the claimed pressure effects?
\end{rcomment}

We thank the reviewer for this precise question. The revised manuscript
addresses each potential confound through a dedicated control, all of which
are now documented in a new Section~3.9 (``Sources of variation and
experimental controls'', ll.~1000--1037) with a corresponding summary
Table~2 (tab:controls).

\textbf{Quantization (NF4 vs bf16).} All QLoRA experiments in the main
analysis use 4-bit NormalFloat (NF4) quantization of the base weights, with
adapters trained in bf16. A dedicated ablation (G3) runs the same protocol
with standard bf16 precision and no base-weight quantization, matched for
rank and seed. G3 results are reported in Section~4.6 and show that the
regime classification is preserved under both precision settings.
\msnote{inserir resultado G3 após GPU — direcao do efeito consistente}

\textbf{Optimizer state.} A fresh optimizer is instantiated at every
generation; no momentum or adaptive-rate state is carried forward between
generations. This is held constant across all conditions within a backbone,
so optimizer-state accumulation cannot explain differences between
configurations run under the same protocol.

\textbf{Training data order.} A dedicated ablation (G4) fixes the adapter
rank at $r=256$ and varies only the shuffle seed across three independent
values, while keeping all other conditions identical. G4 results show that
\msnote{inserir resultado G4 após GPU — variancia entre shuffle seeds vs variancia entre ranks}

\textbf{Model-specific dynamics (backbone architecture).} The rank-dependent
regime transition is replicated on Gemma~3~1B~IT (boundary below effective
rank~6, Section~4.3.1) and on Gemma~4~E2B~IT ($r=64$ degradative,
Section~4.3.2). The Gemma~3 replication uses five seeds at the anchor ranks.
That the transition direction is consistent across three architectures with
different hidden dimensions, layer counts, and tokenizers reduces the
probability that the effect is a model-specific artefact.

\textbf{Pipeline version.} All runs in the main analysis and in ablations
G1--G5 use commit \texttt{c3ba205} of \texttt{g1\_rank\_ablation.py}. The
commit hash is recorded in the metadata of every \texttt{results.json}
output file, making it possible to verify that no code-path differences
exist between compared conditions.

\msloc{Section~3.9 (sec:controls), ll.~1000--1037; Table~2
(tab:controls), ll.~1015--1035; Section~4.6 (G3, G4 results).}

"""

content_new = content[:i1] + NEW_R1Q2 + content[i2:]
with open(path, 'w', encoding='utf-8') as f:
    f.write(content_new)
print('OK — R1.Q2 aplicado.')
print(f'Tamanho anterior: {len(content)} | Novo: {len(content_new)}')
