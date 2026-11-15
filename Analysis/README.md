# Analysis versions

| Directory | Purpose | Main report | Results |
|---|---|---|---|
| cost_iv_v2 | External pulp/plastic cost IV comparisons | [Report](cost_iv_v2/REPORT_zh.md) | [Estimates](cost_iv_v2/results/estimates.csv) |
| paper_iv_v3 | AAC and leave-own-pricing-zone-out price IV | [Report](paper_iv_v3/LITERATURE_AND_RESULTS_zh.md) | [Estimates](paper_iv_v3/results/estimates.csv) |
| mixed_logit_v4 | Separate household-size and income mixed logit | [Report](mixed_logit_v4/REPORT_zh.md) | [Estimates](mixed_logit_v4/results/estimates.csv) |

Within each version, src/ holds code, results/ holds outputs, and data/ holds inputs or prepared data where applicable. requirements.txt files describe dependencies.

v4 linear_attempts/ and optimizer_attempts/ preserve exploratory fits. Rejected fits and logs inside results/ also remain part of the research record. Their presence does not indicate additional accepted models or active processes.

All versions use the archived v1 cleaned panel. v3 imports v2 functions; v4 imports v2 functions and consumes v3 cross-zone instruments. See [setup](../docs/SETUP.md) before running scripts.
