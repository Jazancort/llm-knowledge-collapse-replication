# -*- coding: utf-8 -*-
"""Patch Abstract com números finais e G5 parcial."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\manuscript\manuscript-anonymous.tex'

with open(path, encoding='utf-8') as f:
    content = f.read()

start = content.find(r'\begin{abstract}')
end   = content.find(r'\end{abstract}') + len(r'\end{abstract}')

NEW_ABSTRACT = r"""\begin{abstract}
Recursive fine-tuning on synthetic data enables scalable model adaptation.
However, recursively retraining models on their own outputs can progressively
degrade factual knowledge. The conditions under which recursive degradation
emerges, remains bounded, or can be reversed under parameter-efficient
fine-tuning remain poorly understood.
\rev{Through systematic dose-response experiments spanning three backbones
(Qwen~2.5~1.5B, Gemma~3~1B, and Gemma~4~E2B), ten recursive generations,
and three to six independent seeds for headline conditions (single seed for
intermediate ablations), we investigate how factual retention changes as
adapter capacity, perturbation magnitude, and synthetic exposure vary.}
These experiments reveal a common empirical organizing principle, which we
term effective training pressure. We find:
(1)~\rev{a threshold-like transition within the tested grid} from homeostatic
retention to progressive degradation as adapter rank increases, with the
transition differing by roughly an order of magnitude across architectures
(between effective ranks ${\sim}3$ and ${\sim}6$ on Gemma~3~1B versus 50--88 on Qwen);
(2)~\rev{full fine-tuning (FFT) and} learning-rate sweeps on both backbones
that are consistent with the same qualitative pattern, supporting the view
that the transition is not unique to low-rank adaptation;
(3)~a rank $\times$ learning-rate \rev{joint dependence} demonstrating that
update capacity and perturbation magnitude jointly determine the operating
regime rather than acting as independent axes;
(4)~a retention/distribution dissociation at intermediate pressure, where
output efficiency degrades threefold while factual retention remains near 90\%;
and (5)~\rev{pre-registered dose--response experiments on two backbones:
reducing synthetic exposure by 50\% arrests progressive degradation
(Qwen $r=256$: Gen~5$\to$10 slope $\BsevenSlopeFifty$\,pp/generation,
$\Delta\!=\!\BsevenDeltatenFifty$\,pp at Gen10; Gemma~3 $r=10$:
$\Delta\!=\!\GtwoDeltatenFifty$\,pp at Gen10) and, on Qwen, matches the effect
of halving the learning rate.
A pre-registered prospective test (three cells, one seed) confirms the
qualitative regime ordering of the operational ETP index; numerical threshold
calibration remains exploratory.}
These findings characterize recursive degradation as a pressure-dependent
phenomenon whose stability depends on a multidimensional control landscape,
providing an empirical basis for monitoring and configuring recursive training
pipelines.
\end{abstract}"""

content_new = content[:start] + NEW_ABSTRACT + content[end:]
with open(path, 'w', encoding='utf-8') as f:
    f.write(content_new)

print("Abstract reescrito OK")
# Contar rev{}
print(f"rev{{}} no .tex: {content_new.count(chr(92)+'rev{')}")
