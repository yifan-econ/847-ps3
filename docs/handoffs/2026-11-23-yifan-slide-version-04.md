# 2026-11-23: Yifan / Claude — presentation version 4

- Work IDs: DELIV-001.
- Human/account and agent: Yifan / Claude (Fable 5.2, Claude Code desktop).
- Branch and base commit: `main`, at `8fa02bd` (Wenhan's commit adding his LaTeX source), level with `origin/main`.
- Sharing state: Yifan committed the first build of `revision_04/` as `6c4d5ec` ("Version 4"), and `main` was level with the local `origin/main` reference afterwards. The title page, the files it changed in `revision_04/`, and all `docs/` and root README changes of this round were uncommitted when this file was written.
- Starting state: clean working tree.

## Scope and changes

Wenhan uploaded his part of the talk as `Presentation/2026-11-23/Version-Wenhan/PS3_Wenhan_8slides.tex` and `.pdf`. Yifan asked for version 4: Wenhan's eight slides kept intact, then Yifan's slides 8–13 of revision 03 as slides 9–14, and no backup slides. After seeing the first build, Yifan asked for revision 03's title page to be added, with nothing else changed.

Added, all under `Presentation/2026-11-23/revision_04/`: `main.tex`, `presentation.pdf`, `figures/` (the two figures slides 12 and 13 use, copied from revision 03), `SPEAKER_NOTES.md`, `README.md`, `render_previews.py`, `check_deck.py`, `previews/`, `validation.json`, `.gitignore`.

`main.tex` is revision 03's title page, then Wenhan's preamble and frames, character for character, then Yifan's six frames. The title page is not counted, so the printed slide numbers stay 1–8 and 9–14; the PDF has 15 pages. Two macros the six frames need are added to the preamble. Before slide 9 the title size, title layout and footer are switched; see the [version README](../../Presentation/2026-11-23/revision_04/README.md).

`Version-Wenhan/` and `revision_03/` are not modified. No number changed, and no estimation or price solve ran.

## Evidence

See the [validation record](../validation/2026-11-23-slide-version-04.md).

## Research interpretation

None changed. The two halves of the deck come from different runs: Wenhan's from his v1–v3 outputs (8,508 store-weeks, price in dollars, other-store price as the second instrument), Yifan's from the v5 run (7,996 store-weeks, price in dollars and log price, other-zone price). The slides do not reconcile them. The [speaker notes](../../Presentation/2026-11-23/revision_04/SPEAKER_NOTES.md) list what to say at the handover.

## Open work and next action

- Slide 9's formula writes f(p) and slide 10 shows log-price columns, and nothing on slides 1–8 defines either. Revision 03 defined f(p) on its slide 6, which is not in this deck. Yifan decides whether to add the definition to slide 9 or say it aloud.
- Nobody has rehearsed this version. The talk is today.
- Committing and pushing the title-page build and the records are Yifan's decisions.

## Documentation updates

Updated [STATUS](../STATUS.md), [WORKPLAN](../WORKPLAN.md), the root README pointer, both indexes and the changelog.
