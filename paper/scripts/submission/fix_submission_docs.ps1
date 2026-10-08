Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Build-DocxFromTemplate {
    param(
        [string]$BaseDocx,
        [string]$OutDocx,
        [string]$BodyXmlContent
    )

    $tempDir = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), [System.Guid]::NewGuid().ToString())
    [System.IO.Directory]::CreateDirectory($tempDir) | Out-Null

    [System.IO.Compression.ZipFile]::ExtractToDirectory($BaseDocx, $tempDir)

    $docXmlPath = [System.IO.Path]::Combine($tempDir, "word", "document.xml")

    $fullXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    $BodyXmlContent
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>
"@

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($docXmlPath, $fullXml, $utf8NoBom)

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
    Write-Host "Successfully built: $OutDocx"
}

# XML Builders with strictly named parameters
function H1 {
    param([string]$text)
    return "<w:p><w:pPr><w:spacing w:before=""240"" w:after=""160""/></w:pPr><w:r><w:rPr><w:rFonts w:ascii=""Times New Roman"" w:hAnsi=""Times New Roman""/><w:b/><w:color w:val=""000000""/><w:sz w:val=""32""/></w:rPr><w:t xml:space=""preserve"">$text</w:t></w:r></w:p>"
}

function H2 {
    param([string]$text)
    return "<w:p><w:pPr><w:spacing w:before=""180"" w:after=""120""/></w:pPr><w:r><w:rPr><w:rFonts w:ascii=""Times New Roman"" w:hAnsi=""Times New Roman""/><w:b/><w:color w:val=""000000""/><w:sz w:val=""26""/></w:rPr><w:t xml:space=""preserve"">$text</w:t></w:r></w:p>"
}

function P {
    param(
        [string]$text,
        [switch]$bold,
        [switch]$italic
    )
    $rPr = "<w:rFonts w:ascii=""Times New Roman"" w:hAnsi=""Times New Roman""/><w:color w:val=""000000""/><w:sz w:val=""24""/>"
    if ($bold) { $rPr += "<w:b/>" }
    if ($italic) { $rPr += "<w:i/>" }
    return "<w:p><w:pPr><w:spacing w:after=""140""/></w:pPr><w:r><w:rPr>$rPr</w:rPr><w:t xml:space=""preserve"">$text</w:t></w:r></w:p>"
}

function Bullet {
    param([string]$text)
    # Using clean OpenXML bullet symbol &#8226; without external numbering dependencies
    return "<w:p><w:pPr><w:pStyle w:val=""ListParagraph""/><w:ind w:left=""720"" w:hanging=""360""/><w:spacing w:after=""140""/></w:pPr><w:r><w:rPr><w:rFonts w:ascii=""Times New Roman"" w:hAnsi=""Times New Roman""/><w:color w:val=""000000""/><w:sz w:val=""24""/></w:rPr><w:t>&#8226; </w:t></w:r><w:r><w:rPr><w:rFonts w:ascii=""Times New Roman"" w:hAnsi=""Times New Roman""/><w:color w:val=""000000""/><w:sz w:val=""24""/></w:rPr><w:t xml:space=""preserve"">$text</w:t></w:r></w:p>"
}

$base = (Resolve-Path "title-page.docx").Path

# ==============================================================================
# 1. HIGHLIGHTS (Exactly 5 items, max 85 chars, black title, clean bullet)
# ==============================================================================
$hlXml = H1 -text "Highlights"
$hlXml += P -text "Title: Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study" -bold
$hlXml += Bullet -text "Recursive degradation exhibits a sharp pressure-dependent transition"
$hlXml += Bullet -text "Pressure thresholds differ by an order of magnitude across backbones"
$hlXml += Bullet -text "Adapter rank and learning rate interact to determine the operating regime"
$hlXml += Bullet -text "Output drift accompanies degradative regimes beyond factual retention loss"
$hlXml += Bullet -text "A 5% reduction in synthetic exposure restores near-homeostatic behavior"

Build-DocxFromTemplate -BaseDocx $base -OutDocx (Join-Path (Get-Location) "highlights.docx") -BodyXmlContent $hlXml


# ==============================================================================
# 2. DECLARATION OF COMPETING INTERESTS (Black title, clean entities)
# ==============================================================================
$decXml = H1 -text "Declaration of Competing Interest"
$decXml += P -text "Manuscript Title: Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study" -bold
$decXml += P -text "Target Journal: Results in Engineering"
$decXml += P -text "The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper."
$decXml += H2 -text "Authors:"
$decXml += Bullet -text "Julio Leite Azancort Neto (Universidade Federal do Par&#225;, Brazil)"
$decXml += Bullet -text "Carlos Andr&#233; de Mattos Teixeira (Universidade Federal do Par&#225;, Brazil)"
$decXml += Bullet -text "Andr&#233; Carlos Ponce de Leon Ferreira de Carvalho (University of S&#227;o Paulo, Brazil)"
$decXml += Bullet -text "Carlos Renato Lisboa Franc&#234;s (Universidade Federal do Par&#225;, Brazil)"

