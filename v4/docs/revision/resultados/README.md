# Resultados — Revisão KNOSYS-D-26-21490

Pasta centralizada com todos os resultados, análises e logs dos experimentos
da revisão final do artigo "Effective Training Pressure Gates Recursive
Knowledge Degradation in LLMs".

**Experimentos concluídos:** 02–03/10/2026 | **23/23 runs, 0 FAILs**

---

## Arquivos de análise

| Arquivo | Conteúdo |
|---|---|
| `resultados-revisao-final.md` | **Análise principal** — G1–G5 completos com estatísticas, tabelas e sumário para o .tex |
| `resultados-bloco7.md` | Dose-response Qwen (Bloco 7, pré-registrado a916ebf) — base para §4.5 |
| `verificacoes.md` | V1–V10 — verificações dos parâmetros canônicos do pipeline |
| `bloco0-achados.md` | Bloco 0 — auditoria inicial dos dados brutos |
| `resultados_consolidados.csv` | CSV com TODAS as gerações de TODOS os runs (1285 linhas, 64 diretórios) |

---

## Experimentos

| Grupo | Condição | N runs | Resultado |
|---|---|---|---|
| **G1** | Qwen r=256 dose=0%, seeds 15/137/256 | 3 | Gen5=85.5±0.7%, Gen10=79.1±1.5% |
| **G2** | Gemma3 r=10 doses 0/10/25/50%, seeds 15/137/256 | 12 | dose=50% → +12.9pp Gen10 (p=0.023) |
| **G3** | Qwen bf16 sem NF4, r=16+r=256, seeds 15/137/256 | 6 | NF4≈bf16 (delta=0pp) |
| **G4** | Qwen r=256 seeds 42/101/202 (variância ordem) | 3 | p=0.67 n.s. — ordem não afeta |
| **G5** | Pi prospectivo r=128/r=32, 3 células | 3 | Predição direcional confirmada (1/3) |

---

## Logs

Pasta `logs/` — um arquivo por job, nomeado pelo experimento.
`master.log` — linha do tempo completa de todos os jobs com timestamps e exit codes.

## Scripts

Pasta `scripts/` — scripts de lançamento usados na Athena.

---

## Pipeline

- Athena: `julioazancort@172.20.39.50`, GPU 1 (RTX 4000 Ada 20GB)
- Script: `g1_rank_ablation.py`, commit `c3ba205`
- Pré-registro: `3b1712b` (02/10/2026T09:35 UTC-3)
