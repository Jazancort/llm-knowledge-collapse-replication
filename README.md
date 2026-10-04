<p align="center">
  <h1 align="center">Effective Training Pressure Gates<br>Recursive Knowledge Degradation in LLMs</h1>
  <p align="center">
    Replication package for the KBS revision · MS ID KNOSYS-D-26-21490
  </p>
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://pytorch.org/"><img src="https://img.shields.io/badge/PyTorch-2.4+-ee4c2c?logo=pytorch&logoColor=white" alt="PyTorch"></a>
  <a href="https://huggingface.co/docs/peft"><img src="https://img.shields.io/badge/PEFT-0.13+-green?logo=huggingface" alt="PEFT"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green" alt="License"></a>
  <img src="https://img.shields.io/badge/Journal-Knowledge--Based%20Systems-orange" alt="KBS">
</p>

---

## What this paper is about

Recursive fine-tuning — retraining a model on its own outputs for successive generations — can progressively erode factual knowledge. We ask: *under what conditions does this degradation emerge, remain bounded, or reverse?*

Through **systematic dose-response experiments** across three model families (Qwen 2.5 1.5B, Gemma 3 1B, Gemma 4 E2B), ten recursive generations, and three to six independent seeds per condition, we show that stability is jointly governed by three controllable axes — adapter rank, learning rate, and synthetic exposure — which we organize under the label **effective training pressure (ETP)**.

---

## Key results

| Finding | Backbone | Evidence |
|---------|----------|----------|
| Threshold-like transition from stable to degradative regime within tested rank grid | Qwen + Gemma 3 | Rank sweep, N=3–6 seeds |
| Regime boundary differs ~10× across architectures (erank ∼3–6 vs ∼50–88) | Gemma 3 vs Qwen | Multi-seed comparison |
| Reducing synthetic exposure by 50% arrests progressive loss | Qwen r=256 | +9.8 pp Gen10, p<0.001, N=5 |
| Dose-response generalizes to second backbone | Gemma 3 r=10 | +12.9 pp Gen10, p=0.001, N=3 |
| Full fine-tuning and QLoRA show the same qualitative pattern | Qwen + Gemma 3 | FFT/QLoRA ablation |
| Quantization (NF4 vs bf16) and data order do not explain the effect | Qwen | G3 and G4 controls, p=0.70 n.s. |

---

## Repository structure

```
.
├── README.md                     ← you are here
├── MANIFEST.md                   ← SHA-256 hashes for all artifacts
│
├── manuscript/
│   ├── manuscript-anonymous.tex  ← LaTeX source (revised)
│   └── cas-refs.bib              ← bibliography
│
├── response/
│   └── response-to-reviewers.tex ← complete reviewer response
│
├── data/
│   ├── results-G1-G5.csv         ← raw results (1,285 rows, 23 runs)
│   ├── results-G1-G5-summary.md  ← per-experiment analysis
│   ├── results-bloco7.md         ← pre-registered Bloco 7 dose-response
│   ├── numbers-canonical.csv     ← 112 canonical numbers used in manuscript
│   ├── numbers-canonical.tex     ← LaTeX macros (\input in manuscript)
│   └── verify.txt                ← 15/15 consistency checks
│
├── scripts/
│   ├── make_all.py               ← reproduces all tables and numbers
│   ├── analyze_results.py        ← detailed G1–G5 analysis
│   ├── seed_level_tests.py       ← exact permutation tests
│   ├── check_consistency.py      ← manuscript integrity checker
│   └── figures/
│       └── fig9_dose_response.py ← generates Fig. 9 (cross-backbone)
│
├── figures/
│   ├── fig1_trajectories.png
│   ├── fig2_dose_response.png
│   ├── fig3_cross_backbone.png
│   ├── fig4_fft_vs_qlora.png
│   ├── fig5_distributional.png
│   ├── fig6_interventions.png
│   ├── fig7_methodology.png
│   ├── fig9_dose_response.png    ← new: dose-response cross-backbone
│   └── ...
│
└── v4/                           ← full project history (manuscript, docs, scripts)
```

---

## Reproducing the results

### Requirements

