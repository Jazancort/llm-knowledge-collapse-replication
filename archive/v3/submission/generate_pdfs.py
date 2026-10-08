"""Generate cover letter and title page as professional PDFs using fpdf2."""
from fpdf import FPDF
from pathlib import Path

out = Path(__file__).parent


class CleanPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
        self.set_margins(25, 25, 25)

    def body_text(self, text, bold=False, italic=False):
        style = ""
        if bold:
            style += "B"
        if italic:
            style += "I"
        self.set_font("Times", style, 12)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def heading(self, text, level=1):
        sizes = {1: 16, 2: 13}
        self.set_font("Times", "B", sizes.get(level, 12))
        self.multi_cell(0, 8, text)
        self.ln(4)


# ============================================================
# COVER LETTER
# ============================================================
pdf = CleanPDF()
pdf.add_page()

pdf.body_text("Dear Editor-in-Chief,")
pdf.ln(2)

pdf.body_text(
    'We are pleased to submit our manuscript entitled "Effective Training '
    "Pressure Gates Recursive Knowledge Degradation in LLMs: A Multi-Axis "
    'Dose-Response Study" for consideration as a Research Paper in '
    "Engineering Applications of Artificial Intelligence."
)

pdf.body_text(
    "Recursive fine-tuning on synthetic data is increasingly adopted in "
    "production pipelines, yet the conditions under which it preserves or "
    "degrades factual knowledge remain poorly characterized. Our study "
    "provides the first systematic dose-response analysis of recursive "
    "degradation under parameter-efficient fine-tuning (LoRA/QLoRA), spanning "
    "three backbone architectures, ten recursive generations, and multiple "
    "independent seeds per condition."
)

pdf.body_text(
    "The key contribution is the identification of effective training pressure "
    "as an organizing principle: we demonstrate that recursive degradation is "
    "a pressure-gated phenomenon exhibiting a sharp regime transition from "
    "homeostatic retention to progressive knowledge loss. The transition "
    "threshold differs by an order of magnitude across architectures, is "
    "jointly determined by adapter rank and learning rate, and can be "
    "controlled through modest reductions in synthetic exposure. These "
    "findings provide actionable configuration guidelines for practitioners "
    "deploying recursive training pipelines."
)

pdf.body_text(
    "We believe this work aligns well with the scope of EAAI, which "
    "emphasizes practical applications of AI methods across engineering "
    "domains. The paper offers both empirical characterization and directly "
    "applicable thresholds for safe recursive training configurations."
)

pdf.body_text(
    "This manuscript has not been published elsewhere and is not under "
    "consideration by another journal. All authors have approved the "
    "manuscript and agree with its submission."
)

pdf.ln(8)
pdf.body_text("Sincerely,")
pdf.ln(2)
pdf.body_text("Julio Leite Azancort Neto (corresponding author)", bold=True)
pdf.body_text(
    "On behalf of all co-authors:\n"
    "Carlos Andre de Mattos Teixeira, Andre Carlos Ponce de Leon Ferreira "
    "de Carvalho, Carlos Renato Lisboa Frances"
)
pdf.ln(2)
pdf.body_text("Contact: julio.azancort.neto@itec.ufpa.br")

pdf.output(str(out / "cover-letter.pdf"))
print(f"Cover letter saved: {out / 'cover-letter.pdf'}")


# ============================================================
# TITLE PAGE
# ============================================================
pdf = CleanPDF()
pdf.add_page()

pdf.heading("Title Page", level=1)
pdf.ln(2)

pdf.set_font("Times", "B", 12)
pdf.cell(0, 6, "Title:", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Times", "", 12)
pdf.multi_cell(
    0, 6,
    "Effective Training Pressure Gates Recursive Knowledge Degradation "
    "in LLMs: A Multi-Axis Dose-Response Study"
)
pdf.ln(6)

pdf.heading("Authors", level=2)

authors = [
    ("1", "Julio Leite Azancort Neto *",
     "Universidade Federal do Para (UFPA), Belem, PA, Brazil",
     "0000-0003-2866-5445"),
    ("2", "Carlos Andre de Mattos Teixeira",
     "Universidade Federal do Para (UFPA), Belem, PA, Brazil",
     ""),
    ("3", "Andre Carlos Ponce de Leon Ferreira de Carvalho",
     "ICMC, University of Sao Paulo (USP), Sao Carlos, SP, Brazil",
     ""),
    ("4", "Carlos Renato Lisboa Frances",
     "Universidade Federal do Para (UFPA), Belem, PA, Brazil",
     ""),
]

for num, name, aff, orcid in authors:
    pdf.set_font("Times", "B", 11)
    pdf.cell(0, 6, f"{num}. {name}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Times", "", 10)
    pdf.cell(0, 5, f"   Affiliation: {aff}", new_x="LMARGIN", new_y="NEXT")
    if orcid:
        pdf.cell(0, 5, f"   ORCID: {orcid}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

pdf.set_font("Times", "I", 10)
pdf.cell(0, 5, "* Corresponding author", new_x="LMARGIN", new_y="NEXT")
pdf.ln(8)

pdf.heading("Corresponding Author", level=2)
pdf.body_text("Julio Leite Azancort Neto")
pdf.body_text("Email: julio.azancort.neto@itec.ufpa.br")
pdf.body_text("Universidade Federal do Para (UFPA), Belem, PA, Brazil")
pdf.ln(4)

pdf.heading("CRediT Author Statement", level=2)
credits = [
    ("Julio Leite Azancort Neto:",
     "Conceptualization, Methodology, Software, Investigation, "
     "Writing - Original Draft, Visualization"),
    ("Carlos Andre de Mattos Teixeira:",
     "Writing - Review & Editing, Validation"),
    ("Andre Carlos Ponce de Leon Ferreira de Carvalho:",
     "Supervision, Writing - Review & Editing"),
    ("Carlos Renato Lisboa Frances:",
     "Supervision, Writing - Review & Editing, Funding acquisition"),
]

for name, roles in credits:
    pdf.set_font("Times", "B", 11)
    pdf.cell(0, 6, name, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Times", "", 11)
    pdf.multi_cell(0, 5, f"  {roles}")
    pdf.ln(2)

pdf.ln(4)
pdf.heading("Acknowledgments", level=2)
pdf.body_text(
    "The authors acknowledge the High-Performance Computing and Artificial "
    "Intelligence Center (CCAD/UFPA, www.ccad.ufpa.br) for institutional "
    "support. This work was supported in part by the Coordenacao de "
    "Aperfeicoamento de Pessoal de Nivel Superior (CAPES), Brazil, under "
    "Grant 001; and in part by the National Institute of Science and "
    "Technology in Artificial Intelligence Applied to Smart and Sustainable "
    "Cities in Brazilian Amazon (INCT IAmazonia, inctiamazonia.org.br) funded "
    "by the Brazilian National Council for Scientific and Technological "
    "Development (CNPq) under Grant 409001/2024-4."
)

pdf.output(str(out / "title-page.pdf"))
print(f"Title page saved: {out / 'title-page.pdf'}")
