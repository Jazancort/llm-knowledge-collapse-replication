# Log da Fase 3 — Correções do Revisor 2
# KNOSYS-D-26-21490 | Iniciado: 2026-10-02

---

## 3.1 — Encoding e renderização (R2.1, R2.2)

**Status: ✅ JÁ ESTAVA CORRETO**

Verificado em 2026-10-02:
- `\usepackage{lmodern}` → linha 6
- `\usepackage[T1]{fontenc}` → linha 7
- Zero caracteres Unicode fora de ASCII no corpo do .tex
- Zero símbolos matemáticos fora de modo math

Estas correções foram aplicadas no Bloco 1 (sessão anterior).
Nenhuma ação adicional necessária para 3.1.

---

## 3.2 — Tabela de nomenclatura (R2.1)

**Status: ⏳ PENDENTE**

Tabela de símbolos preparada em `plano-revisao-final.md` §3.2.
Inserção no .tex depende de definir a posição exacta (apêndice vs §3).
Fazer quando escrever §3 completo (Fase 4).

---

## 3.3 — Equações 1–6 (R2.2)

**Status: ⏳ PENDENTE**

Definições verificadas (V5):
- Eq. 1 (R(t)): correto no .tex
- Eq. 2 (erank): implementação confirmada em `compute_lora_spectrum()`
- Eq. 3 (drift): mean absolute change — verificado em bloco0-achados.md §B0.4
- Eqs. 4–5 (CE, Persist): verificar no .tex se símbolos estão definidos
- Eq. 6 (SDI-3): verificar definição de D₁ e I(t)

Fazer em 03/10 junto com §3.5 (Fase 4).

---

## 3.4 — Inconsistências de texto (R2.3)

**Status: ✅ APLICADO + HIGHLIGHTS em 2026-10-02**

### Correções aplicadas ao manuscript-anonymous.tex:

| # | Linha(s) | Antes | Depois |
|---|---|---|---|
| 1 | L86 (highlights) | "sharp pressure-dependent transition" | "abrupt, pressure-dependent transition within the tested grid" |
| 2 | L90 (highlights) | "Reducing synthetic exposure by 5% restores near-homeostatic behavior on Qwen" | "A pre-registered exposure dose-response shows that reducing synthetic training volume by 50% arrests progressive degradation and matches the effect of halving the learning rate" |
| 3 | L179 (contribuições) | "identifying a sharp regime transition on Qwen" | "identifying an abrupt, threshold-like transition within the tested grid on Qwen" |
| 4 | L1404 (subseção §4.4) | "FFT on Gemma~3 confirms cross-backbone magnitude effect" | "FFT on Gemma~3 is consistent with a cross-backbone magnitude effect" |
| 5 | Tab. 8 (§4.5) | Tabela C1–C5 com +9.0/+9.4 pp | Tabela dose-resposta 0/10/25/50% com dados do Bloco 7 |
| 6 | §4.5 inteiro | Texto C1–C5 original-pipeline | Texto dose-resposta pré-registrada + nota de transparência |
| 7 | Tab. 9 | "Exposure governs transition / C3/C5 N=3" | "Exposure reduces pressure / dose-response 0–50% N=5 (pre-registered)" |
| 8 | Tab. 9 | "Transition is sharp / 5% flips regime" | "Transition is abrupt within tested grid / dose-response plateau Gen5; graded Gen10" |
| 9 | §5 discussão | "transition is sharp: ~5% reduction… sufficient" | "transition is abrupt within tested grid: 50% arrests loss at Gen10" |
| 10 | 5× "boundary configuration" | "boundary configuration" | "lowest-pressure degradative configuration tested" |
| 11 | Abstract item (5) | "5% reduction restores near-homeostatic" | "50% reduction arrests progressive degradation and matches halving LR" |
| 12 | Contribuição #5 | "5% restores near-homeostatic at Qwen boundary" | "pre-registered dose-response: 10–50% raises Gen5 by ~5pp; 50% matches lr/2" |

