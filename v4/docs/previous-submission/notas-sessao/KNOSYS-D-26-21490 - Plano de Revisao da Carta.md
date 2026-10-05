# Plano de Revisão — Carta de Resposta aos Revisores
## KNOSYS-D-26-21490 | 2026-10-05

> **Status:** aguardando aprovação antes de qualquer edição na carta ou no manuscrito.

---

## 0. Premissas e fontes disponíveis nesta etapa

| O que está disponível agora | O que depende de conferência posterior |
|---|---|
| LaTeX da carta (`response-to-reviewers.tex`) | Manuscrito compilado (`manuscript-anonymous.tex`) |
| Resumo da conversa anterior (contexto compactado) | Repositório Zenodo v1.0.3 e estado atual |
| `numbers.tex` (macros canônicas) | Planilha `resultados_consolidados.csv` |
| Commits do git (histórico de patches) | Scripts `make_all.py` e resultados de `15/15 checks` |
| PDF de referência IEEE Access | Pareceres integrais dos revisores |

**Critério de operação:** afirmações sem evidência identificável ficam sinalizadas como `[VERIFICAR]`, nunca tratadas como verificadas.

---

## 1. Delimitar fontes e montar trilha de verificação

### 1.1 Fontes dos comentários
- Base exclusiva: blocos `\rquote` transcritos na carta (10 pontos: Editor + R1.1–R1.5 + R2.1–R2.5).
- Não presumir acesso a pareceres integrais separados.

### 1.2 Aproveitamento do padrão IEEE Access
O que aproveitar:
- Organização ponto a ponto com label `Reviewer #X, Concern #Y`.
- Distinção visual entre comentário do revisor, resposta dos autores e ação realizada.
- Indicação explícita de localização no manuscrito.

O que adaptar para KBS/Elsevier:
- Sem exigências específicas da IEEE (formato de submissão, double-blind vs. single-blind, EES vs. ScholarOne).
- **Critério de aceite:** nenhuma exigência específica da IEEE ser apresentada como regra da Elsevier.

### 1.3 Inventário rastreável por afirmação
Para cada ponto da carta, a trilha de verificação segue a cadeia:

```
comentário → resposta → alteração no manuscrito
  → seção/tabela/figura identificável
    → dado ou script
      → versão arquivada (commit / Zenodo release)
```

### 1.4 Matriz de evidências (a preencher antes de editar)

| Ponto | Afirmação | Evidência identificável | Status |
|---|---|---|---|
| R1.1 | G5: 2/3 direção correta | Section 4.4 manuscrito | [VERIFICAR] |
| R1.2 | G3 bf16 r=16: Gen10=97.4% (76/78 por semente) | numbers.tex / CSV | [VERIFICAR] |
| R1.2 | G4 p=0.70, N=3+3 | CSV / script | [VERIFICAR] |
| R1.2 | G1+G4 média 79.7%±1.7 pp | numbers.tex `\DeltaRanks=17.70` | [VERIFICAR] |
| R1.2 | G3 pareado: +18.4 pp, p=0.25 | CSV / script | [VERIFICAR] |
| R1.2 | Gemma r4 vs r16: Δ=+37.8 pp, p=0.0079 | `\GthreeDeltaRanks=37.80` | [VERIFICAR] |
| R1.3 | Strict exact-match: classificações preservadas | Supplementary Table S2 | [VERIFICAR] |
| R1.4 | C1/C5 pipeline inconsistency: +1.9 pp (N=3) | CSV reprocessado | [VERIFICAR] |
| R1.4 | B7 Qwen: doses, 5 sementes, Gen5 e Gen10 | `\BsevenDeltatenFifty=+9.2` etc. | OK (numbers.tex) |
| R1.4 | B7 slope 0%=-1.13, 50%=-0.15 pp/gen | `\BsevenSlopeFifty=-0.15` | OK (numbers.tex) |
| R1.4 | G2 Gemma: +12.9 pp, slope=-0.91 ambos os braços | `\GtwoDeltatenFifty=+12.9` etc. | OK (numbers.tex) |
| R1.4 | LR equivalence: 89.7% vs 90.2%, 90% CI [-0.8,1.6] | `\BsevenLRdelta=+0.43` | [VERIFICAR] |
| R1.5 | 27 runs, 112 números, 15/15 checks | Script make_all.py | [VERIFICAR] |
| R1.5 | Zenodo v1.0.3 conteúdo efetivo | Zenodo DOI 10.5281/zenodo.23146342 | [VERIFICAR] |
| R2.2 | Fonte do defeito: Unicode/T1 | Log de compilação original | [VERIFICAR] |
| R2.3 | Table 2 = controls; Table 2 = rank sweep? | Manuscrito compilado | [VERIFICAR] |
| R2.4 | Gemma N=5+5 independente p=0.0079 | CSV / script | [VERIFICAR] |
| R2.4 | Gemma pareado p=0.0625 | CSV / script (se sementes iguais confirmadas) | [VERIFICAR] |
| R2.5 | fawi2024curlora: arXiv único | cas-refs.bib | [VERIFICAR] |
| R2.5 | ding2024ranktrade: year=2025, AACL-IJCNLP | cas-refs.bib | [VERIFICAR] |
| R2.5 | gemma4_2026: arXiv:2607.02770 | cas-refs.bib | [VERIFICAR] |
| Geral | Edição linguística Elsevier contratada | Comprovante/invoice | [VERIFICAR] |
| Geral | Pré-registro B7 commit a916ebf | git log | [VERIFICAR] |
| Geral | Checkpoints disponíveis "sob solicitação" | Localização física | [VERIFICAR] |

