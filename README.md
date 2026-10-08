<p align="center">
  <h1 align="center">Effective Training Pressure Gates<br>Recursive Knowledge Degradation in LLMs</h1>
  <p align="center"><em>A Multi-Axis Dose-Response Study</em></p>
  <p align="center">
    Replication package &middot; Knowledge-Based Systems (under review) &middot; MS ID KNOSYS-D-26-21490
  </p>
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white" alt="Python 3.12+"></a>
  <a href="https://pytorch.org/"><img src="https://img.shields.io/badge/PyTorch-2.4+-ee4c2c?logo=pytorch&logoColor=white" alt="PyTorch 2.4+"></a>
  <a href="https://huggingface.co/docs/peft"><img src="https://img.shields.io/badge/PEFT-0.13+-brightgreen?logo=huggingface" alt="PEFT 0.13+"></a>
  <a href="https://doi.org/10.5281/zenodo.23145361"><img src="https://zenodo.org/badge/1404826525.svg" alt="DOI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green" alt="License MIT"></a>
  <img src="https://img.shields.io/badge/Journal-Knowledge--Based%20Systems-orange" alt="Knowledge-Based Systems">
  <img src="https://img.shields.io/badge/Checks-14%2F14%20PASS-brightgreen" alt="14/14 PASS">
</p>

---

## Overview

**What happens when you train a language model on its own outputs, recursively?**

We study *recursive fine-tuning* — the feedback loop where a model generates synthetic training data, retrains on it, and repeats — under controlled experimental conditions across three model families, ten recursive generations, and over 50 experimental runs.

<p align="center">
  <img src="https://raw.githubusercontent.com/Jazancort/llm-knowledge-collapse-replication/master/paper/manuscript/figs/scratch/fig1_overview.png" width="700" alt="Study overview: three degradation regimes">
  <br><sub>Fig. 1 — Three degradation regimes emerge as a function of effective training pressure. Homeostatic (>80%): factual retention stable across generations. Bounded (60–80%): moderate, stable loss. Degradative (<60%): progressive collapse.</sub>
</p>

The key finding: **stability is not a fixed property of a model — it is a function of three controllable axes**: adapter rank, learning rate, and synthetic exposure (proportion of synthetic vs. real data). We organize these under the concept of *effective training pressure* (ETP) and show they jointly determine which of three distinct regimes a model enters.

---

## The three-regime structure

<p align="center">
  <img src="https://raw.githubusercontent.com/Jazancort/llm-knowledge-collapse-replication/master/figures/fig1_trajectories.png" width="700" alt="Factual retention trajectories by regime">
  <br><sub>Fig. 2 — Factual retention (% of K₀ items answered correctly) across 10 recursive generations for representative conditions. Green band: homeostatic (>80%). Yellow: bounded. Red: degradative.</sub>
</p>

Across both Qwen 2.5 1.5B and Gemma 3 1B, we observe:

- **Homeostatic** — retention stays above 80% through Gen 10; loss is negligible
- **Bounded** — moderate loss that stabilizes rather than compounding
- **Degradative** — progressive collapse, accelerating over generations

The transition between regimes is **threshold-like**: a small increase in rank or learning rate can shift a model from bounded to degradative within the tested grid.

---

## Dose-response experiments

<p align="center">
  <img src="https://raw.githubusercontent.com/Jazancort/llm-knowledge-collapse-replication/master/figures/fig9_dose_response.png" width="720" alt="Dose-response cross-backbone">
  <br><sub>Fig. 9 — Cross-backbone dose-response. Reducing synthetic exposure (% of training examples replaced by synthetic outputs) improves Gen-10 retention. Qwen (orange): graded, statistically significant response across all doses. Gemma 3 (red): endpoint improvement without rate reduction. Error bands: 95% CI. n = 3–5 paired seeds per dose.</sub>
</p>

| Experiment | Backbone | Dose | Δ Gen10 | 95% CI | p-value | N seeds |
|-----------|----------|------|---------|--------|---------|---------|
| B7 | Qwen 2.5 1.5B r=256 | 10% | +1.8 pp | [−1.1, 4.7] | 0.160 | 5 |
| B7 | Qwen 2.5 1.5B r=256 | 25% | +4.9 pp | [2.5, 7.2] | 0.0044 | 5 |
| B7 | Qwen 2.5 1.5B r=256 | **50%** | **+9.2 pp** | [6.9, 11.6] | **<0.001** | 5 |
| G2 | Gemma 3 1B r=10 | 10% | +9.8 pp | [6.7, 13.0] | 0.006 | 3 |
| G2 | Gemma 3 1B r=10 | 25% | +11.4 pp | [5.8, 17.0] | 0.013 | 3 |
| G2 | Gemma 3 1B r=10 | **50%** | **+12.9 pp** | [9.7, 16.1] | **0.003** | 3 |

