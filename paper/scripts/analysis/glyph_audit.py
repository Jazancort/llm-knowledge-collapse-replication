#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Glyph audit: compare extracted PDF text against LaTeX source.

Usage:
    python glyph_audit.py manuscript.pdf [report.txt]

Checks for corrupt glyphs introduced by PDF re-distillation:
    - Suspect Unicode characters from custom-encoded subsets
    - Minus signs rendered as other characters (e.g., '*')
    - Multiplication signs rendered incorrectly
    - Set membership symbols garbled
"""
import re
import subprocess
import sys
from pathlib import Path

# Characters that appear when custom font encoding is not preserved
SUSPECT_CHARS = "\u00ed\u0130\xcb\u02c6\u02dc\u2299\xf9\u011f"

# Patterns that indicate numeric corruption
MINUS_AS_STAR  = re.compile(r"\*\d")           # "*0.15" instead of "-0.15"
MINUS_AS_DOT   = re.compile(r"\.\d{2,}pp")     # ".15pp" instead of "-0.15pp"
TIMES_GARBLED  = re.compile(r"5[^0-9.x-]10")  # "5I10" instead of "5x10"
SET_GARBLED    = re.compile(r"r E \\d")        # "r E 4" instead of r in {4,...}


def extract_text(pdf_path: str) -> str:
    """Extract text from PDF using pdftotext."""
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        # Try without -layout flag
        result = subprocess.run(
            ["pdftotext", pdf_path, "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
    return result.stdout


def audit(pdf_path: str, report_path: str) -> int:
    """Run glyph audit and write report. Returns number of issues found."""
    pdf = Path(pdf_path)
    if not pdf.exists():
        print(f"ERROR: PDF not found: {pdf_path}")
        return -1

    print(f"Extracting text from {pdf.name}...", end=" ", flush=True)
    text = extract_text(pdf_path)
    print(f"{len(text)} characters extracted.")

    hits = []
    for i, line in enumerate(text.split("\n"), 1):
        issues = []
        # Check for suspect Unicode characters
        bad_chars = [c for c in line if c in SUSPECT_CHARS]
        if bad_chars:
            issues.append(f"suspect chars: {sorted(set(bad_chars))}")
        # Check for numeric corruption patterns
        if MINUS_AS_STAR.search(line):
            issues.append("minus-as-star")
        if MINUS_AS_DOT.search(line):
            issues.append("minus-as-dot")
        if TIMES_GARBLED.search(line):
            issues.append("multiplication-garbled")
        if SET_GARBLED.search(line):
            issues.append("set-notation-garbled")
        if issues:
            hits.append((i, issues, line.strip()[:120]))

    # Write report
    Path(report_path).parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"Glyph audit report\n")
        f.write(f"PDF: {pdf_path}\n")
        f.write(f"Suspect characters: {SUSPECT_CHARS!r}\n")
        f.write(f"Total lines extracted: {len(text.split(chr(10)))}\n")
        f.write(f"Issues found: {len(hits)}\n\n")
        if not hits:
            f.write("PASS --- no suspect glyph or numeric corruption found.\n")
        else:
            f.write("FAIL --- issues by line:\n\n")
            for ln, issues, snippet in hits:
                f.write(f"  L{ln:5d}  {issues}\n")
                f.write(f"         {snippet}\n\n")
    print(f"Report written to {report_path}")
    return len(hits)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    pdf = sys.argv[1]
    report = sys.argv[2] if len(sys.argv) > 2 else "audit/glyph_audit_report.txt"
    n = audit(pdf, report)
    if n < 0:
        sys.exit(2)
    print("PASS" if n == 0 else f"FAIL ({n} issue lines)")
    sys.exit(0 if n == 0 else 1)