Build-DocxFromTemplate -BaseDocx $base -OutDocx (Join-Path (Get-Location) "declaration-of-competing-interests.docx") -BodyXmlContent $decXml


# ==============================================================================
# 3. CREDIT AUTHORSHIP STATEMENT (Black title, clean entities)
# ==============================================================================
$crXml = H1 -text "CRediT Authorship Statement"
$crXml += P -text "Manuscript Title: Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study" -bold
$crXml += P -text "Julio Leite Azancort Neto: Conceptualization, Methodology, Software, Investigation, Writing &#8211; original draft, Visualization."
$crXml += P -text "Carlos Andr&#233; de Mattos Teixeira: Writing &#8211; review &amp; editing, Validation."
$crXml += P -text "Andr&#233; Carlos Ponce de Leon Ferreira de Carvalho: Supervision, Writing &#8211; review &amp; editing."
$crXml += P -text "Carlos Renato Lisboa Franc&#234;s: Supervision, Writing &#8211; review &amp; editing, Funding acquisition."

Build-DocxFromTemplate -BaseDocx $base -OutDocx (Join-Path (Get-Location) "credit-author-statement.docx") -BodyXmlContent $crXml


# ==============================================================================
# 4. TITLE PAGE (Editable version - Black title, clean entities, all details)
# ==============================================================================
$tpXml = H1 -text "Title Page"
$tpXml += P -text "Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study" -bold

$tpXml += H2 -text "Authors and Affiliations"
$tpXml += P -text "1. Julio Leite Azancort Neto *" -bold
$tpXml += P -text "Affiliation: Universidade Federal do Par&#225; (UFPA), Bel&#233;m, PA, Brazil"
$tpXml += P -text "ORCID: 0000-0003-2866-5445"

$tpXml += P -text "2. Carlos Andr&#233; de Mattos Teixeira" -bold
$tpXml += P -text "Affiliation: Universidade Federal do Par&#225; (UFPA), Bel&#233;m, PA, Brazil"
$tpXml += P -text "ORCID: 0000-0003-1902-4347"

$tpXml += P -text "3. Andr&#233; Carlos Ponce de Leon Ferreira de Carvalho" -bold
$tpXml += P -text "Affiliation: Institute of Mathematics and Computer Sciences (ICMC), University of S&#227;o Paulo (USP), S&#227;o Carlos, SP, Brazil"
$tpXml += P -text "ORCID: 0000-0002-1907-5913"

$tpXml += P -text "4. Carlos Renato Lisboa Franc&#234;s" -bold
$tpXml += P -text "Affiliation: Universidade Federal do Par&#225; (UFPA), Bel&#233;m, PA, Brazil"
$tpXml += P -text "ORCID: 0000-0003-0305-7662"

$tpXml += P -text "* Corresponding Author: Julio Leite Azancort Neto (Email: julio.azancort.neto@itec.ufpa.br)" -italic

$tpXml += H2 -text "CRediT Author Statement"
$tpXml += P -text "Julio Leite Azancort Neto: Conceptualization, Methodology, Software, Investigation, Writing &#8211; original draft, Visualization."
$tpXml += P -text "Carlos Andr&#233; de Mattos Teixeira: Writing &#8211; review &amp; editing, Validation."
$tpXml += P -text "Andr&#233; Carlos Ponce de Leon Ferreira de Carvalho: Supervision, Writing &#8211; review &amp; editing."
$tpXml += P -text "Carlos Renato Lisboa Franc&#234;s: Supervision, Writing &#8211; review &amp; editing, Funding acquisition."

$tpXml += H2 -text "Acknowledgments"
$tpXml += P -text "The authors acknowledge the High-Performance Computing and Artificial Intelligence Center (CCAD/UFPA, www.ccad.ufpa.br) for institutional support. This work was supported in part by the Coordena&#231;&#227;o de Aperfei&#231;oamento de Pessoal de N&#237;vel Superior (CAPES), Brazil, under Grant 001; and in part by the National Institute of Science and Technology in Artificial Intelligence Applied to Smart and Sustainable Cities in Brazilian Amazon (INCT IAmaz&#244;nia, inctiamazonia.org.br) funded by the Brazilian National Council for Scientific and Technological Development (CNPq) under Grant 409001/2024-4."

Build-DocxFromTemplate -BaseDocx $base -OutDocx (Join-Path (Get-Location) "title-page.docx") -BodyXmlContent $tpXml
