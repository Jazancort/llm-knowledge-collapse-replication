# Plano de Revisão v2 — Carta de Resposta aos Revisores
## KNOSYS-D-26-21490 | 2026-10-05

> **Status:** aguardando decisões D1–D7 e aprovação antes de qualquer edição.
> **Insumos analisados:** (1) carta do editor Hang Yu; (2) carta de resposta atual em LaTeX com macros `numbers.tex`; (3) modelo IEEE Access (Access-2025-40211); (4) manuscrito revisado com marcações (04/10/2026) e Highlights.

**Diagnóstico central:** a carta está bem estruturada e tem um ponto forte raro — a admissão transparente do erro de pipeline C1/C5. Porém, ela descreve um manuscrito mais corrigido do que o PDF revisado efetivamente mostra. O Revisor #2, que já demonstrou atenção microscópica a inconsistências, encontrará essas divergências na primeira leitura cruzada. A **Fase 1 é bloqueante**: nenhuma reescrita deve começar antes de resolvê-la.

**Legenda:** 🔴 crítico (risco de credibilidade) · 🟠 alto · 🟡 médio

---

## FASE 0 — Decisões que dependem de você

| ID | Decisão | Por que importa |
|---|---|---|
| **D1** 🔴 | O serviço de English Language Editing da Elsevier foi efetivamente contratado? | A carta afirma "We engaged". Se não houve contratação, isso é declaração falsa ao editor. Alternativa: revisão profissional externa com certificado anexado. |
| **D2** 🔴 | Para cada divergência da Fase 1: corrigir o manuscrito (opção A) ou corrigir a carta (opção B)? | Recomendo A na maioria. Prazo: 20/10/2026. |
| **D3** 🔴 | A carta sai em Word (exigência do editor). Converter do LaTeX via pandoc ou redigir nativamente? | As macros `\BsevenSlopeFifty`, `\GtwoDeltatenFifty` etc. precisam estar expandidas em valores literais. |
| **D4** 🟠 | O que entra no novo release do Zenodo: gerações brutas, checkpoints dos adaptadores, scripts revisados? | Hoje a carta e o Apêndice A se contradizem sobre "raw outputs". |
| **D5** 🟠 | Dividir os bullets do Revisor #2 em sub-itens numerados (R2-1.a … R2-5.e)? | O editor pede resposta ponto a ponto. Recomendo dividir: o R2 tem ~30 bullets, hoje agrupados em 5 blocos. |
| **D6** 🟡 | A regressão logística de efeitos mistos entra ou sai? | Ela não aparece no manuscrito revisado. A carta não pode mencioná-la se não existir. |
| **D7** 🟡 | Renomear o experimento "G2" (dose-resposta Gemma) para evitar colisão com a série de ablações G1–G5? | Hoje "G2" é ambíguo dentro do próprio manuscrito. |

---

## FASE 1 — 🔴 Divergências entre a carta e o manuscrito revisado (bloqueante)

Cada linha foi verificada contra o PDF revisado de 04/10/2026.

