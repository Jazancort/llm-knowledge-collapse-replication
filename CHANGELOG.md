# Changelog

All notable changes to the replication package are documented in this file.

## [v1.0.4] - 2026-10-06

### Added
- `scripts/analysis/make_all.py`: regenerates all reported statistics, tables and
  figures from the consolidated per-seed results and verifies each value against
  the manuscript.
- `figs/src/fig9_dose_response.py`: regenerates the dose-response figure at 300 dpi.
- `scripts/audits/glyph_audit.py`: compares the extracted text of every equation,
  table cell, figure label and caption against the LaTeX source.
- `scripts/audits/check_knosys.py`: 16 mechanical checks, including
  `check_13` (confidence interval versus p-value internal consistency),
  `check_14` (integer attainability of reported means and slopes), and
  `check_16` (single-source-of-truth for canonical values).

### Changed
- The paired t-test now uses `scipy.stats.t.sf` for all degrees of freedom,
  replacing a coarse critical-value lookup table that was inaccurate for df >= 3.
- Per-arm Gen 5 means for the 50% exposure arm are stored at two decimal places,
  so endpoint slopes are computed on unrounded means.

### Fixed
Five reported values corrected after an integer-attainability audit of 68 quantities:
- G4 pooled mean, 80.4% to 80.3% (188/234).
- B7 50% endpoint slope, -0.14 to -0.15 pp/generation (350/390 to 347/390).
- B7 25% dose p-value, now 0.0044 (exact 0.004425).
- Gemma 3 r=4 Gen 10 retention in the response letter, 94.4% to 94.3% (217/230).
- r=128 baseline persistence, 5.2% to 5.1% (4/78).

---

## [v1.0.3] - 2026-10-05

Initial public release of the replication package. Contains consolidated per-seed
results files, training configuration files, the evaluation protocol, question
partition identifiers, and K0 baseline sets for all three backbones (Qwen 2.5 1.5B,
Gemma 3 1B, Gemma 4 E2B).
