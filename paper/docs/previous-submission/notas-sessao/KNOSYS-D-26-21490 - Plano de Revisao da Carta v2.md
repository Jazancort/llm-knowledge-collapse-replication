# Plano de Revisão v2 — Carta de Resposta aos Revisores
## KNOSYS-D-26-21490 | Atualizado: 2026-10-05

> **Prazo interno:** 20/10/2026
> **Commit atual:** f3c9a79 (antes das correções C24/C2 desta sessão)

---

## RESUMO EXECUTIVO

| Fase | Arquivo | Status |
|---|---|---|
| Fase 0 — Decisões D1–D7 | Plano v2 (este) | D1 ✅, D5 ✅, D6 ✅, D7 ✅; D2/D3/D4 aplicados |
| Fase 1 — 22 divergências | Dossie Fase 1 + Fechamento Patches | ✅ patches A/B prontos; C24 🔴 reaberto |
| Fase 2 — Estrutura (40 itens) | Fase 2 Arquitetura Estrutura | ✅ blocos prontos |
| Fase 3 — Capa + Editor + Highlights | Fase 3 Carta Apresentacao | ✅ F1-F5 + B-06c prontos |
| Fase 4 — Revisor #1 | Fase 4 Reviewer1 | ✅ R1-1/2/3/5; R1-4 🔴 bloqueado |
| Fase 5 — Revisor #2 (R2-2 a R2-5) | — | ⏳ a desenvolver |
| Verificações C24/C2 | Verificacoes C24 C2 Resultados | 🔴 C24 reaberto (dados B7) |

---

## FASE 0 — Decisões

| ID | Decisão | Status |
|---|---|---|
| **D1** 🔴 | English Language Editing — contratado ou variante honesta? | ✅ Variante 2 aplicada: revisão própria + oferta condicional |
| **D2** 🔴 | Para cada divergência: corrigir manuscrito (A) ou carta (B)? | ✅ Matriz aplicada (11A / 11B / 2 encerrados) |
| **D3** 🔴 | Carta em Word via pandoc ou nativa? | ✅ LaTeX fonte + pandoc (`latexpand` + `--citeproc`) |
| **D4** 🟠 | Conteúdo do novo release Zenodo? | ✅ Manifesto definido: scripts/configs/results/generations/checkpoints/prereg/audit |
| **D5** 🟠 | Dividir bullets R2 em sub-itens? | ✅ Híbrido: tabela para mecânico, sub-itens para substantivo |
| **D6** 🟡 | Regressão logística de efeitos mistos entra? | ✅ Não entra — não existe no manuscrito |
| **D7** 🟡 | Renomear "G2" para evitar colisão? | ✅ Manter "G2" + resolver por glossário (Fase 2 §5) |

---

## FASE 1 — Divergências (estado atual)

### Encerrados
- **C17:** make_all.py reportava "112 macros", na verdade são 98 (agora 100/114 com novos slopes). Patch B-05 aplicado → B-05b.
- **C20:** DOI truncado era falso positivo. `10.5281/zenodo.23146342` correto e consistente.

### Patches A (manuscrito) — prontos para colar
| ID | Patch | Bloqueia C24? |
|---|---|---|
| A-01 | Tabela 1: K₀/σᵢ/pᵢ/erank | não |
| A-02 | Equações 1, 2, 3 corrigidas | não |
| A-03 | Figura 1: 4 correções (ETP, KL/JS, exposure, axes) | não |
| A-04 | Contribuição 1: seed count corrigido | não |
| A-05 | Contribuição 2: "confirming" → "consistent with" | não |
| A-06 | r=128: "above-threshold" → "transition-zone" | não |
| A-07 | r=256: "boundary configuration" → "lowest-pressure degradative" | não |
| A-08 | "Homeo."/"Degrad." em Fig. 5, Tab. 4, Figs. 4/11 | não |
| A-09 | §3.3: hashes de revisão dos checkpoints | não |
| A-10 | §6: protocolo prospectivo de 5 passos | não |
| **A-11** | **Nota de rodapé: 3 slopes B7 auditáveis** | **🔴 SIM** |

### Patches B (carta) — prontos para colar
| ID | Patch | Status |
|---|---|---|
| B-01 | Editor: variante 2 (revisão própria) | ✅ aplicado |
| B-02 | Quantização: baseline correto + auditoria pendente | pronto |
| B-03 | G5: ordenação ≠ classificação | pronto |
| B-04 | Capa item (3): "all headline" → lista explícita | pronto |
| **B-05b** | **R1.5: promessa atenuada enquanto C24 pendente** | **usar esta** |
| B-06c | R2.2: causa = re-destilação EM (condicionado ao teste) | pronto |
| B-07 | C25: ambiguidade 15%/5% removida no manuscrito | pronto |
| B-08 | C13: Shumailov "reinforced" não "added" | pronto |
| B-09 | C21: padronizar em C1–C5 em toda a carta | pronto |
| B-10 | C14/C15/C16: convenção seção+página, tabela de conversão | pronto |

---

## 🔴 C24 — Dados B7 braço 0% (BLOQUEADOR CRÍTICO)

### Situação

Os dados hardcoded em `make_all.py` L86-96 para dose=0% divergem do manuscrito:

