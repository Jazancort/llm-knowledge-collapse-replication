#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifica na carta cada trecho ENTRE ASPAS (dentro de \\newtext{}) contra o
.tex do manuscrito. So as citacoes com marcas de citacao (``...'' ou "...")
precisam existir no manuscrito; texto azul sem aspas e novo texto da carta.

Regra do utilizador: "Só ficam entre aspas frases que existem no manuscrito."
"""
import re, pathlib

ROOT = pathlib.Path(__file__).parent.parent
RES  = (ROOT / "docs/overleaf/response-to-reviewers.tex").read_text(encoding="utf-8")
MAN  = (ROOT / "manuscript/manuscript-anonymous.tex").read_text(encoding="utf-8")

def clean_latex(text):
    """Normaliza texto LaTeX para comparacao aproximada."""
    t = re.sub(r'\\rev\{([^}]*)\}', r'\1', text)        # expand \rev{}
    t = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?\{([^}]*)\}', r'\2', t)  # \cmd{x} -> x
    t = re.sub(r'\\[a-zA-Z]+', ' ', t)                   # \cmd -> space
    t = re.sub(r'[{}~\\$&%#_^`]', ' ', t)               # chars latex
    t = re.sub(r"''|``|\"", ' ', t)                      # quote chars
    t = re.sub(r'\s+', ' ', t)
    return t.strip().lower()

man_clean = clean_latex(MAN)

# Extrair blocos \newtext{...}
newtext_re = re.compile(r'\\newtext\{(.*?)\}', re.DOTALL)

# Dentro de cada newtext, extrair texto entre aspas: "..." ou ``...''
quoted_re = re.compile(r'(?:``|")(.+?)(?:\'\'|")', re.DOTALL)

not_found = []
checked = 0
for m in newtext_re.finditer(RES):
    inner = m.group(1)
    for qm in quoted_re.finditer(inner):
        quoted_text = qm.group(1)
        cleaned = clean_latex(quoted_text)
        needle = cleaned[:60].strip()
        if len(needle) < 10:
            continue
        checked += 1
        if needle not in man_clean:
            ctx_start = max(0, m.start() - 60)
            ctx = RES[ctx_start:m.start()+80].replace('\n', ' ')
            not_found.append((needle, ctx))

print(f"Citacoes com aspas verificadas: {checked}")
print(f"NAO encontradas no manuscrito:  {len(not_found)}")
if not_found:
    for needle, ctx in not_found:
        print(f"\n  MISSING: {needle!r}")
        print(f"  CTX: ...{ctx[:90]}...")
else:
    print("\n  Todas as citacoes azuis com aspas existem no manuscrito. OK")
