# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\manuscript\manuscript-anonymous.tex'

with open(path, encoding='utf-8') as f:
    content = f.read()

OLD = r"""\begin{highlights}
\item \rev{Recursive degradation exhibits an abrupt, pressure-dependent transition within the tested grid}
\item Pressure thresholds differ by an order of magnitude across three backbone families
\item Adapter rank and learning rate interact to determine the operating regime
\item Output drift accompanies degradative regimes beyond factual retention loss
\item \rev{A pre-registered exposure dose--response shows that reducing synthetic training volume by 50\% arrests progressive degradation and matches the effect of halving the learning rate}
\end{highlights}"""

NEW = r"""\begin{highlights}
\item \rev{Rank-dependent threshold-like transition between homeostatic and degradative regimes}
\item \rev{Regime boundaries differ approximately ten-fold across backbones (effective rank ${\sim}3$--$6$ vs ${\sim}50$--$88$)}
\item \rev{Adapter rank and learning rate jointly determine the operating regime}
\item Output drift accompanies degradative regimes while factual retention stays bounded
\item \rev{A pre-registered 50\% synthetic exposure reduction arrests progressive loss on two backbones}
\end{highlights}"""

assert OLD in content, "Bloco não encontrado"
content_new = content.replace(OLD, NEW, 1)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content_new)

print("Highlights atualizados no .tex")
# verificar
i = content_new.find(r'\begin{highlights}')
j = content_new.find(r'\end{highlights}') + len(r'\end{highlights}')
print(content_new[i:j])
