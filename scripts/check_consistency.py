# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

tex_path   = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\manuscript\manuscript-anonymous.tex'
carta_path = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\docs\overleaf\response-to-reviewers.tex'
make_out   = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\docs\revision\resultados\make_all_outputs\verify.txt'

with open(tex_path,   encoding='utf-8') as f: tex   = f.read()
with open(carta_path, encoding='utf-8') as f: carta = f.read()
with open(make_out,   encoding='utf-8') as f: ver   = f.read()

print("=== ESTADO ATUAL ===")
print()
print("CARTA:")
msnote = carta.count(r'\msnote{inserir resposta}')
print("  msnote restantes:  " + str(msnote) + ("  ✅" if msnote == 0 else "  ❌"))

print()
print("MANUSCRITO:")
rev_c = tex.count(r'\rev{')
print("  rev{} no .tex:     " + str(rev_c))

# refs quebradas
flat = tex.replace('\n', ' ')
all_labels = set(re.findall(r'\\label\{([^}]+)\}', flat))
all_refs   = re.findall(r'\\ref\{([^}]+)\}', flat)
broken     = sorted(set(r for r in all_refs if r not in all_labels))
if broken:
    print("  Refs quebradas (" + str(len(broken)) + "):")
    for b in broken:
        print("    - " + b)
else:
    print("  Refs quebradas:    nenhuma  ✅")

# labels críticos
critical = ['sec:res_intervention', 'sec:controls', 'sec:pressure',
            'app:repo', 'sec:statistics', 'sec:res_capacity',
            'sec:limitations', 'sec:intervention']
print()
print("  Labels críticos:")
for s in critical:
    ok = ('label{' + s + '}') in tex
    tag = "  ✅" if ok else "  ❌ FALTA"
    print("    " + s + ": " + tag)

print()
print("MAKE_ALL:")
fails = ver.count('[FAIL]')
print("  FAILs: " + str(fails) + ("  ✅" if fails == 0 else "  ❌"))

print()
print("PENDÊNCIAS DA FASE 4 (reescrita §4.1-4.7, Abstract):")
# Verificar se os números do make_all estão no .tex
macros_to_check = [r'\GoneMten', r'\GtwoDeltatenFifty', r'\BsevenDeltatenFifty',
                   r'\GthreeDeltaRanks', r'\GoneFourMten']
for m in macros_to_check:
    present = m in tex
    print("  " + m + ": " + ("no .tex ✅" if present else "NÃO no .tex ⚠️ (Fase 4 pendente)"))