---

## 2. Verificações de integridade editorial, numérica e de reprodução

### 2.1 Referências de localização no manuscrito (`\msloc`)
- Preferir identificadores estáveis (labels `\label{sec:...}`, `tab:...`, `fig:...`, `eq:...`) a números de linha.
- **Critério de aceite:** cada `\msloc` aponta para um label que existe no manuscrito compilado.

### 2.2 Macros `\input{numbers}` — verificações pendentes

| Macro | Valor em numbers.tex | Verificação necessária |
|---|---|---|
| `\BsevenSlopeFifty` | −0.15 | Confirmar: média (C10−C5)/(78×5), dose=50% |
| `\BsevenSlopeZero` | **não existe** → usado literal −1.13 na carta | Confirmar valor no CSV |
| `\GtwoDeltatenFifty` | +12.9 | Confirmar: Gen10 G2 dose=50% vs dose=0% |
| `\GtwoPtenFifty` | 0.001 | Confirmar: teste t pareado N=3 |
| `\GtwoCItenLoFifty` | 9.70 | Confirmar: IC 95% |
| `\GtwoCItenHiFifty` | 16.10 | Confirmar: IC 95% |

### 2.3 Contagens e escopos a verificar

| Afirmação | Verificação necessária |
|---|---|
| "27 executed training runs" | Listar G1–G5 por experimento e semente |
| "112 canonical numbers, 15/15 checks pass" | Executar `python scripts/make_all.py` na versão atual |
| "release v1.0.3" — conteúdo efetivo | Listar artefatos do release no Zenodo |
| "per-generation boolean correctness vectors included in CSV" | Confirmar colunas no CSV |
| "raw token-level predictions not in current release" | Confirmar ausência no Zenodo e presença local |

### 2.4 Colisão de numeração de tabelas — `[VERIFICAR]`
A carta menciona:
- `Table 2 (tab:controls)` — tabela de controles (Section 3.9)
- `Table 2` com coluna "Homeo." — tabela de rank-sweep (R2.1)

Se ambas compilam como Table 2, há colisão. Verificar numeração no PDF do manuscrito e corrigir referências na carta.

### 2.5 Declarações que exigem comprovação ou reformulação

| Declaração | Ação necessária antes de manter |
|---|---|
| "Elsevier's Author Services English Language Editing" | Mostrar comprovante ou reformular para "revised throughout for language clarity" |
| "protocol committed as a916ebf before any run" | Confirmar com `git log --oneline` |
| "adapter checkpoints available on request; ~70 MB each in bf16" | Confirmar localização e tamanho real |
| "G3 paired design: same seeds at both ranks" | Confirmar no CSV — sementes de r=16 e r=256 em G3 são as mesmas? |
| "Gemma N=5+5: if same five seeds were used at both ranks" | Confirmar ou reformular para condicional explícito |

---

## 3. Revisão ponto a ponto — Editor e Revisor 1

### Editor — idioma e resposta ponto a ponto
- **Verificar:** revisão linguística efetiva e cobertura de todos os comentários.
- **Critério:** abertura sóbria; sem alegação de serviço contratado sem comprovante.
- **Decidir:** cover letter e rebuttal são documentos distintos para o EES da KNOSYS?

