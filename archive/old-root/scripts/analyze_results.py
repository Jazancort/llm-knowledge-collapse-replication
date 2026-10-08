# -*- coding: utf-8 -*-
"""
Análise dos resultados G1-G5 da revisão final.
Roda na Athena: uv run python scripts/analysis/analyze_revisao_final.py
"""
import json, os, glob, math, sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

BASE = os.path.expanduser('~/scratch/llm-knowledge-collapse/outputs')

# ─── helpers ────────────────────────────────────────────────────────────────

def load(path):
    with open(path) as f:
        return json.load(f)

def ret_pct(gens, gen_n, k0):
    g = next((x for x in gens if x.get('generation') == gen_n), None)
    if g and g.get('retention') is not None and k0:
        return round(g['retention'] / k0 * 100, 2)
    return None

def mean_std(vals):
    vals = [v for v in vals if v is not None]
    n = len(vals)
    if n == 0: return None, None, n
    m = sum(vals) / n
    s = math.sqrt(sum((x-m)**2 for x in vals) / (n-1)) if n > 1 else 0.0
    return round(m, 2), round(s, 2), n

def ci95(vals):
    vals = [v for v in vals if v is not None]
    n = len(vals)
    if n < 2: return None, None
    m = sum(vals) / n
    se = math.sqrt(sum((x-m)**2 for x in vals) / (n-1)) / math.sqrt(n)
    t = 3.182 if n == 3 else (2.776 if n == 4 else 2.571)  # t-crit 95% df=n-1
    return round(m - t*se, 2), round(m + t*se, 2)

def paired_ttest(a, b):
    a = [x for x in a if x is not None]
    b = [x for x in b if x is not None]
    if not HAS_SCIPY or len(a) != len(b) or len(a) < 2:
        return None
    _, p = stats.ttest_rel(a, b)
    return round(p, 4)

def slope(vals_gen5, vals_gen10, n_gens=5):
    pairs = [(a, b) for a, b in zip(vals_gen5, vals_gen10)
             if a is not None and b is not None]
    if not pairs: return None, None
    slopes = [(b - a) / n_gens for a, b in pairs]
    return mean_std(slopes)[:2]

# ─── G1: Qwen r=256 dose=0% ─────────────────────────────────────────────────
print("=" * 70)
print("G1 — Qwen r=256 dose=0% (pipeline consistency, N=3 seeds)")
print("=" * 70)

g1 = {}
for seed in [15, 137, 256]:
    path = f'{BASE}/g1_rank256_seed{seed}_G1_dose00/results.json'
    try:
        gens = load(path)
        k0 = gens[0].get('k0_total', gens[0].get('k0_size'))
        g1[seed] = dict(k0=k0,
                        gen5=ret_pct(gens, 5, k0),
                        gen10=ret_pct(gens, 10, k0),
                        raw5=next((x['retention'] for x in gens if x.get('generation')==5), None),
                        raw10=next((x['retention'] for x in gens if x.get('generation')==10), None),
                        curve=[next((x['retention'] for x in gens if x.get('generation')==i), None)
                               for i in range(11)])
        print(f"  seed{seed}: K0={k0}, Gen5={g1[seed]['raw5']}/{k0}={g1[seed]['gen5']}%, "
              f"Gen10={g1[seed]['raw10']}/{k0}={g1[seed]['gen10']}%")
    except Exception as e:
        print(f"  seed{seed}: ERRO — {e}")

vals5  = [g1[s]['gen5']  for s in g1]
vals10 = [g1[s]['gen10'] for s in g1]
m5, s5, _ = mean_std(vals5)
m10, s10, _ = mean_std(vals10)
lo5, hi5   = ci95(vals5)
lo10, hi10 = ci95(vals10)
ms, ss = slope(vals5, vals10)

print(f"\n  Gen5:  {m5}% ± {s5} pp  [95% CI {lo5}–{hi5}]")
print(f"  Gen10: {m10}% ± {s10} pp  [95% CI {lo10}–{hi10}]")
print(f"  Slope Gen5→10: {ms} ± {ss} pp/gen")

