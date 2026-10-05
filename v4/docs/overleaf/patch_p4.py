# -*- coding: utf-8 -*-
"""Patch P4 na carta response-to-reviewers.tex."""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = r"G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\docs\overleaf\response-to-reviewers.tex"
with open(path, encoding="utf-8") as f:
    content = f.read()

original = content
changes = []

# ─── P4-1: R1.Q4 L390-392 — remover "any reduction raises ~5pp" ─────────
OLD_Q4 = r"""  \item At Gen~5, any reduction raises retention by approximately
    $5$\,pp: $+5.0$\,pp (10\%, $p=0.002$), $+5.3$\,pp (25\%, $p=0.014$),
    $+5.7$\,pp (50\%, $p=0.002$), $n=5$ seeds each."""
NEW_Q4 = r"""  \item At Gen~5, the gains are $+5.0$\,pp (10\%, $p=0.002$),
    $+5.3$\,pp (25\%, $p=0.014$), and $+5.7$\,pp (50\%, $p=0.002$),
    $n=5$ seeds each; the Gen~5 benefit is smaller and less differentiated
    by dose than the Gen~10 benefit."""
if OLD_Q4 in content:
    content = content.replace(OLD_Q4, NEW_Q4, 1)
    changes.append("[OK] P4-1: R1.Q4 'any reduction raises ~5pp' corrigido")
else:
    changes.append("[FAIL] P4-1: R1.Q4 nao encontrado")

# ─── P4-2: R1.Q4 — adicionar G2/Gemma3 como segundo backbone ─────────────
OLD_Q4_MECH = r"""\textbf{Mechanism and generalization.}
The mechanism through which exposure reduction acts was not established.
Two candidate explanations are plausible: a reduction in the per-generation
update budget (fewer gradient steps) and a change in data composition (lower
fraction of potentially corrupted synthetic responses). A steps-matched
control (G2b, $n=3$) was inconclusive. The effect was tested on a single
backbone (Qwen) and configuration ($r=256$, Gen~10 horizon); whether it
generalises to other ranks, other backbones, or different datasets is
explicitly listed as a limitation in Section~6 (ll.~2204--2214). The
original reviewer question about Gemma~3 is therefore not yet resolved for
the dose--response setting; the Gemma~3 analysis in the original submission
used the discredited pipeline and is not reported in the revised version."""
NEW_Q4_MECH = r"""\textbf{Cross-backbone replication and mechanism.}
The pre-registered dose--response has since been replicated on a second
backbone: Gemma~3~1B~IT at $r=10$ (G2, three paired seeds, four dose
levels, $K_{0,\mathrm{G2}}=44$ items). The results, reported in
Section~4.5, show that a 50\% reduction raises Gen~10 retention by
$\GtwoDeltatenFifty$\,pp (95\,\% CI $[\GtwoCItenLoFifty, \GtwoCItenHiFifty]$,
$p=\GtwoPtenFifty$), confirming that the dose--response extends to a
second backbone operating at higher pressure.
The mechanism was not established. Two candidate explanations remain
plausible: a reduction in the per-generation update budget (fewer gradient
steps) and a change in data composition. A steps-matched control was
inconclusive at $n=3$. We do not conclude that the update-budget
explanation is correct; the confirmed result is that 50\% dose reduction
arrests progressive loss on both tested backbones, and that this effect is
dose-graded."""
if OLD_Q4_MECH in content:
    content = content.replace(OLD_Q4_MECH, NEW_Q4_MECH, 1)
    changes.append("[OK] P4-2: R1.Q4 mecanismo atualizado; G2 Gemma3 adicionado")
else:
    changes.append("[FAIL] P4-2: R1.Q4 mecanismo nao encontrado verbatim")

# ─── P4-3: R1.Q5 — K0=46 → distinguir K0_G2=44 e K0_rank=46 ─────────────
OLD_Q5_K0 = r"  $K_0$ sets ($|K_0|=78$ for Qwen, $|K_0|=46$ for Gemma~3);"
NEW_Q5_K0 = r"  $K_0$ sets ($|K_0|=78$ for Qwen; $|K_{0,\mathrm{rank}}|=46$ for the Gemma~3 rank-sweep experiments and $|K_{0,\mathrm{G2}}|=44$ for the dose-response experiment G2; see Section~3.6 of the revised manuscript);"
if OLD_Q5_K0 in content:
    content = content.replace(OLD_Q5_K0, NEW_Q5_K0, 1)
    changes.append("[OK] P4-3: R1.Q5 K0=46 -> distinção K0_G2=44 e K0_rank=46")
