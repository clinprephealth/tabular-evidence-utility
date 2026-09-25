# JBI Research Paper — cover letter

**To:** Editors, *Journal of Biomedical Informatics*
**From:** Michael P. Ryder, DO (independent researcher; michaelryder.do@gmail.com)
**Re:** Research Paper submission — *Minimum Evidence, Maximum Utility? Measuring Data-Minimization Cost and Evidence-Acquisition Value for Tabular AI Across Four Domains*
**Date:** [fill on send]

Dear Editors,

Please consider this original research paper for *Journal of Biomedical Informatics*. It treats two complementary measurement problems that biomedical informatics actually faces when tabular models consume clinical or operational records: how much evidence can be removed before predictive utility changes, and which missing evidence class would most change the current inference. Both are answered with a shared, fixed evaluation environment, three producers (logistic regression, histogram gradient boosting, and a frozen tabular foundation-model probe), and pre-registered verdict rules.

The motivating clinical task is acute utilization on synthetic records, with a pre-registered replication in miniature on the open MIMIC-IV demo. Two further public tasks (machine failure; purchase intent) and a regulatory location-precision task test whether the same measurement protocol travels. The findings that matter for informatics method are: the cost of a governed minimization step is producer- and task-dependent, including opposite signs on the same clinical ladder; a frozen probe can rank withheld evidence classes by the change revealing them actually produces, well above a pre-set usefulness bar; and in both studies a single-split result was revised by split replication, which we report as part of the method rather than replacing.

A preprint will be on arXiv (cs.LG) at [arXiv:XXXX.XXXXX, fill after announcement] with a content-addressed reproducibility package at https://github.com/clinprephealth/tabular-evidence-utility and an archival DOI [Zenodo, fill after the GitHub Release is archived]. Elsevier’s sharing policy treats that preprint as not prior publication. Nothing in the manuscript is a clinical decision rule, a privacy proof, or a claim about a commercial system.

I am the sole author. There are no competing interests. Suggested article type: **Research Paper**.

Sincerely,
Michael P. Ryder, DO
Independent researcher
michaelryder.do@gmail.com
