# build.ps1 — gera os dois PDFs (highlighted + clean) a partir de um único .tex
#
# Uso:
#   cd docs\overleaf
#   .\build.ps1
#
# Requer pdflatex no PATH (TeX Live ou MikTeX).
# Os PDFs são gerados na mesma pasta.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$tex = "response-to-reviewers.tex"

if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    Write-Error "pdflatex não encontrado no PATH. Instale TeX Live ou MikTeX."
    exit 1
}

function Compile-PDF {
    param(
        [string]$HighlightValue,   # "1" ou "0"
        [string]$JobName
    )
    Write-Host "`n── Compilando: $JobName ──" -ForegroundColor Cyan

    # Passa o switch via \def antes do \input — sem precisar editar o .tex
    $define = "\def\HIGHLIGHTOVERRIDE{$HighlightValue}\input{$tex}"

    # Duas passagens para hyperref/labels
    foreach ($pass in 1..2) {
        pdflatex `
            -interaction=nonstopmode `
            -jobname $JobName `
            $define | Out-Null
    }

    if (Test-Path "$JobName.pdf") {
        Write-Host "✔  $JobName.pdf gerado." -ForegroundColor Green
    } else {
        Write-Warning "Falha ao gerar $JobName.pdf — verifique o log."
    }
}

Compile-PDF -HighlightValue "1" -JobName "response-HIGHLIGHTED"
Compile-PDF -HighlightValue "0" -JobName "response-CLEAN"

# Limpar auxiliares
Write-Host "`nLimpando auxiliares..." -ForegroundColor Gray
foreach ($ext in @("aux","log","out","toc","fls","fdb_latexmk","synctex.gz")) {
    Remove-Item "response-HIGHLIGHTED.$ext" -ErrorAction SilentlyContinue
    Remove-Item "response-CLEAN.$ext"       -ErrorAction SilentlyContinue
}

Write-Host "`nConcluído. Arquivos gerados:" -ForegroundColor Yellow
Get-Item "response-*.pdf" | ForEach-Object { Write-Host "  $_" }
