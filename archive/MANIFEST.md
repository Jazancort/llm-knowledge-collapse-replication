# Artifact Manifest

**Package:** KNOSYS-D-26-21490 Replication Package  
**Generated:** 2026-10-04 17:54 UTC-3  
**Total files:** 25

SHA-256 values are truncated to 16 characters for readability.
Full hashes can be recomputed with `sha256sum` or `certutil -hashfile <file> SHA256`.

---

## Manuscript source

| File | SHA-256 (first 16) | Size |
|------|--------------------|------|
| `manuscript/manuscript-anonymous.tex` | `62a5ceb4bb1f84f9` | 135.5 KB |
| `manuscript/cas-refs.bib` | `b139052b65903d96` | 16.7 KB |

## Reviewer response

| File | SHA-256 (first 16) | Size |
|------|--------------------|------|
| `response/response-to-reviewers.tex` | `6315bd5958161789` | 53.7 KB |

## Data

| File | SHA-256 (first 16) | Size |
|------|--------------------|------|
| `data/results-G1-G5.csv` | `ff5c74fdef3aa1fc` | 85.4 KB |
| `data/results-G1-G5-summary.md` | `dde4625ff4506bcf` | 8.2 KB |
| `data/results-bloco7.md` | `7e360c0727f4f44e` | 6.7 KB |
| `data/numbers-canonical.csv` | `4ce917796ccdfdb3` | 3.3 KB |
| `data/numbers-canonical.tex` | `01fd88db9152e697` | 4.1 KB |
| `data/verify.txt` | `624f3d265be4a548` | 1.0 KB |

## Analysis scripts

| File | SHA-256 (first 16) | Size |
|------|--------------------|------|
| `scripts/make_all.py` | `ed41f25cce61d8a1` | 29.9 KB |
| `scripts/analyze_results.py` | `d9ca637c36db7fb5` | 9.1 KB |
| `scripts/seed_level_tests.py` | `38bfdccc37fd2b37` | 6.3 KB |
| `scripts/check_consistency.py` | `a60a99c019449fde` | 2.3 KB |

## Figure scripts

| File | SHA-256 (first 16) | Size |
|------|--------------------|------|
| `scripts/figures/fig9_dose_response.py` | `01a6ebad1f54b30b` | 5.1 KB |

## Figures

| File | SHA-256 (first 16) | Size |
|------|--------------------|------|
| `figures/fig1_trajectories.png` | `aafcbf5d0707b75a` | 90.3 KB |
| `figures/fig2_dose_response.png` | `f3bd3666e7769de1` | 231.0 KB |
| `figures/fig3_cross_backbone.png` | `f5a8168d5d5c147b` | 201.5 KB |
| `figures/fig4_fft_vs_qlora.png` | `58620644981c29b3` | 57.7 KB |
| `figures/fig5_distributional.png` | `9e684e14798b9b52` | 363.3 KB |
| `figures/fig6_interventions.png` | `202fe40002c13adf` | 166.3 KB |
| `figures/fig7_methodology.png` | `8280ab42dfd60416` | 695.2 KB |
| `figures/fig9_dose_response.png` | `6adb4081f4fd23fb` | 218.5 KB |
| `figures/fig_gemma3_trajectories.png` | `689d12cc0f007e98` | 374.1 KB |
| `figures/fig_rank_lr_heatmap.png` | `75fca5c9be9d832f` | 94.6 KB |
| `figures/fig_regime_examples.png` | `fe3354b9433f625e` | 207.3 KB |

---

## Reproducing the verification

```bash
# 1. Check all canonical numbers
python scripts/make_all.py
# Expected output: "TODOS OK" with 0 FAILs

# 2. Regenerate Fig. 9
python scripts/figures/fig9_dose_response.py
# Output: figures/fig9_dose_response.png

# 3. Compile manuscript (requires LaTeX with xelatex + bibtex)
cd manuscript
xelatex manuscript-anonymous.tex
bibtex  manuscript-anonymous
xelatex manuscript-anonymous.tex
xelatex manuscript-anonymous.tex
```
