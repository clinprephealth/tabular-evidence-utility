# Claims boundary — tabular paper only (public)

Use this sheet when drafting the preprint, the JBI manuscript, or any talk.
If a sentence is not allowed here, do not say it. Representation-invariance
and federation results are out of scope for this package.

## Allowed

- Data minimization in tabular AI should be characterised per model and task, not assumed to impose either no cost or a fixed cost.
- In the healthcare task, governed P1 minimization improved logistic regression slightly, produced no measured cost for the foundation-model probe, and reduced HistGB performance (replicated 95% CIs).
- More aggressive minimization (P2) generally cost utility; healthcare logistic P2−P1 is the sole interval that touches zero among the twelve producer–task cells on the field-removal axis.
- On replicated means, the frozen tabular foundation-model probe led ten of eleven task–level cells, with modest, task-dependent margins; simple baselines remain close enough that measuring remains mandatory.
- Replicated over 20 healthcare splits, ranking accuracy is 0.797 [0.780, 0.813]; 20 of 20 splits clear the usefulness bar. The 0.874 figure is one pre-registered split and must be labelled as such.
- The acquisition result is value under the frozen predictive capability, not causal importance, and not a decision rule. Its magnitude rises with the number of donor imputations (0.789–0.906 on the v1 split), which must be reported alongside any headline.
- On Cal-FF (location precision, K=10 by facility), governed P1 (exact coordinates → county) cost utility for the probe (−0.016 [−0.027, −0.006]) and HistGB (−0.015 [−0.025, −0.005]) and showed no measured cost for logistic (+0.004 [−0.000, +0.008]).
- On manufacturing (AI4I), ranking accuracy 0.821 on 1,608 evaluable rows with 46% excluded as indistinguishable; on consumer (UCI shoppers) 0.915 at P0 and 0.900 at P1 with 11–13% excluded.
- The MIMIC-IV demo miniature (242 rows, 90 patients) reproduced producer-dependence of the governed step and the acquisition result (0.828 [0.802, 0.854]) and did not reproduce a uniform aggressive cost.

## Not supported — do not say

- Privacy is free, or minimization has a fixed cost.
- The foundation-model probe is generally better than simple models.
- The v1 single-split ranking (logistic ahead of the probe in healthcare) is the finding.
- Google TabFM was evaluated (weights were never downloaded). The instrument is TabICL v2.
- Results generalise beyond the tested tasks, producers, and ladders.
- Acquisition ranking establishes causal feature importance or a data-collection policy.
- Formal differential-privacy, HIPAA, or regulatory-compliance guarantees.
- The Cal-FF 1,000 m label equals the source paper’s unpermitted-facility count.
- Any commercial product, kernel, or platform is the contribution.

Public environment sentence, if needed:

> Analyses were run in a fixed provenance-preserving evaluation environment that held representations, splits, and producer identity constant across evidence levels.
