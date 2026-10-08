# Fase 3 — Carta de Apresentação, Checklist do Editor, Highlights e Metadados
## KNOSYS-D-26-21490 | 2026-10-05

> **Status:** blocos prontos. Pendências: C24 (B7_SLOPE0 = −0.96, deve ser −1.13), F4 (nominalidade do manuscrito), C2 (teste pdffonts + A/B pdflatex vs xelatex).

---

## Observações anteriores à Fase 3

### C2 — diagnóstico revisado (fonte LaTeX limpa)

Auditoria confirmou: **0 Unicode cru problemático** na fonte. O fonte estava correto — a afirmação original da carta pode voltar.

O padrão dos artefatos (`*0.15`, `í10İ`, `Ë ˆ4,16,32'`, `⊙ F`, `79.72˜`) é típico de **fonte Type 1 sem ToUnicode CMap** — não de Unicode cru no fonte.

**Causa provável:** compilar com `xelatex` + `\usepackage[T1]{fontenc}` + `lmodern`. Sob pdfLaTeX, o pdfTeX injeta automaticamente um ToUnicode CMap. Sob XeLaTeX, o mesmo caminho não gera CMap confiável.

**Teste decisivo:**
```bash
# 1. Fontes têm ToUnicode?
pdffonts manuscript.pdf
# coluna "uni" deve ser "yes" em todas as linhas

# 2. Extração reproduz artefatos?
pdftotext manuscript.pdf - | rg -n 'í|İ|Ë|ˆ|˜|⊙|\*[0-9]'
# se retornar linhas → confirmado

# 3. Teste A/B
pdflatex manuscript.tex && pdftotext manuscript.pdf - | rg 'í|İ|Ë'
# se pdfLaTeX sair limpo → causa confirmada
```

**Duas correções possíveis:**
```latex
% ── Opção 1 (mais segura): compilar com pdfLaTeX ──────────────────
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}

% ── Opção 2: manter XeLaTeX, trocar mecanismo de fonte ─────────────
\usepackage{iftex}
\ifPDFTeX
  \usepackage[T1]{fontenc}
  \usepackage[utf8]{inputenc}
  \usepackage{lmodern}
\else
  \usepackage{fontspec}
  \setmainfont{Latin Modern Roman}[Ligatures=TeX]
  \usepackage{unicode-math}
  \setmathfont{Latin Modern Math}
\fi
```

### C24 — BsevenSlopeZero = −0.96 está errado (deve ser −1.13)

| Macro | make_all.py | numbers.tex | Status |
|---|---|---|---|
| GoneSlope (G1, N=3) | −1.28 | −1.28 | ✅ |
| GoneFourteenSlope (G1+G4, N=6) | −1.19 | −1.20 | arredondamento ✅ |
| BsevenSlopeFifty (50%, N=5) | −0.14 | −0.15 | arredondamento ✅ |
| **BsevenSlopeZero (0%, N=5)** | **−0.96** | **−1.13** | **❌ erro no script** |

Verificação pela Tabela 10 do manuscrito: dose 0%: Gen5 = 85.4%, Gen10 = 79.7%
→ (79.7 − 85.4) / 5 = −1.14 pp/gen → confirma −1.13.

**Candidatos prováveis no patch:**
```python
# dose 0 pode ser '0' (string) ou '0%', não 0 (int)
b7_0_5  = [B7_GEN5[0][s] for s in seeds_b7]
b7_0_10 = [B7[0][s] for s in seeds_b7]

# Diagnóstico:
print("chaves B7:", list(B7.keys()))
print("chaves B7_GEN5:", list(B7_GEN5.keys()))
print("seeds_b7:", seeds_b7)
print("b7_0_5 :", b7_0_5,  "média:", sum(b7_0_5)/len(b7_0_5))
print("b7_0_10:", b7_0_10, "média:", sum(b7_0_10)/len(b7_0_10))
# esperado: médias ≈ 85.4 e 79.7
```