| ID | A carta afirma | O manuscrito revisado mostra | Ação |
|---|---|---|---|
| **C1** | "ETP" removido da Fig. 1; KL/JS/coverage removidos | Fig. 1 ainda traz "ETP threshold identification" e "Distribution shift — KL, JS, coverage". Também "Exposure 100% → ~95%" (desatualizado) e "five axes" na legenda vs. "pressure axes" no diagrama. | Refazer a Fig. 1 inteira. |
| **C2** 🔴 | Renderização corrigida com lmodern + T1 | O PDF ainda exibe `í10İ`, `Ë ˆ4,16...`, `10*5`, `5˜`, `⊙` (Tab. 1), `*0.15`, `*1.20 pp`, `3İ3` — em Highlights, Abstract, §3.1, §3.4, §3.5, §4.1, Tab. 1, 2, 8, 9, 13. | Diagnosticar a causa real (provavelmente mapeamento de glifos Unicode na classe cas-dc/elsarticle), gerar PDF de teste pelo Editorial Manager e só então redigir a explicação. |
| **C3** | $K_0$ = conjunto, $\lvert K_0\rvert$ = cardinalidade; $\hat\sigma_i = \sigma_i/\sum_j\sigma_j$ | Tab. 1 ainda diz "K0 (also written n0) denotes its cardinality"; Eq. 1 usa $K_0$ no denominador; Eq. 2 e Tab. 1 ainda trazem $\sigma_i = \sigma_i/\sum_j\sigma_j$ — exatamente a crítica do revisor. | Corrigir no manuscrito. Adotar $p_i$, como o próprio revisor sugeriu. |
| **C4** | r=128 passou a "transition-zone configuration" | §5.3 mantém "phenotypes emerge above the pressure threshold. At intermediate capacity (r=128)"; §4.4 mantém "above-threshold regimes". | Corrigir todas as ocorrências. |
| **C5** | As cinco ocorrências de "boundary configuration" para r=256 foram substituídas | §5.4 mantém "boundary configurations are sensitive to graded changes"; §4.4 mantém "at the regime boundary". | Busca global + correção. |
| **C6** | Abstract corrigido para "three to five independent seeds for headline conditions (single seed for intermediate ablations)" | O Abstract real diz "three or five independent seeds for most headline conditions (six for the pooled r=256 estimate)". A Contribuição 1 ainda diz "confirmed across three to five independent seeds per condition". | Corrigir a Contribuição 1; citar o Abstract literalmente. |
| **C7** | FFT em Gemma 3 deixou de "confirmar" | §4.3.3 já usa "is consistent with" ✔, mas a Contribuição 2 ainda diz "confirming that the phenomenon responds to perturbation magnitude". | Corrigir a Contribuição 2. |
| **C8** | "Homeo." expandido "nas quatro ocorrências da Tabela 2" | A Tabela 2 atual é a de eixos experimentais e não contém "Homeo."; o termo aparece na legenda da Fig. 5 ("Homeo.", "Degrad."). | Corrigir a Fig. 5 e a remissão na carta. |
| **C9** | Quantização: r=256 bf16 = "79.1%, within 0.0 pp of the NF4 G1+G4 mean"; "not the primary driver" | A média G1+G4 é 79,72%, não 79,1%. §4.6 declara que "a causal conclusion about quantization awaits full provenance audit". Em r=16, §4.6 diz "+0.00 pp vs. NF4", mas §4.1 dá 96,2% (NF4, 1 semente) vs. 97,4% (bf16). | Definir qual baseline NF4 vale para r=16; replicar na carta a ressalva de auditoria pendente. Nunca afirmar mais do que o manuscrito. |
| **C10** | G5: "ordered in the expected direction for 2 of 3 configurations" | O manuscrito diz que a ordem saiu como esperado nas três células; o que falhou foi uma classificação de regime (célula de alta pressão: previsto Degradative, obtido Bounded). | Separar "ordenação" de "classificação". |
| **C11** | Pacote inclui "boolean correctness vectors"; Author action diz que não inclui "raw token-level predictions" | Apêndice A diz que v1.0.3 contém "raw outputs". §3.3 é citada para "checkpoint identifiers", mas não traz hashes nem revisões. | Alinhar os três textos após D4. |
| **C12** | "Added a concrete validation protocol for prospective calibration in Section 6" | §6 traz apenas: "Whether such a formulation can be obtained… remains an open question" — não é protocolo. | Escrever o protocolo de fato (4–5 passos) ou remover a afirmação. |
| **C13** | Shumailov "is added as the primary citation" | Shumailov já era a referência [6] na submissão original. | Remover "added"; dizer "reinforced as the primary peer-reviewed citation". |
| **C14** | Tabela de controles = "Table 2 (tab:controls)" | É a Tabela 3. | Ver C15 abaixo. |
| **C15** 🔴 | Auditoria completa de remissões | Ver tabela abaixo. | Corrigir todas as referências cruzadas da carta. |
| **C16** 🔴 | A carta cita l. 72, ll. 2094–2100, ll. 692–698 etc. | O PDF revisado não tem numeração de linhas. O revisor não poderá localizar nada. | Ativar `lineno` no manuscrito destacado ou substituir todas as remissões por seção + página. |
| **C17** 🟠 | Fonte única de verdade numérica | Divergências detectadas: B7 Gen5 (+3,6/+3,8/+4,4 pp vs. +5,0/+5,8 pp anteriores); B7 Gen10 50% (+9,2 pp vs. +9,8 pp que é valor de G2 a 10%); "112 canonical numbers (15/15 checks pass)" vs. "15/15 consistency checks" no manuscrito. | Rodar `make_all.py` e conferir cada número. Verificar os 112. |

