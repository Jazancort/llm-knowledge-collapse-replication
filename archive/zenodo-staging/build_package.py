# -*- coding: utf-8 -*-
"""
Copia os artefatos para o staging e gera MANIFEST.md com SHA-256.
Executar a partir de qualquer diretório.
"""
import sys, hashlib, shutil, datetime
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)')
V4   = BASE / 'v4'
STAGE = BASE / 'zenodo-staging' / 'replication-package'

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()[:16]  # primeiros 16 chars para legibilidade

def copy(src, dst_rel):
    """Copia src para STAGE/dst_rel, criando pastas se necessário."""
    dst = STAGE / dst_rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst

# ── Mapa: destino_relativo → origem ─────────────────────────────────────────
files = {
    # Manuscrito
    'manuscript/manuscript-anonymous.tex': V4 / 'manuscript/manuscript-anonymous.tex',
    'manuscript/cas-refs.bib':             V4 / 'manuscript/cas-refs.bib',

    # Carta de resposta
    'response/response-to-reviewers.tex':  V4 / 'docs/overleaf/response-to-reviewers.tex',

    # Dados
    'data/results-G1-G5.csv':             V4 / 'docs/revision/resultados/resultados_consolidados.csv',
    'data/results-G1-G5-summary.md':      V4 / 'docs/revision/resultados/resultados-revisao-final.md',
    'data/results-bloco7.md':             V4 / 'docs/revision/resultados/resultados-bloco7.md',
    'data/numbers-canonical.csv':         V4 / 'docs/revision/resultados/make_all_outputs/numbers.csv',
    'data/numbers-canonical.tex':         V4 / 'docs/revision/resultados/make_all_outputs/numbers.tex',
    'data/verify.txt':                    V4 / 'docs/revision/resultados/make_all_outputs/verify.txt',

    # Scripts principais
    'scripts/make_all.py':                V4 / 'scripts/analysis/make_all.py',
    'scripts/analyze_results.py':         V4 / 'scripts/analysis/analyze_revisao_final.py',
    'scripts/seed_level_tests.py':        V4 / 'scripts/analysis/seedlevel_tests.py',
    'scripts/check_consistency.py':       V4 / 'scripts/analysis/check_state.py',

    # Script figura
    'scripts/figures/fig9_dose_response.py': V4 / 'figs/src/fig9_dose_response.py',
}

# Figuras finais
for fig in sorted((V4 / 'figs/final').glob('*.png')):
    files[f'figures/{fig.name}'] = fig

# ── Copiar ───────────────────────────────────────────────────────────────────
print("Copiando arquivos...")
copied = []
for dst_rel, src in files.items():
    if not src.exists():
        print(f"  AVISO — não encontrado: {src}")
        continue
    dst = copy(src, dst_rel)
    h = sha256(dst)
    size_kb = round(dst.stat().st_size / 1024, 1)
    copied.append((dst_rel, h, size_kb))
    print(f"  ✓ {dst_rel}  ({size_kb} KB)")

# ── Gerar MANIFEST.md ────────────────────────────────────────────────────────
sections = {
    'Manuscript source': [r for r in copied if r[0].startswith('manuscript/')],
    'Reviewer response': [r for r in copied if r[0].startswith('response/')],
    'Data': [r for r in copied if r[0].startswith('data/')],
    'Analysis scripts': [r for r in copied if r[0].startswith('scripts/') and not r[0].startswith('scripts/figures')],
    'Figure scripts': [r for r in copied if r[0].startswith('scripts/figures')],
    'Figures': [r for r in copied if r[0].startswith('figures/')],
}

manifest = f"""# Artifact Manifest

**Package:** KNOSYS-D-26-21490 Replication Package  
**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} UTC-3  
**Total files:** {len(copied)}

SHA-256 values are truncated to 16 characters for readability.
Full hashes can be recomputed with `sha256sum` or `certutil -hashfile <file> SHA256`.

---

"""

for section, rows in sections.items():
    if not rows:
        continue
    manifest += f"## {section}\n\n"
    manifest += "| File | SHA-256 (first 16) | Size |\n"
    manifest += "|------|--------------------|------|\n"
    for dst_rel, h, size_kb in rows:
        manifest += f"| `{dst_rel}` | `{h}` | {size_kb} KB |\n"
    manifest += "\n"

manifest += """---

## Reproducing the verification

```bash
# 1. Check all canonical numbers
python scripts/make_all.py
# Expected output: "TODOS OK" with 0 FAILs

# 2. Regenerate Fig. 9
python scripts/figures/fig9_dose_response.py
# Output: figures/fig9_dose_response.png

# 3. Compile manuscript (requires LaTeX with xelatex + bibtex)
cd manuscript
xelatex manuscript-anonymous.tex
bibtex  manuscript-anonymous
xelatex manuscript-anonymous.tex
xelatex manuscript-anonymous.tex
```
"""

manifest_path = STAGE / 'MANIFEST.md'
manifest_path.write_text(manifest, encoding='utf-8')
print(f"\nMANIFEST.md gerado: {manifest_path}")
print(f"Total: {len(copied)} arquivos copiados")