### R1.1 — Calibração prospectiva de ETP
- Preservar ETP como estrutura experimental operacional, não preditor escalar validado.
- Separação ETP-design (antes do treino) vs. ETP-observed (depois): confirmar no manuscrito.
- G5 como evidência exploratória de 2/3 células na direção esperada — não backbone inédito.
- **Critério:** protocolo prospectivo proposto é distinto de validação já executada.

### R1.2 — Confundidores e controles
- **G3 pareado (N=3, p=0.25):** confirmar que sementes são as mesmas em r=16 e r=256; resultado é "não significativo por N pequeno", não "sem efeito".
- **Lacuna de 17.7 pp:** descritiva — grupos diferem em rank, quantização E protocolo de ordem de dados; não é comparação pareada.
- **G4:** semente e ordem variaram juntas → não permite atribuição isolada de efeito de ordem. Texto atual diz isso; confirmar que permanece na versão final.
- **Quantização:** G3 bf16 vs. NF4 usa sementes e pipelines diferentes — não comparação pareada; texto atual faz esse cuidado; verificar que não regride.
- **Otimizador:** fresh optimizer por geração é protocol invariant — confirmar no manuscrito.

### R1.3 — Validade externa
- **Separar:** robustez ao strict scorer (testada) de generalização para respostas longas, multi-hop, novos domínios, conjuntos maiores (não testada).
- **Corrigir:** a justificativa de que "ampliar o conjunto de avaliação necessariamente alteraria a composição do treinamento" é imprecisa — ampliar um conjunto de avaliação *disjunto* do treinamento não altera o treino. Reformular para: ampliar a avaliação exigiria um corpus-fonte maior, com implicações para a composição do stream sintético.
- **Critério:** limitações específicas; nenhuma sugestão de experimento inexistente.

### R1.4 — Redução da exposição
- Apresentar a inconsistência C1/C5 com clareza; distinguir 15% dos exemplos de ~5% dos tokens.
- Verificar B7 Qwen: 5 sementes, 4 doses, ganhos Gen5 e Gen10, slopes −0.15 (50%) vs. −1.13 (0%) pp/gen — **fonte: CSV/script, não só numbers.tex**.
- G2 Gemma: ganho em Gen10 sem atenuação do slope; slope −0.91 igual nos dois braços.
- **Não alegar:** mecanismo identificado, equivalência formal com redução de LR.
- LR equivalence: ponto estimado similar (±0.4 pp), CI 90% inclui zero, não declarar formal equivalence.

### R1.5 — Pacote de reprodução
- Distinguir claramente: (a) instruções suficientes para reproduzir análises, (b) artefatos efetivamente publicados no Zenodo v1.0.3, (c) itens não disponibilizados (predições brutas, checkpoints, pesos base).
- **Critério:** sem "pacote completo" nem promessa de reprodução pelo release inicial com scripts ausentes.

---

## 4. Revisão ponto a ponto — Revisor 2

### R2.1 — Siglas e notação
- Auditar primeira ocorrência de ETP, MTLD, KL, JS, bf16, SVD, TCE, QLoRA, LoRA, "Homeo." no manuscrito.
- Confirmar que KL/JS/coverage removidos da Figura 1 não continuam descritos como métricas medidas em outros pontos.
- Uniformizar K₀ como conjunto, |K₀| como cardinalidade, R(t) como proporção — inclusive nas definições de SDI-3.

### R2.2 — Equações e renderização
- Conferir Equações 1–6 e `5×10⁻⁶` no PDF compilado, além do fonte.
- Verificar normalização singular (σ̂ᵢ = σᵢ/Σσⱼ), sinal da entropia em erank (sinal negativo), definições e sinais de SDI-3 (log ratio: MeanLen_T/MeanLen_0 e D1_0/D1_T).
- **Cuidado:** não atribuir causa dos defeitos exclusivamente a Unicode/T1 sem confirmação técnica; é possível que o defeito fosse no fonte, não apenas na renderização.

### R2.3 — Coerência técnica
- Confrontar texto, resumo e tabelas: r=128 (Bounded), r=256 (Degradative), "lowest-pressure degradative configuration tested".
- Verificar N por célula: quais são ablações de N=1 semente (sinalizar com hedging adequado).
- FFT Gemma 3: resultado não monotônico, N=1 — "is consistent with", não "confirms".
- **Critério:** nenhuma afirmação de limiar universal, nenhuma classificação incompatível, nenhuma "confirmação" de N=1.