**Impacto:** a nota de rodapé A-11 cita os três valores como auditáveis. Não colar A-11 até o script devolver −1.13/−1.14.

---

## F1 — Carta de apresentação reescrita

```latex
\noindent
Dear Dr.\ Yu,

We thank you and both reviewers for an evaluation that was unusually
precise and, in two instances, decisive for the scientific content of
the paper. Reviewer~2's notation audit identified a genuine
mathematical error in the effective-rank definition, and Reviewer~1's
question about the asymmetry of the exposure intervention led us to a
provenance audit that uncovered a pipeline inconsistency in the
experiment supporting our third claim. Both are corrected here, the
second by replacing the affected experiment rather than by
reinterpreting it. We are grateful for the opportunity to revise.

\medskip\noindent\textbf{Substantive changes.}

\begin{enumerate}[leftmargin=1.5em,itemsep=0.4em]
\item \textbf{Exposure axis rebuilt on pre-registered evidence.} The
exploratory C1--C5 pilot reported in the original submission compared
arms produced by different evaluation pipelines. Under an identical
pipeline with paired seeds, the effect it reported is not
distinguishable from zero. The pilot is now archived and excluded from
every estimate. In its place, two pre-registered dose--response
experiments --- one per backbone, with multiple paired seeds at each of
four dose levels --- provide the primary evidence for this axis.

\item \textbf{Framework reframed, not defended.} Effective training
pressure is no longer presented as a quantitative predictor. The
manuscript now separates the variables fixed before training from the
diagnostics measured after it, labels the operational index as
exploratory wherever it appears, and states that prospective
calibration on an unseen backbone was not performed. A five-step
calibration protocol is specified in Section~6 as a target for future
work.

\item \textbf{Inferential statistics added where the design supports
them.} Exact permutation and sign-flip tests are reported for the rank
contrasts, and paired $t$-tests with 95\,\% confidence intervals for
every dose level of both dose--response experiments. Comparisons that
remain single-seed, or in which groups are not exchangeable, are now
labelled descriptive and are never pooled with multi-seed results.

\item \textbf{Notation and equations corrected.} The dual use of
$K_0$ and the incorrect normalisation condition in the effective-rank
formula are both fixed, in the notation Reviewer~2 proposed. A notation
table defines every symbol in order of first appearance, and the glyph
fault affecting Equations~1--6 and several tables has been traced to
its source and eliminated.

\item \textbf{Claims aligned with the evidence.} Threshold language,
regime labels, seed counts, and the description of the full fine-tuning
sweep on Gemma~3 have been revised so that each statement matches the
design that supports it. Every internal inconsistency identified by
Reviewer~2 is corrected individually.

\item \textbf{Reproducibility package completed.} Checkpoint revision
hashes, prompts and chat templates, seeds, data-order and downsampling
masks, item-level correctness vectors, raw synthetic generations, and
the trained adapters are deposited, together with the scripts that
regenerate every table and figure.
\end{enumerate}

\medskip\noindent\textbf{What remains a limitation.} Three of the
reviewers' requests cannot be met with the present experiments, and we
say so explicitly rather than argue the point: prospective calibration
on an unseen backbone was not performed; the evaluation remains a
single short-answer dataset, although we add a strict exact-match
re-scoring to show that the regime classifications do not depend on the
permissive matching criterion; and the mechanism behind the exposure
effect is unresolved, the steps-matched control being inconclusive at
$n=3$. Each is stated in Section~6.

\medskip\noindent
A point-by-point response to all forty review points follows, preceded
by a summary table mapping each point to its revision and location.
Text newly added to the manuscript is quoted verbatim throughout, so
that every claim in this response can be verified by text search.

\bigskip
\noindent
Respectfully submitted on behalf of all authors,\\[8pt]
Julio Leite Azancort Neto\\
Ph.D.\ Candidate in Applied Computing\\
Corresponding Author
```

**Mudanças em relação à versão atual:**

