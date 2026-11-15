# Current project status

Updated 2026-11-15. [Wenhan's Chinese baseline](handoffs/2026-11-14-wenhan-baseline_zh.md) records the detailed research history. See [WORKPLAN.md](WORKPLAN.md) for ownership and next tasks, and [the latest handoff](handoffs/2026-11-15-yifan-portability.md) for this engineering round.

## Engineering state

- Python 3.13.9 and Wenhan's recorded NumPy/pandas/SciPy/PyBLP versions are installed through uv; the shared lockfile is present.
- The mixed-logit runner uses cross-platform FileLock. Windows imports, lock contention/release, and cached execution passed six tests.
- Preparation validation defaults to read-only. All four preparation combinations match the existing sample audit.
- One saved PyBLP result loaded and reproduced a 32-product market's shares at saved parameters. No estimation ran; all 194 files in the preservation check remained unchanged.
- Native macOS runtime confirmation is pending. Check GitHub Actions for the Windows/macOS CI results; they are separate from the recorded local validation.
- Delivery branch is main. The [round handoff](handoffs/2026-11-15-yifan-portability.md) includes a receiving-agent checklist and instructions to identify the implementation commit.

Evidence: [Windows validation](validation/2026-11-15-windows-portability.md).

## Completed work

| Stage | Scope | Read first |
|---|---|---|
| v1 | Cleaning, simple logit OLS/IV, packaging and zero-sales diagnostics | [Original README](../Archive/ps3_v1/README.md) |
| v2 | 14 cost-instrument specifications | [Report](../Analysis/cost_iv_v2/REPORT_zh.md) |
| v3 | 12 AAC/other-pricing-zone IV comparisons | [Literature and results](../Analysis/paper_iv_v3/LITERATURE_AND_RESULTS_zh.md) |
| v4 | Eight demographic mixed-logit specifications attempted; six converged, two rejected | [Report](../Analysis/mixed_logit_v4/REPORT_zh.md) |

Markets are store-weeks and products are UPCs. Prices and sales are per package; market size is store customer traffic. All-pack and multipack samples are separate definitions. v4 uses 1991–1992 and estimates household-size and income heterogeneity separately.

## Unresolved work

- Zero sales are excluded from positive-share estimation; actual availability and selection bias remain unresolved.
- External PPI instruments performed poorly. AAC and other-zone prices remain candidates with unresolved exclusion restrictions.
- Five of six converged v4 specifications reject the reported joint model/instrument restrictions at 5%; non-rejection for the remaining specification does not validate it. See [validation results](../Analysis/mixed_logit_v4/results/independent_validation.csv).
- Both multipack household-size fits were rejected. Income integration needs further checking; the 31-point exercise did not re-estimate the models.
- Historical manufacturer ownership, supply-side pricing, marginal costs, merger simulation, and welfare calculations remain unfinished.

Prioritize reproducibility and sample/identification review before model expansion. No final specification has been selected for merger simulation.

## Dependencies and workflow

The archived v1 cleaned panel supplies v2, v3, and v4. v3 imports v2 estimation functions; v4 uses v2 functions and v3 cross-zone instruments. These directories must remain together.

See [SETUP.md](SETUP.md) for uv instructions and safe checks. Read CSV/JSON outputs first; saved PyBLP objects depend on the software environment.

## Organization changes

The 2026-11-14 organization preserved the old guide, status note, and greeting README in [history/](history/README.md). On 2026-11-15, current status moved here and dated handoffs moved into handoffs/. Old documentation paths remain as redirects. See [CHANGELOG.md](CHANGELOG.md). Analysis/data paths and baseline results are preserved; the lock and preparation-validator code changed in this round.
