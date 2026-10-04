# Reviewer Comments — v3 → v4

**Journal:** Knowledge-Based Systems (Elsevier)
**Manuscript ID:** KNOSYS-D-26-21490
**Title:** Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study
**Round:** 1st revision
**Date received:** 2026-09-29
**Deadline for revised manuscript:** 2026-10-20
**Decision:** Conditionally accepted pending revision (major revision)

---

## Editor (Hang Yu, Senior Editor)

Revise (Including Language Editing).

Requirements for resubmission:
- Cover letter, response to reviewers, highlights, revised manuscript, credit author statement, author agreement, and declaration of interest: all in Word format.
- Source file: Word or LaTeX (one final version only); include supporting .bib files.
- Tables, figures, and equations must be in editable format.
- Figures: 300 dpi minimum, not in PDF format.
- Provide point-by-point response to each reviewer comment in the cover letter.

---

## Reviewer 1

This paper studies recursive fine-tuning on synthetic data across Qwen 2.5 1.5B, Gemma 3 1B, and Gemma 4 E2B for ten generations. By varying adapter rank, learning rate, and synthetic exposure, it proposes effective training pressure as an empirical account of transitions between stable retention and factual degradation. The systematic design, multi-seed headline experiments, and distributional diagnostics are valuable. However, the proposed pressure is not yet a transferable quantitative predictor, the main metric uses one short-answer dataset, several analyses are single-seed, and the exposure intervention is shown mainly for one Qwen condition. Major revision is required.

### R1.Q1

How can effective training pressure be quantitatively calibrated and prospectively tested on an unseen backbone or dataset?

### R1.Q2

How are quantization, optimizer state, data order, and model-specific dynamics separated from the claimed pressure effects?

### R1.Q3

Do the conclusions hold for longer answers, multi-hop questions, other domains, and larger factual evaluation sets?

### R1.Q4

Why does the five-percent exposure reduction stabilize Qwen but not Gemma 3, and does this generalize across ranks and seeds?

### R1.Q5

What complete code, checkpoints, prompts, seeds, and raw outputs will support independent reproduction?

---

## Reviewer 2

The paper addresses a timely and practically relevant question and provides a useful empirical dose-response characterization. However, the current manuscript has major issues in notation, equations, table/figure formatting, internal consistency, statistical rigor, and citation accuracy. The "effective training pressure" framework is promising but currently conceptual rather than quantitative. The cross-architecture claims are weakened by the uncited Gemma 4 E2B model and limited scale. I recommend major revision before further consideration.

### R2.1 — Abbreviations and notations

- ETP appears in Figure 1 ("ETP threshold identification") but is never explicitly defined as "effective training pressure."
- MTLD is introduced as "a length-robust diversity estimate" but the acronym is not expanded.
- KL, JS, and coverage appear in Figure 1 without definition.
- bf16, SVD, TCE, QLoRA, and LoRA are used without consistently expanded forms. Some are only indirectly explained.
- "Homeo." is used in Table 2 without definition.
- K0 is used both as a set of questions and as a retention metric. This dual use is not always clear.
- T, D1_T, D10, ΔI, Instability(1), MeanLen_T, and related symbols in Eq. 6 are not fully defined.
- The effective-rank formula uses σ_i as both singular values and normalized singular values. The normalization condition is mathematically incorrect as written.
- BA_F, θ_i^(t), θ_i^(0), and related notation in the drift equation are not consistently defined.
- "r E 4,10,12,14,16" and "r \dot{E} \sim 10,12,14" are garbled; they should be clear set notation.

### R2.2 — Equations and tables

- Equations 1–6 are severely malformed in the provided PDF. For example, Eq. 1 uses "Retention.t /" instead of a clear function notation and has garbled summation over K0.
- Eq. 2 for effective rank is missing the negative sign and summation. It should be something like exp(−Σ p_i log p_i), with p_i = σ_i / Σ_j σ_j.
- Eq. 6 for SDI-3 is unclear: signs, log ratios, and the ΔI term are not consistently defined.
- What is "5İ10^6" in Table 7? Please check also elsewhere.

### R2.3 — Technical and data inconsistencies

- **Qwen threshold inconsistency:** Abstract and Section 4.2.3 say the Qwen boundary is between effective ranks 50–88. Section 5.1 says Qwen remains outside the degradative regime "up to effective rank 150." This contradicts Table 2, where r=256 has effective rank 87.57 and is degradative.
- **r=128 classification:** r=128 is classified as "Bounded" in Table 2, but Section 4.4.3 calls r=128 and r=256 "above-threshold configurations." Inconsistent.
- **r=256 boundary claim:** r=256 is repeatedly called a "boundary configuration," but Table 2 classifies it as degradative, not bounded. The boundary lies between r=128 and r=256, not at r=256 itself.
- **Gemma 3 degradative range:** Section 5.2 says "r ≥ 16 on Gemma 3," but Table 4 shows r=10,12,14 already degradative at Gen5. The boundary is below r=10.
- **Abstract overclaim:** "three to five independent seeds per condition" is not true. Many conditions are single-seed; only headline comparisons have multiple seeds.
- **FFT on Gemma 3:** Non-monotonic results (78.3% at 10^-6, 54.3% at 5×10^-6, 63.0% at 10^-5). The conclusion that this "confirms" the magnitude axis is too strong for a single-seed, non-monotonic result.
- **C5 removal percentage:** Section 3.4 mentions "15° removal," while Section 4.5 reports approximately 5% token reduction. This discrepancy must be clarified.

### R2.4 — Methodology

- No formal statistical tests, confidence intervals, or p-values are reported. The paper relies on ranges and non-overlap, which is weak for inference.
- The effective training pressure framework is not quantified. It is a useful organizing metaphor, but not a predictive model.
- Cross-architecture normalization failed, but no alternative calibration method is proposed.
- "Effective training pressure" is not a new quantitative measure; it is a conceptual label for three already-known axes. The paper does not derive a scalar predictor or formal theory.
- The Gemma 4 E2B backbone is a serious concern: it lacks a citation, may be confused with Gemma 3n E2B, and its architecture is described without a source. This undermines the cross-architecture claims.
- The "sharp transition" claim is weakened by sparse rank grids and wide threshold intervals. "Sharp" may be an overstatement.

### R2.5 — Format and citations

- Reference [12] and [33] share the same arXiv number: arXiv:2408.14572. This is a serious citation error.
- Reference [32] lists arXiv:2512.15634 with year 2024, which is impossible if the arXiv ID is December 2025.
- No citation is provided for Gemma 4 E2B IT, despite it being a central backbone.
- Reference [7] "Keisha et al." is used heavily but appears to be a preprint with no venue. Its reliability should be clarified.
- Reference formatting is inconsistent: some entries include conference proceedings, others only arXiv, some lack page numbers or venues.