| | Script | Manuscrito Tabela 10 |
|---|---|---|
| Gen5 média | 83.96% | 85.4% |
| Gen10 média | 79.14% | 79.7% |
| Slope | −0.96 | −1.13 |

Consequência: os Δ contra a baseline divergem em todas as doses:

| Dose | Δ manuscrito | Δ script |
|---|---|---|
| 10% | +1.8 pp | +2.4 pp |
| 25% | +4.9 pp | +5.5 pp |
| 50% | +9.2 pp | +9.8 pp |

### O que bloqueia
- **A-11** (nota de rodapé slopes)
- **R1-4** (usa `\BsevenSlopeZero`, `\BsevenSlopeFifty`, `\GtwoDeltatenFifty`)
- Promessa de reprodutibilidade integral em R1-5 (usar B-05b)

### Diagnóstico para executar
```python
import csv, glob
base = r"...\v4"
for f in glob.glob(base + r"\**\*.csv", recursive=True):
    txt = open(f, encoding="utf-8", errors="replace").read()
    if "85.4" in txt and "79.7" in txt:
        print("CANDIDATO:", f)
for f in glob.glob(base + r"\**\*.py", recursive=True):
    txt = open(f, encoding="utf-8", errors="replace").read()
    if "85.4" in txt or "table10" in txt.lower():
        print("SCRIPT CANDIDATO:", f)
```

### Decisões possíveis
| | Decisão | Consequência |
|---|---|---|
| A | Manuscrito certo → corrigir dados em `make_all.py` | Tabela 10 e todos os Δ permanecem |
| B | Script certo → corrigir Tabela 10 | Δ Gen10 50% vira +9.8 pp; Δ Gen5 +5.0/+5.2/+5.8; slope 0% −0.96 |
| C | Nenhum rastreável → rerodar braço 0% | — |

---

## C2 — Diagnóstico final (encerrado)

- `pdffonts`: todas as 30 fontes com `uni=yes` → PDF local correto
- Causa real: **re-destilação pelo Editorial Manager** não preserva Unicode maps de fontes Type 1C Custom
- **Pendência para você:** subir PDF no EM, baixar resultado, verificar com `pdftotext + rg`
- Mitigação: LuaLaTeX + fontspec ou pré-destilação com Ghostscript

---

## FASE 2 — Estrutura (prontos)

Todos os blocos estão em `Fase 2 Arquitetura Estrutura.md`:
- Preâmbulo novo (booktabs, longtable, `\newtext{}`, `\renum{}`, `\rsub{}`)
- Inventário dos 40 itens
- Quadro-resumo E5 (longtable)
- Glossário E6 + Convenções E1
- R1-0 e R2-0 (avaliações gerais)
- Tabela R2-1 completa (10 bullets, citação literal)
- Cabeçalho E7 (Ms. Ref. No., Dr. Hang Yu, data fixa)
- Pipeline Word E8 (latexpand + pandoc)

---

## FASE 3 — Capa + Editor + Highlights (prontos)

Todos os blocos estão em `Fase 3 Carta Apresentacao Checklist.md`:
- **F1:** cover letter (nomeia contribuições decisivas dos revisores, bloco de limitações)
- **F2:** ED-2 checklist (9 requisitos do editor)
- **F3:** 5 highlights reescritos (ASCII puro, ≤85 car., sem códigos internos)
- **F4:** metadados (nominalidade 🔴 decisão pendente, paginação, ORCID)
- **F5:** lista de 12 itens submetidos
- **B-06c:** resposta R2.2 com causa correta (condicionado ao teste no EM)

---

## FASE 4 — Revisor #1 (em `Fase 4 Reviewer1.md`)

| Item | Status |
|---|---|
| R1-0 (avaliação geral) | ✅ na Fase 2 |
| R1-1 (calibração prospectiva) | ✅ pronto |
| R1-2 (confusores) | ✅ pronto |
| R1-3 (validade externa) | ✅ pronto |
| **R1-4 (exposição Qwen/Gemma)** | **🔴 bloqueado por C24** |
| R1-5 (reprodutibilidade) | ✅ pronto (usar B-05b) |

---

## FASE 5 — Revisor #2 (R2-2 a R2-5)

**⏳ A desenvolver.** R2-1 já está em Fase 2 (tabela com 10 bullets).

Estrutura prevista:
- R2-2: equações e renderização (B-06c + tabela)
- R2-3: inconsistências (a)–(g) como sub-itens
- R2-4: metodologia (a)–(f) como sub-itens
- R2-5: referências (tabela, uma linha por entrada)

---

## PENDÊNCIAS PARA VOCÊ (3 prioritárias)

| Prioridade | Ação | Desbloqueia |
|---|---|---|
| 🔴 1 | **C24:** localizar dados por semente do braço 0% do B7 (rodar diagnóstico acima) | R1-4, A-11, promessa de reprodutibilidade |
| 🔴 2 | **F4:** confirmar nominalidade do manuscrito (KBS = single-blind) | CRediT, author agreement, ORCID |
| 🟠 3 | **C2/EM:** subir PDF no EM, baixar resultado, `pdftotext + rg` | B-06c (terceiro parágrafo) |
