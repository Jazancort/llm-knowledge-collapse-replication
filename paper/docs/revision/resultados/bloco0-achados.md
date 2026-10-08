# Bloco 0 — Achados (verificações antes de editar o .tex)

**Data:** 2026-09-30
**Propósito:** Confirmar fatos técnicos antes de editar o manuscrito e redigir respostas aos revisores.

---

## B0.1 — Estrutura do repositório

O código de treinamento/geração/avaliação principal está na **Athena** (não localmente).
Os scripts locais em `scripts/` são análise, auditoria e patches de LaTeX.

Estrutura local confirmada:
- `scripts/core/common.py` — funções centrais de avaliação e geração
- `scripts/experiments/run_window.py` — pipeline principal (importa de core)
- `outputs/` — dados de experimentos (locais = análise, treino foi na Athena)

---

## B0.2 — Arquitetura dos modelos (A8 / D1) ✅ CONFIRMADO (2× verificado na Athena)

**Resultado: o `.tex` estava CORRETO. O arquivo de dados consolidados estava ERRADO.**

Verificação 1 e 2 independentes na Athena produziram resultados idênticos:

### Gemma 4 E2B IT (`google/gemma-4-E2B-it`)

| Campo | Valor confirmado | .tex diz | Status |
|---|---|---|---|
| hidden_size (text_config) | **1536** | 1536 | ✅ |
| num_hidden_layers | **35** | 35 | ✅ |
| num_attention_heads | **8** | 8 | ✅ |
| num_key_value_heads | **1** | 1 | ✅ |
| num_kv_shared_layers | **20** | não mencionado | ⚠️ novo dado |
| head_dim | 256 | não mencionado | — |
| intermediate_size | 6144 | não mencionado | — |

O valor "d=2048/28 camadas" do arquivo de dados consolidados é do **Gemma 2 2B**, não do E2B.

### Gemma 3 1B IT (`google/gemma-3-1b-it`)

| Campo | Valor confirmado | .tex diz | Status |
|---|---|---|---|
| hidden_size | **1152** | 1152 | ✅ |
| num_hidden_layers | **26** | 26 | ✅ |
| num_attention_heads | **4** | 4 | ✅ |
| num_key_value_heads | **1** | 1 | ✅ |

O arquivo de dados consolidados dizia "8 heads" para o Gemma 3 — isso estava **errado**.

**Ação:** Remover os comentários [v4] A8 do `.tex` — os valores já estão corretos.

### KV sharing no E2B — achado novo importante (2× verificado)

Layers **0–14** têm `v_proj` separado (15 módulos).
Layers **15–34** NÃO têm `v_proj` — essas 20 camadas compartilham KV (`num_kv_shared_layers=20`).

**Impacto no LoRA com `target_modules=["q_proj","v_proj"]`:**
- `q_proj` adapters: **35** (todas as camadas)
- `v_proj` adapters: **15** (apenas layers 0–14)
- **Total: 50 módulos adaptados, não 70**

Isso afeta o **erank agregado** reportado na Tab. 11. Verificar se o artigo reporta 50 ou 70 módulos e corrigir se necessário. O erank por matriz individual não muda — só o agregado.

---

## B0.3 — Decodificação (A3 / D5) ✅ CONFIRMADO

**`scripts/core/common.py`, linha 183:**

```python
def evaluate_k0(model, tokenizer, questions, answers, cfg, batch_size=None):
    """Greedy, max_new_tokens=20, inference_mode, ..."""
    # ...
    out = model.generate(**enc, max_new_tokens=20, do_sample=False, ...)
```

```python
def generate_synthetic(model, tokenizer, questions, cfg, seed_offset=0):
    # ...
    out = model.generate(**inputs, max_new_tokens=30, temperature=0.7,
                         do_sample=True, top_p=0.9, ...)
```

**Conclusão:**
- Avaliação K0: **greedy** (do_sample=False, max_new_tokens=20)
- Geração sintética: **stochastic** (temp=0.7, top_p=0.9, max_new_tokens=30)
- As duas coexistem — o manuscrito só havia omitido a parte de avaliação (A3 já corrigido)
- D5 resolvido: não há contradição

---

## B0.4 — Definição de drift (A6) ✅ CONFIRMADO

**`outputs/fft_lr_sweep/fft_lr1e-06.json`** tem campo `abs_drift`:
```json
{"gen": 1, "retention": 73, "abs_drift": 0.392, "rel_drift": 0.000240, ...}
```

Valor para LR=1e-6, Gen3: `abs_drift ≈ 0.396` → bate com o 0.39 da tabela do artigo.

