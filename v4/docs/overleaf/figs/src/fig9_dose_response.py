# -*- coding: utf-8 -*-
"""
fig9_dose_response.py — Dose-response cross-backbone (Fig. 9)
Dados: G2 Gemma3 r=10 N=3 + Bloco7 Qwen r=256 N=5
Eixo Y: Δpp em relação ao baseline (Tipo 3 — linha y=0, sem zonas)
Segue STYLE_GUIDE.md do Intervention Window paper.
"""
import sys, math
sys.stdout.reconfigure(encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ── rcParams obrigatórios (STYLE_GUIDE) ──────────────────────────────────────
plt.rcParams.update({
    'font.family':      'sans-serif',
    'font.sans-serif':  ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size':        11,
    'axes.labelsize':   13,
    'axes.titlesize':   14,
    'xtick.labelsize':  11,
    'ytick.labelsize':  11,
    'legend.fontsize':  11,
    'figure.dpi':       150,
    'savefig.dpi':      300,
    'axes.linewidth':   1.0,
    'lines.linewidth':  2.0,
    'lines.markersize': 6,
    'axes.spines.top':   False,
    'axes.spines.right': False,
})

# ── Cores (STYLE_GUIDE cross-backbone) ───────────────────────────────────────
C_GEMMA = '#C0392B'   # vermelho — Gemma3
C_QWEN  = '#E67E22'   # laranja — Qwen

# ── Dados: Δpp Gen10 vs baseline por dose ────────────────────────────────────
# Bloco7 Qwen r=256 N=5 (make_all.py A7)
qwen_doses  = np.array([0, 10, 25, 50])
qwen_delta  = np.array([0.0, 1.8, 4.9, 9.2])   # Δpp Gen10 vs baseline (canônico manuscrito)
qwen_se     = np.array([0.0, 2.96, 2.45, 1.20])  # CI half-width / 1.96: doses 10%=[-1.1,4.7], 25%=[2.5,7.2], 50%=[6.9,11.6]

# G2 Gemma3 r=10 N=3 (make_all.py A8)
gemma_doses = np.array([0, 10, 25, 50])
gemma_delta = np.array([0.0, 9.8, 11.4, 12.9])  # Δpp Gen10 vs baseline
gemma_se    = np.array([0.0, 1.7, 2.9, 1.7])     # CI half-width / 1.96

# ── Figura ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))

# Tipo 3: linha de referência y=0 (sem zonas de retenção)
ax.axhline(y=0, color='#9CA3AF', linestyle='--', linewidth=1, alpha=0.6, zorder=1)

# Gemma3
ax.fill_between(gemma_doses, gemma_delta - gemma_se, gemma_delta + gemma_se,
                alpha=0.15, color=C_GEMMA)
ax.plot(gemma_doses, gemma_delta, '-o', color=C_GEMMA, linewidth=2.5,
        markersize=6, zorder=3)

# Qwen
ax.fill_between(qwen_doses, qwen_delta - qwen_se, qwen_delta + qwen_se,
                alpha=0.15, color=C_QWEN)
ax.plot(qwen_doses, qwen_delta, '-s', color=C_QWEN, linewidth=2.5,
        markersize=6, zorder=3)

# Direct labels (STYLE_GUIDE — 2 curvas com espaço à direita)
ax.text(51.5, gemma_delta[-1] + 0.3,
        'Gemma\u00a03 (r\u2009=\u200910)',
        fontsize=10, color=C_GEMMA, va='bottom', ha='left', fontweight='bold')
ax.text(51.5, qwen_delta[-1] - 0.4,
        'Qwen (r\u2009=\u2009256)',
        fontsize=10, color=C_QWEN, va='top', ha='left', fontweight='bold')

# Anotações dos p-valores
ax.annotate('p = 0.001',
            xy=(10, gemma_delta[1]), xytext=(10 - 4, gemma_delta[1] + 2.0),
            fontsize=8.5, color=C_GEMMA, ha='center',
            arrowprops=dict(arrowstyle='->', color=C_GEMMA, lw=0.8))
ax.annotate('p = 0.001',
            xy=(50, gemma_delta[3]), xytext=(50 - 5, gemma_delta[3] + 1.8),
            fontsize=8.5, color=C_GEMMA, ha='center',
            arrowprops=dict(arrowstyle='->', color=C_GEMMA, lw=0.8))
ax.annotate('p < 0.001',
            xy=(50, qwen_delta[3]), xytext=(38, qwen_delta[3] + 2.8),
            fontsize=8.5, color=C_QWEN, ha='center',
            arrowprops=dict(arrowstyle='->', color=C_QWEN, lw=0.8))

# Eixos
ax.set_xlabel('Synthetic exposure reduction (%)', fontweight='bold')
ax.set_ylabel('\u0394 Factual retention vs. baseline (pp)', fontweight='bold')
ax.set_xlim(-2, 70)
ax.set_ylim(-3, 17)
ax.set_xticks([0, 10, 25, 50])
ax.set_yticks([0, 5, 10, 15])

# Nota de rodapé
ax.text(0.98, 0.03,
        '\u0394Gen10 vs. unmodified baseline; error bands: 95% CI; n\u2009=\u20093\u20135 paired seeds',
        transform=ax.transAxes, fontsize=9, color='#555555',
        style='italic', ha='right', va='bottom')

plt.tight_layout()

# ── Salvar ───────────────────────────────────────────────────────────────────
out_dir = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\figs\final'

png_path = out_dir + r'\fig9_dose_response.png'
pdf_path = out_dir + r'\fig9_dose_response.pdf'

plt.savefig(png_path, bbox_inches='tight', dpi=300, facecolor='white')
plt.savefig(pdf_path, bbox_inches='tight', facecolor='white')
plt.close()

print(f'Salvo: {png_path}')
print(f'Salvo: {pdf_path}')

# Verificar DPI
from PIL import Image
img = Image.open(png_path)
print(f'PNG: {img.size[0]}x{img.size[1]}px  dpi={img.info.get("dpi", "N/A")}')
