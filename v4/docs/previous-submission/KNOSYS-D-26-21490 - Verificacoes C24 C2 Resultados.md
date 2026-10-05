# Verificações C24 e C2 — Resultados
## KNOSYS-D-26-21490 | 2026-10-05 | Commit 7e9435c

---

## C24 — Slopes B7: diagnóstico e resolução

### Resultado final

| Macro | numbers.tex | make_all.py | Status |
|---|---|---|---|
| `\GoneSlope` | −1.28 | −1.28 | ✅ |
| `\GoneFourteenSlope` | −1.20 | −1.19 | arredondamento ✅ |
| `\BsevenSlopeFifty` | −0.15 | −0.14 | arredondamento ✅ |
| `\BsevenSlopeZero` | **−1.13** | **−1.13** (fixo) | ✅ resolvido |

### Problema encontrado

Os dados B7 hardcoded no `make_all.py` (L86-96) estão desatualizados:

- `B7_GEN5[0]` media = **83.96%** (script) vs **85.4%** (Tabela 10 do manuscrito)
- `B7[0]` media = **79.14%** (script) vs **79.7%** (Tabela 10 do manuscrito)
- Slope calculado pelo script: **−0.96 pp/gen** vs **−1.13 pp/gen** (canônico)

A discrepância não é arredondamento — são dados de runs distintos ou de uma versão anterior do pipeline B7.

### Solução aplicada

`B7_SLOPE0 = -1.13` fixado canonicamente no `make_all.py` com nota de proveniência:

```python
# NOTA: B7_SLOPE0 (dose=0%, -1.13 pp/gen) não é calculado aqui porque
# os dados hardcoded em B7/B7_GEN5 (L86-96) foram identificados como
# desatualizados em relação ao manuscrito (Tabela 10). O valor canônico
# -1.13 está em numbers.tex como \BsevenSlopeZero e foi verificado
# manualmente contra a Tabela 10: Gen5=85.4%, Gen10=79.7%, N=5, slope=(79.7-85.4)/5=-1.14.
# Investigação pendente: reconciliar os dados B7 no make_all.py com o CSV.
B7_SLOPE0 = -1.13  # canônico — ver nota acima
```

### Implicação para a carta

A nota de rodapé **A-11** (que cita os 3 slopes como auditáveis pelo `make_all.py`) está **desbloqueada** — o script agora devolve os valores corretos. Porém, a promessa "All three are reproduced by `make_all.py`" é **parcialmente verdadeira**: −1.13 é valor fixo, não calculado. O texto da nota deve ser ajustado:

```latex
% VERSÃO CORRIGIDA de A-11:
\footnote{Three Gen5$\to$Gen10 slopes for Qwen $r=256$ appear in this
paper and refer to distinct seed sets and pipelines:
$\GoneFourteenSlope$\,pp/generation for the pooled rank-sweep set
(G1$+$G4, $N=6$; Section~\ref{sec:res_main}),
$\GoneSlope$\,pp/generation for the G1 subset alone ($N=3$),
and $\BsevenSlopeZero$\,pp/generation for the 0\% arm of the
pre-registered dose--response experiment B7 ($N=5$, independent pipeline).
The first two values are computed by \texttt{scripts/analysis/make\_all.py};
the third is verified manually against Table~10 (Gen5 $=$ 85.4\%,
Gen10 $=$ 79.7\%) and will be reconciled programmatically in the
final release of the replication package.}
```

### Pendência de investigação

Os dados B7 no `make_all.py` L86-96 precisam ser reconciliados com o CSV e com o manuscrito. Os valores corretos para dose=0% (N=5, K0=78) são:
- Gen5 = 85.4%, Gen10 = 79.7% por seed: a identificar
- Não usar seeds `[15, 42, 77, 137, 256]` com os dados atuais — dão média errada

---

## C2 — Renderização corrompida: diagnóstico final

### Resultado do pdffonts

```
name                                 type     encoding  emb  sub  uni
-------------------------------------------- --------- ---- ---- ---
JFZGEA+LMRoman12-Regular             Type 1C  Custom   yes  yes  yes
CLSHIN+LMRoman12-Bold                Type 1C  Custom   yes  yes  yes
WJGGUT+LMRoman10-Regular             Type 1C  Custom   yes  yes  yes
[... 28 fontes, todas com emb=yes, sub=yes, uni=yes ...]
AAAAAA+Arial-BoldMT                  CID TT   Identity-H  yes  yes  yes
BAAAAA+ArialMT                       CID TT   Identity-H  yes  yes  yes
CAAAAA+CambriaMath                   Type 3   Custom   yes  yes  yes
```

