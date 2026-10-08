# Replication Package

**Manuscript:** Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs  
**MS ID:** KNOSYS-D-26-21490  
**Journal:** Knowledge-Based Systems (Elsevier)  
**Submission date:** October 2026

---

## What is in this package

This package contains all materials necessary to verify the results reported in the
manuscript and to reproduce the main analyses:

| Folder | Contents |
|--------|----------|
| `manuscript/` | LaTeX source (`.tex`) and bibliography (`.bib`) of the revised manuscript |
| `response/` | Complete response-to-reviewers letter (`.tex`) |
| `data/` | Raw experimental results (CSV), summary tables, and canonical numbers used in all figures and tables |
| `scripts/` | Python analysis scripts that regenerate every table and figure from the CSV |
| `figures/` | All 9 publication-quality figures (PNG, 300 dpi) |

---

## How to reproduce the results

### Step 1 — Verify the numbers

```bash
python scripts/make_all.py
```

This script reads `data/results-G1-G5.csv`, computes all statistics, and writes
`data/numbers-canonical.tex` and `data/verify.txt`. The verify file reports
pass/fail for 15 canonical checks against the values in the manuscript.

### Step 2 — Regenerate Fig. 9 (dose-response cross-backbone)

```bash
python scripts/figures/fig9_dose_response.py
```

Requires: `matplotlib >= 3.7`, `numpy >= 1.24`, `Pillow >= 9.0`.  
Output: `figures/fig9_dose_response.png` (300 dpi).

### Step 3 — Compile the manuscript

```bash
xelatex manuscript/manuscript-anonymous.tex
bibtex  manuscript/manuscript-anonymous
xelatex manuscript/manuscript-anonymous.tex
xelatex manuscript/manuscript-anonymous.tex
```

The manuscript source uses `\input{data/numbers-canonical}` in its preamble,
so Step 1 must be completed before compiling.

---

## Experimental protocol summary

| Parameter | Value |
|-----------|-------|
| Base models | Qwen 2.5 1.5B-Instruct, Gemma 3 1B-IT, Gemma 4 E2B-IT |
| Training framework | QLoRA (bitsandbytes NF4 + bf16 compute) |
| Synthetic data | TriviaQA rc.nocontext split, 2,000 training questions |
| Evaluation set | 200 questions held out (disjoint from training) |
| Recursive generations | 10 (main); 5 (G5 prospective) |
| Seeds (headline conditions) | 3–6 independent seeds |
| GPU | NVIDIA RTX 4000 Ada (20 GB) |
| Experiments | G1–G5 + Bloco 7 (23 runs, 0 failures) |

---

## Experiment groups

| Group | Condition | N seeds | Purpose |
|-------|-----------|---------|---------|
| G1 | Qwen r=256, dose=0% | 3 | Primary degradative baseline |
| G2 | Gemma 3 r=10, doses 0/10/25/50% | 3 per dose | Dose-response cross-backbone |
| G3 | Qwen NF4 vs bf16, r=16+r=256 | 3 per rank | Quantization control |
| G4 | Qwen r=256, shuffle seeds 42/101/202 | 3 | Data-order control |
| G5 | Qwen r=128/r=32, prospective Pi index | 1 | Prospective regime test |
| Bloco 7 | Qwen r=256, doses 0/10/25/50% | 5 | Pre-registered dose-response |

---

## Key results at a glance

| Comparison | Δ Gen10 | Test | p-value |
|------------|---------|------|---------|
| Qwen r=256 vs baseline (G1+G4, N=6) | −17.7 pp | Descriptive gap | — |
| Qwen G3 paired (same 3 seeds, N=3) | +18.4 pp | Sign-flip | 0.25 (N=3) |
| Gemma 3 r=4 vs r=16 (N=5+5) | +37.8 pp | Permutation C(10,5) | 0.008 |
| Qwen dose=50% vs baseline (Bloco 7, N=5) | +9.8 pp | Paired t-test | <0.001 |
| Gemma 3 dose=50% vs baseline (G2, N=3) | +12.9 pp | Paired t-test | 0.001 |

---

## Data description

### `data/results-G1-G5.csv`

One row per (experiment, seed, generation). Columns:

| Column | Description |
|--------|-------------|
| `dirname` | Unique experiment identifier |
| `group` | Experiment group (G1–G5) |
| `rank` | Nominal LoRA adapter rank |
| `seed` | Random seed for data shuffling |
| `dose` | Synthetic exposure reduction fraction (0–0.5) |
| `bf16` | True if bf16 precision (G3 ablation) |
| `ordem` | True if data-order control seed (G4) |
| `k0` | Size of baseline-correct evaluation set |
| `generation` | Recursive generation index (0–10) |
| `retention` | Raw count of correct answers in K_0 set |
| `retention_pct` | Retention as percentage of K_0 |

Note: The raw CSV has 1,285 rows including duplicates from multiple logging passes.
`make_all.py` deduplicates automatically before analysis.

---

## Software environment

```
Python  3.12
torch   2.4.1+cu121
bitsandbytes  0.43.3
transformers  4.46.0
peft    0.13.2
trl     0.11.4
matplotlib  3.11.1
numpy   2.1.2
```

---

## License

The analysis scripts and figures in this package are released under the
**MIT License**. The manuscript source is provided for review purposes only;
all rights reserved by the authors pending journal publication.

Base model weights (Qwen 2.5, Gemma 3, Gemma 4) are governed by their
respective licenses and are not redistributed here.

---

## Contact

Correspondence regarding the manuscript: see cover letter submitted with MS ID KNOSYS-D-26-21490.
