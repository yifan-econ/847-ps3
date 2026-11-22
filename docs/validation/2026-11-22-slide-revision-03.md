# 2026-11-22: Presentation revision 03

Work ID: DELIV-001.
Platform: Windows 11, x64.
Python and dependency lock: Python 3.13.9, existing `uv.lock`, unchanged. Matplotlib 3.10.8 supplied with `--with` from the local cache.
Branch / commit: `codex/deliv-001-beamer` at `df42368`, plus the additions listed in the [handoff](../handoffs/2026-11-22-yifan-slide-revision-03.md).

## Checks

| Command or check | Outcome | Evidence |
|---|---|---|
| `uv run --locked --offline python Presentation/2026-11-23/revision_03/prepare_tables.py` | Wrote ten table files from the saved v5 run | `revision_03/tables/` |
| `uv run --locked --offline --with matplotlib==3.10.8 python Presentation/2026-11-23/revision_03/build_figures.py` | Wrote five figures; 369 research files hashed before and after, identical | `revision_03/figures/`, `preservation.json` |
| `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex` through the TeX Live alias | Exit 0; 18 pages; no overfull or underfull boxes, missing characters or undefined references | `revision_03/build/main.log` (not tracked) |
| `uv run --locked --offline --with matplotlib==3.10.8 python Presentation/2026-11-23/revision_03/render_previews.py` | 18 slide images and 3 contact sheets from the final PDF | `revision_03/previews/` |
| Visual inspection of all 18 rendered slides | No clipped text, overlaps or unreadable labels after four layout fixes | `revision_03/previews/` |
| `uv run --locked --offline python Presentation/2026-11-23/revision_03/check_deck.py` | Passed: every number on the slides matches `tables/`; 13 main and 5 backup slides; delivered PDF equals the build | `revision_03/validation.json` |
| Notes' figures against saved results | 1/\|β\| = \$0.49; log-price markup 19%; non-negative cost for 92.5% to 98.3% of packages under log price; pack size is 92% of price variance, stores 0.2%; first-stage F equals the saved Wald statistic | `tables/cost_check.csv`, `tables/price_variation.json`, `tables/first_stage.csv` |
| Lecture notation | ρ = 1 − λ and p = −(Ω ⊙ D)⁻¹s + c confirmed in the course slides | `02Demand_Lecture.pdf`, `03Supply_Lecture.pdf` (outside this repository) |

## Wording follow-up, same day

Three wording changes after Yifan's check of the deck, made on `main` at `38dec19`. No number changed.

- Slide 10: the title is now "Manufacturers price all their products; cost is wholesale price minus markup", and a line under the formula says p is the wholesale price. The longer title first tried wrapped to two lines.
- Slide 8: "We have one instrument" became "Both our instruments move the product's own price. Neither moves its share of tissue sales separately." The speaker-note answer on estimating ρ matches.
- Backup B1: "32 UPCs on sale" became "32 UPCs sold".

| Command or check | Outcome | Evidence |
|---|---|---|
| `latexmk` rebuild, same command | Exit 0; 18 pages; no layout warnings | `revision_03/build/main.log` (not tracked) |
| `render_previews.py`, same command | 18 slide images and 3 contact sheets re-rendered from the new PDF; slides 8, 10 and B1 inspected | `revision_03/previews/` |
| `check_deck.py`, same command | Passed. It now recomputes the Scott white example from the saved markups: price 0.5248, AAC 0.4783, markup 0.5821 and 1.0134, cost −0.1038 and −0.5351 | `revision_03/validation.json` |

The 369 research files are still byte-identical, and no estimation or price solve ran. `revision_02` has no differences from the commit. In the working copy, 21 of its text files now have LF line endings where they had CRLF before: Git rewrote them when the branch was checked out between the two rounds. Their content is the same.

## Preservation

No estimation and no price solve ran. `check_deck.py` re-hashed the 369 files under Analysis, Archive, Data and Paper: unchanged. `git status` shows changes only under `Presentation/2026-11-23/revision_03/`, `docs/` and the root README. All 71 files in `revision_02`, including its untracked build and rendered folders, match SHA-256 hashes taken before work began. The first-draft PDF hash is unchanged.

## Limits and follow-up

- Slides were inspected as rendered images on this machine, not on the classroom projector.
- No human has rehearsed or timed this version.
- The Scott white example was carried over from the earlier diagnosis report in the first build; the follow-up check above recomputes it.
- No Mac build was attempted.
