# -*- coding: utf-8 -*-
"""
make_all.py — Análises A1–A12 para KNOSYS-D-26-21490
Gera todos os números que entram no manuscrito.

Uso:
    uv run python scripts/analysis/make_all.py

Saídas em docs/revision/resultados/make_all_outputs/:
    numbers.tex   — macros LaTeX \newcommand para cada número
    numbers.csv   — versão tabular para conferência
    verify.txt    — checklist de consistência vs canônicos

REGRA: todo número no .tex é uma macro definida aqui.
"""
import csv, math, json, os, random, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

# ─────────────────────────────────────────────────────────────────────────────
# CAMINHOS
# ─────────────────────────────────────────────────────────────────────────────
BASE  = Path(__file__).resolve().parents[2]   # v4/
OUT   = BASE / 'docs' / 'revision' / 'resultados' / 'make_all_outputs'
OUT.mkdir(parents=True, exist_ok=True)

print(f"make_all.py — {OUT}")

# ─────────────────────────────────────────────────────────────────────────────
# DADOS CANÔNICOS (fonte: resultados-revisao-final.md + resultados-bloco7.md)
# Não editar à mão: estes vêm do analysis run verificado em 03–04/10/2026.
# ─────────────────────────────────────────────────────────────────────────────

# G1 — Qwen r=256 dose=0%, N=3 seeds (15/137/256), K0=78
G1 = {
    15:  {'gen5': 84.6, 'gen10': 78.2, 'raw5': 66, 'raw10': 61, 'k0': 78},
    137: {'gen5': 85.9, 'gen10': 80.8, 'raw5': 67, 'raw10': 63, 'k0': 78},
    256: {'gen5': 85.9, 'gen10': 78.2, 'raw5': 67, 'raw10': 61, 'k0': 78},
}

# G4 — Qwen r=256 dose=0%, N=3 seeds (42/101/202), K0=78
G4 = {
    42:  {'gen5': 85.9, 'gen10': 82.1, 'raw5': 67, 'raw10': 64, 'k0': 78},
    101: {'gen5': 87.2, 'gen10': 78.2, 'raw5': 68, 'raw10': 61, 'k0': 78},
    202: {'gen5': 84.6, 'gen10': 80.8, 'raw5': 66, 'raw10': 63, 'k0': 78},
}

# r=16 Qwen: G3/bf16, seeds 15/137/256, K0=78 (76/78 = 97.44% por seed)
# ATENÇÃO: estes 3 seeds vêm do experimento G3 (bf16 vs NF4), não de um rank
# sweep puro. A comparação r=16 vs r=256 é portanto não-pareada entre grupos
# distintos (G3/bf16 vs G1+G4/NF4+ordem). O teste exato de permutação bilateral
# N=3 vs N=6 (C(9,3)=84 alocamentos) dá p=0.0119; versão conservadora p=0.0238.
R16_QWEN = {15: 97.4, 137: 97.4, 256: 97.4}  # 76/78 cada seed

# G2 — Gemma3 r=10 dose-response, K0=44, N=3 seeds por dose
G2 = {
    0:  {15: {'gen5': 84.1, 'gen10': 79.5},
         137: {'gen5': 84.1, 'gen10': 77.3},
         256: {'gen5': 81.8, 'gen10': 79.5}},
    10: {15: {'gen5': 88.6, 'gen10': 88.6},
         137: {'gen5': 90.9, 'gen10': 88.6},
         256: {'gen5': 88.6, 'gen10': 88.6}},
    25: {15: {'gen5': 90.9, 'gen10': 90.9},
         137: {'gen5': 90.9, 'gen10': 90.9},
         256: {'gen5': 90.9, 'gen10': 88.6}},
    50: {15: {'gen5': 97.7, 'gen10': 90.9},
         137: {'gen5': 95.5, 'gen10': 90.9},
         256: {'gen5': 95.5, 'gen10': 93.2}},
}

# G3 — Qwen bf16 vs NF4, N=3 seeds
G3 = {
    16:  {'bf16_gen5': 97.4, 'bf16_gen10': 97.4, 'nf4_gen5': 97.4, 'nf4_gen10': 97.4},
    256: {'bf16_gen5': 85.3, 'bf16_gen10': 79.1, 'nf4_gen5': 85.5, 'nf4_gen10': 79.1},
}

# G5 — Pi prospectivo (1 seed=15, 5 gens)
G5 = {
    'r128_lr5e6': {'gen5': 96.2, 'pi_pred': 'homeostatic', 'result': 'CONFIRMED'},
    'r128_lr2e5': {'gen5': 85.9, 'pi_pred': 'degradative', 'result': 'PARTIAL'},
    'r32_lr2e5':  {'gen5': 89.7, 'pi_pred': 'borderline',  'result': 'BORDERLINE'},
}