### C15 — Auditoria de remissões (carta → manuscrito correto)

| Na carta | Correto no manuscrito |
|---|---|
| Tabela 2 (controles) | Tabela 3 |
| §4.4 (G5) | §4.6 |
| §4.2 (Qwen, contraste G3) | §4.1 |
| §4.3.1 (Gemma 3) | §4.2.1 |
| Tabela 7 (rank × LR) | Tabela 9 |
| Tabela 6 (normalizações) | Tabela 13 |
| Tabela 4 (Gemma 3 ranks) | Tabela 6 |
| Tabela 2 (regimes r=128/256) | Tabela 4 |
| §3.6 ($K_0$) | §3.2 |
| §3.1 (protocolo de avaliação) | §3.2 |
| §A.1 | Apêndice A |
| §3.9 + Tab. 2 | §3.9 + Tab. 3 ✔ seção correta |

---

## FASE 2 — Estrutura e formato (modelo IEEE adaptado às regras Elsevier)

| ID | Item |
|---|---|
| **E1** | Adotar o padrão do modelo IEEE para cada item: título em verde/negrito com o comentário integral embutido — *Reviewer #1, Concern #1 (Prospective calibration of ETP): How can effective training pressure be...* — seguido de **Author response:** e **Author action:**, com régua horizontal entre itens. |
| **E2** 🟠 | Reforçar a seção **Author action**. No modelo IEEE, cada ação é uma lista numerada com (i) seção + página, (ii) o trecho novo citado literalmente entre aspas. Hoje a maioria das ações é descritiva sem exibir o texto novo. |
| **E3** | Adicionar resposta ao parágrafo de avaliação geral de cada revisor, hoje ausente: R#1 ("not yet a transferable quantitative predictor…"); R#2 ("ETP framework is promising but currently conceptual…"). |
| **E4** | Dividir o Revisor #2 conforme D5 (sub-itens R2-1.a … R2-5.e), garantindo que nenhum bullet fique sem resposta nominal. |
| **E5** | Inserir quadro-resumo de alterações (comentário → alteração → local), atendendo literalmente ao pedido do editor. |
| **E6** | Incluir glossário dos códigos internos (G1, G2, G2b, G3, G4, G5, B7, C1–C5) no início. Hoje a carta usa "Bloco 7" (português) e "B7" alternadamente. |
| **E7** | Cabeçalho: substituir `\today` pela data fixa de submissão; endereçar a Hang Yu, Senior Editor, Knowledge-Based Systems; usar "Ms. Ref. No.: KNOSYS-D-26-21490"; remover chaves .bib do corpo do texto e usar autor + ano + número da referência. |
| **E8** | Na versão Word: trocar `\citet{...}` por "[n] Autor et al."; manter equações como objetos editáveis (MathType/equação nativa), não imagens. |

---

## FASE 3 — Carta de apresentação e resposta ao Editor

