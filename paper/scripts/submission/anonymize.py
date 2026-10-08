"""
Anonymize the CAS-DC template for EAAI blind review submission.
Removes: authors, affiliations, cortext, ead, credit, shortauthors,
acknowledgments section, and GitHub URL with username.
"""
import re
from pathlib import Path

src = Path(__file__).parent.parent / "cas-dc-template.tex"
dst = Path(__file__).parent / "manuscript-anonymous.tex"

text = src.read_text(encoding="utf-8")

# Remove \shortauthors line
text = re.sub(r'\\shortauthors\{.*?\}\n', '', text)

# Remove all \author blocks (including multi-line options)
text = re.sub(r'\\author\[.*?\]\{.*?\}\[[\s\S]*?\]\n', '', text)
text = re.sub(r'\\author\[.*?\]\{.*?\}\n', '', text)

# Remove \cormark, \ead, \credit lines
text = re.sub(r'\\cormark\[.*?\]\n', '', text)
text = re.sub(r'\\ead\{.*?\}\n', '', text)
text = re.sub(r'\\credit\{[\s\S]*?\}\n', '', text)

# Remove \affiliation blocks
text = re.sub(r'\\affiliation\[.*?\]\{[\s\S]*?\}\n', '', text)

# Remove \cortext
text = re.sub(r'\\cortext\[.*?\]\{.*?\}\n', '', text)

# Remove \printcredits
text = re.sub(r'\\printcredits\n', '', text)

# Remove Acknowledgments section (from \section*{Acknowledgments} to next \section or \bibliographystyle)
text = re.sub(
    r'% =+\n% CREDIT\n% =+\n',
    '',
    text
)
text = re.sub(
    r'% =+\n% ACKNOWLEDGMENTS\n% =+\n\\section\*\{Acknowledgments\}[\s\S]*?(?=% =+\n% REFERENCES)',
    '',
    text
)

# Anonymize GitHub URL (contains username)
text = re.sub(
    r'\\href\{https://github\.com/Jazancort/llm-knowledge-collapse-experiments\}\{github\.com/Jazancort/llm-knowledge-collapse-experiments\}',
    r'\\textit{[Repository URL removed for blind review]}',
    text
)

# Also handle the appendix text mentioning the repo
text = re.sub(
    r'All source code, configuration files, and experimental outputs developed for\nthis paper are publicly available at\n.*?\.\nThese resources ensure full reproducibility.*?results\.',
    'All source code, configuration files, and experimental outputs are publicly\navailable in a repository that will be disclosed upon acceptance. These\nresources ensure full reproducibility of the experimental protocol.',
    text
)

dst.write_text(text, encoding="utf-8")
print(f"Anonymized manuscript saved to: {dst}")
print(f"Now compile with: pdflatex manuscript-anonymous.tex (run twice for refs)")