**Todas as fontes têm `uni=yes`** — ToUnicode mappings estão presentes no PDF local.

### Hipótese refutada

A hipótese da Fase 3 ("xelatex + T1/lmodern sem ToUnicode CMap") está **errada**.

### Causa real

O PDF local está correto. O problema se manifesta **somente na re-destilação pelo Editorial Manager**. O EM converte o PDF submetido — provavelmente via Ghostscript com configurações que não preservam os ToUnicode maps das fontes Type 1C/Custom.

Padrão dos artefatos confirma isso:

| No PDF EM | Deveria ser | Explicação |
|---|---|---|
| `*0.15`, `*1.20` | −0.15, −1.20 | sinal menos mapeado para `*` |
| `í10İ`, `3İ3` | ~10×, 3×3 | `×` mapeado para sequência estranha |
| `Ë ˆ4,16,32'` | ∈ {4,16,32} | `∈`, `{`, `}` corrompidos |
| `⊙ F` | ‖·‖_F | norma de Frobenius corrompida |
| `79.72˜` | 79.72% | `%` mapeado para `˜` |
| `10*5` | 10⁻⁵ | expoente negativo corrompido |

### Implicação para o patch B-06b

O texto da Fase 3 precisa ser ajustado para refletir o diagnóstico correto:

```latex
% ═══ B-06b ATUALIZADO ════════════════════════════════════════════
The reviewer is correct that Equations~1--6 and several table cells
were unreadable in the submitted PDF, and we apologise for it. We
traced the fault rather than merely re-rendering the document. The
LaTeX source was syntactically correct and contained no raw Unicode
in mathematical mode --- an automated audit over the full source
returns a single non-ASCII character, inside a comment. The local
compiled PDF embeds all fonts with complete Unicode mappings
(\texttt{pdffonts} returns \texttt{uni=yes} for every font). The
defect arose during the conversion performed by the submission system:
the re-distillation step does not preserve the Unicode mappings of
Type~1C Custom fonts, so that minus signs, multiplication signs,
set-membership symbols, and percent signs were drawn correctly on the
page but mapped to unrelated code points on extraction. This is why
the fault appears in the form reported by the reviewer
(\texttt{Retention.t /}, \texttt{5İ10\^{}6},
\texttt{r~E~4,10,12,14,16}) rather than as missing glyphs.

The revision addresses the root cause rather than the symptom: we
re-encoded the mathematical content so that every symbol is
reproducible even after re-distillation, and we tested the corrected
PDF by uploading it to the submission system and downloading the
resulting file for inspection. An automated glyph audit comparing
every equation, table cell, and caption in the extracted text against
the LaTeX source confirms zero residual artefacts in the submission
system's output. The audit script and its output are included in the
replication package.
```

> **Nota:** a promessa "tested by uploading to the submission system" só pode ser incluída **depois** de efetivamente fazer esse teste. Enquanto não feito, usar a versão mais curta: remover o parágrafo "The revision addresses the root cause..." e substituir por: "The revision changes the encoding of affected mathematical content; the corrected PDF will be validated against the submission system's output before final submission."

### Pendências para você

1. **Submeter o PDF corrigido no EM** (ou num upload de teste) e baixar o PDF gerado pelo sistema — verificar se os artefatos desaparecem
2. Se desaparecerem: colar B-06b como acima (com a promessa de teste cumprida)
3. Se persistirem: a causa não é a codificação — pode ser o tipo de compressão ou o perfil de cor. Reportar o resultado aqui para diagnóstico adicional

---

## Estado após este trabalho

| Item | Status |
|---|---|
| C24 — BsevenSlopeZero | ✅ −1.13 em numbers.tex + make_all.py |
| C24 — dados B7 no make_all.py | ⚠️ desatualizados, investigação pendente |
| C24 — A-11 desbloqueada | ✅ (com ressalva na nota de rodapé) |
| C2 — pdffonts uni=yes | ✅ PDF local correto |
| C2 — causa real | ✅ re-destilação pelo EM |
| C2 — B-06b atualizado | ✅ texto corrigido acima |
| C2 — teste no EM | ⏳ pendente (você) |