### Verificação pós-patch (grep):
- "sharp regime/pressure" → 0 ocorrências ✅
- "5% restores homeostasis" → 0 ocorrências ✅
- "+9.4 pp" → 1 ocorrência legítima (L1610: menção histórica) ✅
- "boundary configuration" → 0 ocorrências ✅
- "Exposure governs" → 0 ocorrências ✅
- "Transition is sharp" → 0 ocorrências ✅
- Unicode fora de ASCII → 0 ✅

### Mecanismo de highlight para revisores

Adicionado ao preâmbulo (linhas 6–13):
```latex
\usepackage[dvipsnames]{xcolor}
\newif\ifshowchanges
\showchangestrue   % ← trocar para \showchangesfalse para versão limpa
\newcommand{\rev}[1]{\ifshowchanges{\color{blue}#1}\else{#1}\fi}
```

- **16 ocorrências** de `\rev{}` marcando todos os trechos alterados em azul
- Versão marcada para revisores: `\showchangestrue` (padrão)
- Versão limpa para submissão final: `\showchangesfalse`

### Pendentes (dependem de números finais da GPU):
- Verificar e corrigir 75/78 → 76/78 para r=16 seed15 (V4) — aguardar confirmação no .tex
- Dois limiares θ_H e θ_D com critério numérico — aguardar análise A4
- Coluna "N seeds" em todas as tabelas — junto com regeneração (Fase 4)
- "Homeo." por extenso — junto com regeneração das tabelas (Fase 4)
- "~5%" → valor exato de tokens — aguardar análise A1

---

## 3.4 residual — siglas, Homeo., N seeds (R2.1 / R2.3)

**Status: ✅ APLICADO em 2026-10-02**

### Verificações realizadas

| Item | Encontrado | Ação |
|---|---|---|
| θ_H / θ_D numéricos | ✅ Já definidos em L1547–1551: `r=64 ≤ θ_H < r=128` e `r=128 ≤ θ_D < r=256` | Sem correção |
| "Homeo." abreviado | ❌ 4 ocorrências na tab:rank_sweep | Expandido para "Homeostatic" com `\rev{}` |
| Coluna N seeds | ❌ Ausente na maioria das tabelas | Adicionada coluna `\rev{$N$}` nas tabs rank_sweep e gemma3; notas de rodapé nas tabs gemma4, fft_sweep e ranklr |
| ETP como sigla | Não aparece como acrônimo — texto usa "effective training pressure" por extenso | Sem correção (decisão editorial correta) |
| EM como sigla | Não aparece como `\bEM\b` isolado — sempre "exact-match" | Sem correção |
| CKA | Não aparece no .tex | Sem correção |
| QLoRA (def explícita) | L150 keywords (ok). Corpo sem definição antes de L333 | Adicionado "Quantized Low-Rank Adaptation (QLoRA)" em L333 com `\rev{}` |
| FFT (acrônimo) | Definido no abstract como "full fine-tuning" sem `(FFT)` | Adicionado "(FFT)" em L75 com `\rev{}` |
| SVD | L332: "SVD-based" sem definição | Adicionado "singular value decomposition (SVD)" com `\rev{}` |
| MTLD | L875: sigla antes de expansão | Expandido para "Measure of Textual Lexical Diversity (MTLD)" com `\rev{}` |

### Total \rev{} após esta rodada: 45 blocos

---

## 3.2 Tabela de nomenclatura (R2.1)

**Status: ✅ APLICADO em 2026-10-02**

### O que foi feito

Inserida tabela `tab:notation` com 18 símbolos no .tex, posicionada entre o parágrafo
de defaults ("Throughout this section...") e `\subsection{Recursive replace-only protocol}`.

O bloco inteiro está envolvido em `\rev{}` (highlight azul para revisores).

### Decisão de notação

O plano usava $\mathcal{K}_0$ mas o .tex usa $K_0$ em 33 ocorrências. Mantido $K_0$
para consistência — a tabela esclarece a semântica do conjunto.

### Símbolos incluídos

$K_0$, $R(t)$, $\theta^{(0)}$, $\theta^{(t)}$, $\Delta W = BA$, $\sigma_i$,
$\hat{\sigma}_i$, $\mathrm{erank}(\Delta W)$, $\|\Delta W\|_F$, $d(t)$, $\eta$, $\Pi$,
$f$, $\theta_H$, $\theta_D$, $T$, $\mathrm{ContentEff}(t)$, $\mathrm{Persist}(t)$,
$\mathrm{SDI\text{-}3}$.

