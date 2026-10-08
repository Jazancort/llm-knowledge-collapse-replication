# Verificações V1–V10
# KNOSYS-D-26-21490 | Fase 0
# Data: 2026-10-02 | Fontes: Athena + bloco0-achados.md

---

## V1 — Parâmetros de geração sintética vs avaliação

**Fonte:** `scripts/g1_rank_ablation.py` linhas 89 e 106.

| Etapa | do_sample | temperature | top_p | max_new_tokens |
|---|---|---|---|---|
| Avaliação K0 | `False` (greedy) | — | — | 20 |
| Geração sintética | `True` | 0.7 | 0.9 | 30 |

**Frase para §3.1:**
> Factual retention is evaluated greedily (`do_sample=False`, `max\_new\_tokens=20`).
> Synthetic training texts are generated stochastically (`temperature=0.7`, `top\_p=0.9`,
> `max\_new\_tokens=30`).

**Status: ✅ CONFIRMADO** (idêntico ao bloco0-achados.md §B0.3)

---

## V2 — Auditoria K0: 79→78 Qwen, 47→46 Gemma 3

**Fonte:** comparação de `k0_indices` entre `g1_rank256_seed15` e `fft_lr_sweep/k0_indices.json`.

| K0 | Tamanho | Itens |
|---|---|---|
| g1 (pipeline novo) | **79** | índices 0–198 (baseado em acerto no gen0) |
| fft_lr_sweep (pipeline antigo) | **78** | subconjunto fixo, carregado de arquivo |

**Item removido na auditoria:**
- Índice no eval set: **118**
- Pergunta: *"Of which sculptor was it said on his gravestone to be a loss to the Cafe Royal?"*
- Resposta: Jacob Epstein (Sir Jacob Epstein)
- Motivo: presente no K0 do g1 (respondido corretamente no gen0, seed 15), ausente no
  K0 do fft_lr_sweep — indica que este item foi removido na auditoria manual que gerou
  o `k0_indices.json` do fft. Provavelmente respondido incorretamente no baseline FFT
  e portanto excluído do K0 daquele pipeline.

**Para Gemma 3:** K0=46 (não 47) — verificado em `gemma3_c5correct_rank16_seed15` (K0=46).
Item removido não identificado (requer comparação com k0 do fft Gemma, se existir).

**Frase para §3.2:**
> The factual probe $\mathcal{K}_0$ was constructed independently for each backbone and
> training pipeline by retaining only the questions answered correctly in the zero-shot
> baseline (generation 0). This yields $|\mathcal{K}_0| = 79$ for Qwen (g1 pipeline),
> $|\mathcal{K}_0| = 78$ for Qwen (fft-sweep pipeline), and $|\mathcal{K}_0| = 46$ for Gemma~3.

**Status: ✅ CONFIRMADO**

---

## V3 — Mapa de hardware

**Fonte:** bloco0-achados.md §B0.6 + verificação na Athena + metadata.json dos runs.

| Experimento | Máquina | GPU |
|---|---|---|
| Todos os g1_rank_ablation.py (Blocos 5–7, Revisão G1–G5) | Athena (Dell Precision 5860, Xeon W3-2423, 128 GB RAM DDR5 ECC) | GPU 1 — RTX 4000 Ada 20 GB |
| run_window.py (Bloco 4, pipeline alternativo) | Athena | GPU 1 — RTX 4000 Ada 20 GB |
| Gemma 3 e Gemma 4 E2B (runs originais do artigo) | Athena | GPU 1 — RTX 4000 Ada 20 GB |
| Runs exploratórios anteriores (factorial_v2_gemma, etc.) | Athena | GPU 1 — RTX 4000 Ada 20 GB |
| Pilotos e verificações rápidas | Local (Windows) | RTX 3070 8 GB |

