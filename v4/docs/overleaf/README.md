# overleaf/ — Response to Reviewers (LaTeX)

Carta de resposta para o round 1 do KNOSYS-D-26-21490.
Um único `.tex` gera os **dois** arquivos exigidos pela Elsevier:
versão com alterações destacadas e versão limpa.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `response-to-reviewers.tex` | Fonte LaTeX — editar aqui |
| `build.ps1` | Gera `response-HIGHLIGHTED.pdf` + `response-CLEAN.pdf` de uma vez |
| `latexmkrc` | Config para compilação local com latexmk |

---

## Como usar no Overleaf

1. Crie dois projetos em branco no Overleaf — um para cada versão.
2. Em ambos, faça upload de `response-to-reviewers.tex`.
3. No projeto **highlighted**: deixe `\highlighttrue` (padrão).
4. No projeto **clean**: mude para `\highlightfalse`.
5. Compile com pdfLaTeX. Sem `.bib` — sem dependências externas.

---

## Como gerar os dois PDFs localmente (recomendado)

```powershell
cd "G:\...\v4\docs\overleaf"
.\build.ps1
```

Gera automaticamente:
- `response-HIGHLIGHTED.pdf` — versão com texto inserido em azul/fundo, deletado riscado
- `response-CLEAN.pdf` — versão limpa, sem marcações

Requer `pdflatex` no PATH (TeX Live ou MikTeX).

---

## Como compilar manualmente (um por vez)

```powershell
# Versão highlighted
pdflatex "\def\HIGHLIGHTOVERRIDE{1}\input{response-to-reviewers}" -jobname response-HIGHLIGHTED
pdflatex "\def\HIGHLIGHTOVERRIDE{1}\input{response-to-reviewers}" -jobname response-HIGHLIGHTED

# Versão clean
pdflatex "\def\HIGHLIGHTOVERRIDE{0}\input{response-to-reviewers}" -jobname response-CLEAN
pdflatex "\def\HIGHLIGHTOVERRIDE{0}\input{response-to-reviewers}" -jobname response-CLEAN
```

---

## Macros disponíveis no .tex

| Macro | Uso | Efeito highlighted | Efeito clean |
|---|---|---|---|
| `\chg{texto}` | texto inserido/alterado | fundo azul-claro | texto normal |
| `\del{texto}` | texto removido | riscado vermelho | invisível |
| `\ins{texto}` | sinônimo de `\chg` | fundo azul-claro | texto normal |
| `\revised{trecho}` | trecho do MS citado na resposta | sempre azul itálico | sempre azul itálico |
| `\msnote{texto}` | nota interna de trabalho | aparece em cinza | invisível |
| `\msloc{p.~14, ll.~327--345}` | localização da mudança no MS | sempre visível | sempre visível |

---

## Workflow de preenchimento

1. Para cada ponto, substitua `\msnote{inserir resposta}` pela resposta em inglês.
2. Marque trechos alterados no MS com `\revised{texto citado}`.
3. Preencha `\msloc{...}` com página e linhas reais após editar o `.tex` do manuscrito.
4. Quando terminar, rode `.\build.ps1` e submeta os dois PDFs + o Word convertido.

---

## Pacotes necessários (todos na instalação padrão)

`geometry`, `lmodern`, `microtype`, `parskip`, `xcolor`, `mdframed`,
`soul`, `enumitem`, `hyperref`, `titlesec`.
