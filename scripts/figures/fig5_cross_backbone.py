"""
fig5_cross_backbone.py — regenerate Fig.5 (cross-backbone scatter)
with full regime labels: Homeostatic / Bounded / Degradative

Data from manuscript tables (Tab.4, Tab.6, Tab.7, Tab.8).
Run: python scripts/figures/fig5_cross_backbone.py
Output: v4/manuscript/figs/final/fig5_cross_backbone.{png,pdf,svg}
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ── rcParams (Style Guide) ─────────────────────────────────────────────────
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
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# ── Data ───────────────────────────────────────────────────────────────────
# (erank, retention_pct, marker, color, backbone)
# Qwen 2.5 1.5B — Tab.4 (Gen10 except r=4,32 at Gen5)
qwen = [
    (3.34,  97.4),   # r=4   Gen5
    (11.08, 96.2),   # r=16  Gen10
    (17.85, 96.2),   # r=32  Gen5
    (29.52, 92.3),   # r=64  Gen10
    (50.16, 89.7),   # r=128 Gen10
    (87.57, 79.7),   # r=256 Gen10  (mean 6 seeds)
]

# Gemma 3 1B — Tab.6 (Gen10 for anchors, Gen5 for intermediates)
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
    (5.1,   88.2),   # r=16
    (13.3,  75.0),   # r=64
]

# ── Colors ─────────────────────────────────────────────────────────────────
C_QWEN   = '#2980B9'   # blue
C_GEMMA3 = '#E67E22'   # orange
C_E2B    = '#E6C117'   # gold/yellow

# Regime zone colors
C_HOMEO  = '#E8F6F3'   # green tint  >90%
C_BOUND  = '#FEF9E7'   # yellow tint 80-90%
C_DEGRAD = '#FDEDEC'   # red tint    <80%

# ── Figure ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 5.5))

# Regime zones (horizontal bands)
ax.axhspan(90, 102, alpha=0.55, color=C_HOMEO,  zorder=0)
ax.axhspan(80,  90, alpha=0.55, color=C_BOUND,  zorder=0)
ax.axhspan(44,  80, alpha=0.55, color=C_DEGRAD, zorder=0)

# Regime boundary dashed lines
ax.axhline(90, color='#2ECC71', linestyle='--', linewidth=0.9, alpha=0.7, zorder=1)
ax.axhline(80, color='#E74C3C', linestyle='--', linewidth=0.9, alpha=0.7, zorder=1)

# Regime labels (FULL names)
ax.text(0.98, 0.965, 'Homeostatic', transform=ax.transAxes,
        ha='right', va='top', fontsize=10, color='#1A8762', fontweight='bold')
ax.text(0.98, 0.680, 'Bounded', transform=ax.transAxes,
        ha='right', va='top', fontsize=10, color='#D4AC0D', fontweight='bold')
ax.text(0.98, 0.430, 'Degradative', transform=ax.transAxes,
        ha='right', va='top', fontsize=10, color='#C0392B', fontweight='bold')

# Scatter plots
qx, qy = zip(*qwen)
gx, gy = zip(*gemma3)
ex, ey = zip(*e2b)

ax.scatter(qx, qy, s=90, color=C_QWEN,   marker='o', zorder=3, label='Qwen 2.5 1.5B',  edgecolors='white', linewidths=0.5)
ax.scatter(gx, gy, s=90, color=C_GEMMA3, marker='s', zorder=3, label='Gemma 3 1B',     edgecolors='white', linewidths=0.5)
ax.scatter(ex, ey, s=90, color=C_E2B,    marker='^', zorder=3, label='Gemma 4 E2B',    edgecolors='white', linewidths=0.5)

# ── Axes ───────────────────────────────────────────────────────────────────
ax.set_xscale('log')
ax.set_xlim(1.5, 150)
ax.set_ylim(44, 102)
ax.set_xlabel('Mean Effective Rank', fontweight='bold')
ax.set_ylabel('$K_0$ Retention at Gen10 (%)', fontweight='bold')
ax.set_yticks([50, 60, 70, 80, 90, 100])
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
    lambda x, _: f'{x:.0f}' if x >= 1 else f'{x:.1f}'))

# Legend
ax.legend(loc='lower left', frameon=False, fontsize=10)

plt.tight_layout()

# ── Save ───────────────────────────────────────────────────────────────────
base = Path(__file__).parents[2]
out_dir = base / 'v4' / 'manuscript' / 'figs' / 'final'
out_dir.mkdir(parents=True, exist_ok=True)

for fmt in ['png', 'pdf', 'svg']:
    out = out_dir / f'fig5_cross_backbone.{fmt}'
    plt.savefig(str(out), bbox_inches='tight', facecolor='white')
    print(f'Saved: {out}')

plt.close()
print('Done.')