| ID | Item |
|---|---|
| **F1** | Reescrever as "key enhancements" para refletir somente o que existe no manuscrito final. Substituir "for all headline comparisons" por lista explícita (B7, G2, G3-pareado, Gemma 3 anchor ranks). |
| **F2** 🟠 | Checklist explícito das exigências do editor: cover letter, response to reviewers, highlights, revised manuscript, CRediT author statement, author agreement, declaration of interest — todos em Word; tabelas/figuras/equações em formato editável; figuras em 300 dpi TIFF/PNG/EPS (não PDF); arquivos .bib incluídos. |
| **F3** 🟠 | Highlights. Limite Elsevier = 85 caracteres por item; o 5º item excede largamente. Também contém códigos internos ("Qwen B7", "Gemma 3 G2") e caracteres corrompidos. Reescrever os 5 itens e registrar a correção na carta. |
| **F4** 🟠 | Metadados do manuscrito. O PDF revisado exibe "First Author et al.", orcid(s): vazio e paginação quebrada ("Page 25 of 24", "Page 28 of 24"). Corrigir e mencionar na resposta ao editor. |
| **F5** | Atualizar a lista de itens enviados (a)–(d) para incluir documentos Word, .bib, material suplementar (Tabela S2) e novo DOI/versão Zenodo. Nota: no Apêndice A o DOI aparece truncado ("10.5281/zenodo.2314634") — corrigir. |

---

## FASE 4 — Revisor #1 (cinco perguntas)

### R1.1 — Calibração prospectiva
- Manter "does not establish a transferable scalar predictor": é o tom correto.
- Apresentar Π com a fórmula idêntica à de §3.5: $\Pi = \mathrm{erank}(\Delta W)\cdot(\eta/10^{-5})$.
- Corrigir a descrição do G5 (C10).
- Escrever o protocolo prospectivo concreto no manuscrito (C12): (i) varredura piloto de 2–3 ranks no backbone novo; (ii) ajuste do limiar por backbone; (iii) pré-registro de duas células em lados opostos; (iv) critério de desfecho (inclinação Gen5→10); (v) avaliação sem reajuste.

### R1.2 — Confusores
- Reescrever o parágrafo de quantização com as ressalvas de C9, incluindo a auditoria de proveniência pendente.
- 🟠 Responder "model-specific dynamics", hoje sem resposta direta: os limiares são backbone-dependentes, as cinco normalizações da Tab. 13 falharam, e o próprio desenho replica em três backbones.
- Manter G4 com a ressalva de que semente e ordem variaram juntas.
- Manter os dois testes de Gemma 3 com a ressalva de pareamento.

### R1.3 — Validade externa
- Declarar com clareza o que não foi feito: nenhum experimento com respostas longas, multi-hop ou outro domínio.
- 🟠 Substituir o argumento frágil: a carta diz que ampliar o conjunto de avaliação "would alter the training-data composition" — não procede, pois o held-out pode crescer sem tocar nas 2.000 questões de treino. Trocar por: (i) custo computacional; (ii) ICs por bootstrap sobre os $|K_0|$ atuais; (iii) estratificação por comprimento de resposta como análise de robustez já disponível.
- Confirmar que a Tabela S2 (exact-match) existe fisicamente e está no pacote.

### R1.4 — Exposição: Qwen vs. Gemma 3
- Responder ao "porquê" de frente: a premissa da pergunta caiu sob pipeline pareado (+1,9 pp, n=3).
- Explicitar a assimetria: Qwen contém a inclinação; Gemma 3 ganha nível sem mudar inclinação (−0,91 pp/gen nos dois braços).
- Apresentar hipóteses rotuladas como hipóteses.
- Justificar r=10 em G2 em vez de r=16.
- Reportar os três níveis de G2 (+9,8 / +11,4 / +12,9 pp), não só 50%.
- Considerar correção para múltiplas comparações (Holm) nas 3–4 doses por geração.
- Admitir um rank por backbone como limitação declarada.

