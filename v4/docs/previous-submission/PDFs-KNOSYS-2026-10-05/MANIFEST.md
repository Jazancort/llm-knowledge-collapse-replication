# KNOSYS-D-26-21490 — Pacote de Submissão Revisão 1

**Data do pacote:** 2026-10-06  
**Journal:** Knowledge-Based Systems (Elsevier)  
**Submission ID:** KNOSYS-D-26-21490  
**HEAD commit:** 4157fdc (branch master)  
**Checks mecânicos:** 14/14 PASS  

---

## Instruções de upload (ED-2)

> "The revised cover letter, response to reviewers, highlights, revised manuscript…  
> should all be in **word format**. Source file alone can be in word or Latex file."

Submeter no Editorial Manager nesta ordem:

| # | Ficheiro | Tipo EM | Formato | Notas |
|---|----------|---------|---------|-------|
| 1 | `manuscript-anonymous.docx` | Manuscript | Word | **Artefacto principal** — equações OMML, 0 glifos |
| 2 | `response-to-reviewers.docx` | Response to Reviewers | Word | equações OMML; 2 glifos intencionais em verbatim |
| 3 | `highlights-revised.docx` | Highlights | Word | Versão CORRECTA |
| 4 | `supplementary.pdf` | Supplementary | PDF | Tabela S1 + hash SHA-1 dos modelos |
| 5 | `title-page.docx` | Title Page | Word | Com nomes dos autores e afiliações |
| 6 | `credit-author-statement.docx` | Author Statement | Word | CRediT taxonomy |
| 7 | `declaration-of-competing-interests.docx` | Declaration | Word | |

**PDFs de referência** (não enviar separadamente — source files):
- `manuscript-anonymous.pdf` — PDF LaTeX compilado (source file per ED-2)
- `response-to-reviewers.pdf` — PDF da carta (para arquivo)

---

## Conteúdo do pacote

### Artefactos da REVISÃO (novos — enviar)

| Ficheiro | Tamanho | Compilado/Criado | Finalidade |
|----------|---------|------------------|------------|
| `manuscript-anonymous.docx` | 1,617 KB | 2026-10-06 02:04 | Submissão principal (Word) |
| `manuscript-anonymous.pdf` | 2,106 KB | 2026-10-06 02:01 | PDF LaTeX (source file) |
| `response-to-reviewers.docx` | 455 KB | 2026-10-06 02:04 | Carta resposta (Word) |
| `response-to-reviewers.pdf` | 995 KB | 2026-10-06 01:48 | Carta resposta (PDF ref.) |
| `supplementary.pdf` | 44 KB | 2026-10-06 01:06 | Material suplementar |
| `highlights-revised.docx` | 11 KB | 2026-10-04 | Highlights (versão correcta) |
| `title-page.docx` | 11 KB | 2026-09-09 | Página de título |
| `credit-author-statement.docx` | 11 KB | 2026-09-09 | CRediT |
| `declaration-of-competing-interests.docx` | 11 KB | 2026-09-09 | Declaração interesses |

### Artefactos da SUBMISSÃO ORIGINAL (arquivo — não enviar)

| Ficheiro | Tamanho | Data | Nota |
|----------|---------|------|------|
| `KNOSYS-D-26-21490_manuscript.pdf` | 1,994 KB | 2026-10-05 | PDF antes das correcções — arquivo |
| `KNOSYS-D-26-21490_response-to-reviewers.pdf` | 890 KB | 2026-10-05 | Carta antes das correcções — arquivo |
| `KNOSYS-D-26-21490_supplementary.pdf` | 183 KB | 2026-10-05 | Suplementar antes das correcções — arquivo |

---

## Verificação de integridade

### SHA-256 (primeiros 16 hex) dos 4 artefactos principais

| Ficheiro | SHA-256 (prefixo) |
|----------|------------------|
| `manuscript-anonymous.docx` | `fd8f448dc9fc33eb...` |
| `manuscript-anonymous.pdf` | `0bcff97f1df07269...` |
| `response-to-reviewers.docx` | `e5ddee65863d49a9...` |
| `response-to-reviewers.pdf` | `cb3804fcf011d0c7...` |

### Checks mecânicos (14/14 PASS — commit 4157fdc)

```
check_01 PASS  no bare K₀ = <digit> without bars
check_02 PASS  canonical retention % match integer counts to 1 dp
check_03 PASS  Tab.1 body identical in manuscript and carta
check_04 PASS  known [verbatim] passages exist in manuscript or figure source
check_05 PASS  key section labels exist in manuscript
check_06 PASS  erank() always has argument ΔW
check_07 PASS  N per condition consistent (r=256 N=6, r=16 N=3)
check_08 PASS  Tab.10 delta Gen10 documented
check_09 PASS  refs [15] and [45] have correct authors in BBL
check_10 PASS  zero British spellings in manuscript
check_11 PASS  Appendix A run counts present (27 G1-G5, 20 B7, 5 pilot = 52)
check_12 PASS  scripts/analysis/glyph_audit.py exists
check_13 PASS  CI/p internal consistency for all B7+G2 pairs (|p_calc-p_rep|≤0.01)
check_14 PASS  integer reachability: reported means and slopes derive from integer counts
```

---

## Correcções aplicadas nesta revisão (vs. MANIFEST anterior 306f2d6)

Cinco erros da classe arredondamento-em-cascata identificados e corrigidos por varredura automática (check_14) do paper completo (68 grandezas):

| # | Erro | Localização | Commit |
|---|------|------------|--------|
| 1 | B7 p dose 10%: 0.200 → **0.160** | manuscrito + carta | e5c0659 + 2b59960 |
| 2 | B7 p dose 25%: 0.001 → **0.0044** | manuscrito + carta | e5c0659 + 2b59960 |
| 3 | B7 slope 50%: −0.14 → **−0.15** | manuscrito + carta (macro) | 2b59960 |
| 4 | Table 6 carta Gemma 3 r=4: 94.4 → **94.3** | carta L1371 | 95e8e06 |
| 5 | Persistência r=128: 5.2 → **5.1** | manuscrito §4.4.2 + §5.3 | 4157fdc |

---

## Principais alterações desta revisão

### Respostas ao Editor
- ED-1: Revisão linguística completa (American English)
- ED-2: Manuscrito e carta em formato Word (.docx); equações OMML
- ED-3: Tabela de 40 pontos de alteração

### Respostas ao Reviewer 1
- R1-4: Comparação Qwen vs Gemma 3 substituída por B7 (Qwen) e G2 (Gemma 3) com paired t-tests
- R1-5: Pacote de reprodutibilidade no Zenodo + GitHub

### Respostas ao Reviewer 2
- R2-2: Equações 1, 2, 6 corrigidas matematicamente; defeito de glifos resolvido via .docx
- R2-3: Fig.2(c) corrigida (1959, Ronnie Carroll); legenda Fig.10 corrigida
- R2-5: Referências [15] e [45] corrigidas; peterson2024 adicionado

---

## Itens pendentes (não bloqueiam submissão)

| Item | Estado |
|------|--------|
| Zenodo v1.0.4 com scripts de análise | Recomendado mas não bloqueador |
| Confirmar destinatário (Dr. Hang Yu vs Dr. Jie Lu) | Verificar no EM |

---

*Gerado por: Kiro CLI, 2026-10-06 02:05*
