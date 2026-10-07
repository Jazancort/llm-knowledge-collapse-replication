Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

# Unicode characters definition via ConvertFromUtf32
$bullet = [char]::ConvertFromUtf32(0x2022)
$endash = [char]::ConvertFromUtf32(0x2013)
$e_acute = [char]::ConvertFromUtf32(0x00E9)   # é
$e_circ  = [char]::ConvertFromUtf32(0x00EA)   # ê
$a_acute = [char]::ConvertFromUtf32(0x00E1)   # á
$a_tilde = [char]::ConvertFromUtf32(0x00E3)   # ã
$i_acute = [char]::ConvertFromUtf32(0x00ED)   # í
$o_circ  = [char]::ConvertFromUtf32(0x00F4)   # ô
$c_cedil = [char]::ConvertFromUtf32(0x00E7)   # ç

function XmlEscape([string]$s) {
    if ([string]::IsNullOrEmpty($s)) { return "" }
    return $s.Replace("&", "&amp;").Replace("<", "&lt;").Replace(">", "&gt;").Replace('"', "&quot;").Replace("'", "&apos;")
}

function H1([string]$text) {
    $t = XmlEscape $text
    return "<w:p><w:pPr><w:jc w:val=""left""/><w:spacing w:before=""240"" w:after=""160""/></w:pPr><w:r><w:rPr><w:rFonts w:ascii=""Times New Roman"" w:hAnsi=""Times New Roman""/><w:b/><w:color w:val=""000000""/><w:sz w:val=""32""/></w:rPr><w:t xml:space=""preserve"">$t</w:t></w:r></w:p>"
}

function H2([string]$text) {
    $t = XmlEscape $text
    return "<w:p><w:pPr><w:jc w:val=""left""/><w:spacing w:before=""200"" w:after=""120""/></w:pPr><w:r><w:rPr><w:rFonts w:ascii=""Times New Roman"" w:hAnsi=""Times New Roman""/><w:b/><w:color w:val=""000000""/><w:sz w:val=""26""/></w:rPr><w:t xml:space=""preserve"">$t</w:t></w:r></w:p>"
}

function P([string]$text, [switch]$bold, [switch]$italic) {
    $t = XmlEscape $text
    $rPr = "<w:rFonts w:ascii=""Times New Roman"" w:hAnsi=""Times New Roman""/><w:color w:val=""000000""/><w:sz w:val=""24""/>"
    if ($bold) { $rPr += "<w:b/>" }
    if ($italic) { $rPr += "<w:i/>" }
    return "<w:p><w:pPr><w:spacing w:after=""140""/></w:pPr><w:r><w:rPr>$rPr</w:rPr><w:t xml:space=""preserve"">$t</w:t></w:r></w:p>"
}

function Bullet([string]$text) {
    $t = XmlEscape $text
    $b = XmlEscape "$bullet "
    return "<w:p><w:pPr><w:ind w:left=""720"" w:hanging=""360""/><w:spacing w:after=""140""/></w:pPr><w:r><w:rPr><w:rFonts w:ascii=""Times New Roman"" w:hAnsi=""Times New Roman""/><w:color w:val=""000000""/><w:sz w:val=""24""/></w:rPr><w:t xml:space=""preserve"">$b</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii=""Times New Roman"" w:hAnsi=""Times New Roman""/><w:color w:val=""000000""/><w:sz w:val=""24""/></w:rPr><w:t xml:space=""preserve"">$t</w:t></w:r></w:p>"
}

function Build-Docx {
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

    # Write pure UTF-8 bytes without BOM
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($fullXml)
    [System.IO.File]::WriteAllBytes($docXmlPath, $utf8Bytes)

    $outFullPath = (Resolve-Path $OutDocx -ErrorAction SilentlyContinue)
    if ($null -eq $outFullPath) {
        $outFullPath = [System.IO.Path]::GetFullPath($OutDocx)
    } else {
        $outFullPath = $outFullPath.Path
    }

    if ([System.IO.File]::Exists($outFullPath)) {
        [System.IO.File]::Delete($outFullPath)
    }

    $zipArchive = [System.IO.Compression.ZipFile]::Open($outFullPath, [System.IO.Compression.ZipArchiveMode]::Create)
    Get-ChildItem -Path $tempDir -Recurse -File | ForEach-Object {
        $relPath = $_.FullName.Substring($tempDir.Length + 1).Replace('\', '/')
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zipArchive, $_.FullName, $relPath) | Out-Null
    }
    $zipArchive.Dispose()

    [System.IO.Directory]::Delete($tempDir, $true)
    Write-Host "Created successfully: $outFullPath"
}

$base = (Resolve-Path "title-page.docx").Path

# Names with verified unicode characters
$ufpa = "Universidade Federal do Par$a_acute (UFPA), Bel$e_acute" + "m, PA, Brazil"
$carlos_teixeira = "Carlos Andr$e_acute de Mattos Teixeira"
$andre_carvalho  = "Andr$e_acute Carlos Ponce de Leon Ferreira de Carvalho"
$usp = "Institute of Mathematics and Computer Sciences (ICMC), University of S$a_tilde" + "o Paulo (USP), S$a_tilde" + "o Carlos, SP, Brazil"
$carlos_frances  = "Carlos Renato Lisboa Franc$e_circ" + "s"

