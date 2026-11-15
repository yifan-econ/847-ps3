# 2026-11-15: Yifan / Codex — Fable cost-review reconciliation

- Work ID: REVIEW-004; continuation of DIAG-001 interpretation and reporting.
- User supplied Fable's review and asked us to consider it. Human/account: Yifan / Codex.
- Branch `codex/review-004-cost-feedback`; base `d5fcf7c9b0c9cc44cdf382f634904e2082618669`. Fetched origin and verified no newer main commit.
- Preserved pre-existing uncommitted diagnosis files and current-document changes from codex/diag-001-cost-failures. No work was reset or overwritten to create the branch.
- Sharing: v5 source commit is on main/origin. Diagnosis plus this review remain local/uncommitted/unpushed. Fable reports reading the local files and making no changes; no transfer was needed in his session.

## Scope and paths

Added `Analysis/cost_failure_diagnosis/src/review_feedback.py` and the isolated `reviews/2026-11-15_fable_01/` directory. It contains supplied feedback, code snapshots, joint cost classifications and both orders, retailer identity checks, promotion-related cost and IV cross-product tables, single-roll elasticities, weekly/market purchase volumes and scope-specific Scott cost checks. A small supplementary script reconciles the broader-v1 weekly counts and post-event summary definitions.

Updated current WORKPLAN/STATUS, root README, changelog, handoff/validation indexes and this round's records. Historical diagnosis scripts, report and results remain byte-identical. No new demand specification, reduced-sample refit, ownership change or equilibrium was run. The four existing IV coefficients were reconstructed algebraically to check the feedback, not presented as new estimates.

## What changed in the assessment

Fable's main numbers reproduce. Retire the exclusive interpretation of “retailer wedge only” and “portfolio first crosses”: at linear/AAC rho zero, 61.41% of negative-cost package volume already has singleton markup above AAC; 38.59% requires the portfolio increment to cross AAC at fixed observed inputs. Show the five joint inequalities and both accounting orders. The direct nesting markup comparison remains valid.

Make the observed-AAC/percentage-markup diagnostic prominent (18.85% negative volume, versus 37.22% for observed-AAC/dollar markup), alongside the calibrated percentage cost (22.37%). The percentage manufacturer/effective sign match is an identity. The mean-q identity in Fable's wording is exact with package weights for linear price; log price requires inverse-slope/revenue weights.

Clarify that the log-price improvement exists on the full input (39.06%→1.70% negative manufacturer-cost volume); selection only removes the remaining 1.70% on the common sample. Discount-related moment contributions reproduce, but their complement ratios are not new demand estimates. Lower absolute beta would worsen costs at fixed other objects, without proving that every demand adjustment must fail.

Rolls/trip, unflagged discounts and chain-wide Scott spikes reproduce. Fable's 76/78 store counts use the broader v1 panel, whereas v5 keys have 73/75. The modal-discount measure is a price proxy, not a verified promotion label. Physical rolls/trip can exceed one even with one multipack purchase and must not be used as choice shares. No stockpiling/recoupment share is identified.

Historical reporting claim superseded by [REVIEW-005](2026-11-15-yifan-numerical-selection.md): the accepted-sample zero in the two log/rho-zero percentage scenarios is not independent cost evidence. Numerical acceptance equals effective-cost nonnegativity in all four log/rho-zero scenarios, and percentage cost signs agree by identity. Report full-input failure magnitudes and selection dependence; retain the qualification against a general rejection of static pricing.

## Evidence and next action

Both verification scripts passed; the primary took 7.38 seconds. Maximum discrepancy in reconstruction of the four existing coefficients is 8.18e-14. All 333 pre-existing research files, including both prior runs, are unchanged. See [validation](../validation/2026-11-15-cost-feedback.md) and [review report](../../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01/REPORT.md).

Final review passed Git whitespace checks, local links across 40 Markdown files, reconciliation of every joint-classification total to the prior diagnosis, both accounting-order totals, and the full-input versus accepted-sample Scott claim. A final hash check again found all 333 protected files unchanged. [Final evidence](../../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01/final_checks.json).

The finite post-processing tables recommended by Fable are now complete. Do not launch additional estimation or prolong the same descriptive tail audit merely to repeat these facts. The next proposed deliverable is consolidated conditional reporting/presentation claims with explicit sample/cost/identification limits. This does not mark all research limitations solved or choose a preferred causal model. New modeling remains a separately scoped decision.