else:
    changes.append("[FAIL] P4-3: R1.Q5 K0=46 nao encontrado")

# ─── P4-4: R1.Q5 — item 7 "per-item predictions" — qualificar o que está depositado ──
OLD_Q5_ITEM7 = r"  \item per-generation, item-level predictions and correctness labels; and
  \item scripts used to regenerate every table and figure."
NEW_Q5_ITEM7 = r"  \item \rev{per-generation, item-level correctness vectors (boolean arrays of length $|K_0|$ per seed per generation) are included in the CSV; raw token-level predictions are not deposited in the current release but are available from the authors upon request}; and
  \item scripts used to regenerate every table and figure."
if OLD_Q5_ITEM7 in content:
    content = content.replace(OLD_Q5_ITEM7, NEW_Q5_ITEM7, 1)
    changes.append("[OK] P4-4: R1.Q5 item 7 qualificado (CSV boolean vs raw predictions)")
else:
    # Tentar sem \n explícito
    import re
    m = re.search(r"per-generation, item-level predictions.*?scripts used to regenerate every table and figure\.", content, re.DOTALL)
    if m:
        changes.append(f"[FOUND] P4-4: trecho existe ({m.start()}-{m.end()}), substituição manual necessária")
    else:
        changes.append("[FAIL] P4-4: item 7 nao encontrado")

# ─── P4-5: R1.Q5 — "raw experimental results" → precisar conteúdo ────────
OLD_Q5_RAW = r"""The replication package — source code, configurations,
raw experimental results, analysis scripts, and all publication figures — is
permanently archived at
\url{https://doi.org/10.5281/zenodo.23145362} (DOI: \texttt{10.5281/zenodo.23145362})
and mirrored at
\url{https://github.com/Jazancort/llm-knowledge-collapse-replication} (release \texttt{v1.0.2}).
Running \texttt{python scripts/make\_all.py} from the package root reproduces all
112 canonical numbers used in the manuscript (15/15 consistency checks pass).
An artifact manifest with SHA-256 hashes for every file is provided in
\texttt{MANIFEST.md}.}"""
NEW_Q5_RAW = r"""\rev{The replication package contains: (1) all analysis and figure-generation
scripts; (2) the consolidated results CSV with per-generation, per-seed retention
values for all 23 runs (G1--G5); (3) all 11 publication figures at 300\,dpi; and
(4) the pre-registration commit for B7 (\texttt{a916ebf}).
The package does \emph{not} contain per-item token-level predictions, adapter
checkpoints (available upon request; ${\sim}70$\,MB per run in bf16), or
base-model weights (obtained from their original distributors).
The package is archived at
\url{https://doi.org/10.5281/zenodo.23145362}
(note: DOI v1.0.2 predates the P1--P3 manuscript corrections; a new release
will be deposited after the final manuscript is frozen).
Running \texttt{python scripts/make\_all.py} reproduces all 112 canonical numbers
(15/15 consistency checks pass). An artifact manifest with SHA-256 hashes is
provided in \texttt{MANIFEST.md}.}}"""
if OLD_Q5_RAW in content:
    content = content.replace(OLD_Q5_RAW, NEW_Q5_RAW, 1)
    changes.append("[OK] P4-5: R1.Q5 raw experimental results -> conteúdo preciso + nota DOI")
else:
    changes.append("[FAIL] P4-5: R1.Q5 raw block nao encontrado verbatim")

# ─── Salvar ──────────────────────────────────────────────────────────────
if content != original:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    n_ok  = sum(1 for c in changes if "[OK]" in c)
    n_fail = sum(1 for c in changes if "[FAIL]" in c)
    print(f"SALVO — {n_ok} ok, {n_fail} falhas")
else:
    print("NENHUMA MUDANÇA")

print()
for c in changes:
    print(f"  {c}")
