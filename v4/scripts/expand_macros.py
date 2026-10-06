#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
expand_macros.py - Pre-expande todos os macros numericos do manuscrito
antes de converter para docx via pandoc.

Produz: manuscript-expanded.tex (nao modifica o original)
"""
import re
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
TEX  = ROOT / "manuscript" / "manuscript-anonymous.tex"
OUT  = ROOT / "manuscript" / "manuscript-expanded.tex"
NUMS = ROOT / "docs" / "overleaf" / "numbers.tex"


def parse_macros(src):
    # Regex sem docstring com backslash - usa raw string
    pat = re.compile(
        r'\\(?:new|renew)command\s*\{\\([A-Za-z]+)\}\s*\{([^{}]*)\}',
        re.MULTILINE
    )
    macros = {}
    for m in pat.finditer(src):
        name = m.group(1)
        val  = m.group(2).strip()
        macros[name] = val
    return macros


def expand(text, macros):
    # Ordenar por comprimento decrescente para evitar substituicao parcial
    for name in sorted(macros, key=len, reverse=True):
        val = macros[name]
        # Usar lambda para evitar interpretacao do val como regex replacement
        pat = re.compile(r'\\' + re.escape(name) + r'(?![A-Za-z])')
        text = pat.sub(lambda m, v=val: v, text)
    return text


if __name__ == "__main__":
    print(f"Lendo macros de {NUMS.name} ...")
    nums_src = NUMS.read_text(encoding="utf-8")
    macros_nums = parse_macros(nums_src)
    print(f"  {len(macros_nums)} macros em numbers.tex")

    print(f"Lendo manuscrito ...")
    tex_src = TEX.read_text(encoding="utf-8")
    macros_tex = parse_macros(tex_src)
    print(f"  {len(macros_tex)} macros no manuscrito")

    # numbers.tex tem precedencia (valores calculados vs redefinicoes locais)
    all_macros = {**macros_tex, **macros_nums}
    print(f"Total: {len(all_macros)} macros para expandir")

    expanded = expand(tex_src, all_macros)

    OUT.write_text(expanded, encoding="utf-8")
    print(f"Escrito: {OUT}")
    print(f"  Original: {len(tex_src):,} chars")
    print(f"  Expandido: {len(expanded):,} chars")

    # Verificar quantos macros ainda nao foram expandidos
    remaining = re.findall(r'\\[A-Z][a-zA-Z]{3,}(?![A-Za-z])', expanded)
    unique_rem = set(remaining)
    print(f"  Macros nao-expandidos restantes: {len(remaining)} ({len(unique_rem)} unicos)")
    for m in sorted(unique_rem)[:20]:
        print(f"    {m}")
