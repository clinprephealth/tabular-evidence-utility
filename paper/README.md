# Minimum Evidence, Maximum Utility? — paper sources (preprint draft, 2026-09-25)

main.tex / main.pdf          the paper (pdflatex; packages: mathptmx, booktabs, multirow, natbib, hyperref, microtype)
tab_means.tex, tab_deltas.tex, tab_acq.tex, tab_sens.tex, tab_mimic.tex
                             tables generated from the frozen v1 JSON in data/ by an inline script (each file ends with \bottomrule; every cell re-verified by the audit pass)
make_paper_figs.py           regenerates figs/fig1..fig6 from data/ (matplotlib)
data/                        read-only copies of the frozen v1 result files the tables and figures are built from
figs/                        fig1_frontier_4dom, fig2_forest_7groups, fig3_acquisition, fig4_sensitivity, fig5_tasks, fig6_calibration

Build:  python3 make_paper_figs.py && pdflatex main.tex && pdflatex main.tex

QA record (2026-09-25): 286 numeric claims checked against data/*.json by an independent audit pass; 7 prose statements
corrected (probe leads at 10/11 cells not "every"; aggressive step costs 11/12 cells not "every"; 15 field-removal cells not 12;
"eight points" -> "nearly eight (0.874 to 0.797)"; base-rate source; split-identity wording; labelled producer order).
Forbidden-vocabulary scan against CLAIMS_BOUNDARY.md: clean.

Revision 2026-09-25 (later): Section 5 "Replication in miniature on real de-identified records" added from
data/ci_study_mimic.v0.json and data/acquisition_ci_mimic.v0.json (MIMIC-IV demo run on the Mac, plan frozen at b99531cf);
abstract, Discussion, Limitations (determinism status: 39/39 cells reproduced on re-execution; cross-version HistGB caveat),
Reproducibility and bibliography updated. 13 pages, 0 overfull, 0 undefined.