# Verificação vs canônicos do handoff
print(f"\n  VERIFICAÇÃO vs handoff (seed15: Gen5=83.5%, Gen10=75.9%):")
print(f"  seed15 Gen5={g1.get(15,{}).get('gen5')}% (esperado ~83.5%)  "
      f"{'OK' if g1.get(15,{}).get('gen5',0) > 82 else 'DIVERGE'}")
print(f"  seed15 Gen10={g1.get(15,{}).get('gen10')}% (esperado ~75.9%)  "
      f"{'OK' if g1.get(15,{}).get('gen10',0) > 74 else 'DIVERGE'}")

# ─── G2: Gemma3 r=10 dose-response ──────────────────────────────────────────
print()
print("=" * 70)
print("G2 — Gemma3 r=10 dose-response (N=3 seeds por dose)")
print("=" * 70)

doses = [0, 10, 25, 50]
seeds_g2 = [15, 137, 256]
g2 = {}

for dose in doses:
    g2[dose] = {}
    for seed in seeds_g2:
        path = f'{BASE}/g1_rank10_seed{seed}_G2_dose{dose}/results.json'
        try:
            gens = load(path)
            k0 = gens[0].get('k0_total', gens[0].get('k0_size'))
            g2[dose][seed] = dict(
                k0=k0,
                gen5=ret_pct(gens, 5, k0),
                gen10=ret_pct(gens, 10, k0),
                raw5=next((x['retention'] for x in gens if x.get('generation')==5), None),
                raw10=next((x['retention'] for x in gens if x.get('generation')==10), None)
            )
        except:
            g2[dose][seed] = None

b5  = [g2[0][s]['gen5']  for s in seeds_g2 if g2[0][s]]
b10 = [g2[0][s]['gen10'] for s in seeds_g2 if g2[0][s]]
mb5, _, _ = mean_std(b5)
mb10, _, _ = mean_std(b10)

print(f"\n  {'Dose':>5} | {'N':>2} | {'Gen5 mean':>10} {'±SD':>5} | {'Gen10 mean':>11} {'±SD':>5} | "
      f"{'ΔGen5':>7} | {'ΔGen10':>7} | {'p(5)':>6} | {'p(10)':>6}")
print("  " + "-"*88)

for dose in doses:
    d5  = [g2[dose][s]['gen5']  for s in seeds_g2 if g2[dose][s]]
    d10 = [g2[dose][s]['gen10'] for s in seeds_g2 if g2[dose][s]]
    if not d5: continue
    m5, s5, n = mean_std(d5)
    m10, s10, _ = mean_std(d10)
    delta5  = round(m5  - mb5,  2) if dose > 0 else 0.0
    delta10 = round(m10 - mb10, 2) if dose > 0 else 0.0
    p5  = paired_ttest(b5,  d5)  if dose > 0 else None
    p10 = paired_ttest(b10, d10) if dose > 0 else None
    d5s  = f'{delta5:+.1f}'  if dose > 0 else '—'
    d10s = f'{delta10:+.1f}' if dose > 0 else '—'
    p5s  = f'{p5:.3f}' if p5  else '—'
    p10s = f'{p10:.3f}' if p10 else '—'
    print(f"  {dose:>4}% | {n:>2} | {m5:>9.1f}% {s5:>4.1f} | {m10:>10.1f}% {s10:>4.1f} | "
          f"{d5s:>7} | {d10s:>7} | {p5s:>6} | {p10s:>6}")

# CI para dose=50% Gen10
d50_10 = [g2[50][s]['gen10'] for s in seeds_g2 if g2[50][s]]
lo, hi = ci95(d50_10)
m, _, n = mean_std(d50_10)
mb10_g2, _, _ = mean_std(b10)
d50_delta10 = round(m - mb10_g2, 2)
p50_10 = paired_ttest(b10, d50_10)
print(f"\n  dose=50% Gen10 detalhado:")
print(f"    {m}% 95%CI [{lo},{hi}], Δ={d50_delta10:+.1f} pp, p={p50_10}")