### R2.4 — Método e estatística
- Revalidar: teste exato independente Gemma N=5+5, p=0.0079 (bilateral, 252 alocações) **sob hipótese de sementes independentes**.
- Revalidar: teste pareado sign-flip p=0.0625 (N=5, bilateral) **sob hipótese de mesmas sementes nos dois ranks** — confirmar no CSV.
- B7 doses: paired t-tests, N=5 sementes. Verificar: t-test ou permutation? Consistência interna.
- G2: N=3, t-test ou wilcoxon? Verificar potência e comunicar limitação.
- Multiplidade: 4 doses × 2 horizontes = 8 testes em B7 — considerar se correção é necessária ou se hipótese direcional pré-registrada a dispensa.
- Normalizações entre arquiteturas e malha esparsa: apresentar como limites, não como calibração resolvida.

### R2.5 — Referências
- Verificar no .bib:
  - fawi2024curlora: arXiv 2408.14572 aparece exatamente uma vez.
  - ding2024ranktrade: year=2025, venue AACL-IJCNLP 2025.
  - gemma4_2026: arXiv:2607.02770 — confirmar que o arXiv existe.
  - keisha2025: arXiv:2509.04796, status de preprint declarado.
  - Todos os entries com venue completo (journal/proceedings, volume, páginas, DOI).
- **Critério:** afirmações bibliográficas na carta concordam com as fontes listadas no .bib.

---

## 5. Critérios para a reescrita e conferência final

### 5.1 Estrutura e concisão
- Condensar repetições entre respostas sem eliminar: resposta direta, evidência, ação realizada, localização verificável.
- Cada ponto deve ter: (a) `Author response:` — posição e evidência; (b) `Author action:` — o que foi feito; (c) `\msloc` — localização por label estável.

### 5.2 Tom
- Reconhecer a inconsistência de pipeline sem minimizá-la.
- Explicitar o que foi corrigido, o que os novos testes mostram e o que permanece inconclusivo.
- Formal, construtivo, persuasivo — sem defensive writing.

### 5.3 Padronização terminológica
| Dimensão | Padrão a manter |
|---|---|
| Regimes | Homeostatic, Bounded, Degradative (não "Homeo.") |
| Experimentos | G1, G2, G3, G4, G5, B7 (siglas consistentes) |
| Horizontes | Gen 5, Gen 10 (não misturar "Gen~5" e "generation 5") |
| Unidades | pp para pontos percentuais; pp/generation para slopes |
| N | sempre declarado por célula; N=1 sinalizado |
| p-values | p=0.xxx; "not significant" quando p>0.05; não "ns" sozinho |
| ICs | 95% CI [a, b] em pp; 90% CI quando pré-especificado |
| Exploratório | "exploratory", "consistent with", nunca "confirms" para N=1 |

### 5.4 Anonimato e entregáveis
- Confirmar modalidade de avaliação (single-blind vs. double-blind) para KNOSYS.
- Verificar: a assinatura com nome na carta é adequada ao processo editorial?
- Entregáveis a confirmar para esta rodada: (a) response letter, (b) manuscrito destacado, (c) manuscrito limpo (LaTeX + PDF), (d) replication package.

### 5.5 Conferência técnica final da carta compilada
- [ ] 0 erros fatais de compilação.
- [ ] Todas as referências cruzadas resolvem (sem `??`).
- [ ] `\input{numbers}` carrega sem macro indefinida.
- [ ] Todas as macros G2/B7 usadas na carta existem em numbers.tex.
- [ ] Equações 1–6 renderizam corretamente no PDF.
- [ ] `5×10⁻⁶` em Table 7 renderiza com expoente negativo.
- [ ] Figuras declaradas como 300 dpi: verificar resolução efetiva.
- [ ] Nenhum `\msloc` aponta para label inexistente no manuscrito.
- [ ] Nenhuma promessa incompatível com artefatos efetivamente entregues.

---

## Próximos passos

1. **Aprovação deste plano** (ou ajustes solicitados).
2. Executar buscas e verificações no Kiro (manuscrito, CSV, git log, .bib, Zenodo).
3. Registrar resultados e pendências na matriz de evidências (Seção 1.3 acima).
4. **Somente após aprovação dos resultados:** editar a carta ponto a ponto.
5. Compilar, verificar lista de conferência técnica final, atualizar previous-submission, commitar.