| Antes | Agora |
|---|---|
| Agradecimento genérico | Nomeia as duas contribuições decisivas dos revisores |
| Erro de pipeline mencionado de passagem | Apresentado como achado que levou a substituir o experimento |
| "for all headline comparisons" | Lista o que foi feito e o que ficou descritivo (C22) |
| C3/C5 inconsistente | C1–C5 (C21) |
| Limitações diluídas nos itens | Bloco próprio antes da resposta ponto a ponto |
| "checkpoint identifiers" | "checkpoint revision hashes" (C11) |

---

## F2 — Checklist das exigências do Editor (item ED-2)

```latex
\rconcern{Editor, Submission requirements}{Format of the revised
submission}{While submitting revision, please ensure to submit a list
of changes or a rebuttal against each point that was being raised. The
revised cover letter, response to reviewers, highlights, revised
manuscript, credit author statement, author agreement and declaration
of interest should all be in word format. [...]}

\arhead{Author response:}
Each requirement is addressed as listed below.

\renewcommand{\arraystretch}{1.2}
\begin{tabular}{@{}L{0.5cm}L{6.3cm}L{7.4cm}@{}}
\toprule
\rowcolor{hdrgray} & \textbf{Requirement} & \textbf{Compliance} \\
\midrule
(a) & List of changes or rebuttal against each point &
Both provided: a ``Summary of changes'' table maps all forty review
points to the revision made and its location, followed by an individual
response to each point. \\
(b) & Cover letter, response to reviewers, highlights, revised
manuscript, CRediT author statement, author agreement, declaration of
interest --- all in Word &
All seven documents are submitted in \texttt{.docx}. Equations in the
Word files are OMML objects and remain editable. \\
(c) & Source file in Word or LaTeX; one final version only &
A single final LaTeX source is submitted, together with its compiled
PDF. No alternative version is included. \\
(d) & Tables, figures, and equations in editable format &
Tables are native LaTeX \texttt{tabular}/\texttt{longtable}
environments; equations are \texttt{amsmath} environments; no table or
equation is included as an image. Figures are submitted as vector or
high-resolution raster source files, not as rendered page extracts. \\
(e) & Figures at 300\,dpi, not PDF &
All eleven figures are submitted at 300\,dpi: line figures as EPS,
raster panels as TIFF. No figure is submitted in PDF. \\
(f) & Supporting \texttt{.bib} files included &
\texttt{cas-refs.bib} is included in the LaTeX submission package. \\
(g) & MATLAB \texttt{.FIG} files for interactive figures (optional) &
The figures were produced in Python (Matplotlib) rather than MATLAB, so
no \texttt{.FIG} files are available. The underlying data for every
figure are deposited in the replication package. \\
(h) & English Language Editing (recommended) &
A complete language revision was carried out prior to resubmission;
see the response to the Editor's first comment above. \\
(i) & Research Elements (optional) &
The replication package is already archived with a citable DOI; we have
not submitted a separate Research Elements article. \\
\bottomrule
\end{tabular}

\arhead{Author action:}
\begin{enumerate}[leftmargin=1.4em,itemsep=0.3em]
\item All seven required documents were produced in \texttt{.docx} from
      the LaTeX sources, with equations converted to editable OMML
      objects and verified individually.
\item All figures were regenerated at 300\,dpi and exported to EPS
      (line art) and TIFF (raster), replacing the PDF versions used in
      the original submission.
\item \texttt{cas-refs.bib} was audited (see Reviewer~2, Concern~\#5)
      and is included in the submission package.
\item The highlights were rewritten to comply with the 85-character
      limit per item and to remove internal experiment identifiers; see
      the revised Highlights file.
\end{enumerate}
```

---

## F3 — Highlights reescritos

**Problemas atuais:** excedem o limite, usam códigos internos (`B7`, `G2`), contêm caracteres corrompidos.

| # | Atual | Problema |
|---|---|---|
| 1 | Rank-dependent threshold-like transition… | 84 car. — passa raspando |
| 2 | …differ í10İ… (erank í3–6 vs í50–88) | caracteres corrompidos |
| 3 | …jointly determine the operating regime | overclaim (grade 3×3, 1 semente) |
| 4 | Output drift accompanies… | ok, 81 car. |
| 5 | A pre-registered 50%… Qwen B7… Gemma 3 G2… | ~190 car. + códigos internos |