All paired t-tests. The effect generalizes across both backbones, ranks, and seed sizes.

---

## Gemma 3 trajectories

<p align="center">
  <img src="https://raw.githubusercontent.com/Jazancort/llm-knowledge-collapse-replication/master/figures/fig_gemma3_trajectories.png" width="700" alt="Gemma 3 trajectories across rank conditions">
  <br><sub>Gemma 3 1B factual retention across 10 recursive generations for multiple rank conditions. The transition from homeostatic to degradative occurs between effective ranks 3 and 6 — approximately 10× lower than the equivalent transition in Qwen.</sub>
</p>

---

## Distributional degradation

<p align="center">
  <img src="https://raw.githubusercontent.com/Jazancort/llm-knowledge-collapse-replication/master/figures/fig5_distributional.png" width="700" alt="Distributional quality metrics">
  <br><sub>At r=128 (Qwen), factual retention remains near 90% — but output-distribution quality collapses. Content efficiency drops 3×, baseline persistence falls to 5.1% (4/78 items), and MTLD drops from 2673 to 745. This dissociation is invisible to scalar retention metrics alone.</sub>
</p>

**Key insight:** a system monitored *only* by factual accuracy would classify r=128 as stable, while its output distribution has already degraded substantially. Distribution-level monitoring catches what retention alone misses.

---

## Intervention effects

<p align="center">
  <img src="https://raw.githubusercontent.com/Jazancort/llm-knowledge-collapse-replication/master/figures/fig6_interventions.png" width="700" alt="Intervention effects">
  <br><sub>Fig. 6 — Comparison of intervention strategies. Reducing synthetic exposure (dose-response, pre-registered) produces the largest and most consistent improvements. Quantization and data-order controls show negligible effects.</sub>
</p>

---

## Study design

<p align="center">
  <img src="https://raw.githubusercontent.com/Jazancort/llm-knowledge-collapse-replication/master/figures/fig7_methodology.png" width="750" alt="Study design and experimental protocol">
  <br><sub>Fig. 7 — Experimental protocol. Each run: (1) sample K₀ from TriviaQA, (2) generate synthetic answers, (3) fine-tune, (4) evaluate retention. Repeat for 10 generations. Three backbones × multiple rank and dose conditions × 3–6 seeds per headline condition.</sub>
</p>

### Experiment summary

| Group | Condition | Backbone | Seeds | Purpose |
|-------|-----------|----------|-------|---------|
| G1 | r=256, dose=0% | Qwen 2.5 1.5B | 3 | Primary degradative baseline |
| G2 | r=10, dose=0/10/25/50% | Gemma 3 1B | 3/dose | Dose-response cross-backbone (pre-registered) |
| G3 | NF4 vs bf16, r=16+r=256 | Qwen 2.5 1.5B | 3/rank | Quantization control |
| G4 | r=256, shuffle seeds | Qwen 2.5 1.5B | 3 | Data-order control |
| G5 | r=128/r=32, prospective Π | Qwen 2.5 1.5B | 1 | Prospective regime test |
| **B7** | r=256, dose=0/10/25/50% | Qwen 2.5 1.5B | **5/dose** | **Pre-registered dose-response** |

**Total: 27 multi-seed runs + 5 single-seed pilots = 52 experimental runs**, all completed with 0 failures on an NVIDIA RTX 4000 Ada (20 GB VRAM).

---

## Reproducing the results (v1.0.4)

### 1. Install dependencies

```bash
pip install torch==2.4.1 transformers==4.46.0 peft==0.13.2 \
            bitsandbytes==0.43.3 scipy matplotlib numpy Pillow
```

### 2. Run all mechanical checks (14/14 PASS)

```bash
cd paper
python scripts/check_knosys.py
```

Checks CI/p-value internal consistency, integer attainability of all reported means and slopes, single-source-of-truth for canonical values, and 10 more structural checks.

### 3. Regenerate all statistics

```bash
cd paper
python scripts/analysis/make_all.py
```

Reads per-seed results files and recomputes all statistics reported in the manuscript. Writes `docs/revision/resultados/make_all_outputs/numbers.tex`.

