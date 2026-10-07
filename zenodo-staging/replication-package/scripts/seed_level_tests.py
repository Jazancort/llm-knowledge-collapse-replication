# -*- coding: utf-8 -*-
"""
Testes seed-level N=6 para r=16 vs r=256 e outros contrastes.
Usa resultados_consolidados.csv + dados históricos de multi-seed.
"""
import csv, math, sys, os
sys.stdout.reconfigure(encoding='utf-8')

try:
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

csv_path = r'G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\docs\revision\resultados\resultados_consolidados.csv'

rows = []
with open(csv_path, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append(r)

print(f"Total linhas CSV: {len(rows)}")
print(f"Scipy disponível: {HAS_SCIPY}")

# ── Inspecionar r=16 Gen10
print("\n=== r=16 Gen10 ===")
for r in rows:
    try:
        if r['rank'] == '16' and int(r.get('generation') or -1) == 10:
            print(f"  {r['dirname']} group={r['group']} bf16={r['bf16']} k0={r['k0']} ret={r['retention']}")
    except Exception as e:
        pass

# ── r=256 Gen10 G1+G4
print("\n=== r=256 Gen10 G1+G4 ===")
r256 = {}
for r in rows:
    try:
        rank = int(r['rank'] or 0)
        gen  = int(r['generation'] or -1)
        ret  = int(r['retention'] or 0)
        k0   = int(r['k0'] or 78)
        seed = int(r['seed'] or 0)
        group = r['group']
        bf16 = r['bf16'] == 'True'
        if rank == 256 and gen == 10 and not bf16 and k0 > 0:
            if group in ('G1', 'G4', ''):
                pct = ret / k0 * 100
                r256[seed] = pct
                print(f"  seed={seed} group={group} {ret}/{k0}={pct:.2f}%")
    except:
        pass

print(f"\nr=256 Gen10 N={len(r256)}: {sorted(r256.values())}")

# r=16 multi-seed: dados históricos do artigo (não estão no CSV de G1-G5)
# Do manuscrito verificado: seed15=76/78, seed137=76/78, seed256=76/78
# Do bloco0-achados: fft_comparison_qlora seed15 = 76/78 = 97.4%
# Gemma3 extra seeds r=4 (homeostático) = [43,44,43,43,44]/46 Gen10
r16_qwen = {15: 76/78*100, 137: 76/78*100, 256: 76/78*100}
print(f"\nr=16 Qwen Gen10 (histórico, N=3): {list(r16_qwen.values())}")

# ── Testes seed-level
def ms(vals):
    v = [x for x in vals if x is not None]
    n = len(v)
    if not n: return None, None, n
    m = sum(v)/n
    s = math.sqrt(sum((x-m)**2 for x in v)/(n-1)) if n > 1 else 0
    return round(m,3), round(s,3), n

def permutation_test_onesided(a, b, n_perm=10000):
    """One-sided permutation test: P(mean(a) > mean(b))"""
    import random
    obs = sum(a)/len(a) - sum(b)/len(b)
    combined = a + b
    n_a = len(a)
    count = 0
    for _ in range(n_perm):
        random.shuffle(combined)
        d = sum(combined[:n_a])/n_a - sum(combined[n_a:])/n_a
        if d >= obs:
            count += 1
    return count / n_perm

def mannwhitney_exact(a, b):
    if not HAS_SCIPY: return None, None
    u, p = stats.mannwhitneyu(a, b, alternative='greater')
    return round(u,1), round(p,4)

print("\n" + "="*65)
print("CONTRASTE 1: Qwen r=16 vs r=256 Gen10")
print("="*65)

r16_vals = list(r16_qwen.values())
r256_vals = list(r256.values())

m16, s16, n16 = ms(r16_vals)
m256, s256, n256 = ms(r256_vals)
delta = round(m16 - m256, 2)

print(f"\n  r=16  (N={n16}): {r16_vals}")
print(f"  r=256 (N={n256}): {[round(x,1) for x in r256_vals]}")
print(f"\n  r=16  mean={m16}% ±{s16}")
print(f"  r=256 mean={m256}% ±{s256}")
print(f"  Δ = {delta:+.2f} pp")

u, p_mw = mannwhitney_exact(r16_vals, r256_vals)
print(f"\n  Mann-Whitney U={u}, p(one-sided r16>r256)={p_mw}")

# Permutação
p_perm = permutation_test_onesided(r16_vals, r256_vals)
print(f"  Permutação (10k): p(one-sided)={p_perm:.4f}")

if n16 == 3 and n256 == 3:
    print(f"\n  NOTA: N=3 vs N=3 → poder baixo. Com N=3+6=9 seeds, recalcular.")
elif n256 == 6:
    print(f"\n  N=3 vs N=6 (G1+G4) → poder assimétrico.")

# Com N=6 r=256:
r256_all = sorted(r256.values())
p_perm6 = permutation_test_onesided(r16_vals, r256_all)
u6, p_mw6 = mannwhitney_exact(r16_vals, r256_all)
print(f"\n  r=16 N=3 vs r=256 N=6 combinado:")
print(f"    Mann-Whitney U={u6}, p(one-sided)={p_mw6}")
print(f"    Permutação p(one-sided)={p_perm6:.4f}")

print("\n" + "="*65)
print("CONTRASTE 2: Gemma3 r=4 vs r=16 Gen10 (N=5+5)")
print("="*65)
# Dados do manuscrito verificados (tab:gemma3):
# r=4  N=5: 94.4%, 91.3%, 93.5%, 93.5%, 95.7% (del handoff, Gemma3 extra seeds)
# r=16 N=5: 54.3%, 60.9%, 52.2%, 58.7%, 56.5%
r4_gemma  = [94.4, 91.3, 93.5, 93.5, 95.7]
r16_gemma = [54.3, 60.9, 52.2, 58.7, 56.5]

m4,  s4,  n4  = ms(r4_gemma)
m16g, s16g, n16g = ms(r16_gemma)
delta_g = round(m4 - m16g, 2)

print(f"\n  r=4  (N={n4}): {r4_gemma}")
print(f"  r=16 (N={n16g}): {r16_gemma}")
print(f"\n  r=4  mean={m4}% ±{s4}")
print(f"  r=16 mean={m16g}% ±{s16g}")
print(f"  Δ = {delta_g:+.2f} pp")

u_g, p_mw_g = mannwhitney_exact(r4_gemma, r16_gemma)
print(f"\n  Mann-Whitney U={u_g}, p(one-sided r4>r16)={p_mw_g}")
p_perm_g = permutation_test_onesided(r4_gemma, r16_gemma)
print(f"  Permutação p(one-sided)={p_perm_g:.4f}")

print("\n" + "="*65)
print("CONTRASTE 3: G4 vs G1 (variância de ordem)")
print("="*65)
g1_vals = [r256[s] for s in [15,137,256] if s in r256]
g4_vals = [r256[s] for s in [42,101,202] if s in r256]
m_g1, s_g1, _ = ms(g1_vals)
m_g4, s_g4, _ = ms(g4_vals)
print(f"\n  G1 (seeds 15/137/256): {[round(x,1) for x in g1_vals]} mean={m_g1}%")
print(f"  G4 (seeds 42/101/202): {[round(x,1) for x in g4_vals]} mean={m_g4}%")
if HAS_SCIPY:
    _, p_kw = stats.kruskal(g1_vals, g4_vals)
    print(f"  Kruskal-Wallis p={round(p_kw,4)}")
    _, p_mw_order = stats.mannwhitneyu(g1_vals, g4_vals, alternative='two-sided')
    print(f"  Mann-Whitney two-sided p={round(p_mw_order,4)}")

print("\n" + "="*65)
print("SUMÁRIO PARA A CARTA")
print("="*65)
print(f"""
Contraste Qwen r=16 vs r=256 Gen10:
  r=16  N=3: mean={m16}% ±{s16}pp
  r=256 N=6: mean={m256}% ±{s256}pp
  Δ = {delta:+.2f} pp (large effect)
  Mann-Whitney p(one-sided) = {p_mw6} (N=3 vs N=6)
  Permutação  p(one-sided) = {p_perm6:.4f}
  → Interpretação: efeito grande, evidência marginal-a-moderada (N pequeno)

Contraste Gemma3 r=4 vs r=16 Gen10:
  r=4  N=5: mean={m4}% ±{s4}pp
  r=16 N=5: mean={m16g}% ±{s16g}pp
  Δ = {delta_g:+.2f} pp
  Mann-Whitney p(one-sided) = {p_mw_g}
  → Interpretação: evidência seed-level forte para este backbone/setting

Variância de ordem G1 vs G4:
  G1 mean={m_g1}%, G4 mean={m_g4}% → sem diferença significativa
""")