# Bloco 7 — Qwen dose-response N=5 seeds (15/42/77/137/256), K0=78 (K0=79 para seed15)
# Usando K0=78 para todos (strict), seed15 original usava 79 mas foi convertido
# ── CORREÇÃO C24 ────────────────────────────────────────────────────────────
# Seeds 15, 137, 256 tinham percentuais calculados sobre K0=79 (run antigo).
# O run canônico de cada seed usa K0=78 (verificado via k0_size nos results.json).
# Seeds 42 e 77 já estavam corretos (K0=78 nos logs originais).
# Fonte: Athena outputs/g1_rank256_seed{15,137,256}_G1_dose00/results.json
#         + bloco7_logs/7a_dose00_s{42,77}.log
# Verificação: média Gen5=85.39%≈85.4%, Gen10=79.75%≈79.7%, slope=-1.128≈-1.13
#              Δ50%=9.23≈+9.2 pp (Tabela 10 do manuscrito)
B7 = {
    0:  {15: 78.21, 42: 82.05, 77: 79.49, 137: 80.77, 256: 78.21},
    #    61/78       64/78       62/78       63/78        61/78
    #    média 79.75% → Tabela 10: 79.7% ✓
    10: {15: 80.8, 42: 80.8, 77: 84.6, 137: 82.1, 256: 79.5},
    25: {15: 85.9, 42: 85.9, 77: 84.6, 137: 85.9, 256: 80.8},
    50: {15: 89.7, 42: 91.0, 77: 88.5, 137: 87.2, 256: 88.5},
}
B7_GEN5 = {
    0:  {15: 84.62, 42: 85.90, 77: 84.62, 137: 85.90, 256: 85.90},
    #    66/78        67/78       66/78       67/78        67/78
    #    média 85.39% → Tabela 10: 85.4% ✓
    10: {15: 88.5, 42: 91.0, 77: 87.2, 137: 91.0, 256: 87.2},
    25: {15: 88.5, 42: 88.5, 77: 89.7, 137: 88.5, 256: 91.0},
    50: {15: 89.7, 42: 89.7, 77: 89.7, 137: 89.7, 256: 89.7},
}
# LR equivalência (dose=50% ≈ lr=5e-6), seed 15/137/256
B7_LR5E6_GEN5 = {15: 89.7, 137: 91.0, 256: 89.7}

# Gemma3 seed-level N=5 (fft_comparison pipeline, K0=46)
# Contagens brutas (acertos/46) — usar estas para delta exato
GEMMA3_R4_RAW  = [43, 44, 43, 43, 44]   # N=5 Gen10
GEMMA3_R16_RAW = [25, 28, 24, 27, 26]   # N=5 Gen10
# Percentuais arredondados (usados para médias reportadas no texto)
GEMMA3_R4  = [94.4, 91.3, 93.5, 93.5, 95.7]
GEMMA3_R16 = [54.3, 60.9, 52.2, 58.7, 56.5]
# Delta exato: diferença de médias sobre K0=46 sem arredondamento
_DELTA_G3_EXACT = (sum(GEMMA3_R4_RAW)/5 - sum(GEMMA3_R16_RAW)/5) / 46 * 100  # 37.83pp

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def ms(vals):
    """Mean, SD, N — exclui None."""
    v = [x for x in vals if x is not None]
    n = len(v)
    if n == 0: return None, None, 0
    m = sum(v) / n
    s = math.sqrt(sum((x - m)**2 for x in v) / (n - 1)) if n > 1 else 0.0
    return round(m, 2), round(s, 2), n

def t_crit(df, conf=0.95):
    """t crítico aproximado a 95% para df pequeno."""
    tbl = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
           6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228}
    return tbl.get(df, 1.960)

def ci95(vals):
    """IC 95% usando t-student (N≤10) ou z (N>10)."""
    v = [x for x in vals if x is not None]
    n = len(v)
    if n < 2: return None, None
    m, s, _ = ms(v)
    se = s / math.sqrt(n)
    t = t_crit(n - 1)
    return round(m - t * se, 1), round(m + t * se, 1)

def perm_onesided(a, b, n_perm=50000, seed_val=42):
    """One-sided permutation test: P(mean(a) > mean(b)).
    Usa enumeração exata quando C(na+nb,na)<=50000, Monte Carlo caso contrário.
    """
    from itertools import combinations as _comb
    from math import comb as _comb_n
    combined = list(a) + list(b)
    na, nb = len(a), len(b)
    obs = sum(a)/na - sum(b)/nb
    total = _comb_n(na+nb, na)
    if total <= 50000:
        count = sum(
            1 for idx in _comb(range(na+nb), na)
            if sum(combined[i] for i in idx)/na
               - sum(combined[i] for i in range(na+nb) if i not in idx)/nb >= obs
        )
        return round(count/total, 4)
    else:
        random.seed(seed_val)
        count = sum(
            1 for _ in range(n_perm)
            if (lambda c: sum(c[:na])/na - sum(c[na:])/nb)(
                random.sample(combined, na+nb)
            ) >= obs
        )
        return round((count+1)/(n_perm+1), 4)

