# arXiv upload — tabular paper

**Title.** Minimum Evidence, Maximum Utility? Measuring Data-Minimization Cost and Evidence-Acquisition Value for Tabular AI Across Four Domains

**Authors.** Michael P. Ryder, DO (Independent researcher) <michaelryder.do@gmail.com>

**Primary category.** cs.LG
**Cross-lists.** stat.ML, cs.AI

**License on arXiv.** Submitter's choice. Recommended: Creative Commons Attribution (CC BY 4.0). arXiv also offers CC BY-SA, CC BY-NC-SA, CC BY-NC-ND, CC0, and its own perpetual non-exclusive license; the selected license is irrevocable. Not required by arXiv — pick it because it matches the repo.

**Comments line.** 13 pages, 6 figures. Code and frozen result files: [GitHub URL]. Archival DOI: [Zenodo, after first release].

**Abstract.** Paste the abstract from `paper/main.tex` (the `\begin{abstract}` block). arXiv metadata abstracts should be plain text, no LaTeX except `\'` etc. Replace `$\Delta\mathrm{AUROC}$` with "delta AUROC".

## Upload

Upload `arxiv-source.tar.gz` (this directory after `assemble`). Do **not** upload the compiled `main.pdf` as the source. arXiv builds from TeX.

Compiler: PDFLaTeX / tectonic-equivalent. Top-level file: `main.tex`.

If endorsement is requested for cs.LG, ask a colleague who has submitted there recently. Independent-researcher submissions are accepted; they are sometimes slower.

## After announcement

1. Put the arXiv id in `CITATION.cff` and in the JBI cover letter.
2. Enable the GitHub repo in Zenodo **before** tagging `v0.1.1`. The existing `v0.1.0` release will not be archived after the fact. Put the version-specific DOI in a preprint replacement.
3. Then submit to JBI (`../journal/jbi/`).