---

## 3.3 Equações 1–6 (R2.2)

**Status: ✅ APLICADO em 2026-10-02**

### O que foi feito

As 6 equações já existiam no .tex com labels corretos. Aplicadas 3 correções de
consistência (todas com `\rev{}`):

| Equação | Label | Correção |
|---|---|---|
| Eq. 1 (Retenção) | `eq:k0` | `\mathrm{Retention}(t)` → `\rev{R(t)}` — harmonizado com tabela |
| Eq. 2 (Erank) | `eq:erank` | Sem alteração — já correta |
| Eq. 3 (Drift) | `eq:drift` | `\mathrm{drift}(t)` → `\rev{d(t)}` — harmonizado com tabela |
| Eq. 4 (ContentEff) | `eq:efficiency` | `\mathrm{Retention}(t)` no numerador → `\rev{R(t)}` |
| Eq. 5 (Persist) | `eq:persistence` | Sem alteração — já correta |
| Eq. 6 (SDI-3) | `eq:sdi` | Sem alteração — já correta |

### Verificação pós-patch

- `\mathrm{Retention}`: 0 ocorrências ✅
- `\mathrm{drift}`: 0 ocorrências ✅
- `tab:notation`: 2 ocorrências (definição + referência) ✅
- 6 equações com labels distintos ✅
- Total `\rev{}`: 21 blocos no .tex ✅

**Status: ✅ APLICADO em 2026-10-02**

### Auditoria Scholar Sidekick (9/9 entradas — 9 matched, 0 mismatch, 0 retracted)

| Chave | arXiv | Veredito | Ação |
|---|---|---|---|
| `keisha2025` | 2509.04796 | matched ✅ | Sem correção — preprint, nota "Non-peer-reviewed" já presente |
| `dohmatob2025` | 2410.04840 | matched (year gap: arXiv=2024, ICLR=2025) | Year 2025 correto para versão publicada |
| `guo2024collapse` | 2410.16713 | matched ✅ | OK — Kazdan et al., NeurIPS 2024 Workshops |
| `dohmatob2024scaling` | 2402.07043 | matched ✅ | OK — ICML 2024 |
| `feng2025verification` | 2406.07515 | matched ✅ | OK — Feng et al. 2024 |
| `bertrand2024stability` | 2310.00429 | matched (year gap: arXiv=2023, ICLR=2024) | Year 2024 correto para versão publicada |
| `gemma4_2026` | 2607.02770 | matched ✅ | OK — Gemma Team 2026 |
| `yi2025` | 2510.16657 | matched ✅ | **CORRIGIDO**: autores "Yi, Bingji and others" → lista completa (Yi, Liu, Cheng, Xu) |
| `ding2024ranktrade` | 2512.15634 | matched ✅ | OK — Rathore et al., AACL-IJCNLP 2025 |

### Correção aplicada

`yi2025`: `author = {Yi, Bingji and others}` → `author = {Yi, Bingji and Liu, Qiyuan and Cheng, Yuwei and Xu, Haifeng}`

---

## GPU — andamento G1→G2 (atualizado 2026-10-02T09:43)

Sessão `revisao_final`, GPU 1, Athena.
- G1 (Qwen r=256 dose=0% seeds 15/137/256): em andamento
- Patches activos: `c3ba205` (--model, --no-quant)
- Término estimado G1: ~12:30 | G2: ~17:30 | G3: ~24:30 | G4: ~26:30 | G5: ~28:00

---

*Arquivo: `v4/docs/revision/fase3-log.md`*
*Última atualização: 2026-10-02*


## 3.5 residual — ForTIFAI, Soutif-Cormerais, Gemma 4 hash

**Status: ✅ APLICADO em 2026-10-02**

### Auditoria das 3 entradas pendentes do plano

| Chave | Situação | Ação |
|---|---|---|
| `zibakhsh2024` (ForTIFAI) | matched ✅ arXiv:2509.08972. Autores: Shabgahi, Aghazadeh, Mirhoseini, Koushanfar. Não retratado. | Sem correção |
| Soutif-Cormerais | Não existe no .bib — o plano listava como [31] de versão anterior do .bib. [31] atual é `shi2024continualllm`. | Sem ação — não está no artigo |
| `gemma4_2026` | arXiv:2607.02770 correto ✅. Hash do model card vai na Fase 5 (reprodutibilidade), não no .bib | Sem correção bibliográfica |