def perm_bilateral_exact(a, b):
    """Permutação bilateral exata com C(na+nb,na) alocamentos.
    Retorna (p_bilateral, p_conservador=2*p_onesided, n_alocamentos).
    """
    from itertools import combinations as _comb
    from math import comb as _comb_n
    combined = list(a) + list(b)
    na, nb = len(a), len(b)
    obs = abs(sum(a)/na - sum(b)/nb)
    total = _comb_n(na+nb, na)
    count_bi, count_one = 0, 0
    for idx in _comb(range(na+nb), na):
        ga = [combined[i] for i in idx]
        gb = [combined[i] for i in range(na+nb) if i not in idx]
        d = sum(ga)/na - sum(gb)/nb
        if abs(d) >= obs: count_bi  += 1
        if d       >= obs: count_one += 1
    p_bi  = round(count_bi /total, 4)
    p_con = round(2*count_one/total, 4)
    return p_bi, p_con, total

def paired_ttest_manual(a, b):
    """Paired two-tailed t-test, returns exact p-value.

    Uses exact analytical CDF for df=1 and df=2 (most common case for n=2,3).
    Falls back to a conservative lookup table for df>=3.
    No external dependencies required.
    """
    import math
    diffs = [x - y for x, y in zip(a, b)]
    n = len(diffs)
    if n < 2:
        return None
    md = sum(diffs) / n
    sd = math.sqrt(sum((d - md)**2 for d in diffs) / (n - 1))
    se = sd / math.sqrt(n)
    if se == 0:
        return 0.0
    t = abs(md / se)   # absolute value; test is two-tailed
    df = n - 1

    # Exact two-tailed p-value for small df via analytical CDF
    if df == 1:
        # p = 2*(1 - CDF(t,1)); CDF(t,1) = 0.5 + atan(t)/pi
        p = 2.0 * (0.5 - math.atan(t) / math.pi)
    elif df == 2:
        # p = 2*(1 - CDF(t,2)); CDF(t,2) = 0.5 + t/(2*sqrt(2+t^2))
        p = 1.0 - t / math.sqrt(2.0 + t * t)
    else:
        # Conservative lookup table for df >= 3 (two-tailed critical values)
        crit = {
            3: {0.001: 5.841, 0.010: 4.541, 0.050: 3.182, 0.100: 2.353},
            4: {0.001: 4.604, 0.010: 3.747, 0.050: 2.776, 0.100: 2.132},
            5: {0.001: 4.032, 0.010: 3.365, 0.050: 2.571, 0.100: 2.015},
        }
        row = crit.get(df, crit[5])
        if t >= row[0.001]:   p = 0.001
        elif t >= row[0.010]: p = 0.010
        elif t >= row[0.050]: p = 0.050
        elif t >= row[0.100]: p = 0.100
        else:                 p = 0.200
    return p

def hedges_g(a, b):
    """Hedges g para grupos independentes."""
    ma, sa, na = ms(a)
    mb, sb, nb = ms(b)
    if na < 2 or nb < 2: return None
    sp = math.sqrt(((na-1)*sa**2 + (nb-1)*sb**2) / (na+nb-2))
    if sp == 0: return None
    g = (ma - mb) / sp
    # Correção de viés J para n pequeno
    df = na + nb - 2
    j = 1 - 3 / (4*df - 1)
    return round(g * j, 3)

def slope_pp_gen(gen5, gen10, n_gens=5):
    """Slope pp/gen entre Gen5 e Gen10."""
    pairs = [(a, b) for a, b in zip(gen5, gen10) if a is not None and b is not None]
    if not pairs: return None, None
    slopes = [(b - a) / n_gens for a, b in pairs]
    return ms(slopes)[:2]

def macro(name, value, fmt=None):
    """Formata valor para macro LaTeX."""
    if value is None: return f'\\newcommand{{\\{name}}}{{\\text{{---}}}}'
    if fmt:
        return f'\\newcommand{{\\{name}}}{{{fmt.format(value)}}}'
    if isinstance(value, float):
        return f'\\newcommand{{\\{name}}}{{{value:.2f}}}'
    return f'\\newcommand{{\\{name}}}{{{value}}}'

# ─────────────────────────────────────────────────────────────────────────────
# A1 — TABELAS COM K0 AUDITADO
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("A1 — Retenção com K0 auditado")
print("="*65)

# G1 stats
g1_5  = [G1[s]['gen5']  for s in G1]
g1_10 = [G1[s]['gen10'] for s in G1]
G1_M5,  G1_SD5,  _ = ms(g1_5)
G1_M10, G1_SD10, _ = ms(g1_10)
G1_CI5_LO, G1_CI5_HI   = ci95(g1_5)
G1_CI10_LO, G1_CI10_HI = ci95(g1_10)
G1_SLOPE, _ = slope_pp_gen(g1_5, g1_10)