# Slopes
print(f"\n  Slope Gen5→Gen10 por dose (pp/gen):")
for dose in doses:
    d5  = [g2[dose][s]['gen5']  for s in seeds_g2 if g2[dose][s]]
    d10 = [g2[dose][s]['gen10'] for s in seeds_g2 if g2[dose][s]]
    ms, ss = slope(d5, d10)
    print(f"    dose={dose:>2}%: {ms:+.2f} ± {ss:.2f} pp/gen")

# ─── G3: NF4 vs bf16 ────────────────────────────────────────────────────────
print()
print("=" * 70)
print("G3 — Qwen NF4 vs bf16 (quantization control)")
print("=" * 70)

g3 = {}
for rank in [16, 256]:
    g3[rank] = {}
    for seed in [15, 137, 256]:
        path = f'{BASE}/g1_rank{rank}_seed{seed}_G3_bf16_r{rank}/results.json'
        try:
            gens = load(path)
            k0 = gens[0].get('k0_total', gens[0].get('k0_size'))
            g3[rank][seed] = dict(
                k0=k0,
                gen5=ret_pct(gens, 5, k0),
                gen10=ret_pct(gens, 10, k0)
            )
        except:
            g3[rank][seed] = None

for rank in [16, 256]:
    bf16_5  = [g3[rank][s]['gen5']  for s in [15,137,256] if g3[rank].get(s)]
    bf16_10 = [g3[rank][s]['gen10'] for s in [15,137,256] if g3[rank].get(s)]
    m5, s5, n = mean_std(bf16_5)
    m10, s10, _ = mean_std(bf16_10)
    nf4_5  = [g1[s]['gen5']  for s in [15,137,256] if s in g1]
    nf4_5_paired = nf4_5[:n]
    delta5 = round(m5 - sum(nf4_5_paired)/len(nf4_5_paired), 2) if nf4_5_paired else None
    p5 = paired_ttest(nf4_5_paired, bf16_5[:n]) if n >= 2 else None
    print(f"\n  r={rank} bf16 (N={n}): Gen5={m5}% ± {s5}, Gen10={m10}% ± {s10}")
    if delta5 is not None:
        print(f"    vs NF4: Δ Gen5 = {delta5:+.1f} pp"
              + (f", p={p5:.3f}" if p5 else "") + f"  n={n}")
        verdict = "Quantização NF4 não afeta classificação de regime" if abs(delta5) < 3 else "ATENÇÃO: diferença > 3 pp"
        print(f"    → {verdict}")

print()
print("=" * 70)
print("SUMÁRIO EXECUTIVO")
print("=" * 70)
m5g1, s5g1, _ = mean_std([g1[s]['gen5'] for s in g1])
m10g1, s10g1, _ = mean_std([g1[s]['gen10'] for s in g1])
ms_g1, _ = slope([g1[s]['gen5'] for s in g1], [g1[s]['gen10'] for s in g1])
print(f"\nG1 Qwen r=256 dose=0% (C1 pipeline novo, N=3):")
print(f"  Gen5={m5g1}% ± {s5g1}, Gen10={m10g1}% ± {s10g1}, slope={ms_g1} pp/gen")

d50_5  = [g2[50][s]['gen5']  for s in seeds_g2 if g2[50][s]]
d50_10 = [g2[50][s]['gen10'] for s in seeds_g2 if g2[50][s]]
md50_5,  _,  _ = mean_std(d50_5)
md50_10, _, _ = mean_std(d50_10)
ms50, _ = slope(d50_5, d50_10)
print(f"\nG2 Gemma3 r=10 dose=50% (N=3):")
print(f"  Gen5={md50_5}% ± {mean_std(d50_5)[1]}, Gen10={md50_10}% ± {mean_std(d50_10)[1]}, slope={ms50} pp/gen")
print(f"  Δ Gen5={round(md50_5-mb5,1):+.1f} pp, Δ Gen10={round(md50_10-mb10,1):+.1f} pp")
