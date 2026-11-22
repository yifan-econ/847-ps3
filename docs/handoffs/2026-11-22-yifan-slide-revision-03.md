# 2026-11-22: Yifan / Claude — presentation revision 03

- Work IDs: DELIV-001.
- Human/account and agent: Yifan / Claude (Fable 5.2, Claude Code desktop).
- Branch and base commit: `codex/deliv-001-beamer`, at `df42368` (the delivery commit; its parent is `d5fcf7c`).
- Sharing state: included in the local commit that adds this file; not pushed.
- Starting state: clean working tree. `Presentation/2026-11-23/revision_03/` existed and was empty.

## Scope and changes

Yifan supplied slide revision notes written the same day and asked for a new deck in `revision_03`, with no number changed, no new estimation, and preview images of the final PDF. The notes are copied to [revision_03/SLIDE_REVISION_NOTES.md](../../Presentation/2026-11-23/revision_03/SLIDE_REVISION_NOTES.md).

Added, all under `Presentation/2026-11-23/revision_03/`: `main.tex`, `presentation.pdf`, `SPEAKER_NOTES.md`, `README.md`, `prepare_tables.py`, `build_figures.py`, `render_previews.py`, `check_deck.py`, `tables/`, `figures/`, `previews/`, `validation.json`, `preservation.json`, `protected_before.json`, `.gitignore`.

The deck has thirteen main slides and five backups. Wenhan presents slides 1–7, Yifan 8–13. The notes' thirteen content issues and the wording table are implemented. See the [revision README](../../Presentation/2026-11-23/revision_03/README.md) for the list.

Where the deck departs from the notes:

- Slide 9 shows one table with both price forms. The log-price own elasticities are the saved medians (−5.38 to −5.64), not "−5.4 throughout".
- Slide 6's caption is cut to one line; the usual-price definition of a discount moved into the bullet.
- Slide 11's chart labels its lines directly; a legend box covered a line.
- Slide 2's last bullet and slide 13's last bullet are new wording, written to match the notes' conclusion.
- Slide 5's "Dropped" line is taken from the code: positive-sales records, weeks with seven days of traffic counts, and store-weeks where every product has both instruments.
- Slides 8 and 10 use the lecture's symbols: ρ = 1 − λ and Ω ⊙ D.
- Backup B2 says "more likely, fewer shoppers bought several rolls each". That is a reading of the totals; units per buyer are not observed.

## Evidence

Commands and results are in the [validation record](../validation/2026-11-22-slide-revision-03.md). No estimation and no price solve ran. All 369 research files are byte-identical; revision 02 and the first draft are unchanged.

## Research interpretation

The conclusion slide now treats non-negative implied cost as a check a model must pass, following the course lecture. The log-price model passes for 93% to 98% of packages; the dollar-price model fails for most Scott single rolls. The talk therefore reports the log-price range first.

This replaces the earlier recorded position that cost signs should not be used to prefer a price form. Two facts from the closed diagnosis still hold and belong in the answers to questions: the log-price elasticities lean on discount weeks, and both models are static.

## Open work and next action

- Wenhan has not yet agreed to the speaking split or to the new conclusion.
- No timed rehearsal of this version has taken place. The talk is on November 23.
- Pushing the branch is Yifan's decision.

## Documentation updates

Updated [STATUS](../STATUS.md), [WORKPLAN](../WORKPLAN.md), the root README pointer, both indexes and the changelog.