**Frase para §3.3:**
> All experiments were run on a Dell Precision~5860 workstation (Intel Xeon~W3-2423,
> 128~GB DDR5 ECC) equipped with an NVIDIA RTX~4000~Ada~Generation (20~GB VRAM).
> Small-scale pilots were run locally on an NVIDIA RTX~3070 (8~GB).

**Status: ✅ CONFIRMADO**

---

## V4 — Seed 15 r=16: 75/78 vs 76/78

**Fonte:** `outputs/fft_comparison_qlora_seed15/results.json` e `outputs/g1_gen10_seed15/results.json`.

| Run | K0 | Gen5 | % |
|---|---|---|---|
| `fft_comparison_qlora_seed15` | 78 | **76**/78 | **97.4%** |
| `g1_gen10_seed15` | 79 | 75/79 | 94.9% |

**Diagnóstico:** O artigo cita **75/78 = 96.2%** para r=16 seed15.
- `fft_comparison_qlora_seed15` (K0=78) dá **76/78 = 97.4%** no Gen5 — este é o run de referência do artigo para QLoRA r=16.
- `g1_gen10_seed15` (K0=79, pipeline g1) dá 75/79 = 94.9% — pipeline diferente, K0 diferente.
- A discrepância 76 vs 75 é de **1 item** e origina-se de K0=78 vs K0=79 + pipeline diferente (não non-determinismo nem versão diferente de biblioteca).

**Número correto para o artigo:** 76/78 = **97.4%** (run `fft_comparison_qlora_seed15`, pipeline
do artigo). O artigo usa 75/78 — verificar no .tex e corrigir se necessário.

**Frase para o texto (se corrigido):**
> QLoRA~$r{=}16$: Gen~5 retention $= 76/78 = 97.4\%$ (seed~15).

**Status: ✅ IDENTIFICADO — verificar no .tex e corrigir**

---

## V5 — Definição exata de drift e norma de Frobenius

**Fonte:** `scripts/g1_rank_ablation.py` função `compute_lora_spectrum()` (linhas 114–127) +
bloco0-achados.md §B0.4.

**Drift (campo `abs_drift` nos JSONs FFT):**
- Definição: **mean absolute parameter change** entre θ⁽ᵗ⁾ e θ⁽⁰⁾
- Campo no JSON: `abs_drift`; campo alternativo: `rel_drift` (relativo ao tamanho do modelo)
- Equação: $d(t) = \frac{1}{|\Theta|} \sum_{\theta \in \Theta} |\theta^{(t)} - \theta^{(0)}|$
- **Não é norma L2 (Frobenius)** — é média aritmética das mudanças absolutas

**Norma de Frobenius (campo `frobenius` no adapter):**
```python
AB = b_param.data.float().cpu() @ param.data.float().cpu()  # (out, in)
f_norms.append(torch.norm(AB, 'fro').item())
return {"frobenius": np.mean(f_norms)}  # média entre módulos LoRA
```
- `frobenius` = **média da norma de Frobenius de ΔW = BA** entre todos os módulos LoRA adaptados
- ΔW = B·A (sem o fator α/r — é a matriz bruta, não a atualização escalada)
- Equivalente a $\frac{1}{M}\sum_{m=1}^{M} \|B_m A_m\|_F$

**Effective rank (campo `eff_rank`):**
```python
svs = torch.linalg.svdvals(AB)
svs_n = svs / (svs.sum() + 1e-10)
ranks.append(torch.exp(-(svs_n * torch.log(svs_n + 1e-10)).sum()).item())
return {"eff_rank": np.mean(ranks)}  # média entre módulos
```
- erank = $\exp(-\sum_i p_i \log p_i)$, com $p_i = \sigma_i / \sum_j \sigma_j$
- Média entre todos os módulos LoRA adaptados