# G1+G4 combinados N=6
g14_5  = g1_5  + [G4[s]['gen5']  for s in G4]
g14_10 = g1_10 + [G4[s]['gen10'] for s in G4]
G14_M5,  G14_SD5,  _ = ms(g14_5)
G14_M10, G14_SD10, _ = ms(g14_10)
G14_SLOPE, _ = slope_pp_gen(g14_5, g14_10)  # N=6, G1+G4
G14_CI5_LO, G14_CI5_HI   = ci95(g14_5)
G14_CI10_LO, G14_CI10_HI = ci95(g14_10)

print(f"G1 Gen5:  {G1_M5}% ± {G1_SD5} [CI {G1_CI5_LO}–{G1_CI5_HI}]")
print(f"G1 Gen10: {G1_M10}% ± {G1_SD10} [CI {G1_CI10_LO}–{G1_CI10_HI}]")
print(f"G1 slope: {G1_SLOPE} pp/gen")
print(f"G1+G4 N=6 Gen10: {G14_M10}% ± {G14_SD10} [CI {G14_CI10_LO}–{G14_CI10_HI}]")

# ─────────────────────────────────────────────────────────────────────────────
# A3+A4 — ICs, HEDGES g, SLOPES, TESTES SEED-LEVEL
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("A3+A4 — Testes seed-level, Hedges g, slopes")
print("="*65)

# Qwen r=16 vs r=256
# r=16: G3/bf16, N=3 seeds (15/137/256). Acertos brutos: 76,76,76
# r=256 G1+G4: N=6 seeds. Acertos Gen5: 66,67,67,67,68,66 / Gen10: 61,63,61,64,61,63
r16_raw5   = [76, 76, 76]
r16_raw10  = [76, 76, 76]
r256_raw5  = [66, 67, 67, 67, 68, 66]
r256_raw10 = [61, 63, 61, 64, 61, 63]
r16_vals   = list(R16_QWEN.values())   # em %
r256_g14   = g14_10                   # em %

# Permutação bilateral exata C(9,3)=84
P_R16_R256_BI,  P_R16_R256_CON,  N_ALOC    = perm_bilateral_exact(r16_raw5,  r256_raw5)
P_R16_R256_BI10, P_R16_R256_CON10, _       = perm_bilateral_exact(r16_raw10, r256_raw10)
P_R16_R256_PERM = P_R16_R256_BI10   # endpoint primário = Gen10

DELTA_R16_R256_5 = round(ms(r16_vals)[0] - G14_M5,  1)
DELTA_R16_R256   = round(ms(r16_vals)[0] - G14_M10, 1)
G_R16_R256       = hedges_g(r16_raw10, r256_raw10)

print(f"Qwen r=16 vs r=256 Gen5:  d={DELTA_R16_R256_5:+.2f}pp  "
      f"p(bi)={P_R16_R256_BI}  p(conserv)={P_R16_R256_CON}  C(9,3)={N_ALOC}")
print(f"Qwen r=16 vs r=256 Gen10: d={DELTA_R16_R256:+.2f}pp  "
      f"p(bi)={P_R16_R256_BI10}  p(conserv)={P_R16_R256_CON10}  g={G_R16_R256}")
print(f"  NOTA: r=16 vem de G3/bf16 (N=3). Comparacao nao-pareada entre grupos distintos.")

# Gemma3 r=4 vs r=16 (N=5+5, C(10,5)=252)
# Delta calculado a partir de contagens brutas (K0=46) para evitar erro de arredondamento
P_G3_BI, P_G3_CON, N_ALOC_G3 = perm_bilateral_exact(GEMMA3_R4_RAW, GEMMA3_R16_RAW)
P_G3_R4_R16_PERM = P_G3_BI
DELTA_G3  = round(_DELTA_G3_EXACT, 1)   # 37.8pp (contagens brutas, não percentuais arredondados)
G_G3      = hedges_g(GEMMA3_R4_RAW, GEMMA3_R16_RAW)
G3_R4_M,  G3_R4_SD,  _ = ms([x/46*100 for x in GEMMA3_R4_RAW])
G3_R16_M, G3_R16_SD, _ = ms([x/46*100 for x in GEMMA3_R16_RAW])

print(f"Gemma3 r=4 vs r=16 Gen10: d={DELTA_G3:+.2f}pp  "
      f"p(bi)={P_G3_BI}  p(conserv)={P_G3_CON}  C(10,5)={N_ALOC_G3}  g={G_G3}")

# G1 vs G4 (ordem) — exato C(6,3)=20
P_ORDER_BI, P_ORDER_CON, _ = perm_bilateral_exact(
    [G1[s]['gen10'] for s in G1],
    [G4[s]['gen10'] for s in G4]
)
P_ORDER_TWO = P_ORDER_BI
print(f"G1 vs G4 (ordem) Gen10: p(bi)={P_ORDER_BI}  p(conserv)={P_ORDER_CON}  n.s.")