### R1.5 — Reprodutibilidade
- Estruturar em tabela espelhando os cinco itens pedidos (code / checkpoints / prompts / seeds / raw outputs) com status: incluído · sob solicitação · não disponível.
- Esclarecer o escopo de "27 executed training runs (G1–G5)" — aparentemente não inclui B7 nem G2; se incluir, recontar.
- 🟠 Hardware: o manuscrito declara RTX 4000 Ada 20 GB para "all other conditions", mas os logs locais indicam RTX 3070 8 GB + nó Athena. Corrigir antes de prometer reprodutibilidade "on workstation-class hardware".

---

## FASE 5 — Revisor #2 (cinco blocos, ~30 bullets)

### R2.1 — Abreviações e notação
- Cobrir itens hoje omitidos: $\mathrm{BA}_F$, $\theta_i^{(t)}$, $\theta_i^{(0)}$ — o revisor citou explicitamente; Eq. 3 (perdeu valor absoluto e somatório); notação de conjunto `r ∈ {4,10,12,14,16}`; expansão de bf16 (bfloat16) e LoRA na primeira ocorrência.
- Confirmar que §2.3 traz "Truncated Cross-Entropy (TCE)".
- Resolver incoerência interna da Tab. 1: $\theta^{(t)}$ é definido como "adapter-augmented weights", mas $d(t)$ mede deriva de FFT sobre os mesmos símbolos.
- Definir $K_t$ (usado em $R(t)=|K_t|/|K_0|$) ou eliminá-lo em favor da notação de conjunto da Eq. 1.

### R2.2 — Equações e tabelas
- 🔴 Reescrever a explicação técnica somente após o diagnóstico de C2. Remover ou condicionar "while the source was syntactically correct" — hoje é afirmação não verificada que o PDF contradiz.
- Estender a verificação às Eqs. 3, 4 e 5.
- Corrigir a remissão: `5×10^6` está na Tabela 9 (rank × LR), não na Tabela 7.

### R2.3 — Inconsistências técnicas (a–g)
- **(a)** 🟠 Explicitar qual fronteira cada intervalo descreve. Em Qwen, "50–88" é a fronteira bounded → degradative; em Gemma 3, "3–6" é homeostatic → degradative. Ajustar também "up to effective rank 50" em §5.1.
- **(b), (c)** → ver C4 e C5.
- **(d)** Já corrigido em §5.2 ✔ — manter e citar literalmente.
- **(e)** → ver C6.
- **(f)** → ver C7 (Contribuição 2).
- **(g)** Confirmar nos dados brutos se C5 removeu 15% dos exemplos (≈5% dos tokens) e usar a mesma formulação em §3.7 e na carta. O manuscrito atual diz "approximately 5% downsampling effect" sem distinguir exemplos de tokens.
- Revisar "clear, monotonic decline" em §4.1: a tabela mistura horizontes Gen5 (r=4, 32) e Gen10 (demais) — monotonicidade entre horizontes diferentes é afirmação frágil.

### R2.4 — Metodologia
- 🟠 "Sharp transition": o manuscrito substituiu "sharp" por "abrupt", mas "abrupt" continua em todo o texto. §5.1 usa o contraste de doses (10% vs. 50%) como evidência de abruptidade, o que é inválido — são doses não adjacentes com n=5. Adotar "threshold-like within the tested grid" e remover o argumento de coincidência.
- "ETP não é medida nova": concordar sem rodeios e reposicionar a contribuição como desenho fatorial + evidência dose-resposta + resultado pré-registrado.
- Normalização entre arquiteturas: propor calibração por backbone via varredura piloto curta (2 ranks × 1 semente × 5 gerações).
- **Gemma 4 E2B** 🔴: (i) verificar se arXiv:2607.02770 e o model card `google/gemma-4-e2b-it` existem de fato; (ii) diferenciar explicitamente do Gemma 3n E2B; (iii) citar `config.json` como fonte da descrição arquitetural (35 camadas, `num_kv_shared_layers=20`).