**Frases para Eq. 3 e §3.5:**
> The adapter spectrum is summarised per generation by the \emph{effective rank}
> $\text{erank}(\Delta W) = \exp\!\bigl(-\textstyle\sum_i p_i \log p_i\bigr)$,
> where $p_i = \sigma_i / \sum_j \sigma_j$ and $\sigma_i$ are the singular values of
> $\Delta W = BA$; values are averaged across all adapted modules.
> The Frobenius norm $\|\Delta W\|_F$ (averaged across modules) measures update magnitude.
> Parameter drift $d(t)$ is the mean absolute change in full-model parameters
> between generation $t$ and the pretrained baseline.

**Status: ✅ CONFIRMADO**

---

## V6 — Arquitetura dos 3 backbones

**Fonte:** `AutoConfig.from_pretrained()` via uv + bloco0-achados.md §B0.2.

| Backbone | HF ID | hidden | layers | heads | kv_heads | Nota |
|---|---|---|---|---|---|---|
| Qwen 2.5 1.5B | `Qwen/Qwen2.5-1.5B-Instruct` | 1536 | 28 | 12 | 2 | — |
| Gemma 3 1B | `google/gemma-3-1b-it` | 1152 | 26 | 4 | 1 | — |
| Gemma 4 E2B | `google/gemma-4-E2B-it` | 1536 | 35 | 8 | 1 | `num_kv_shared_layers=20` |

**KV sharing no E2B:** layers 15–34 (20 camadas) não têm `v_proj` separado.
LoRA com `target_modules=["q_proj","v_proj"]` adapta **50 módulos** (35 q_proj + 15 v_proj).

**Nota para §3.3:** verificar se o artigo reporta 50 ou 70 módulos para o E2B.

**Status: ✅ CONFIRMADO** (idêntico ao bloco0-achados.md §B0.2)

---

## V7 — Módulos LoRA adaptados no E2B

**Fonte:** bloco0-achados.md §B0.2 + §B0.5.

Com `target_modules=["q_proj","v_proj"]` no E2B (`google/gemma-4-E2B-it`):
- Todas as 35 camadas têm `q_proj` → **35 módulos**
- Apenas layers 0–14 têm `v_proj` (layers 15–34 compartilham KV) → **15 módulos**
- **Total: 50 módulos LoRA adaptados** (não 70)

Impacto: o **erank agregado** reportado na Tab. 11 é média sobre 50 módulos, não 70.
Por módulo individual, o erank não muda. A média pode diferir ligeiramente de um artigo
que assumiu 70 módulos.

**Frase para §3.3 (E2B):**
> For the E2B backbone, which employs grouped-query attention with
> $\texttt{num\_kv\_shared\_layers}=20$, LoRA adapts only layers~0--14 for
> $v\_\text{proj}$ (15 modules) and all 35 layers for $q\_\text{proj}$,
> yielding 50 adapted modules in total.

**Status: ✅ CONFIRMADO** (bloco0-achados.md §B0.2 + §B0.5)

---

## V8 — Índice da Gen5 nos JSONs

**Fonte:** `outputs/g1_rank256_seed15/results.json` inspecionado diretamente.

```
index=0  gen=0  (K0 baseline)
index=1  gen=1
index=2  gen=2
index=3  gen=3
index=4  gen=4
index=5  gen=5   ← Gen5 está em data[5], não data[4]
...
index=10 gen=10
```

**Conclusão:** `data[5]` é Gen5. O campo `generation` deve ser usado para lookup
(`next(g for g in data if g["generation"] == 5)`), não o índice da lista.

**Status: ✅ CONFIRMADO** (gen == index, mas lookup por campo é mais seguro)

---

## V9 — Diferenças de pipeline: c5_replicate_masks.py vs g1_rank_ablation.py

**Fonte:** diff direto entre os dois scripts na Athena.