# ==============================================================================
# 1. HIGHLIGHTS (Exactly 5 items, max 85 chars, black title, clean bullet)
# ==============================================================================
$hlXml = H1 "Highlights"
$hlXml += P "Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study" -bold
$hlXml += Bullet "Recursive degradation exhibits a sharp pressure-dependent transition"
$hlXml += Bullet "Pressure thresholds differ by an order of magnitude across backbones"
$hlXml += Bullet "Adapter rank and learning rate interact to determine the operating regime"
$hlXml += Bullet "Output drift accompanies degradative regimes beyond factual retention loss"
$hlXml += Bullet "Reducing synthetic exposure by 5% restores near-homeostatic behavior on Qwen"

Build-Docx -BaseDocx $base -OutDocx "highlights.docx" -BodyXmlContent $hlXml

# ==============================================================================
# 2. DECLARATION OF COMPETING INTERESTS (Black title, clean text)
# ==============================================================================
$decXml = H1 "Declaration of Competing Interest"
$decXml += P "Manuscript Title: Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study" -bold
$decXml += P "Target Journal: Results in Engineering"
$decXml += P "The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper."
$decXml += H2 "Authors:"
$decXml += Bullet "Julio Leite Azancort Neto ($ufpa)"
$decXml += Bullet "$carlos_teixeira ($ufpa)"
$decXml += Bullet "$andre_carvalho ($usp)"
$decXml += Bullet "$carlos_frances ($ufpa)"

Build-Docx -BaseDocx $base -OutDocx "declaration-of-competing-interests.docx" -BodyXmlContent $decXml

# ==============================================================================
# 3. CREDIT AUTHORSHIP STATEMENT (Black title, clean text)
# ==============================================================================
$crXml = H1 "CRediT Authorship Statement"
$crXml += P "Manuscript Title: Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study" -bold
$crXml += P "Julio Leite Azancort Neto: Conceptualization, Methodology, Software, Investigation, Writing $endash original draft, Visualization."
$crXml += P "$carlos_teixeira`: Writing $endash review & editing, Validation."
$crXml += P "$andre_carvalho`: Supervision, Writing $endash review & editing."
$crXml += P "$carlos_frances`: Supervision, Writing $endash review & editing, Funding acquisition."

Build-Docx -BaseDocx $base -OutDocx "credit-author-statement.docx" -BodyXmlContent $crXml

# ==============================================================================
# 4. TITLE PAGE (Editable version - Black title, clean text, all details)
# ==============================================================================
$tpXml = H1 "Title Page"
$tpXml += P "Effective Training Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis Dose-Response Study" -bold

$tpXml += H2 "Authors and Affiliations"
$tpXml += P "1. Julio Leite Azancort Neto *" -bold
$tpXml += P "Affiliation: $ufpa"
$tpXml += P "ORCID: 0000-0003-2866-5445"

$tpXml += P "2. $carlos_teixeira" -bold
$tpXml += P "Affiliation: $ufpa"
$tpXml += P "ORCID: 0000-0003-1902-4347"

$tpXml += P "3. $andre_carvalho" -bold
$tpXml += P "Affiliation: $usp"
$tpXml += P "ORCID: 0000-0002-1907-5913"

$tpXml += P "4. $carlos_frances" -bold
$tpXml += P "Affiliation: $ufpa"
$tpXml += P "ORCID: 0000-0003-0305-7662"

$tpXml += P "* Corresponding Author: Julio Leite Azancort Neto (Email: julio.azancort.neto@itec.ufpa.br)" -italic

$tpXml += H2 "CRediT Author Statement"
$tpXml += P "Julio Leite Azancort Neto: Conceptualization, Methodology, Software, Investigation, Writing $endash original draft, Visualization."
$tpXml += P "$carlos_teixeira`: Writing $endash review & editing, Validation."
$tpXml += P "$andre_carvalho`: Supervision, Writing $endash review & editing."
$tpXml += P "$carlos_frances`: Supervision, Writing $endash review & editing, Funding acquisition."

$tpXml += H2 "Acknowledgments"
$ack = "The authors acknowledge the High-Performance Computing and Artificial Intelligence Center (CCAD/UFPA, www.ccad.ufpa.br) for institutional support. This work was supported in part by the Coordena$c_cedil$a_tilde" + "o de Aperfei$c_cedil" + "oamento de Pessoal de N$i_acute" + "vel Superior (CAPES), Brazil, under Grant 001; and in part by the National Institute of Science and Technology in Artificial Intelligence Applied to Smart and Sustainable Cities in Brazilian Amazon (INCT IAmaz$o_circ" + "nia, inctiamazonia.org.br) funded by the Brazilian National Council for Scientific and Technological Development (CNPq) under Grant 409001/2024-4."
$tpXml += P $ack

Build-Docx -BaseDocx $base -OutDocx "title-page.docx" -BodyXmlContent $tpXml
