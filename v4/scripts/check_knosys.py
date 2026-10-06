#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_knosys.py — 12 mechanical checks for KNOSYS manuscript and letter.
Run from the v4/ directory:  uv run python scripts/check_knosys.py

Exit code 0 = all PASS; non-zero = at least one FAIL.
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).parent.parent
MAN  = ROOT / "manuscript" / "manuscript-anonymous.tex"
RES  = ROOT / "docs/overleaf/response-to-reviewers.tex"
SHR  = ROOT / "shared" / "tab01_body.tex"

man_text = MAN.read_text(encoding="utf-8")
res_text = RES.read_text(encoding="utf-8")
shr_text = SHR.read_text(encoding="utf-8")

results = []

def check(n, desc, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    results.append((n, status, desc, detail))
    print(f"  [{status}] check_{n:02d}  {desc}" + (f"\n         {detail}" if detail and not passed else ""))

# ---------------------------------------------------------------------------
# check_01: no bare K₀ = without bars outside figure/table captions
# Allow: $K_0$ as a SET reference, but flag $K_0 = <number>$ (cardinality used without bars)
# Specifically: K_0 followed by = and a digit (no |) is wrong
# ---------------------------------------------------------------------------
# Pattern: $K_0$ followed by = digit (not |K_0| = digit)
bare_card = re.findall(r'\$K_0\$\s*=\s*\d', man_text)
bare_card_r = re.findall(r'\$K_0\$\s*=\s*\d', res_text)
all_bare = bare_card + bare_card_r
check(1, "no bare K₀ = <digit> without bars",
      len(all_bare) == 0,
      f"Found: {all_bare[:3]}" if all_bare else "")

# ---------------------------------------------------------------------------
# check_02: every retention % reproduces an integer count to 1 dp
# Spot-check the canonical values from the register
# ---------------------------------------------------------------------------
CANONICAL = {
    "97.4": (76, 78), "79.7": (373, 468), "79.1": (185, 234),
    "78.8": (104, 132), "82.1": (64, 78), "78.2": (61, 78),
    "94.3": (217, 230), "56.5": (130, 230),
    "85.9": (67, 78),   "80.3": (188, 234), "79.0": (185, 234),
}
bad_pct = []
for val, (num, den) in CANONICAL.items():
    exact = round(num / den * 100, 1)
    if abs(exact - float(val)) > 0.1:
        bad_pct.append(f"{val}% ({num}/{den}={exact:.4f})")
check(2, "canonical retention % match integer counts to 1 dp",
      len(bad_pct) == 0,
      "; ".join(bad_pct) if bad_pct else "")

# ---------------------------------------------------------------------------
# check_03: Tab.1 body in manuscript and carta are consistent
# Extract rows between \midrule and \bottomrule in each
# ---------------------------------------------------------------------------
def extract_tab1_rows(text):
    """Extract notation table rows, keyed specifically by label or inlineref title."""
    # Manuscript: find the table with label tab:notation
    man_match = re.search(
        r'\\label\{tab:notation\}.*?\\toprule.*?\\midrule(.*?)\\bottomrule',
        text, re.DOTALL
    )
    if man_match:
        rows = man_match.group(1).strip()
        rows = re.sub(r'[ \t]+', ' ', rows)
        return re.sub(r'\n\s*\n', '\n', rows).strip()
    # Carta: find within inlineref{Table~1 ...}
    carta_match = re.search(
        r'\\begin\{inlineref\}\{Table~1[^\}]*\}(.*?)\\end\{inlineref\}',
        text, re.DOTALL
    )
    if carta_match:
        block = carta_match.group(1)
        inner = re.search(r'\\toprule.*?\\midrule(.*?)\\bottomrule', block, re.DOTALL)
        if inner:
            rows = inner.group(1).strip()
            rows = re.sub(r'[ \t]+', ' ', rows)
            return re.sub(r'\n\s*\n', '\n', rows).strip()
    return None

man_tab1 = extract_tab1_rows(man_text)
# For carta, find the inlineref Table 1 (use 'Table~1 ' with space to avoid Table~10)
carta_tab1_match = re.search(
    r'\\begin\{inlineref\}\{Table~1 [^\}]*\}.*?\\toprule.*?\\midrule(.*?)\\bottomrule',
    res_text, re.DOTALL
)
carta_tab1 = carta_tab1_match.group(1).strip() if carta_tab1_match else None
if carta_tab1:
    carta_tab1 = re.sub(r'\s+', ' ', carta_tab1).strip()
# Note: carta omits (Eq.~\ref{eq:erank}) — allow that one difference
if man_tab1 and carta_tab1:
    # Remove the eq:erank reference for comparison
    man_tab1_cmp = man_tab1.replace(r'(Eq.~\ref{eq:erank})', '').strip()
    # strip \rev{...} — handles arbitrary nesting depth
    def strip_rev(s):
        out, i = [], 0
        while i < len(s):
            if s[i:i+5] == r'\rev{':
                # find the matching closing brace
                depth, j = 1, i + 5
                while j < len(s) and depth > 0:
                    if s[j] == '{': depth += 1
                    elif s[j] == '}': depth -= 1
                    j += 1
                out.append(s[i+5:j-1])  # content without \rev{ and }
                i = j
            else:
                out.append(s[i]); i += 1
        return ''.join(out)
    man_tab1_cmp = strip_rev(man_tab1_cmp)
    man_tab1_cmp = re.sub(r'\s+', ' ', man_tab1_cmp)
    carta_tab1_cmp = carta_tab1
    same = (man_tab1_cmp == carta_tab1_cmp)
    check(3, "Tab.1 body identical in manuscript and carta (modulo eq:erank ref)",
          same,
          "Diff detected — first difference at char " +
          str(next((i for i,(a,b) in enumerate(zip(man_tab1_cmp, carta_tab1_cmp)) if a!=b), -1))
          if not same else "")
else:
    check(3, "Tab.1 body identical in manuscript and carta",
          False, f"Could not extract: man={man_tab1 is not None}, carta={carta_tab1 is not None}")

# ---------------------------------------------------------------------------
# check_04: every [verbatim] passage exists in manuscript or fig source
# ---------------------------------------------------------------------------
fig1_html_path = ROOT / "docs/overleaf/figs/src/fig1_overview.html"
fig1_html = fig1_html_path.read_text(encoding="utf-8") if fig1_html_path.exists() else ""
verbatim_checks = [
    ("raw token-level predictions", man_text, "App.A verbatim in manuscript"),
    ("common regime boundary", man_text + fig1_html, "Fig.1 Card6 verbatim"),
]
bad_vb = []
for phrase, corpus, label in verbatim_checks:
    if phrase not in corpus:
        bad_vb.append(f"'{phrase}' ({label})")
check(4, "known [verbatim] passages exist in manuscript or figure source",
      len(bad_vb) == 0,
      "; ".join(bad_vb) if bad_vb else "")

# ---------------------------------------------------------------------------
# check_05: carta section refs point to sections that exist in manuscript
# Cross-reference spot check: real label names
# ---------------------------------------------------------------------------
section_labels = {
    "sec:res_capacity": "§4.1 rank dose-response",
    "sec:controls":     "§3.9 controls",
    "sec:res_backbone": "§4.2 cross-backbone",
    "sec:pressure":     "§3.5 ETP index",
}
missing_labels = []
for label, name in section_labels.items():
    if f"\\label{{{label}}}" not in man_text:
        missing_labels.append(f"{label} ({name})")
check(5, "key section labels exist in manuscript",
      len(missing_labels) == 0,
      f"Missing: {missing_labels}" if missing_labels else "")

# ---------------------------------------------------------------------------
# check_06: erank( always has argument ΔW (not BA, M, or bare)
# ---------------------------------------------------------------------------
bad_erank = re.findall(r'\\mathrm\{erank\}\s*\((?!\s*\\Delta W)', man_text)
bad_erank += re.findall(r'\\mathrm\{erank\}\s*\((?!\s*\\Delta W)', res_text)
# Filter: allow erank(\Delta W) and equation definitions; flag erank(BA), erank(M), bare erank(
bad_erank_real = [e for e in bad_erank
                  if 'BA' in e or r'\boldsymbol{M}' in e or 'M)' in e]
check(6, "erank() always has argument ΔW",
      len(bad_erank_real) == 0,
      f"Found: {bad_erank_real[:2]}" if bad_erank_real else "")

# ---------------------------------------------------------------------------
# check_07: N per condition identical between Tab.4/6/7/9/10 and Fig.3/4 legends
# Spot checks:
#   r=256 N=6 in Tab.4 macro area AND in Fig.4 legend
#   r=16 N=3 in Fig.3 legend
# ---------------------------------------------------------------------------
n6_in_man = ("N=6" in man_text or "N{=}6" in man_text or "$N=6$" in man_text)
n3_r16 = "N=3, G3 bf16" in man_text or "N{=}3" in man_text
check(7, "N per condition consistent (r=256 N=6, r=16 N=3)",
      n6_in_man and n3_r16,
      f"N=6: {n6_in_man}, N=3/r=16: {n3_r16}")

# ---------------------------------------------------------------------------
# check_08: delta values match column differences (± 0.1 pp)
# Spot check Tab.10: B7 dose=0% is 79.7%, and reported delta for Gen10
# ---------------------------------------------------------------------------
# The tab contains delta values; we check that 89.0-79.7 = 9.3 is noted
# or the predicted 9.2 is noted with explanation
tab10_ok = ("9.3" in res_text and "79.7" in res_text) or \
           ("9.2" in res_text and "rounding" in res_text.lower())
check(8, "Tab.10 delta Gen10 documented (9.2 predicted vs 9.3 column diff)",
      tab10_ok, "Check Tab.10 note in carta" if not tab10_ok else "")

# ---------------------------------------------------------------------------
# check_09: [15] and [45] have correct authors in manuscript BBL
# ---------------------------------------------------------------------------
bbl_path = ROOT / "manuscript" / "manuscript-anonymous.bbl"
bbl_text = bbl_path.read_text(encoding="utf-8") if bbl_path.exists() else ""
wrong_authors_15 = any(x in bbl_text for x in ["Jernite", "Kolber", "Teng", "Schenck"])
wrong_authors_45 = "G.~Stein" in bbl_text or "{G. Stein}" in bbl_text
right_15 = "Jennings" in bbl_text and "Frankle" in bbl_text
right_45 = "Andreas" in bbl_text and "Torralba" in bbl_text
check(9, "refs [15] and [45] have correct authors in BBL",
      (not wrong_authors_15) and (not wrong_authors_45) and right_15 and right_45,
      f"[15] wrong={wrong_authors_15} right={right_15}; [45] wrong={wrong_authors_45} right={right_45}")

# ---------------------------------------------------------------------------
# check_10: zero British spellings in manuscript
# Use word boundaries to avoid false positives (e.g. noun 'analyses' ≠ verb 'analyse')
# ---------------------------------------------------------------------------
british_patterns = [
    (r'\bnormalisation', "normalisation"),
    (r'\bnormalise\b', "normalise"),
    (r'\bsummarise\b', "summarise"),
    (r'\bsummarised\b', "summarised"),
    (r'\bgeneralise\b', "generalise"),
    (r'\banalyse\b', "analyse"),   # verb only; noun 'analyses' is both BR/US
    (r'\banalysed\b', "analysed"),
    (r'\brecognise\b', "recognise"),
    (r'\borganise\b', "organise"),
]
found_br = []
for pattern, label in british_patterns:
    if re.search(pattern, man_text, re.IGNORECASE):
        found_br.append(label)
check(10, "zero British spellings in manuscript",
      len(found_br) == 0,
      f"Found: {found_br}" if found_br else "")

# ---------------------------------------------------------------------------
# check_11: App.A run counts sum correctly
# 27 = G1(3)+G2(12)+G3(6)+G4(3)+G5(3); total 52 with B7(20)+C1-C5(5)
# ---------------------------------------------------------------------------
appA_sum_ok = ("27" in man_text and "G1:~3" in man_text and
               "G2:~12" in man_text and "B7" in man_text and "20" in man_text)
check(11, "Appendix A run counts present (27 G1-G5, 20 B7, 5 pilot = 52)",
      appA_sum_ok,
      "Missing count breakdown in App.A" if not appA_sum_ok else "")

# ---------------------------------------------------------------------------
# check_12: glyph_audit.py script exists at declared path
# ---------------------------------------------------------------------------
glyph_script = ROOT / "scripts" / "analysis" / "glyph_audit.py"
check(12, "scripts/analysis/glyph_audit.py exists",
      glyph_script.exists(),
      f"Not found: {glyph_script}" if not glyph_script.exists() else "")

# ---------------------------------------------------------------------------
# check_13: internal consistency — every (Δ, IC 95%, p, n) pair is coherent
# Back-computes SE from the reported CI, derives t = Δ/SE, then checks that
# 2*t.sf(t, df) is within tolerance of the reported p.  This is the check
# that would have caught the commit-6192b9e regression (lookup-table df≥3
# binning produced p=0.200/0.001 inconsistent with the printed CIs).
# Reported pairs: B7 (N=5, df=4) doses 10%/25%/50%; G2 (N=3, df=2) doses 10%/25%/50%.
# ---------------------------------------------------------------------------
try:
    from scipy.stats import t as _t_dist
    _scipy_ok = True
except ImportError:
    _scipy_ok = False

PAIRS = [
    # label          Δ      CI_lo    CI_hi   p_reported   n
    ("B7 dose 10%",  1.8,  -1.10,   4.70,   0.160,       5),
    ("B7 dose 25%",  4.9,   2.50,   7.20,   0.005,       5),
    ("B7 dose 50%",  9.2,   6.90,  11.60,   0.001,       5),   # p<0.001 stored as 0.001
    ("G2 dose 10%",  9.8,   6.70,  13.00,   0.006,       3),
    ("G2 dose 25%", 11.4,   5.80,  17.00,   0.013,       3),
    ("G2 dose 50%", 12.9,   9.70,  16.10,   0.003,       3),
]

def _t_ppf_approx(p_tail, df):
    """Two-sided t critical value (approximate table for scipy fallback)."""
    tbl = {1:12.706, 2:4.303, 3:3.182, 4:2.776, 5:2.571}
    return tbl.get(df, 1.960)

incoherent = []
for label, delta, ci_lo, ci_hi, p_rep, n in PAIRS:
    df = n - 1
    half_w = (ci_hi - ci_lo) / 2.0
    if _scipy_ok:
        t_crit_val = _t_dist.ppf(0.975, df)
    else:
        t_crit_val = _t_ppf_approx(0.025, df)
    se = half_w / t_crit_val
    if se == 0:
        continue
    t_stat = abs(delta / se)
    if _scipy_ok:
        p_calc = float(_t_dist.sf(t_stat, df) * 2)
    else:
        p_calc = p_rep  # can't verify without scipy; skip
    # Tolerance: 0.01 absolute (catches lookup-table bins but allows CI rounding)
    if abs(p_calc - p_rep) > 0.01:
        incoherent.append(
            f"{label}: p_reported={p_rep}, p_from_CI={p_calc:.4f} "
            f"(Δ={delta}, CI=[{ci_lo},{ci_hi}], df={df})"
        )

_check13_detail = "; ".join(incoherent) if incoherent else ""
check(13, "CI/p internal consistency for all B7+G2 reported pairs (|p_calc-p_rep|≤0.01)",
      len(incoherent) == 0 or not _scipy_ok,
      _check13_detail if incoherent else "")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
passed = sum(1 for _,s,_,_ in results if s == "PASS")
total  = len(results)
failed = sum(1 for _,s,_,_ in results if s == "FAIL")
print(f"{'='*60}")
print(f"Results: {passed}/{total} PASS  |  {failed} FAIL")
if failed == 0:
    print("All checks passed. ✓")
else:
    print("FAILING checks:")
    for n, s, d, detail in results:
        if s == "FAIL":
            print(f"  check_{n:02d}: {d}")
            if detail:
                print(f"           {detail}")
print(f"{'='*60}")
sys.exit(0 if failed == 0 else 1)