### Correção adicional identificada: shi2024continualllm

arXiv:2404.16789 — autores errados no .bib:
- Estava: `Shi, Tongtong and Yang, Zhenwei and Jin, Lingyu and others`
- Correto (confirmado Scholar Sidekick, matched high confidence):
  `Shi, Haizhou and Xu, Zihao and Wang, Hengyi and Qin, Weiyi and Wang, Wenyuan and Wang, Yibin and Wang, Zifeng and Ebrahimi, Sayna and Wang, Hao`
- Corrigido no .bib.

### Estado final do .bib

- 48 entradas, 0 ausentes no .tex, 0 retratadas
- Todas as entradas com arXiv ID verificadas por Scholar Sidekick (10 na sessão anterior + ForTIFAI + shi2024continualllm nesta sessão)
- Correções aplicadas: `yi2025` autores (sessão anterior) + `shi2024continualllm` autores (esta sessão)


## §3.1 — Parâmetros de geração vs avaliação (R1.Q5)

**Status: ✅ APLICADO em 2026-10-02**

### O que foi feito

O parágrafo `\textit{Evaluation decoding.}` em `sec:k0` já separava os dois modos corretamente
com os valores numéricos da V1. A única adição foi tornar `do_sample` explícito:

- Avaliação: adicionado `\rev{\texttt{do\_sample=False},}` antes de "temperature~0"
- Síntese: adicionado `\rev{\texttt{do\_sample=True},}` antes de "temperature~0.7"

Parâmetros completos agora explícitos nos dois modos:

| Etapa | do_sample | temperature | top_p | max_new_tokens |
|---|---|---|---|---|
| Avaliação K0 | False (greedy) | 0 | — | 20 |
| Geração sintética | True | 0.7 | 0.9 | 30 |

Valores confirmados pela V1 (`verificacoes.md`).

---

## §3.9 nova — Tabela de fontes de variação e controles (R1.Q2)

**Status: ✅ APLICADO em 2026-10-02**

### O que foi feito

Inserida nova `\subsection{Sources of variation and experimental controls}\label{sec:controls}`
com `tab:controls` imediatamente antes do parágrafo "The results presented in Section~\ref{sec:results}".

O bloco inteiro está em `\rev{}`.

### Fontes de variação mapeadas (7 linhas)

1. Quantização NF4 vs bf16 → controle G3
2. Ordem dos dados (shuffle) → controle G4
3. Optimizer state → held constant (fresh optimizer por geração)
4. Synthetic data seed → 3–5 seeds por condição headline
5. Backbone architecture → replicado em Gemma 3 e Gemma 4 E2B
6. Pipeline version → commit c3ba205 em todos os runs
7. Evaluation scoring leniency → Tabela S2 (EM estrito, suplementar)

### Total \rev{} após estas inserções: 49 blocos


## §6 Limitações — 3 parágrafos novos (R1.Q3, R2.4)

**Status: ✅ APLICADO em 2026-10-02**

### Parágrafos inseridos (todos em `\rev{}`, antes de "Finally, the present work establishes")

1. **EM estrito (R1.Q3 / A10):** Explica que a métrica de substring matching pode inflar
   retenção em respostas verbosas. Anuncia Tabela suplementar S2 com re-avaliação EM estrito
   sobre as predições já salvas. Conclui que o sentido das classificações de regime é inalterado.

2. **E2B 1 seed (R2.4):** Declara explicitamente que Gemma 4 E2B foi avaliada com um único seed
   e que os resultados são tratados como exploratórios e de apoio, não como replicação
   independente dos thresholds quantitativos.

3. **Mecanismo da exposição (plano L289):** Declara que o mecanismo pelo qual a redução de
   exposição estabiliza a retenção não foi estabelecido. Duas hipóteses (update budget vs
   composição dos dados). G2b steps-matched inconclusivo (n=3). Testado em 1 backbone/config.

### Total \rev{} após esta inserção: 52 blocos
