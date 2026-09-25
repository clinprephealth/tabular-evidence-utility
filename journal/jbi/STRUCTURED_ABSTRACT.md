# JBI structured abstract (Objective / Methods / Results / Conclusion)

Target: ≤300 words. Paste into Editorial Manager. Do not add product names.

**Objective.** To measure, rather than assume, the predictive cost of data minimization and the value of acquiring withheld evidence for tabular models, using a shared evaluation protocol that can be re-executed from content-addressed artifacts.

**Methods.** Three producers (logistic regression, histogram gradient boosting, and a frozen TabICL v2 probe, checkpoint pinned by SHA-256) were evaluated on a three-rung evidence ladder. Study 1 reports split-replicated paired ΔAUROC with 95% *t*-intervals on four tasks: synthetic clinical utilization (K=20), AI4I machine failure (K=10), UCI Online Shoppers purchase intent (K=10), and Cal-FF facility permit status with a location-precision ladder (K=10). Study 2 asks the frozen probe to rank withheld evidence classes by the change revealing them produces, validated by reveal. A pre-registered miniature of both studies was run on the MIMIC-IV Clinical Database Demo (242 rows, 90 patients, K=20). Verdict rules were fixed before the runs.

**Results.** The governed minimization step improved clinical logistic regression (+0.024 [+0.006, +0.042]), cost HistGB (−0.028 [−0.047, −0.010]), and left the probe unchanged (+0.005 [−0.010, +0.020]); on the regulatory location-precision ladder the same step cost the probe (−0.016 [−0.027, −0.006]). Aggressive minimization cost eleven of twelve producer–task cells. Study 2 ranking accuracy on 20 clinical splits was 0.797 [0.780, 0.813], versus 0.874 on the original single split; manufacturing and consumer tasks scored 0.821 (46% of cases excluded as indistinguishable) and 0.915/0.900. The MIMIC miniature reproduced producer-dependence of the governed step and acquisition (0.828 [0.802, 0.854]) but not a uniform aggressive cost: the linear model improved.

**Conclusion.** Minimization cost and acquisition value are measurable, producer- and task-dependent quantities. They are not constants, privacy proofs, or causal importance scores. The protocol, frozen result files, and claims boundary are released with the code.