```bash
pip install torch==2.4.1 transformers==4.46.0 peft==0.13.2 \
            bitsandbytes==0.43.3 matplotlib numpy Pillow
```

### Step 1 — Verify all canonical numbers

```bash
python scripts/make_all.py
```

Expected output: `TODOS OK` with **0 FAILs** across 15 checks. This script reads `data/results-G1-G5.csv`, computes all statistics (means, SDs, CIs, permutation tests), and writes `data/numbers-canonical.tex` with 112 LaTeX macros.

### Step 2 — Regenerate Fig. 9

```bash
python scripts/figures/fig9_dose_response.py
```

Outputs `figures/fig9_dose_response.png` (300 dpi). Requires `matplotlib ≥ 3.7`.

### Step 3 — Compile the manuscript

```bash
cd manuscript
xelatex manuscript-anonymous.tex
bibtex  manuscript-anonymous
xelatex manuscript-anonymous.tex
xelatex manuscript-anonymous.tex
```

The source uses `\input{../data/numbers-canonical}` — run Step 1 first.

---

## Experiment summary

| Group | Condition | Backbone | Seeds | Purpose |
|-------|-----------|----------|-------|---------|
| G1 | r=256, dose=0% | Qwen 2.5 1.5B | 3 | Primary degradative baseline |
| G2 | r=10, dose=0/10/25/50% | Gemma 3 1B | 3/dose | Dose-response cross-backbone |
| G3 | NF4 vs bf16, r=16+r=256 | Qwen 2.5 1.5B | 3/rank | Quantization control |
| G4 | r=256, shuffle seeds 42/101/202 | Qwen 2.5 1.5B | 3 | Data-order control |
| G5 | r=128/r=32, prospective Π index | Qwen 2.5 1.5B | 1 | Prospective regime test |
| Bloco 7 | r=256, dose=0/10/25/50% | Qwen 2.5 1.5B | 5/dose | Pre-registered dose-response |

All 23 runs completed with 0 failures on an NVIDIA RTX 4000 Ada (20 GB).

---

## Data description

`data/results-G1-G5.csv` — one row per (experiment, seed, generation):

| Column | Type | Description |
|--------|------|-------------|
| `dirname` | string | Unique experiment identifier |
| `group` | string | Experiment group (G1–G5) |
| `rank` | int | Nominal LoRA adapter rank |
| `seed` | int | Random seed for data shuffling |
| `dose` | float | Synthetic exposure reduction (0–0.5) |
| `bf16` | bool | True = bf16 precision (G3 ablation) |
| `ordem` | bool | True = data-order control seed (G4) |
| `k0` | int | Baseline-correct evaluation set size |
| `generation` | int | Recursive generation index (0–10) |
| `retention` | int | Correct answers in K₀ at this generation |
| `retention_pct` | float | retention / k0 × 100 |

Note: the raw CSV has 1,285 rows including duplicates from multiple logging passes. `make_all.py` deduplicates automatically.

---

## Statistical approach

- **Experimental unit:** training seed/run (not individual evaluation items)
- **Primary test (Gemma 3):** exact bilateral permutation over C(10,5)=252 allocations — p=0.008
- **Within-protocol Qwen (G3 paired):** sign-flip test, N=3 pairs — p=0.25 (consistent direction, underpowered)
- **Dose-response:** paired t-test per dose vs. unmodified baseline
- **Order control (G4):** exact bilateral permutation C(6,3)=20 — p=0.70 n.s.
- **Quantization control (G3):** paired sign-flip — p=1.00 (Δ=0 pp at both ranks)

---

## Citation

```bibtex
@article{azancort2026etp,
  title   = {Effective Training Pressure Gates Recursive Knowledge Degradation in {LLMs}},
  author  = {Azancort, J{\'u}lio and {[co-authors]}},
  journal = {Knowledge-Based Systems},
  note    = {Under review, MS ID KNOSYS-D-26-21490},
  year    = {2026}
}
```

---

## License

Analysis scripts and figures: **MIT License** — see `LICENSE`.  
Manuscript source: provided for review purposes; all rights reserved pending journal publication.  
Base model weights are governed by their respective licenses (Qwen, Gemma) and are not redistributed.
