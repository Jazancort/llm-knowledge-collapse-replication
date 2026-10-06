"""
fig5_cross_backbone.py — regenerate Fig.5 (cross-backbone scatter)
Follows the Intervention Window STYLE_GUIDE.md exactly.

Run: python scripts/figures/fig5_cross_backbone.py
Output: v4/manuscript/figs/final/fig5_cross_backbone.{png,pdf,svg}
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

# ── rcParams OBRIGATÓRIOS (Style Guide) ────────────────────────────────────
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 11,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'axes.linewidth': 1.0,
    'lines.linewidth': 2.0,
    'lines.markersize': 6,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# ── Paleta canônica (Style Guide) ──────────────────────────────────────────
C_QWEN   = '#2980B9'   # azul    — backbone primário
C_GEMMA3 = '#C0392B'   # vermelho escuro — Gemma baseline
C_E2B    = '#E67E22'   # laranja — terceiro backbone

# Zonas de retenção (Style Guide: alpha=0.6, zorder=0)
C_HOMEOSTATIC = '#E8F6F3'
C_BOUNDED     = '#FEF9E7'
C_DEGRADATIVE = '#FDEDEC'

# ── Dados (das tabelas do manuscrito) ──────────────────────────────────────
# (erank, retention_pct)
# Qwen 2.5 1.5B — Tab.4 (Gen10 exceto r=4,32 em Gen5)
qwen = [
    (3.34,  97.4),   # r=4   Gen5
    (11.08, 96.2),   # r=16  Gen10
    (17.85, 96.2),   # r=32  Gen5
    (29.52, 92.3),   # r=64  Gen10
    (50.16, 89.7),   # r=128 Gen10 (Bounded)
    (87.57, 79.7),   # r=256 Gen10 (Degradative; média 6 sementes)
]

# Gemma 3 1B — Tab.6 (Gen10 para âncoras, Gen5 para intermediários)
gemma3 = [
    (3.07,  94.4),   # r=4   Gen10
    (6.37,  78.3),   # r=10  Gen5
    (7.35,  73.9),   # r=12  Gen5
    (8.37,  69.6),   # r=14  Gen5
    (9.17,  56.5),   # r=16  Gen10
]

# Gemma 4 E2B — Tab.7 (Gen10, single seed)
e2b = [
    (2.04,  94.7),   # r=4
    (5.1,   88.2),   # r=16 (Bounded)
    (13.3,  75.0),   # r=64 (Degradative)
]

# ── Figura ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))

# Zonas de retenção (Tipo 1: eixo Y = retenção absoluta %)
# Thresholds específicos deste estudo: >90% homeostático, 80-90% bounded, <80% degradativo
ax.axhspan(90, 102, alpha=0.6, color=C_HOMEOSTATIC, zorder=0)
ax.axhspan(80,  90, alpha=0.6, color=C_BOUNDED,     zorder=0)
ax.axhspan(44,  80, alpha=0.6, color=C_DEGRADATIVE,  zorder=0)

# Linhas de fronteira
ax.axhline(90, color='#2ECC71', linestyle='--', linewidth=0.9, alpha=0.7, zorder=1)
ax.axhline(80, color='#E74C3C', linestyle='--', linewidth=0.9, alpha=0.7, zorder=1)

# Labels de zona (nomes completos)
ax.text(0.98, 0.967, 'Homeostatic', transform=ax.transAxes,
        ha='right', va='top', fontsize=10, color='#1A8762', fontweight='bold')
ax.text(0.98, 0.685, 'Bounded', transform=ax.transAxes,
        ha='right', va='top', fontsize=10, color='#B7950B', fontweight='bold')
ax.text(0.98, 0.430, 'Degradative', transform=ax.transAxes,
        ha='right', va='top', fontsize=10, color='#C0392B', fontweight='bold')

# Scatter plots
qx, qy   = zip(*qwen)
gx, gy   = zip(*gemma3)
ex, ey   = zip(*e2b)

ax.scatter(qx, qy, s=80, color=C_QWEN,   marker='o', zorder=3,
           label='Qwen 2.5 1.5B',  edgecolors='white', linewidths=0.5)
ax.scatter(gx, gy, s=80, color=C_GEMMA3, marker='s', zorder=3,
           label='Gemma 3 1B',     edgecolors='white', linewidths=0.5)
ax.scatter(ex, ey, s=80, color=C_E2B,    marker='^', zorder=3,
           label='Gemma 4 E2B',    edgecolors='white', linewidths=0.5)

# ── Eixos ──────────────────────────────────────────────────────────────────
ax.set_xscale('log')
ax.set_xlim(1.5, 150)
ax.set_ylim(44, 102)
ax.set_xlabel('Mean Effective Rank', fontweight='bold')
ax.set_ylabel('$K_0$ Retention at Gen10 (%)', fontweight='bold')
ax.set_yticks([50, 60, 70, 80, 90, 100])
ax.xaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: str(int(x)) if x >= 1 else f'{x:.1f}'))

# ── Legenda SEMPRE abaixo (Style Guide) ────────────────────────────────────
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12),
          ncol=3, frameon=False)

plt.tight_layout()
plt.subplots_adjust(bottom=0.18)

# ── Salvar ─────────────────────────────────────────────────────────────────
base = Path(__file__).parents[2]
out_dir = base / 'v4' / 'manuscript' / 'figs' / 'final'
out_dir.mkdir(parents=True, exist_ok=True)

for fmt in ['pdf', 'png', 'svg']:
    out = out_dir / f'fig5_cross_backbone.{fmt}'
    plt.savefig(str(out), bbox_inches='tight', facecolor='white')
    print(f'Saved: {out}  ({out.stat().st_size//1024} KB)')

plt.close()
print('Done.')
