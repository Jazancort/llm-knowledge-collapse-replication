Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Create-Docx {
    param(
        [string]$BaseDocx,
        [string]$OutDocx,
        [string]$Title,
        [string[]]$Paragraphs,
        [string[]]$Bullets = @()
    )

    $tempDir = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), [System.Guid]::NewGuid().ToString())
    [System.IO.Directory]::CreateDirectory($tempDir) | Out-Null

    [System.IO.Compression.ZipFile]::ExtractToDirectory($BaseDocx, $tempDir)

    $docXmlPath = [System.IO.Path]::Combine($tempDir, "word", "document.xml")

    $pXml = ""
    # Title
    $pXml += "<w:p><w:pPr><w:pStyle w:val=""Heading1""/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val=""32""/></w:rPr><w:t>$([System.Security.SecurityElement]::Escape($Title))</w:t></w:r></w:p>"

    foreach ($para in $Paragraphs) {
        $pXml += "<w:p><w:pPr><w:spacing w:after=""160""/></w:pPr><w:r><w:rPr><w:sz w:val=""24""/></w:rPr><w:t>$([System.Security.SecurityElement]::Escape($para))</w:t></w:r></w:p>"
    }

    foreach ($b in $Bullets) {
        $pXml += "<w:p><w:pPr><w:pStyle w:val=""ListParagraph""/><w:spacing w:after=""120""/></w:pPr><w:r><w:rPr><w:sz w:val=""24""/></w:rPr><w:t>• $([System.Security.SecurityElement]::Escape($b))</w:t></w:r></w:p>"
    }

    $bodyXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    $pXml
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>
"@

    [System.IO.File]::WriteAllText($docXmlPath, $bodyXml, [System.Text.Encoding]::UTF8)

    if (Test-Path $OutDocx) {
        [System.IO.File]::Delete($OutDocx)
    }

    $zipArchive = [System.IO.Compression.ZipFile]::Open($OutDocx, [System.IO.Compression.ZipArchiveMode]::Create)
    Get-ChildItem -Path $tempDir -Recurse -File | ForEach-Object {
        $relPath = $_.FullName.Substring($tempDir.Length + 1).Replace('\', '/')
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zipArchive, $_.FullName, $relPath) | Out-Null
    }
    $zipArchive.Dispose()

    Remove-Item $tempDir -Recurse -Force
    Write-Host "Created: $OutDocx"
}

$base = (Resolve-Path "title-page.docx").Path

# 1. Highlights
Create-Docx -BaseDocx $base -OutDocx (Join-Path (Get-Location) "highlights.docx") `
    -Title "Highlights" `
    -Paragraphs @("Title: Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study") `
    -Bullets @(
        "Recursive degradation exhibits a sharp pressure-dependent transition",
        "Pressure thresholds differ by an order of magnitude across three backbone families",
        "Adapter rank and learning rate interact to determine the operating regime",
        "Output drift accompanies degradative regimes beyond factual retention loss",
        "Reducing synthetic exposure by 5% restores near-homeostatic behavior on Qwen"
    )

# 2. Declaration of Interests Statement
Create-Docx -BaseDocx $base -OutDocx (Join-Path (Get-Location) "declaration-of-competing-interests.docx") `
    -Title "Declaration of Competing Interest" `
    -Paragraphs @(
        "Title of manuscript: Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study",
        "Target journal: Results in Engineering",
        "The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.",
        "Authors:",
        "- Julio Leite Azancort Neto (Universidade Federal do Pará, Brazil)",
        "- Carlos André de Mattos Teixeira (Universidade Federal do Pará, Brazil)",
        "- André Carlos Ponce de Leon Ferreira de Carvalho (University of São Paulo, Brazil)",
        "- Carlos Renato Lisboa Francês (Universidade Federal do Pará, Brazil)"
    )

# 3. CRediT Author Statement
Create-Docx -BaseDocx $base -OutDocx (Join-Path (Get-Location) "credit-author-statement.docx") `
    -Title "CRediT Authorship Statement" `
    -Paragraphs @(
        "Manuscript: Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study",
        "Julio Leite Azancort Neto: Conceptualization, Methodology, Software, Investigation, Writing - original draft, Visualization.",
        "Carlos André de Mattos Teixeira: Writing - review & editing, Validation.",
        "André Carlos Ponce de Leon Ferreira de Carvalho: Supervision, Writing - review & editing.",
        "Carlos Renato Lisboa Francês: Supervision, Writing - review & editing, Funding acquisition."
    )

# 4. Updated Cover Letter for Results in Engineering
Create-Docx -BaseDocx $base -OutDocx (Join-Path (Get-Location) "cover-letter-rineng.docx") `
    -Title "Cover Letter" `
    -Paragraphs @(
        "Dear Editor-in-Chief and Scientific Handling Editors,",
        "We are pleased to submit our manuscript entitled ""Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study"" for consideration as a Research Paper in Results in Engineering, following a transfer recommendation from Engineering Applications of Artificial Intelligence (Ms. Ref. EAAI-26-22493).",
        "Recursive fine-tuning on synthetic data is increasingly adopted in production pipelines, yet the conditions under which it preserves or degrades factual knowledge remain poorly characterized. Our study provides the first systematic dose-response analysis of recursive degradation under parameter-efficient fine-tuning (LoRA/QLoRA), spanning three backbone architectures, ten recursive generations, and multiple independent seeds per condition.",
        "The key contribution is the identification of effective training pressure as an organizing principle: we demonstrate that recursive degradation is a pressure-gated phenomenon exhibiting a sharp regime transition from homeostatic retention to progressive knowledge loss. The transition threshold differs by an order of magnitude across architectures, is jointly determined by adapter rank and learning rate, and can be controlled through modest reductions in synthetic exposure. These findings provide actionable configuration guidelines for practitioners and systems engineers deploying recursive training pipelines.",
        "We believe this work aligns well with the scope of Results in Engineering, which emphasizes sound, rigorous, and reproducible computational, AI, and systems engineering research.",
        "This manuscript has not been published elsewhere and is not under consideration by another journal. All authors have approved the manuscript and agree with its submission.",
        "Sincerely,",
        "Julio Leite Azancort Neto (corresponding author)",
        "On behalf of all co-authors: Carlos André de Mattos Teixeira, André Carlos Ponce de Leon Ferreira de Carvalho, Carlos Renato Lisboa Francês",
        "Contact: julio.azancort.neto@itec.ufpa.br"
    )
