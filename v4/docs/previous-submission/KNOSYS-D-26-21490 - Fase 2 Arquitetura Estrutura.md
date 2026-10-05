# Fase 2 — Arquitetura, Estrutura e Formato da Carta
## KNOSYS-D-26-21490 | 2026-10-05

> **Status:** blocos prontos para colar. Pendências: ED-2 (Fase 3), R1.1–R1.5 (Fase 4), R2.2–R2.5 (Fase 5). Decisões D5/D7/D3/D6 aplicadas e sinalizadas como reversíveis.

---

## 1. Diagnóstico de arquitetura

A carta atual tem 11 itens. Os insumos exigem 40:

| Fonte | Pontos | Hoje na carta |
|---|---|---|
| Editor — "Revise (including language editing)" | 1 | 1 ✅ |
| Editor — requisitos de submissão (7 docs Word, tabelas editáveis, 300 dpi, .bib, .FIG) | 1 checklist | 0 ❌ |
| Revisor #1 — parágrafo de avaliação geral | 1 | 0 ❌ |
| Revisor #1 — perguntas 1–5 | 5 | 5 ✅ |
| Revisor #2 — parágrafo de avaliação geral | 1 | 0 ❌ |
| Revisor #2 — bloco 1 (notação, 10 bullets) | 10 | 1 agrupado |
| Revisor #2 — bloco 2 (equações/tabelas, 4 bullets) | 4 | 1 agrupado |
| Revisor #2 — bloco 3 (inconsistências, 7 bullets) | 7 | 1 agrupado |
| Revisor #2 — bloco 4 (metodologia, 6 bullets) | 6 | 1 agrupado |
| Revisor #2 — bloco 5 (formato/citações, 5 bullets) | 5 | 1 agrupado |
| **Total** | **40** | **11** |

**D5 — decisão aplicada: divisão híbrida**

| Bloco R2 | Natureza | Formato |
|---|---|---|
| R2.1 notação (10 bullets) | mecânico | tabela de correções, uma linha por bullet, texto novo citado literalmente |
| R2.2 equações (4 bullets) | mecânico + técnico | prosa curta + equações exibidas |
| R2.3 inconsistências (7 bullets) | substantivo | sub-itens (a)–(g), resposta própria para cada |
| R2.4 metodologia (6 bullets) | substantivo | sub-itens (a)–(f), prosa completa |
| R2.5 referências (5 bullets) | mecânico | tabela, uma linha por referência |

**8 bullets hoje sem menção nominal:** R2-1.h, R2-1.i, R2-1.j, R2-2.d (parcial), R2-4.c (sem alternativa proposta), R2-4.e (confusão com Gemma 3n e fonte arquitetural não endereçadas). Os três primeiros são os mais graves: σᵢ, BA_F/θ e notação de conjunto são exatamente os pontos que o PDF revisado ainda não corrigiu (C3).

---

## 2. Preâmbulo novo (E1, E2)

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[margin=2.3cm]{geometry}
\usepackage{lmodern}
\usepackage{microtype}
\usepackage{parskip}
\usepackage[table]{xcolor}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{enumitem}
\usepackage[numbers,sort&compress]{natbib}
\usepackage{hyperref}
\usepackage{titlesec}
\hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue, citecolor=blue}

\input{numbers}   % macros expandidas; ver C17/C24 da Fase 1

\definecolor{chgcolor}{RGB}{0,80,180}    % texto novo do manuscrito
\definecolor{rccolor}{RGB}{0,110,40}     % rótulo do revisor
\definecolor{hdrgray}{RGB}{240,240,240}  % fundo de cabeçalho de tabela

\titleformat{\section}{\large\bfseries}{}{0em}{}
\titlespacing*{\section}{0pt}{2.2em}{0.8em}

% ── Macros de estrutura ──────────────────────────────────────────────