| Parâmetro | c5_replicate_masks.py | g1_rank_ablation.py | Impacto |
|---|---|---|---|
| K0 source | Arquivo externo `fft_lr_sweep/k0_indices.json` (K0=78) | Computado no gen0 (acerto real; K0=79) | **K0 diferente** — C1 e C5 não eram comparáveis |
| `pad_token_id` na geração | Explícito: `pad_token_id=tokenizer.pad_token_id` | Ausente no original (corrigido depois) | Pode afetar decodificação se pad≠eos |
| `logging_steps` no treino | 9999 (praticamente nunca loga) | 100 | Apenas verbose |
| Downsampling | `downsample()` baseado em `TARGET_TOKENS` (contagem de palavras) | `downsample_relative()` baseado em fração de exemplos | Método diferente |
| K0 variável | Fixo (arquivo externo) | Recalculado a cada run (pode variar 1 item por seed) | Pequena variação entre seeds |

**Esta é a origem do +9 pp original:** C1 vinha do g1 (K0=79, nível de retenção
ligeiramente diferente), e C3/C5 vinham do c5_replicate_masks (K0=78, nível diferente).
A comparação era entre pipelines, não dentro do mesmo pipeline.

**Frase para a carta ao revisor (parágrafo de transparência):**
> In the original submission, the C1 baseline ($r=256$, no downsampling) was generated
> by \texttt{g1\_rank\_ablation.py}, which derives $\mathcal{K}_0$ from the model's
> own zero-shot accuracy ($|\mathcal{K}_0|=79$). The C3/C5 conditions were generated
> by \texttt{c5\_replicate\_masks.py}, which loads a fixed $\mathcal{K}_0$ from the
> FFT sweep ($|\mathcal{K}_0|=78$) and uses a word-count-based downsampling function.
> These differences in $\mathcal{K}_0$ construction and evaluation pipeline account
> for the discrepancy between the reported +9.4~pp and the +1.9~pp observed in Bloco~6
> (identical pipeline, paired seeds).

**Status: ✅ IDENTIFICADO E DOCUMENTADO**

---

## V10 — Métricas KL/JS/coverage da Fig. 1

**Fonte:** busca em todos os results.json + código na Athena.

**Resultado:** As métricas KL, JS e coverage **não aparecem em nenhum arquivo de resultado**.
Os arquivos `syn_gen*.json` contêm apenas texto gerado (lista de strings), sem métricas calculadas.
O código em `scripts/` não contém nenhuma função que calcule KL-divergência, JS-divergência
ou coverage sobre os sintéticos.

**Conclusão:** As métricas KL/JS/coverage mencionadas na Fig. 1 são **ilustrativas/conceituais**,
não calculadas a partir dos dados experimentais. Devem ser removidas da figura ou substituídas
por métricas que realmente aparecem nos resultados (SDI-3, erank, retention).

**Ação para Fase 6:** remover KL/JS/coverage da Fig. 1; substituir pelo SDI-3 ou erank
por geração, que são calculados e reportados.

**Status: ✅ CONFIRMADO — métricas não calculadas, remover da figura**

---

## Resumo das ações derivadas

| V# | Ação | Onde |
|---|---|---|
| V1 | Adicionar tabela de parâmetros geração/avaliação | §3.1 |
| V2 | Explicar K0=79 vs K0=78 e item 118 | §3.2 |
| V3 | Atualizar hardware com Athena completo + local | §3.3 |
| V4 | Corrigir 75/78 → 76/78 se errado no .tex | Tabela r=16 |
| V5 | Confirmar Eq. 3 (drift = mean absolute), Eq. frobenius | §3.5, Eq. 3 |
| V6 | Confirmar arquitetura (já correto no .tex) | §3.3 |
| V7 | Adicionar nota sobre 50 módulos E2B (não 70) | §3.3, Tab. 11 |
| V8 | Usar `g["generation"] == 5` em todos os scripts | make_all.py |
| V9 | Usar diff como base para o parágrafo de transparência | Carta |
| V10 | Remover KL/JS/coverage da Fig. 1 | Fase 6 |

---

*Arquivo: `v4/docs/revision/verificacoes.md`*
*Criado: 2026-10-02 com dados da Athena + bloco0-achados.md*