**Conclusão:** É **mean absolute parameter change** (não L2). O `.tex` está correto.

Nota: `rel_drift` também existe nos dados (drift relativo ao tamanho do modelo).
O artigo usa `abs_drift`. A definição da Eq. 3 está correta.

---

## B0.5 — Módulos treináveis do E2B (KV sharing)

**Não verificável localmente** — código de treino está na Athena.

Verificar via SSH antes de submeter (ver comando em B0.2).

---

## B0.6 — Mapa de hardware (A2) ✅ CONFIRMADO na Athena

**Athena — GPUs físicas:**
- GPU 0: **NVIDIA RTX 5000 Ada Generation, 32 GB** (compartilhada com inferência)
- GPU 1: **NVIDIA RTX 4000 Ada Generation, 20 GB** (uso primário para treino)

O `run_window.py` usa `--gpu N` para selecionar via `CUDA_VISIBLE_DEVICES`.
O artigo menciona "RTX 4000 Ada 20 GB" = GPU 1 da Athena. ✅

**Local — RTX 3070 (8GB):** Para pilots e experimentos de verificação rápida.

**Já corrigido no `.tex`** com o comentário [v4] A2 na §3.3.

---

## B0.7 — r=256 Gen5 e C1 com N=3 ✅ CALCULADO

**Descoberta importante:** Os `g1_rank256` runs têm **K0=79**, não K0=78.

| Seed | Ret Gen5 | K0 | % |
|------|----------|-----|-----|
| 15   | 66       | 79  | 83.5% |
| 137  | 67       | 79  | 84.8% |
| 256  | 64       | 79  | 81.0% |

**Média: 83.1%, range: 81.0–84.8%**

O artigo cita **83.3% para C1 (65/78)** — o C1 da tabela de intervenções usa **K0=78**.
Os g1_rank256 runs usam **K0=79** (um item a mais no baseline).

**Implicação para A10 (C1 com N=3):**
- Esses 3 runs não são diretamente intercambiáveis com o C1 da Tab. de intervenções
- Porém, os valores (81–85%) são consistentes com C1=83.3%, confirmando que o
  baseline single-seed não é um outlier
- Para usar como C1 N=3 oficial, é necessário ou:
  (a) confirmar que K0=79 vs K0=78 é apenas um item a mais e reportar como tal, ou
  (b) rodar C1 com K0=78 pelo pipeline de intervenção (controle recomendado no plano)

**Ação:** Rodar C1 com N=2–3 pelo pipeline de intervenção (0% remoção) — confirma
que o pipeline não introduz viés e que K0=78.

---

## Resumo: o que o Bloco 0 resolveu

| Alerta | Status | Conclusão |
|--------|--------|-----------|
| A3 (decodificação) | ✅ 2× verificado | Greedy para avaliação (do_sample=False, max_new_tokens=20), stochastic para síntese (temp=0.7). Coexistem. |
| A6 (drift) | ✅ 2× verificado | abs_drift = mean absolute. .tex estava correto. |
| A8/D1 (arquitetura E2B) | ✅ 2× verificado | .tex CORRETO: 1536/35/8heads. Dados consolidados estavam errados (era Gemma 2 2B). |
| A8/D1 (arquitetura Gemma 3) | ✅ 2× verificado | .tex CORRETO: 1152/26/4heads. Dados consolidados diziam "8 heads" — errado. |
| KV sharing E2B | ✅ 2× verificado | 20 camadas sem v_proj. LoRA adapta 50 módulos (35q + 15v), não 70. Verificar Tab. 11. |
| D5 (decodificação contradição) | ✅ | Não há contradição — são etapas diferentes do pipeline. |
| A2 (hardware) | ✅ confirmado na Athena | GPU 0=RTX 5000 Ada 32GB, GPU 1=RTX 4000 Ada 20GB. .tex corrigido. |
| B0.7 (C1 N=3) | ✅ calculado | K0=79 (não 78). Valores 81–85% confirmam que C1=83.3% não é outlier. |

## Ações derivadas do Bloco 0

1. **Remover comentários [v4] A8** do `.tex` — os valores estão corretos
2. **Adicionar nota sobre KV sharing** no §3.3 ou Tab. 11 do E2B (50 módulos, não 70)
3. **Adicionar hardware Athena** ao §3.3 com GPU 0/GPU 1 explicitados (já parcialmente feito em A2)
4. **Rodar C1 com N=2–3** pelo pipeline de intervenção para confirmar equivalência com K0=78