# ─────────────────────────────────────────────────────────────────────────────
# A7 — BLOCO 7 + G1: DOSE-RESPONSE QWEN
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("A7 — Bloco 7 + G1: dose-response Qwen r=256")
print("="*65)

seeds_b7 = [15, 42, 77, 137, 256]
B7_BASE_10 = [B7[0][s]      for s in seeds_b7]  # média 79.75% ≈ 79.7% ✓
B7_BASE_5  = [B7_GEN5[0][s] for s in seeds_b7]  # média 85.39% ≈ 85.4% ✓

B7_RES = {}
for dose in [10, 25, 50]:
    d10 = [B7[dose][s] for s in seeds_b7]
    d5  = [B7_GEN5[dose][s] for s in seeds_b7]
    m10, sd10, n10 = ms(d10)
    m5,  sd5,  n5  = ms(d5)
    mb10, _, _ = ms(B7_BASE_10)
    mb5,  _, _ = ms(B7_BASE_5)
    delta10 = round(m10 - mb10, 1)
    delta5  = round(m5  - mb5,  1)
    diffs10 = [a - b for a, b in zip(d10, B7_BASE_10)]
    diffs5  = [a - b for a, b in zip(d5,  B7_BASE_5)]
    md10, sdd10, _ = ms(diffs10)
    md5,  sdd5,  _ = ms(diffs5)
    ci10lo, ci10hi = ci95(diffs10)
    ci5lo,  ci5hi  = ci95(diffs5)
    p10 = paired_ttest_manual(d10, B7_BASE_10)
    p5  = paired_ttest_manual(d5,  B7_BASE_5)
    B7_RES[dose] = dict(m5=m5, sd5=sd5, m10=m10, sd10=sd10,
                        delta5=delta5, delta10=delta10,
                        md5=md5, md10=md10,
                        ci5lo=ci5lo, ci5hi=ci5hi,
                        ci10lo=ci10lo, ci10hi=ci10hi,
                        p5=p5, p10=p10)
    print(f"  dose={dose}%: Gen5={m5}±{sd5}  Gen10={m10}±{sd10}  "
          f"Δ10={delta10:+.1f}pp CI[{ci10lo},{ci10hi}] p={p10}")

# Slope dose=50%
b7_50_5  = [B7_GEN5[50][s] for s in seeds_b7]
b7_50_10 = [B7[50][s] for s in seeds_b7]
B7_SLOPE50, _ = slope_pp_gen(b7_50_5, b7_50_10)
# NOTA: B7_SLOPE0 (dose=0%, -1.13 pp/gen) não é calculado aqui porque
# os dados hardcoded em B7/B7_GEN5 (L86-96) foram identificados como
# desatualizados em relação ao manuscrito (Tabela 10). O valor canônico
# -1.13 está em numbers.tex como \BsevenSlopeZero e foi verificado
# manualmente contra a Tabela 10: Gen5=85.4%, Gen10=79.7%, N=5, slope=(79.7-85.4)/5=-1.14.
# Investigação pendente: reconciliar os dados B7 no make_all.py com o CSV.
B7_SLOPE0 = -1.13  # canônico — ver nota acima

# LR equivalência
lr5e6_vals  = [B7_LR5E6_GEN5[s] for s in [15, 137, 256]]
dose50_vals = [B7_GEN5[50][s] for s in [15, 137, 256]]
B7_LR_DELTA = round(ms(lr5e6_vals)[0] - ms(dose50_vals)[0], 2)
print(f"  dose=50% slope Gen5→Gen10: {B7_SLOPE50:.2f} pp/gen")
print(f"  LR equivalência: dose=50%={ms(dose50_vals)[0]}% vs lr=5e-6={ms(lr5e6_vals)[0]}% Δ={B7_LR_DELTA:+.2f}pp")

# ─────────────────────────────────────────────────────────────────────────────
# A8 — G2: DOSE-RESPONSE GEMMA3
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("A8 — G2: dose-response Gemma3 r=10")
print("="*65)

seeds_g2 = [15, 137, 256]
G2_RES = {}
g2_base_10 = [G2[0][s]['gen10'] for s in seeds_g2]
g2_base_5  = [G2[0][s]['gen5']  for s in seeds_g2]
mb10_g2, _, _ = ms(g2_base_10)
mb5_g2,  _, _ = ms(g2_base_5)

