# Plano Bloco 7 — Dose-Resposta de Exposição
# KNOSYS-D-26-21490 | v4 revision

**Início:** 2026-09-30T20:40 UTC-3
**Pré-registro:** `a916ebf` (Intervention Window, antes de qualquer run)
**Script:** `scripts/revision/run_bloco7_sequential.sh` (commit `c64d863`)
**Patch g1_rank_ablation.py:** commit `5805579` (--steps, --dose, proveniência)

---

## Contexto: por que este bloco existe

O Bloco 6 revelou que a Contribuição 5 ("+9 pp de C3/C5") vinha de uma
comparação entre pipelines diferentes, não de uma comparação C1 × C5 controlada.
Comparação pareada no mesmo pipeline (3 seeds): C5 − C1 = **+1.9 pp** (CI [-0.1, +3.9]).

A Contribuição 5 como escrita não se sustenta.
Este bloco testa se existe um efeito real de exposição, com design correto.

---

## O que já existe (reutilizado via resume)

| Condição | Seeds | Diretórios |
|---|---|---|
| dose=0% (C1) | 15, 137, 256 | `g1_rank256_seed{s}` |
| dose=5% (C5) | 15, 137, 256 | `g1_rank256_seed{s}_c5d05` |

---

## Experimentos do Bloco 7

### 7a — Dose-response (primário)
- **Doses:** 0%, 5%, 10%, 25%, 50%
- **Seeds:** 15, 137, 256, 42, 77
- **Novos runs:** 19 (doses 0/5% seeds 42/77 = 4; doses 10/25/50% × 5 seeds = 15)
- **Output naming:** `g1_rank256_seed{s}_dose{frac}` (tag `_dose{frac}`)
- **Métrica principal:** Gen5 retention %
- **Análise:** GLMM logístico por item + diferenças pareadas por seed

### 7b — Controle de passos igualados
- **dose=25%** com `--steps 250` (igual ao dose=0%)
- **Objetivo:** separar "menos dados" de "menos passos de gradiente"
- **Seeds:** 15, 137, 256
- **Output:** `g1_rank256_seed{s}_dose25_matched`

### 7c — Teste da previsão LR-equivalência
- **dose=50%** vs **dose=0%, lr=5e-6**
- **Previsão pré-registrada:** dose=50% → Gen5 ≈ 89–92%
- **Falsificação:** < 86% ou > 95%
- **Seeds:** 15, 137, 256
- dose=50% já roda no 7a; lr=5e-6 seeds 137/256 são novos

---

## Cronograma estimado

| Slot | Experimentos | Duração est. |
|---|---|---|
| 7a doses 0/5 (resume) | ~2s cada (pula) | ~1 min |
| 7a doses 10/25/50 × 5 seeds | 15 runs × ~30 min | ~7.5h |
| 7a doses 0/5 seeds 42/77 | 4 runs × ~30 min | ~2h |
| 7c lr=5e-6 seeds 137/256 | 2 runs × ~30 min | ~1h |
| 7b matched × 3 seeds | 3 runs × ~30 min | ~1.5h |
| **Total** | | **~12h** |

**Término estimado:** 2026-10-01 ~09:00 UTC-3

---

## Análise (após conclusão)

### Primária: GLMM logístico por item
```python
# statsmodels MixedLM
import statsmodels.formula.api as smf
import numpy as np

# montar df com colunas: item, seed, dose, correct
df["log_keep"] = np.log(1 - df["dose"])  # 0 para dose=0
model = smf.mixedlm("correct ~ log_keep", df, groups=df["seed"],
                    re_formula="~1")
result = model.fit()
# Teste unilateral: slope positivo com p < 0.05
```

### Secundária: diferenças pareadas por seed
- Para cada seed: Δ(dose) = ret(dose) − ret(dose=0%), Gen5
- IC 95% por bootstrap (1000 resamples, estratificado por seed)

### Teste da previsão 7c
- `dose=50%` vs previsão [89%, 92%]
- Comparar com `lr=5e-6, dose=0%` (Bloco 5 seed 15: 96.2%)

### Teste 7b (confound)
- Se `dose=25%_matched ≈ dose=0%`: efeito é de passos, não de dados
- Se `dose=25%_matched ≈ dose=25%`: efeito é composição dos dados

---

## Interpretação dos resultados possíveis

| Resultado 7a | Resultado 7c | Resultado 7b | Conclusão |
|---|---|---|---|
| Monotônico + p<0.05 | Dentro [86,95%] | Matched ≈ dose=25% | Exposição = 3º eixo de pressão via composição. Melhor cenário. |
| Monotônico + p<0.05 | Dentro [86,95%] | Matched ≈ dose=0% | Exposição age via passos, não composição. Equivalência com LR confirma. |
| Efeito pequeno (+2-4pp) | Parcialmente | — | Efeito modesto, não robusto. Relatar como exploratório. |
| Nenhum efeito | Fora | — | Exposição não é eixo independente. Retirar das afirmações principais. |

---

## O que muda no .tex (qualquer que seja o resultado)

**Obrigatório (todos os cenários):**
- §4.5: adicionar parágrafo sobre Bloco 6 (C1 × C5 pareados) e diferença +1.9 pp
- Carta ao revisor: explicar que C1 e C5 originais vieram de pipelines diferentes
- Contribuição 5: reformular para não afirmar +9 pp

**Condicional ao resultado 7a:**
- Se monotônico + significativo: §4.5 expandido, eixo de exposição mantido em §5
- Se não: §4.5 contém o resultado negativo/nulo, §5.1 retira "third axis" do abstract

**Imutável (continua de pé):**
- Dose-resposta de rank (3 backbones)
- Varredura LR no FFT
- Combinação rank × LR
- Dissociação em r=128
- FFT vs QLoRA (mesmo pipeline)

---

## Comandos de monitoramento

```bash
# Progresso atual:
ssh -i C:\Users\julio\.ssh\id_ed25519_mcp julioazancort@172.20.39.50 \
  "tmux capture-pane -p -t bloco7 | tail -15"

# Log de DONE/FAIL:
ssh -i C:\Users\julio\.ssh\id_ed25519_mcp julioazancort@172.20.39.50 \
  "grep -E 'DONE|FAIL|START|CONCLUIDO' ~/scratch/llm-knowledge-collapse/outputs/bloco7_logs/master.log"

# Resultado parcial (Gen5 de tudo que já terminou):
ssh -i C:\Users\julio\.ssh\id_ed25519_mcp julioazancort@172.20.39.50 "python3 -c \"
import json, pathlib
for d in sorted(pathlib.Path('outputs').glob('g1_rank256_seed*')):
    p = d / 'results.json'
    if not p.exists(): continue
    data = json.loads(p.read_text())
    K0 = data[0]['k0_size']
    g5 = next((g['retention']/K0*100 for g in data if g.get('gen')==5), None)
    dose = next((g.get('dose_frac',0) for g in data if g.get('gen')==1), 0)
    if g5: print(f'{d.name:<45} dose={dose:.0%} Gen5={g5:.1f}%')
\""
```
