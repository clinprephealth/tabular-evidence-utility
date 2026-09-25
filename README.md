# Minimum Evidence, Maximum Utility? — reproducibility package

Preprint sources, frozen result files, and the scripts that regenerate every table and figure in:

> Ryder, M. P. *Minimum Evidence, Maximum Utility? Measuring Data-Minimization Cost and Evidence-Acquisition Value for Tabular AI Across Four Domains.* Preprint, September 2026.

Public repository: https://github.com/clinprephealth/tabular-evidence-utility

This package reproduces **every number in the paper** from committed JSON. It does not re-train models. A later extract may add a substrate-free re-run harness; that is not required to check the manuscript.

## Layout

| Path | Purpose |
|---|---|
| `paper/main.tex` / `paper/main.pdf` | The preprint |
| `paper/tab_*.tex` | Tables generated from `paper/data/` |
| `paper/figs/` | Figures 1–6 (PDF + PNG) |
| `paper/make_paper_figs.py` | Regenerates figures from `paper/data/` |
| `paper/data/` | Frozen v1/v0 result files (read-only) |
| `CLAIMS_BOUNDARY.md` | Allowed / refused public phrasing |
| `journal/jbi/` | JBI kit (cover letter, structured abstract, highlights, cut plan) |
| `arxiv/` | Source tarball and metadata for arXiv upload |

## Build the PDF

```bash
cd paper
# tectonic is enough; pdflatex also works
tectonic main.tex
```

Figures already sit in `figs/`. To regenerate them (optional; needs matplotlib):

```bash
python3 -m pip install matplotlib numpy
python3 make_paper_figs.py
```

## Licence

- Code and scripts: Apache License 2.0 (`LICENSE-APACHE`)
- Manuscript, figures, and frozen result files: CC BY 4.0 (`LICENSE-CC-BY`)

## Data you must obtain independently (only for a full re-run, not for checking the paper)

- Synthea synthetic records (no patient data)
- AI4I 2020 Predictive Maintenance (CC BY 4.0)
- UCI Online Shoppers Purchasing Intention (CC BY 4.0)
- Cal-FF (CC0-1.0)
- MIMIC-IV Clinical Database Demo and MIMIC-IV-ED Demo v2.2 (PhysioNet, ODbL 1.0)
- TabICL v2 checkpoint (BSD-3-Clause), pinned SHA-256 `bdc7dbd5…`

Google TabFM weights were never downloaded and are not part of this work.

## What this paper does not claim

See `CLAIMS_BOUNDARY.md`. Short version: no privacy proof, no causal importance, no clinical decision rule, no generalisation beyond the tested tasks, producers, and ladders.