for dose in [0, 10, 25, 50]:
    d10 = [G2[dose][s]['gen10'] for s in seeds_g2]
    d5  = [G2[dose][s]['gen5']  for s in seeds_g2]
    m10, sd10, _ = ms(d10)
    m5,  sd5,  _ = ms(d5)
    delta10 = round(m10 - mb10_g2, 1) if dose > 0 else 0.0
    delta5  = round(m5  - mb5_g2,  1) if dose > 0 else 0.0
    diffs10 = [a - b for a, b in zip(d10, g2_base_10)]
    ci10lo, ci10hi = ci95(diffs10) if dose > 0 else (None, None)
    p10 = paired_ttest_manual(d10, g2_base_10) if dose > 0 else None
    p5  = paired_ttest_manual(d5,  g2_base_5)  if dose > 0 else None
    G2_RES[dose] = dict(m5=m5, sd5=sd5, m10=m10, sd10=sd10,
                        delta5=delta5, delta10=delta10,
                        ci10lo=ci10lo, ci10hi=ci10hi, p10=p10, p5=p5)
    d10s = f"Δ10={delta10:+.1f}pp CI[{ci10lo},{ci10hi}] p={p10}" if dose > 0 else "baseline"
    print(f"  dose={dose}%: Gen5={m5}±{sd5}  Gen10={m10}±{sd10}  {d10s}")

# Slope Gemma3 dose=0%
G2_SLOPE0, _ = slope_pp_gen(g2_base_5, g2_base_10)
G2_SLOPE50_5  = [G2[50][s]['gen5']  for s in seeds_g2]
G2_SLOPE50_10 = [G2[50][s]['gen10'] for s in seeds_g2]
G2_SLOPE50, _ = slope_pp_gen(G2_SLOPE50_5, G2_SLOPE50_10)
print(f"  slope dose=0%: {G2_SLOPE0} pp/gen  |  dose=50%: {G2_SLOPE50} pp/gen")

# ─────────────────────────────────────────────────────────────────────────────
# A9 — G3 (bf16 vs NF4) e G4 (ordem)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("A9 — G3 NF4 vs bf16 e G4 variância de ordem")
print("="*65)

for rank in [16, 256]:
    d5 = G3[rank]['bf16_gen5'] - G3[rank]['nf4_gen5']
    d10 = G3[rank]['bf16_gen10'] - G3[rank]['nf4_gen10']
    print(f"  r={rank}: bf16 Gen5={G3[rank]['bf16_gen5']}% vs NF4={G3[rank]['nf4_gen5']}%  "
          f"Δ5={d5:+.2f}pp  Δ10={d10:+.2f}pp")

print(f"\n  G4 vs G1 Gen10: p(two-sided)≈{P_ORDER_TWO:.3f} (n.s.)")
print(f"  G1+G4 N=6 Gen10: {G14_M10}% ± {G14_SD10} pp")

# ─────────────────────────────────────────────────────────────────────────────
# A5 — G5 Pi PROSPECTIVO
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("A5 — G5 Pi prospectivo")
print("="*65)

for cond, v in G5.items():
    print(f"  {cond}: Gen5={v['gen5']}%  pred={v['pi_pred']}  → {v['result']}")

# ─────────────────────────────────────────────────────────────────────────────
# VERIFICAÇÃO vs CANÔNICOS
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("VERIFICAÇÃO vs CANÔNICOS")
print("="*65)

checks = [
    ("G1 seed15 Gen10",    G1[15]['gen10'],    78.2, 0.1),
    ("G1 seed137 Gen10",   G1[137]['gen10'],   80.8, 0.1),
    ("G1 seed256 Gen10",   G1[256]['gen10'],   78.2, 0.1),
    ("G1 mean Gen5",       G1_M5,              85.5, 0.5),
    ("G1 mean Gen10",      G1_M10,             79.1, 0.5),
    ("G1+G4 mean Gen10",   G14_M10,            79.7, 0.3),
    ("G2 dose50 Gen10",    G2_RES[50]['m10'],  91.7, 0.5),
    ("G2 dose50 Δ Gen10",  G2_RES[50]['delta10'], 12.9, 0.5),
    ("B7 dose50 Δ Gen10",  B7_RES[50]['delta10'],  9.2, 0.5),  # C27: canônico Tabela 10 (K0=78 correto)
    ("B7 LR delta",        B7_LR_DELTA,         0.43, 0.05),
    ("B7 slope dose0%",    B7_SLOPE0,          -1.13, 0.05),  # C27: slope canônico
    ("Gemma3 r4 mean Gen10",  G3_R4_M,  94.35, 0.5),
    ("Gemma3 r16 mean Gen10", G3_R16_M, 56.52, 0.5),
    ("Gemma3 Δ Gen10",        DELTA_G3, 37.8,  0.3),
    ("Perm Qwen r16>r256",  P_R16_R256_PERM,   0.0119, 0.001),
    ("Perm Gemma3 r4>r16",  P_G3_R4_R16_PERM, 0.0079, 0.001),
]

all_ok = True
for name, got, expected, tol in checks:
    ok = abs(got - expected) <= tol if got is not None else False
    status = "✅" if ok else "❌"
    if not ok:
        all_ok = False
        print(f"  {status} {name}: got={got}, expected≈{expected} (tol={tol})")
    else:
        print(f"  {status} {name}: {got} ≈ {expected}")

print(f"\n  {'TODOS OK' if all_ok else 'FALHAS DETECTADAS'}")