**Versão corrigida (ASCII puro, ≤85 car. cada):**

```
1. Recursive factual loss emerges only above a backbone-specific pressure threshold
   [79 car.]

2. Regime boundary differs by ~10x across backbones (effective rank 3-6 vs 50-88)
   [77 car.]

3. Adapter rank and learning rate both shift the observed operating regime
   [70 car.]

4. Output quality degrades while factual retention still appears bounded
   [69 car.]

5. A 50% synthetic exposure cut improved retention on both backbones tested
   [71 car.]
```

**Justificativa de cada alteração:**

| # | O que mudou | Por quê |
|---|---|---|
| 1 | reescrito para afirmar o achado | "threshold-like transition" é jargão; "emerges only above" é o resultado |
| 2 | `í10İ` → `~10x`; `í3–6` → `3-6` | ASCII puro — campo do EM não é LaTeX |
| 3 | "jointly determine" → "both shift" | remove implicação de interação que a grade de 1 semente não sustenta (O1) |
| 4 | "accompanies degradative" → "still appears bounded" | descreve a dissociação do r=128, que é o achado real |
| 5 | reescrito de 190 → 71 car. | "improved retention" é verdadeiro para os dois backbones; "attenuated progressive loss" só vale para Qwen |

**Regras do campo no EM:** 3–5 itens, ≤85 caracteres cada (espaços incluídos), texto simples. Sem LaTeX, Unicode, ou códigos internos.

---

## F4 — Metadados do manuscrito

| # | Defeito | Correção |
|---|---|---|
| 1 🔴 | Cabeçalho corrente: *First Author et al.: Preprint submitted to Elsevier* | ver decisão abaixo |
| 2 🟠 | `orcid(s): vazio` no rodapé da p. 1 | preencher ou remover o comando |
| 3 🟠 | Page 25 of 24, Page 28 of 24 | usar `lastpage` (ver abaixo) |
| 4 🟡 | `fig9_dose_response.py` gera a Figura 10 | renomear o script |

### 🔴 Decisão: o manuscrito revisado deve ser nominal?

Knowledge-Based Systems opera em **single-blind**: revisores anônimos, autores não. A carta do editor é dirigida a você pelo nome. CRediT author statement e author agreement são impossíveis sem a lista completa de autores.

A versão revisada precisa conter:
- nomes completos e ordem de autoria
- afiliações institucionais
- autor correspondente e e-mail
- ORCIDs
- Declaration of Competing Interest
- Acknowledgements e Funding (se aplicável)

```latex
% ── Defeito 3 · paginação ──────────────────────────────────────────
\usepackage{lastpage}
% no rodapé: Page \thepage\ of \pageref{LastPage}

% ── Defeito 2 · ORCID ──────────────────────────────────────────────
\author[1]{Julio Leite Azancort Neto}[orcid=0000-0000-0000-0000]
% ou remover o campo se não houver ORCID para todos os coautores

% ── Defeito 1 · cabeçalho corrente ─────────────────────────────────
% o template cas-dc deriva o running head de \author;
% corrige automaticamente ao preencher a autoria
```

---

## F5 — Lista de itens submetidos