% Item principal: comentário EMBUTIDO no título (padrão IEEE Access)
\newcommand{\rconcern}[3]{%
  \bigskip\noindent\rule{\linewidth}{0.4pt}\par\medskip
  \noindent\textcolor{rccolor}{\textbf{#1 (#2):}\itshape\ #3}\par
}

% Sub-item (R2.3.a, R2.4.b, ...)
\newcommand{\rsub}[2]{%
  \medskip\noindent\textcolor{rccolor}{\textbf{#1}\itshape\ #2}\par\smallskip
}

\newcommand{\arhead}[1]{\medskip\noindent\textbf{#1}\par\smallskip}

% Texto novo do manuscrito, citado literalmente
\newcommand{\newtext}[1]{\textcolor{chgcolor}{``#1''}}

% Localização: SEÇÃO + PÁGINA (nunca número de linha — C16)
\newcommand{\msloc}[1]{%
  \smallskip\noindent\textit{Revised manuscript: #1}\par
}

% Mapeamento de numeração original → revisada (C14/C15)
\newcommand{\renum}[2]{#1 of the original submission (now #2)}

\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
```

**Mudanças em relação ao preâmbulo atual:**

| Antes | Agora | Motivo |
|---|---|---|
| Comentário do revisor em `\rquote` separado | embutido em `\rconcern` | padrão do modelo IEEE aprovado |
| Sub-itens inexistentes | `\rsub` | E4 / D5 |
| `\textcolor{chgcolor}{...}` manual | `\newtext{}` | força aspas + cor uniformemente |
| Localização por linhas (l. 72) | seção + página | C16 — linhas não existem no PDF |
| `ulem` carregado, nunca usado | removido | — |
| `booktabs`, `longtable` ausentes | adicionados | tabelas de correção |

---

## 3. Inventário de itens — 40 pontos (E1, E3, E4)

```
SEÇÃO 0 · Cover page + quadro-resumo + glossário
  §0.1  Cabeçalho (E7)
  §0.2  Carta de apresentação (F1 — Fase 3)
  §0.3  Quadro-resumo de alterações (E5) ........ bloco pronto §4
  §0.4  Glossário de códigos internos (E6) ...... bloco pronto §5
  §0.5  Convenções de leitura ..................... bloco pronto §6

SEÇÃO 1 · Editor                                     2 itens
  ED-1  Revise (including language editing) ..... patch B-01, Fase 1
  ED-2  Submission requirements checklist ....... Fase 3 (F2)

SEÇÃO 2 · Reviewer #1                               6 itens
  R1-0  General assessment ...................... bloco pronto §7
  R1-1  Prospective calibration of ETP .......... + patch A-10
  R1-2  Separating confounds .................... + patch B-02
  R1-3  External validity ....................... reescrever (Fase 4)
  R1-4  Exposure reduction ...................... + patch B-03/B-07
  R1-5  Reproducibility package ................. + manifesto D4

SEÇÃO 3 · Reviewer #2                              33 itens
  R2-0  General assessment ...................... bloco pronto §7

  R2-1  Abbreviations and notation (10 bullets)  TABELA, bloco §8
          a ETP não definida em Fig. 1
          b MTLD não expandida
          c KL / JS / coverage em Fig. 1
          d bf16, SVD, TCE, QLoRA, LoRA
          e "Homeo." em Tab. 2
          f K0: conjunto vs. métrica           ← C3
          g T, D1_T, D1_0, ΔI, Instability, MeanLen_T
          h σ_i duplo uso + normalização       ← C3  [sem menção hoje]
          i BA_F, θ_i^(t), θ_i^(0)                   [sem menção hoje]
          j notação de conjunto garbled               [sem menção hoje]

  R2-2  Equations and tables (4 bullets)
          a Eq. 1–6 malformadas               ← C2
          b Eq. 2 sinal negativo + somatório  ← C3
          c Eq. 6 sinais e termos
          d 5×10^6 na Tab. 9 + "check elsewhere"    [parcial hoje]

  R2-3  Technical inconsistencies (7 bullets)   SUB-ITENS (a)–(g)
          a limiar Qwen 50–88 vs "até 150"
          b r=128 Bounded vs above-threshold   ← C4
          c r=256 "boundary configuration"     ← C5
          d Gemma 3 r≥16 vs r=10,12,14
          e Abstract: sementes                 ← C6
          f FFT Gemma 3 "confirms"             ← C7
          g C5 15% vs ~5%                      ← C25

  R2-4  Methodology (6 bullets)                 SUB-ITENS (a)–(f)
          a sem testes formais / IC / p
          b ETP não quantificada
          c normalização falhou, sem alternativa     [sem alternativa hoje]
          d ETP não é medida nova
          e Gemma 4 E2B: citação + confusão 3n + fonte arquitetural
          f "sharp transition" vs grade esparsa

  R2-5  Format and citations (5 bullets)        TABELA, bloco §9
          a [12] e [33] mesmo arXiv
          b [32] ano impossível
          c Gemma 4 E2B sem citação
          d [7] Keisha: preprint sem venue
          e formatação inconsistente
```

---

## 4. Bloco pronto — Quadro-resumo de alterações (E5)

```latex
\section*{Summary of changes}

\noindent
Forty review points were raised (five by Reviewer~1, thirty-two by
Reviewer~2, three by the Editor). Each is answered individually below.
The table maps every point to the revision made and its location in the
revised manuscript. Points marked \textsc{part} are addressed in part,
with the residual limitation stated explicitly in Section~6.

\renewcommand{\arraystretch}{1.15}
\begin{longtable}{@{}L{1.5cm}L{5.2cm}L{5.4cm}L{3.2cm}@{}}
\toprule
\rowcolor{hdrgray}\textbf{Point} & \textbf{Issue raised} &
\textbf{Revision made} & \textbf{Location} \\
\midrule
\endfirsthead
\rowcolor{hdrgray}\textbf{Point} & \textbf{Issue raised} &
\textbf{Revision made} & \textbf{Location} \\
\midrule
\endhead
\bottomrule
\endfoot

\multicolumn{4}{@{}l}{\textbf{Editor}}\\
ED-1 & Language editing & Full language revision; terminology
       standardised & Throughout \\
ED-2 & Submission format & All seven documents in Word; figures at
       300\,dpi (non-PDF); \texttt{.bib} included & Submission package \\
\addlinespace

\multicolumn{4}{@{}l}{\textbf{Reviewer 1}}\\
R1-0 & Not a transferable predictor; single dataset; single-seed
       analyses; one exposure condition & Framework reframed as
       operational; scope and seed policy stated per claim &
       §3.5, §3.8, §6 \\
R1-1 & Prospective calibration \textsc{part} & Five-step calibration
       protocol specified; held-out validation declared not performed &
       §3.5, §6 \\
R1-2 & Confound separation & Dedicated controls G3 (precision),
       G4 (data order); fresh optimizer per generation; design/observed
       split & §3.9, Tab.~3, §4.6 \\
R1-3 & External validity \textsc{part} & Strict exact-match
       re-scoring (Tab.~S2); scope restriction stated &
       §3.2, §6, Tab.~S2 \\
R1-4 & Exposure: Qwen vs.\ Gemma~3 & Pipeline inconsistency corrected;
       two pre-registered dose--response experiments (B7, G2) replace
       the pilot & §3.7, §4.5 \\
R1-5 & Reproducibility & Checkpoint revisions, prompts, seeds, masks,
       item-level vectors, raw generations, adapters deposited &
       §3.3, App.~A \\
\addlinespace

\multicolumn{4}{@{}l}{\textbf{Reviewer 2}}\\
R2-0 & Framework conceptual; Gemma~4 uncited; limited scale &
       Contribution restated as factorial design and dose--response
       evidence; Gemma~4 cited and disambiguated; scale stated as
       limitation & §1, §3.3, §6 \\
R2-1 & Abbreviations and notation (10 items) & All acronyms expanded at
       first use; notation table rebuilt; set/cardinality and singular
       value notation corrected & Tab.~1, §3.2--3.6 \\
R2-2 & Malformed equations (4 items) & Glyph fault diagnosed and fixed;
       Eq.~1--6 rewritten; automated glyph audit over the compiled PDF &
       Eq.~1--6, Tab.~9 \\
R2-3 & Internal inconsistencies (7 items) & Each corrected individually;
       threshold language unified; seed claims aligned with the seed
       policy & Abstract, §4, §5 \\
R2-4 & Methodology (6 items) & Inferential statistics added;
       backbone-local calibration proposed; ``sharp'' removed;
       Gemma~4 sourced & §3.5, §4, §6 \\
R2-5 & References (5 items) & Duplicate arXiv ID resolved; year
       corrected; Gemma~4 added; preprint status declared; list
       harmonised & \texttt{cas-refs.bib} \\
\end{longtable}
```

---

## 5. Bloco pronto — Glossário de códigos internos (E6)

**D7 — decisão aplicada:** manter "G2", resolver por glossário. Renomear exigiria editar manuscrito, scripts, numbers.tex, CSV e pré-registro com risco de inconsistência a 15 dias do prazo.

```latex
\section*{Experiment identifiers used in this response}

\noindent
The following internal identifiers appear in the revised manuscript and
in this response. They are listed here for convenience; Table~3 of the
revised manuscript maps the control experiments to the sources of
variation they address.

\renewcommand{\arraystretch}{1.15}
\begin{tabular}{@{}L{1.4cm}L{5.0cm}L{2.0cm}L{1.5cm}L{3.4cm}@{}}
\toprule
\rowcolor{hdrgray}\textbf{ID} & \textbf{Experiment} &
\textbf{Backbone} & \textbf{Seeds} & \textbf{Role} \\
\midrule
G1 & QLoRA rank sweep, NF4 & Qwen 2.5 1.5B & 3 at $r{=}256$ &
     Primary dose--response \\
G2 & Pre-registered exposure dose--response, $r{=}10$ &
     Gemma 3 1B IT & 3 per dose & Cross-backbone replication \\
G2b & Steps-matched control for G2 & Gemma 3 1B IT & 3 &
     Mechanism probe (inconclusive) \\
G3 & Precision control: bf16, no base-weight quantization &
     Qwen 2.5 1.5B & 3 at $r{=}16$, 3 at $r{=}256$ &
     Rules out quantization artefact \\
G4 & Data-order control: three new shuffle seeds &
     Qwen 2.5 1.5B & 3 at $r{=}256$ & Rules out ordering artefact \\
G5 & Pre-registered prospective rank$\times$LR probe &
     Qwen 2.5 1.5B & 1 per cell & Exploratory ordering test \\
B7 & Pre-registered exposure dose--response, $r{=}256$ &
     Qwen 2.5 1.5B & 5 per dose & Primary exposure evidence \\
C1--C5 & Exploratory intervention pilot (archived) &
     Qwen 2.5 1.5B & 1 & Superseded by B7; not used in any estimate \\
\bottomrule
\end{tabular}
```

---

## 6. Bloco pronto — Convenções de leitura (E1, C14–C16)

```latex
\section*{Conventions used in this response}

\begin{itemize}[leftmargin=1.2em,itemsep=0.35em]
\item Reviewer comments are reproduced \textcolor{rccolor}{\itshape in
      green italics} and are quoted verbatim, including the table and
      section numbers of the \emph{original} submission.
\item Text newly added to the manuscript is quoted
      \newtext{in blue, between quotation marks}, so that every claim in
      this response can be located by text search in the revised
      manuscript.
\item Locations are given as \emph{section and page of the revised
      manuscript}. Where the revision renumbered a table or section, both
      numbers are given at first mention, e.g.
      \renum{Table~7}{Table~9, p.~27}.
\item All numerical values quoted here are generated from the archived
      results by \texttt{scripts/analysis/make\_all.py} and are
      reproduced verbatim from its output.
\end{itemize}
```

---

## 7. Blocos prontos — Respostas às avaliações gerais (E3)

```latex
% ═══ E3-R1 · Reviewer #1, General assessment ═══════════════════════
\rconcern{Reviewer \#1, General assessment}{Scope of the evidence}{%
This paper studies recursive fine-tuning on synthetic data across
Qwen 2.5 1.5B, Gemma 3 1B, and Gemma 4 E2B for ten generations. [...]
The systematic design, multi-seed headline experiments, and
distributional diagnostics are valuable. However, the proposed pressure
is not yet a transferable quantitative predictor, the main metric uses
one short-answer dataset, several analyses are single-seed, and the
exposure intervention is shown mainly for one Qwen condition. Major
revision is required.}

\arhead{Author response:}
We accept all four reservations and have restructured the paper so that
each is stated as a property of the evidence rather than left for the
reader to infer.

First, effective training pressure is no longer presented as a
predictor. It is introduced as an operational experimental framework
that organises three independently manipulated variables, and the
operational index $\Pi$ is labelled an exploratory post-training summary
wherever it appears. Second, the single-dataset limitation is retained
as a limitation, but we have added a strict exact-match re-scoring of
all saved predictions to show that the regime classifications do not
depend on the permissive matching criterion. Third, the seed policy is
now explicit at the level of individual claims: headline conditions use
three to five seeds, intermediate ablations use one seed and are
labelled descriptive, and the two classes are never pooled. Fourth, the
exposure axis is no longer shown for one Qwen condition: the revision
replaces the single-seed pilot with two pre-registered dose--response
experiments, one per backbone, each with multiple paired seeds at every
dose level.

The one reservation we cannot remove is the first. Prospective
calibration on an unseen backbone was not performed, and we now say so
in those words.

\msloc{§3.5 (framework), p.~8; §3.8 (seed policy), p.~9;
§3.7 and §4.5 (dose--response), pp.~9 and 16--17; §6, pp.~21--22;
supplementary Table~S2.}

% ═══ E3-R2 · Reviewer #2, General assessment ═══════════════════════
\rconcern{Reviewer \#2, General assessment}{Status of the framework and
of the cross-architecture claims}{%
The paper addresses a timely and practically relevant question and
provides a useful empirical dose-response characterization. However, the
current manuscript has major issues in notation, equations, table/figure
formatting, internal consistency, statistical rigor, and citation
accuracy. The ``effective training pressure'' framework is promising but
currently conceptual rather than quantitative. The cross-architecture
claims are weakened by the uncited Gemma 4 E2B model and limited scale.
I recommend major revision before further consideration.}

\arhead{Author response:}
We agree with the characterisation and have treated the two substantive
objections as corrections rather than as matters of emphasis.

On the status of the framework: the reviewer is right that effective
training pressure, as submitted, was a conceptual label for three
already-known axes and not a quantitative measure. We do not defend the
original framing. The revised manuscript states that no scalar predictor
is derived, separates the variables fixed before training from the
diagnostics measured after it, and restates the contribution as the
factorial design, the dose--response evidence along three axes, the two
pre-registered exposure experiments, and the finding that the regime
boundary is backbone-dependent and not reconcilable by any architectural
normalisation we tested.

On the cross-architecture claims: Gemma~4~E2B~IT is now cited, explicitly
distinguished from Gemma~3n~E2B, and its architectural description is
attributed to the released model configuration. Because that backbone was
evaluated with a single seed, it is labelled supportive validation and is
excluded from every threshold estimate. The scale restriction to 1--2\,B
parameter models is retained as the first limitation in Section~6.

The remaining objections --- notation, equations, internal consistency,
statistical reporting, and citations --- are answered individually below,
with the corrected text quoted so that each correction can be verified
directly.

\msloc{§1 (contributions), p.~3; §3.3 (Gemma~4), p.~6;
§3.5 (framework), p.~8; §6, pp.~21--22.}
```

> **Nota de tom (T1/T3):** a frase "We do not defend the original framing" é deliberada — desarma a objeção mais difícil do Revisor #2. O modelo IEEE faz isso ("We acknowledge that the original manuscript lacked...") e funciona melhor do que defesa.

---

## 8. Bloco pronto — R2-1 em tabela (E2, E4)

```latex
\rconcern{Reviewer \#2, Concern \#1}{Abbreviations and notation}{%
ETP appears in Figure~1 (``ETP threshold identification'') but is never
explicitly defined as ``effective training pressure.'' MTLD is
introduced as ``a length-robust diversity estimate'' but the acronym is
not expanded. KL, JS, and coverage appear in Figure~1 without
definition. bf16, SVD, TCE, QLoRA, and LoRA are used without
consistently expanded forms. ``Homeo.'' is used in Table~2 without
definition. $K_0$ is used both as a set of questions and as a retention
metric. $T$, $D1_T$, $D10$, $\Delta I$, Instability(1), $MeanLen_T$,
and related symbols in Eq.~6 are not fully defined. The effective-rank
formula uses $\sigma_i$ as both singular values and normalized singular
values; the normalization condition is mathematically incorrect as
written. $BA_F$, $\theta_i^{(t)}$, $\theta_i^{(0)}$, and related
notation in the drift equation are not consistently defined.
``r E 4,10,12,14,16'' and ``r~E~10,12,14'' are garbled; they should be
clear set notation.}

\arhead{Author response:}
All ten points are accepted and corrected. Two of them --- the dual use
of $K_0$ and the normalisation condition in the effective-rank formula
--- were genuine defects rather than presentation issues, and we address
them in the notation the reviewer proposed.

\renewcommand{\arraystretch}{1.2}
\begin{longtable}{@{}L{0.5cm}L{3.3cm}L{7.2cm}L{3.0cm}@{}}
\toprule
\rowcolor{hdrgray} & \textbf{Point raised} & \textbf{Correction} &
\textbf{Location} \\
\midrule
\endfirsthead
\bottomrule
\endfoot

(a) & ETP undefined in Fig.~1 &
Figure~1 redrawn; the panel now reads
\newtext{Pressure--regime mapping and threshold localisation}. The
acronym is not used anywhere in the manuscript; the term is written in
full at every occurrence. & Fig.~1, p.~8 \\

(b) & MTLD not expanded &
\newtext{Measure of Textual Lexical Diversity (MTLD)} at first use. &
§3.6, p.~9 \\

(c) & KL, JS, coverage undefined &
Labels for diagnostics never computed or reported. Removed from
Figure~1; replaced by the quantities actually measured:
\newtext{Distribution shift --- Distinct-$n$, MTLD, stopword ratio}. &
Fig.~1, p.~8 \\

(d) & bf16, SVD, TCE, QLoRA, LoRA &
All expanded at first use: \newtext{bfloat16 (bf16)},
\newtext{singular value decomposition (SVD)},
\newtext{Truncated Cross-Entropy (TCE)},
\newtext{Quantized Low-Rank Adaptation (QLoRA)},
\newtext{Low-Rank Adaptation (LoRA)}. &
§2.3--2.4, p.~4; §3.3, p.~6 \\

(e) & ``Homeo.'' undefined &
Expanded to \newtext{Homeostatic}; ``Degrad.'' likewise to
\newtext{Degradative}. Appeared in regime labels of
\renum{Table~2}{Table~4, p.~26} and in Figure~5 legend. &
Tab.~4, p.~26; Fig.~5, p.~13 \\

(f) & $K_0$: set vs.\ metric &
$\mathcal{K}_0$ is now the set; $|\mathcal{K}_0|$ its cardinality;
$R(t)$ the retention ratio. Notation $n_0$ withdrawn.
Equation~1 rewritten accordingly. &
Tab.~1, p.~25; Eq.~1, §3.2, p.~5 \\

(g) & Eq.~6 symbols &
$T$, $D1_t$, $\mathrm{MeanLen}_t$, $\mathrm{Instability}(t)$, and
$\Delta I$ defined in Table~1 and restated inline before Equation~6;
convention $0\log 0 = 0$ stated explicitly. &
Tab.~1, p.~25; §3.6, p.~9 \\

(h) & $\sigma_i$ dual use; normalisation incorrect &
Mathematical error accepted. Normalised weights now:
\newtext{$p_i = \sigma_i/\sum_j \sigma_j$, with $p_i \ge 0$ and
$\sum_i p_i = 1$}; Equation~2 reads
$\mathrm{erank}(BA) = \exp(-\sum_i p_i \log p_i)$. &
Tab.~1, p.~25; Eq.~2, §3.5.1, p.~8 \\

(i) & $BA_F$, $\theta_i^{(t)}$, $\theta_i^{(0)}$ &
Defined in Table~1: $\|\Delta W\|_F$ is the Frobenius norm averaged
across adapted modules; $\theta^{(0)}$ pretrained weights;
$\theta^{(t)}$ weights after generation $t$,
\newtext{adapter-augmented under QLoRA; fully updated under FFT}.
Ambiguity in the original table resolved. Equation~3 now shows the
absolute value and summation explicitly. &
Tab.~1, p.~25; Eq.~3, §3.5.2, p.~8 \\

(j) & Garbled set notation &
All occurrences: $r \in \{4, 10, 12, 14, 16\}$ and
$r \in \{10, 12, 14\}$. Garbling was part of the glyph fault addressed
in Concern~\#2. & §3.4, p.~7; §4.2.1, p.~12 \\
\end{longtable}

\arhead{Author action:}
\begin{enumerate}[leftmargin=1.4em,itemsep=0.3em]
\item Table~1 (p.~25) rebuilt: every symbol defined in order of first
      appearance, with protocol-specific values of $|\mathcal{K}_0|$
      listed per backbone.
\item Figure~1 (p.~8) redrawn, removing the undefined acronym and the
      three uncomputed diagnostics; exposure panel corrected to doses
      actually used \newtext{0 / 10 / 25 / 50\% removal}.
\item Equations~1, 2, and 3 rewritten in the corrected notation and
      cross-checked against Table~1, term by term.
\item Acronym audit run over the full source: each of the twelve
      abbreviations used in the paper is expanded at first use and used
      consistently thereafter.
\end{enumerate}
```

---

## 9. Padrão E2 — Author action com citação literal

| Formato | Exemplo |
|---|---|
| ❌ Atual | "We removed 'ETP' from Figure 1, expanded MTLD and all acronyms…" |
| ✅ Modelo | "Figure 1 (p. 8) was redrawn. The panel now reads `\newtext{Pressure–regime mapping}`. The acronym is not used anywhere in the manuscript." |

**Regra para todos os 40 itens:**

```
Author action:
  1. [Verbo no passado] + [elemento] + (§X, p. Y).
     Texto novo: \newtext{citação literal, verificável por busca}
  2. ...
```

Mínimo de uma citação literal por item. Itens sem texto novo (ex.: "arquivamos o piloto") devem separar o que mudou no texto e o que mudou fora dele.

---

## 10. E7 — Cabeçalho corrigido

```latex
\noindent
Ms.\ Ref.\ No.: \textbf{KNOSYS-D-26-21490}\\[2pt]
Title: \textit{Effective Training Pressure Gates Recursive Knowledge
Degradation in LLMs: A Multi-Axis Dose-Response Study}\\[2pt]
Journal: \textit{Knowledge-Based Systems} (Elsevier)\\[2pt]
To: Dr.\ Hang Yu, Senior Editor\\[2pt]
Re: Response to Reviewers --- Revision Round~1\\[2pt]
Date: 19 October 2026
```

| Correção | Antes | Agora |
|---|---|---|
| Nomenclatura | "Manuscript ID" | "Ms. Ref. No." — termo do Editorial Manager |
| Destinatário | "Knowledge-Based Systems Editor" | Dr. Hang Yu, Senior Editor |
| Data | `\today` | data fixa de submissão |
| Journal | implícito | linha própria |

**E todo o corpo:** remover chaves .bib (`ding2024ranktrade`, `fawi2024curlora`, `zibakhsh2024`, `gemma4_2026`, `keisha2025`) e usar autor + ano + número da referência no manuscrito.

---

## 11. E8 / D3 — Conversão para Word

**D3 — decisão aplicada:** manter LaTeX como fonte única e converter.

```bash
# 1. Expandir macros de numbers.tex (pandoc não resolve \input)
latexpand --expand-usepackage response.tex > response-flat.tex

# 2. Converter
pandoc response-flat.tex \
  --from=latex \
  --to=docx \
  --bibliography=cas-refs.bib \
  --citeproc \
  --csl=elsevier-with-titles.csl \
  --reference-doc=reference.docx \
  --output=Response-to-Reviewers.docx

# 3. Verificar após conversão
#   [ ] cores preservadas (verde = revisor, azul = texto novo)
#   [ ] equações como objetos editáveis, não imagens
#   [ ] longtable não quebrada entre páginas
#   [ ] \newtext{} manteve aspas E cor
#   [ ] nenhuma macro não expandida (buscar "\")
```

**Atenção:** equações — pandoc converte `$...$` em OMML (editável). Se alguma sair como imagem, substituir manualmente. Citações — se preferir evitar `--citeproc`, substituir `\citet{}` por `[n] Autor et al.` antes da conversão.

---

## 12. Estado da Fase 2

| Status | Itens |
|---|---|
| ✅ Prontos para colar | preâmbulo novo · quadro-resumo (E5) · glossário (E6) · convenções (E1/C14-16) · respostas gerais R1-0 e R2-0 (E3) · tabela R2-1 completa (E2/E4) · cabeçalho (E7) · pipeline Word (E8) |
| 📋 Padrão definido | inventário dos 40 itens · estrutura híbrida tabela/prosa · regra Author action com citação literal |
| ⏳ A desenvolver | ED-2 (checklist do editor) → Fase 3 · R1-1 a R1-5 → Fase 4 · R2-2 a R2-5 → Fase 5 |

**Decisões aplicadas, reversíveis:**
- **D5** → divisão híbrida (tabela para mecânico, sub-itens para substantivo)
- **D7** → manter "G2", resolver por glossário
- **D3** → LaTeX como fonte + pandoc (confirmar se `pandoc` e `latexpand` estão disponíveis)
- **D6** → regressão logística de efeitos mistos **não entra**: não existe no manuscrito