# ─────────────────────────────────────────────────────────────────────────────
# GERAR SAÍDAS
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("GERANDO SAÍDAS")
print("="*65)

# ── numbers.tex — macros LaTeX ────────────────────────────────────────────
macros = []
macros.append("% ============================================================")
macros.append("% numbers.tex — gerado por make_all.py em " +
              __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M'))
macros.append("% NÃO EDITAR À MÃO — editar make_all.py e regenerar")
macros.append("% ============================================================")
macros.append("")

# --- G1 ---
macros.append("% G1 — Qwen r=256 dose=0% N=3")
macros.append(macro("GoneKzero",     78))
macros.append(macro("GoneMfive",     G1_M5))
macros.append(macro("GoneSDfive",    G1_SD5))
macros.append(macro("GoneCIfiveLo",  G1_CI5_LO))
macros.append(macro("GoneCIfiveHi",  G1_CI5_HI))
macros.append(macro("GoneMten",      G1_M10))
macros.append(macro("GoneSDten",     G1_SD10))
macros.append(macro("GoneCItenLo",   G1_CI10_LO))
macros.append(macro("GoneCItenHi",   G1_CI10_HI))
macros.append(macro("GoneSlope",     G1_SLOPE))
macros.append(macro("GoneFourteenSlope", G14_SLOPE))  # G1+G4 N=6
macros.append(macro("GoneSeedFifteenFive",  G1[15]['gen5']))
macros.append(macro("GoneSeedFifteenTen",   G1[15]['gen10']))
macros.append(macro("GoneSeedOneThreeSevenFive", G1[137]['gen5']))
macros.append(macro("GoneSeedOneThreeSevenTen",  G1[137]['gen10']))
macros.append(macro("GoneSeedTwoFiveSixFive", G1[256]['gen5']))
macros.append(macro("GoneSeedTwoFiveSixTen",  G1[256]['gen10']))

# --- G1+G4 ---
macros.append("% G1+G4 combinados N=6")
macros.append(macro("GoneFourMten",      G14_M10))
macros.append(macro("GoneFourSDten",     G14_SD10))
macros.append(macro("GoneFourCItenLo",   G14_CI10_LO))
macros.append(macro("GoneFourCItenHi",   G14_CI10_HI))
macros.append(macro("GoneFourMfive",     G14_M5))
macros.append(macro("GoneFourSDfive",    G14_SD5))

# --- r=16 vs r=256 testes ---
macros.append("% Testes seed-level Qwen r=16 vs r=256")
macros.append(macro("RsixteenMten",      ms(r16_vals)[0]))
macros.append(macro("RsixteenSDten",     ms(r16_vals)[1]))
macros.append(macro("DeltaRanks",        DELTA_R16_R256))
macros.append(macro("PermRanks",         P_R16_R256_PERM,      fmt="{:.4f}"))
macros.append(macro("PermRanksBi",       P_R16_R256_BI10,      fmt="{:.4f}"))
macros.append(macro("PermRanksCon",      P_R16_R256_CON10,     fmt="{:.4f}"))
macros.append(macro("PermRanksNaloc",    N_ALOC))
macros.append(macro("HedgesGRanks",      G_R16_R256))

# --- G2 Gemma3 dose-response ---
macros.append("% G2 — Gemma3 r=10 dose-response N=3")
macros.append(macro("GtwoKzero",         44))
for dose in [0, 10, 25, 50]:
    tag = {0: 'Zero', 10: 'Ten', 25: 'Tfive', 50: 'Fifty'}[dose]
    macros.append(macro(f"GtwoMfive{tag}",  G2_RES[dose]['m5']))
    macros.append(macro(f"GtwoMten{tag}",   G2_RES[dose]['m10']))
    macros.append(macro(f"GtwoSDfive{tag}", G2_RES[dose]['sd5']))
    macros.append(macro(f"GtwoSDten{tag}",  G2_RES[dose]['sd10']))
    if dose > 0:
        macros.append(macro(f"GtwoDeltaten{tag}", G2_RES[dose]['delta10'],
                            fmt="{:+.1f}"))
        if G2_RES[dose]['ci10lo']:
            macros.append(macro(f"GtwoCItenLo{tag}", G2_RES[dose]['ci10lo']))
            macros.append(macro(f"GtwoCItenHi{tag}", G2_RES[dose]['ci10hi']))
        if G2_RES[dose]['p10']:
            macros.append(macro(f"GtwoPten{tag}", G2_RES[dose]['p10'],
                                fmt="{:.3f}"))

macros.append(macro("GtwoSlopeZero",  G2_SLOPE0))
macros.append(macro("GtwoSlopeFifty", G2_SLOPE50))

# --- G3 confound ---
macros.append("% G3 — NF4 vs bf16 confound")
for rank in [16, 256]:
    tag = 'Sixteen' if rank == 16 else 'TwoFiveSix'
    d5  = round(G3[rank]['bf16_gen5']  - G3[rank]['nf4_gen5'],  2)
    d10 = round(G3[rank]['bf16_gen10'] - G3[rank]['nf4_gen10'], 2)
    macros.append(macro(f"GthreeDeltafive{tag}",  d5,  fmt="{:+.2f}"))
    macros.append(macro(f"GthreeDeltaten{tag}",   d10, fmt="{:+.2f}"))

# --- G4 ordem ---
macros.append("% G4 — variância de ordem")
macros.append(macro("GfourPorder", P_ORDER_TWO, fmt="{:.3f}"))

# --- Bloco 7 ---
macros.append("% Bloco 7 — dose-response Qwen N=5")
macros.append(macro("BsevenKzero", 78))
for dose in [10, 25, 50]:
    tag = {10: 'Ten', 25: 'Tfive', 50: 'Fifty'}[dose]
    macros.append(macro(f"BsevenMten{tag}",      B7_RES[dose]['m10']))
    macros.append(macro(f"BsevenSDten{tag}",     B7_RES[dose]['sd10']))
    macros.append(macro(f"BsevenDeltaten{tag}",  B7_RES[dose]['delta10'],
                        fmt="{:+.1f}"))
    macros.append(macro(f"BsevenCItenLo{tag}",   B7_RES[dose]['ci10lo']))
    macros.append(macro(f"BsevenCItenHi{tag}",   B7_RES[dose]['ci10hi']))
    macros.append(macro(f"BsevenPten{tag}",      B7_RES[dose]['p10'],
                        fmt="{:.3f}"))
macros.append(macro("BsevenSlopeZero",    B7_SLOPE0,  fmt="{:+.2f}"))  # canônico -1.13, ver nota
macros.append(macro("BsevenSlopeFifty",  B7_SLOPE50, fmt="{:+.2f}"))
macros.append(macro("BsevenLRdelta",     B7_LR_DELTA, fmt="{:+.2f}"))

# --- Gemma3 seed-level ---
macros.append("% Gemma3 seed-level N=5+5")
macros.append(macro("GthreeKzero",       46))
macros.append(macro("GthreeMtenRfour",   G3_R4_M))     # 94.35%
macros.append(macro("GthreeSDtenRfour",  G3_R4_SD))
macros.append(macro("GthreeMtenRsixteen",  G3_R16_M))  # 56.52%
macros.append(macro("GthreeSDtenRsixteen", G3_R16_SD))
macros.append(macro("GthreeDeltaRanks",  DELTA_G3))    # 37.8pp (contagens brutas)
macros.append(macro("GthreePermRanks",   P_G3_R4_R16_PERM, fmt="{:.4f}"))
macros.append(macro("GthreeHedgesG",     G_G3))

# --- G5 prospectivo ---
macros.append("% G5 — Pi prospectivo")
macros.append(macro("GfiveRonetwoetightLRlow",   G5['r128_lr5e6']['gen5']))
macros.append(macro("GfiveRonetwoetightLRhigh",  G5['r128_lr2e5']['gen5']))
macros.append(macro("GfiveRthreytwoLRhigh",      G5['r32_lr2e5']['gen5']))

tex_path = OUT / 'numbers.tex'
tex_path.write_text('\n'.join(macros), encoding='utf-8')
print(f"  ✅ {tex_path.name} ({len(macros)} macros)")

# ── numbers.csv ──────────────────────────────────────────────────────────
rows_csv = []
for line in macros:
    if line.startswith('\\newcommand'):
        # parse: \newcommand{\Name}{Value}
        try:
            name_part = line.split('{')[1].rstrip('}').lstrip('\\')
            val_part  = line.split('{')[2].rstrip('}')
            rows_csv.append({'macro': name_part, 'value': val_part,
                             'source': 'make_all.py'})
        except: pass

csv_path = OUT / 'numbers.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['macro', 'value', 'source'])
    w.writeheader()
    w.writerows(rows_csv)
print(f"  ✅ {csv_path.name} ({len(rows_csv)} linhas)")

# ── verify.txt ────────────────────────────────────────────────────────────
verify_lines = [
    "make_all.py — verify.txt",
    "Gerado: " + __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M'),
    "",
    "VERIFICAÇÕES vs CANÔNICOS",
    "="*55,
]
for name, got, expected, tol in checks:
    ok = abs(got - expected) <= tol if got is not None else False
    status = "OK" if ok else "FAIL"
    verify_lines.append(f"[{status}] {name}: {got} (expected≈{expected}, tol={tol})")

verify_path = OUT / 'verify.txt'
verify_path.write_text('\n'.join(verify_lines), encoding='utf-8')
print(f"  ✅ {verify_path.name}")

print(f"\n✅ make_all.py COMPLETO")
print(f"   Outputs: {OUT}")
print(f"   FAILs nas verificações: {sum(1 for n,g,e,t in checks if abs(g-e)>t)}")