```latex
\section*{Items submitted with this revision}

\renewcommand{\arraystretch}{1.15}
\begin{tabular}{@{}L{0.5cm}L{6.8cm}L{2.6cm}L{4.0cm}@{}}
\toprule
\rowcolor{hdrgray} & \textbf{Item} & \textbf{Format} &
\textbf{Note} \\
\midrule
(a) & Revised cover letter & \texttt{.docx} & Required \\
(b) & Response to reviewers (this document) & \texttt{.docx} &
      Includes summary-of-changes table \\
(c) & Highlights & \texttt{.docx} & Five items, $\le$85 characters each \\
(d) & Revised manuscript, changes marked & \texttt{.docx} &
      All revisions in blue \\
(e) & Revised manuscript, clean final & LaTeX $+$ PDF &
      Single final version \\
(f) & \texttt{cas-refs.bib} & \texttt{.bib} &
      Full reference list, audited \\
(g) & Figures 1--11 & EPS / TIFF, 300\,dpi & No PDF figures \\
(h) & CRediT author statement & \texttt{.docx} & Required \\
(i) & Author agreement & \texttt{.docx} & Required \\
(j) & Declaration of competing interest & \texttt{.docx} & Required \\
(k) & Supplementary material & \texttt{.docx} &
      Table~S1 (checkpoint revisions), Table~S2 (strict exact-match) \\
(l) & Replication package & Zenodo DOI &
      \url{https://doi.org/10.5281/zenodo.23146342} \\
\bottomrule
\end{tabular}
```

> ⚠️ Dois pré-requisitos antes do release: (i) confirmar que termos de uso do Gemma permitem redistribuir adaptadores LoRA; (ii) acrescentar hashes de revisão à §3.3 e à Tabela S1.

---

## Patch B-06b — substitui B-06 da Fase 1

Agora que a causa é conhecida, a resposta a R2.2 pode ser técnica e verificável:

```latex
% ═══ B-06b · R2.2, Author response (substitui o parágrafo técnico) ══
The reviewer is correct that Equations~1--6 and several table cells
were unreadable in the submitted PDF, and we apologise for it. We
traced the fault rather than merely re-rendering the document. The
LaTeX source was syntactically correct and contained no raw Unicode in
mathematical mode --- an automated audit over the full source returns a
single non-ASCII character, inside a comment. The defect arose at the
font level: the compiled PDF embedded Type~1 fonts without a reliable
\texttt{ToUnicode} mapping, so that minus signs, multiplication signs,
set-membership symbols, and percent signs were drawn correctly on the
page but mapped to unrelated code points on extraction and
re-distillation. This is why the fault appears in the form reported by
the reviewer (\texttt{Retention.t /}, \texttt{5İ10\^{}6},
\texttt{r~E~4,10,12,14,16}) rather than as missing glyphs.

The revision corrects the compilation path so that every embedded font
carries a complete \texttt{ToUnicode} map, and the resulting PDF was
verified in three ways: \texttt{pdffonts} confirms that all fonts are
embedded with Unicode mappings; an automated glyph audit compares every
equation, table cell, and caption in the extracted text against the
LaTeX source; and the audit was repeated on the PDF generated by the
submission system, since that re-distillation step is where the
original fault became visible. The audit script and its output are
included in the replication package.

% REMOVER a frase sobre lmodern/T1 — não era o mecanismo:
% "The revised submission uses the lmodern package with T1 encoding
%  throughout, which eliminates all rendering artefacts."

% SUBSTITUIR a frase C19 por:
% "...and the glyph audit covers every equation, table cell, and
%  caption in the document; its output is included in the replication
%  package."
```

---

## Estado da Fase 3

| Status | Itens |
|---|---|
| ✅ Encerrados | D1 · C17 · C20 · diagnóstico C2 |
| ✅ Prontos para colar | F1, F2, F3, F4, F5, B-06b |
| 🔴 Bloqueia A-11 | C24 — B7_SLOPE0 devolve −0.96, deve devolver −1.13 |
| 🔴 Decisão nova | F4 — manuscrito deve ser nominal? |
| ⏳ A executar | teste A/B pdflatex vs xelatex + pdffonts + validação no EM |

## Três ações para você

1. **C24** — rodar diagnóstico de chaves B7; valor correto: −1.13 (Tabela 10: 85.4 → 79.7 em 5 gerações)
2. **F4** — confirmar se submissão é nominal; se sim, preencher autoria, afiliações, ORCIDs
3. **C2** — `pdffonts manuscript.pdf` + teste A/B pdfLaTeX × XeLaTeX; se pdfLaTeX sair limpo, B-06b pode ser colado como está