### 4. Regenerate Fig. 9

```bash
cd paper
python figs/src/fig9_dose_response.py
```

Outputs `figs/final/fig9_dose_response.png` at 300 dpi (2360 × 1460 px).

### 5. Compile the manuscript

```bash
cd paper/manuscript
pdflatex -interaction=nonstopmode manuscript-anonymous.tex
bibtex manuscript-anonymous
pdflatex -interaction=nonstopmode manuscript-anonymous.tex
pdflatex -interaction=nonstopmode manuscript-anonymous.tex
```

---

## Repository structure

```
.
├── README.md
├── CHANGELOG.md          ← version history
├── .zenodo.json          ← Zenodo metadata (auto-read on release)
│
├── paper/                ← replication package (current submission)
│   ├── data/
│   │   ├── per-seed-results/         ← 50 per-seed JSON files (G1–G5, B7, G2)
│   │   │   ├── B7/  G1/  G2/  G3/  G4/  G5/
│   │   └── resultados_consolidados.csv
│   │
│   ├── manuscript/
│   │   ├── manuscript-anonymous.tex  ← LaTeX source
│   │   ├── manuscript-anonymous.pdf  ← compiled PDF
│   │   └── figs/                     ← all manuscript figures
│   │
│   ├── docs/
│   │   └── overleaf/
│   │       ├── response-to-reviewers.tex  ← reviewer response
│   │       └── numbers.tex               ← 100+ canonical value macros
│   │
│   ├── scripts/
│   │   ├── analysis/
│   │   │   ├── make_all.py               ← reproduces all statistics
│   │   │   └── make_per_seed_jsons.py    ← generates per-seed JSONs
│   │   └── audits/
│   │       ├── check_knosys.py           ← 14 mechanical checks
│   │       └── glyph_audit.py            ← equation extraction audit
│   │
│   └── figs/
│       └── src/
│           └── fig9_dose_response.py     ← Fig. 9 generator (300 dpi)
│
└── archive/              ← previous revision artifacts (not needed for reproduction)
    ├── v1/  v2/  v3/     ← earlier manuscript revisions
    ├── old-root/         ← consolidated files from previous package versions
    └── zenodo-staging/   ← internal staging artifacts
```

---

## Data integrity

This package was prepared with a systematic integer-attainability audit of **68 reported quantities** across Tables 4–9 and all body text in §4–§5. All 68 quantities have a unique integer count m such that m/(K₀ × N) rounds to the reported value at the stated precision. Five values were corrected in v1.0.4; see [CHANGELOG.md](CHANGELOG.md).

The `check_knosys.py` script implements 14 mechanical checks. Running it takes < 2 seconds and produces:

```
Results: 14/14 PASS  |  0 FAIL
All checks passed. ✓
```

---

## Zenodo archive

| DOI type | Link | Resolves to |
|----------|------|-------------|
| **Concept** (all versions, always latest) | [10.5281/zenodo.23145361](https://doi.org/10.5281/zenodo.23145361) | Latest release |
| **Version v1.0.4** (this submission) | [10.5281/zenodo.23185146](https://doi.org/10.5281/zenodo.23185146) | This exact snapshot |

> v1.0.4 is the first release that includes the analysis scripts (`make_all.py`), figure-generation scripts, and audit tools. Previous releases (v1.0.2–v1.0.3) contain results data only.

---

## Citation

```bibtex
@article{azancort2026etp,
  title   = {Effective Training Pressure Gates Recursive Knowledge Degradation
             in {LLMs}: {A} Multi-Axis Dose-Response Study},
  author  = {Azancort, J{\'u}lio Leite and
             Teixeira, Carlos Andr{\'e} de Mattos and
             de Carvalho, Andr{\'e} Carlos Ponce de Leon Ferreira and
             Fran{\c{c}}{\`e}s, Carlos Renato Lisboa},
  journal = {Knowledge-Based Systems},
  note    = {Under review, MS ID KNOSYS-D-26-21490},
  year    = {2026},
  doi     = {10.5281/zenodo.23145361}
}
```

---

## License

| Component | License |
|-----------|---------|
| Analysis scripts and figures | **MIT** — see [LICENSE](LICENSE) |
| Manuscript LaTeX source | Provided for review; all rights reserved pending publication |
| Base model weights | Governed by respective model licenses (Qwen, Gemma); not redistributed |

Base-model checkpoint SHA-1 hashes for exact reproducibility are listed in supplementary Table S1 of the article.
