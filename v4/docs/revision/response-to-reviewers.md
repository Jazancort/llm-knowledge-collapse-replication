# Response to Reviewers — v4

**Journal:** Knowledge-Based Systems (Elsevier)
**Manuscript ID:** KNOSYS-D-26-21490
**Title:** Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study
**Round:** 1st revision
**Date:** <!-- inserir data de envio -->

---

We thank the editor and both reviewers for their careful and constructive reading of the manuscript. The comments identify genuine weaknesses — in notation consistency, equation rendering, internal data consistency, statistical reporting, and the framing of the ETP construct — and we have addressed each point systematically below. All changes are indicated in **bold** in the revised manuscript.

---

## Editor

> Revise (Including Language Editing). Provide point-by-point response to each comment.

We have revised the manuscript throughout for language clarity and have used Elsevier's Author Services English Language Editing service. The point-by-point response follows below.

---

## Reviewer 1

### R1.Q1

> How can effective training pressure be quantitatively calibrated and prospectively tested on an unseen backbone or dataset?

<!-- resposta -->

### R1.Q2

> How are quantization, optimizer state, data order, and model-specific dynamics separated from the claimed pressure effects?

<!-- resposta -->

### R1.Q3

> Do the conclusions hold for longer answers, multi-hop questions, other domains, and larger factual evaluation sets?

<!-- resposta -->

### R1.Q4

> Why does the five-percent exposure reduction stabilize Qwen but not Gemma 3, and does this generalize across ranks and seeds?

<!-- resposta -->

### R1.Q5

> What complete code, checkpoints, prompts, seeds, and raw outputs will support independent reproduction?

<!-- resposta -->

---

## Reviewer 2

### R2.1 — Abbreviations and notations

> ETP appears in Figure 1 ("ETP threshold identification") but is never explicitly defined as "effective training pressure."

<!-- resposta -->

> MTLD is introduced as "a length-robust diversity estimate" but the acronym is not expanded.

<!-- resposta -->

> KL, JS, and coverage appear in Figure 1 without definition.

<!-- resposta -->

> bf16, SVD, TCE, QLoRA, and LoRA are used without consistently expanded forms.

<!-- resposta -->

> "Homeo." is used in Table 2 without definition.

<!-- resposta -->

> K0 is used both as a set of questions and as a retention metric. This dual use is not always clear.

<!-- resposta -->

> T, D1_T, D10, ΔI, Instability(1), MeanLen_T, and related symbols in Eq. 6 are not fully defined.

<!-- resposta -->

> The effective-rank formula uses σ_i as both singular values and normalized singular values. The normalization condition is mathematically incorrect as written.

<!-- resposta -->

> BA_F, θ_i^(t), θ_i^(0), and related notation in the drift equation are not consistently defined.

<!-- resposta -->

> "r E 4,10,12,14,16" and "r \dot{E} \sim 10,12,14" are garbled; they should be clear set notation.

<!-- resposta -->

---

### R2.2 — Equations and tables

> Equations 1–6 are severely malformed in the provided PDF. Eq. 1 uses "Retention.t /" instead of a clear function notation and has garbled summation over K0.

<!-- resposta -->

> Eq. 2 for effective rank is missing the negative sign and summation.

<!-- resposta -->

> Eq. 6 for SDI-3 is unclear: signs, log ratios, and the ΔI term are not consistently defined.

<!-- resposta -->

> What is "5İ10^6" in Table 7? Please check also elsewhere.

<!-- resposta -->

---

### R2.3 — Technical and data inconsistencies

> **Qwen threshold inconsistency:** Abstract and Section 4.2.3 say the Qwen boundary is between effective ranks 50–88. Section 5.1 says Qwen remains outside the degradative regime "up to effective rank 150." This contradicts Table 2, where r=256 has effective rank 87.57 and is degradative.

<!-- resposta -->

> **r=128 classification:** r=128 is classified as "Bounded" in Table 2, but Section 4.4.3 calls r=128 and r=256 "above-threshold configurations."

<!-- resposta -->

> **r=256 boundary claim:** r=256 is repeatedly called a "boundary configuration," but Table 2 classifies it as degradative. The boundary lies between r=128 and r=256.

<!-- resposta -->

> **Gemma 3 degradative range:** Section 5.2 says "r ≥ 16 on Gemma 3," but Table 4 shows r=10,12,14 already degradative at Gen5. The boundary is below r=10.

<!-- resposta -->

> **Abstract overclaim:** "three to five independent seeds per condition" is not true. Many conditions are single-seed.

<!-- resposta -->

> **FFT on Gemma 3:** Non-monotonic results (78.3%, 54.3%, 63.0%). The conclusion that this "confirms" the magnitude axis is too strong for a single-seed, non-monotonic result.

<!-- resposta -->

> **C5 removal percentage:** Section 3.4 mentions "15° removal," while Section 4.5 reports approximately 5% token reduction.

<!-- resposta -->

---

### R2.4 — Methodology

> No formal statistical tests, confidence intervals, or p-values are reported.

<!-- resposta -->

> The effective training pressure framework is not quantified. It is a useful organizing metaphor, but not a predictive model.

<!-- resposta -->

> Cross-architecture normalization failed, but no alternative calibration method is proposed.

<!-- resposta -->

> "Effective training pressure" is not a new quantitative measure; it is a conceptual label for three already-known axes.

<!-- resposta -->

> The Gemma 4 E2B backbone lacks a citation, may be confused with Gemma 3n E2B, and its architecture is described without a source.

<!-- resposta -->

> The "sharp transition" claim is weakened by sparse rank grids and wide threshold intervals.

<!-- resposta -->

---

### R2.5 — Format and citations

> Reference [12] and [33] share the same arXiv number: arXiv:2408.14572.

<!-- resposta -->

> Reference [32] lists arXiv:2512.15634 with year 2024, which is impossible if the arXiv ID is December 2025.

<!-- resposta -->

> No citation is provided for Gemma 4 E2B IT, despite it being a central backbone.

<!-- resposta -->

> Reference [7] "Keisha et al." is used heavily but appears to be a preprint with no venue.

<!-- resposta -->

> Reference formatting is inconsistent.

<!-- resposta -->