### R2.5 — Formato e citações
- Verificar autoria e venue de: [31] (Biderman et al. para arXiv:2405.18069), [20] ("S. Xu, et al." incompleto), [32] (Rathore et al., AACL-IJCNLP 2025), [7] (Keisha et al.).
- Padronizar DOIs em todas as entradas publicadas.
- 🟠 Declarar as correções pelo número da referência no manuscrito ([12], [32], [33]), não pela chave .bib.
- Acrescentar para [7]: "nenhuma conclusão quantitativa depende exclusivamente dele e §2.2 marca a comparação como 'suggestive context rather than a controlled comparison'".

---

## FASE 6 — Overclaims remanescentes no manuscrito

| ID | Item |
|---|---|
| **O1** 🟠 | Suavizar e registrar na carta: §4.3.2 "The joint dependence is evident" / "This demonstrates" — grade 3×3 com uma semente. §4.5 "the degradative regime is reversible" / "restores near-homeostatic behavior" — contradiz o próprio resultado (regime Bounded) e o G2. §5.2 "we reduce synthetic exposure by a marginal amount" — desatualizado; a dose eficaz é 50%. §5.1 e Conclusão "abrupt, backbone-dependent, and reproducible". Highlights "strongly attenuated". |
| **O2** | Uniformizar r=256: Tabela 4 traz 79,1% (N=3); texto de §4.1 e §4.6 traz 79,72% (N=6). Escolher um e anotar o outro em nota de rodapé. |
| **O3** 🟡 | Corrigir inconsistência de §4.5: "arrests progressive loss" vs. Abstract "strongly attenuated". Padronizar no termo mais conservador. |

---

## FASE 7 — Tom, linguagem e persuasão

| ID | Item |
|---|---|
| **T1** | Manter registro formal e cooperativo, sem os superlativos do modelo IEEE ("gold-standard reproducibility framework", "mathematical proof"). Em KBS, com um revisor hipercrítico, sobriedade é mais persuasiva. |
| **T2** | Padronizar a estrutura argumentativa para pedidos não atendidos: reconhecer → explicar o motivo → apresentar a mitigação executada → registrar como limitação com seção citada. Aplicar em R1.1, R1.3, R1.4 ("across ranks") e R2.4 (normalização). |
| **T3** | Reformular "This error was uncovered as a direct result of the reviewer's question" → "The reviewer's question prompted a full provenance audit of the exposure pipeline, which revealed that...". |
| **T4** | Revisão final de estilo: passado nas ações realizadas, presente nos fatos do manuscrito; terminologia única (Homeostatic / Bounded / Degradative com inicial maiúscula consistente); "effective training pressure" sempre expandido; evitar alternância pp/percentage points. |

---

## FASE 8 — Controle de qualidade e entrega

| ID | Item |
|---|---|
| **Q1** | Entregar carta em LaTeX e .docx, com macros expandidas e cores preservadas (azul = texto novo, verde = rótulo do revisor). |
| **Q2** 🔴 | Checklist cruzado de citações literais: cada trecho entre aspas e em azul na carta deve ser localizável por busca textual no PDF revisado. Meta: zero divergências. |
| **Q3** | Checklist de cobertura: mapear cada bullet dos dois revisores + cada exigência do editor para um item de resposta. Meta: 100%. |
| **Q4** 🔴 | Varredura de caracteres corrompidos (`í`, `İ`, `Ë`, `ˆ`, `˜`, `⊙`, `ù`, `*` como menos) no PDF final gerado pelo Editorial Manager, não apenas no compilador local. |
| **Q5** | Verificar paginação, numeração de tabelas/figuras e remissões internas do manuscrito após todas as edições. |

---

## Próximo passo

Aprovar a task list ou solicitar ajustes, de preferência já respondendo D1–D7.
Com a aprovação, serão gerados: (i) a carta final revisada; (ii) os trechos de correção para o manuscrito (caso opção A em D2).
