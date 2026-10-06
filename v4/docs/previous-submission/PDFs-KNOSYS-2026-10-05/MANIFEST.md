# KNOSYS-D-26-21490 — Pacote de Submissão Revisão 1

**Data do pacote:** 2026-10-06  
**Journal:** Knowledge-Based Systems (Elsevier)  
**Submission ID:** KNOSYS-D-26-21490  
**HEAD commit:** 306f2d6 (branch master)  
**Checks mecânicos:** 12/12 PASS  

---

## Instruções de upload (ED-2)

> "The revised cover letter, response to reviewers, highlights, revised manuscript…  
> should all be in **word format**. Source file alone can be in word or Latex file."

Submeter no Editorial Manager nesta ordem:

| # | Ficheiro | Tipo EM | Formato | Notas |
|---|----------|---------|---------|-------|
| 1 | `manuscript-anonymous.docx` | Manuscript | Word | **Artefacto principal** — 611 equações OMML, 0 glifos |
| 2 | `response-to-reviewers.docx` | Response to Reviewers | Word | 370 equações OMML; 2 glifos intencionais em verbatim |
| 3 | `highlights-revised.docx` | Highlights | Word | Versão CORRECTA (highlights.docx original tem erros) |
| 4 | `supplementary.pdf` | Supplementary | PDF | Tabela S1 + hash SHA-1 dos modelos |
| 5 | `title-page.docx` | Title Page | Word | Com nomes dos autores e afiliações |
| 6 | `credit-author-statement.docx` | Author Statement | Word | CRediT taxonomy |
| 7 | `declaration-of-competing-interests.docx` | Declaration | Word | |

**PDFs de referência** (não enviar separadamente):
- `manuscript-anonymous.pdf` — PDF LaTeX compilado (source file per ED-2)
- `response-to-reviewers.pdf` — PDF da carta (para arquivo)

---

## Conteúdo do pacote

### Artefactos da REVISÃO (novos — enviar)

| Ficheiro | Tamanho | Compilado/Criado | Finalidade |
|----------|---------|------------------|------------|
| `manuscript-anonymous.docx` | 1,616 KB | 2026-10-06 00:52 | Submissão principal (Word) |
| `manuscript-anonymous.pdf` | 2,104 KB | 2026-10-06 01:06 | PDF LaTeX (source file) |
| `response-to-reviewers.docx` | 454 KB | 2026-10-06 01:01 | Carta resposta (Word) |
| `response-to-reviewers.pdf` | 993 KB | 2026-10-06 00:55 | Carta resposta (PDF ref.) |
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

### Manuscrito .docx
- Glifos corrompidos no XML: **0**
- Equações OMML nativas: **611**
- Palavras abstract: **237** (limite KBS: 250)

### Carta .docx
- Glifos corrompidos reais: **0**
- Glifos intencionais (exemplos em verbatim): 2 (Ë, ù)
- Equações OMML: **370**

### Checks mecânicos (12/12 PASS)
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
```

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
| Abstract: clarificação §4.2.3 "tenfold" | Aguarda o utilizador |
| Confirmar destinatário (Dr. Hang Yu vs Dr. Jie Lu) | Verificar no EM |

---

*Gerado por: Kiro CLI, 2026-10-06*
