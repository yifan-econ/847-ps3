# 2026-11-23: Presentation version 4

Work ID: DELIV-001.
Platform: Windows 11, x64.
Python and dependency lock: Python 3.13.9, existing `uv.lock`, unchanged. Matplotlib 3.10.8 (for Pillow) supplied with `--with` from the local cache.
Branch / commit: `main`, started at `8fa02bd`; the first build is commit `6c4d5ec`, and the title-page build and records are uncommitted additions listed in the [handoff](../handoffs/2026-11-23-yifan-slide-version-04.md).

## Checks

| Command or check | Outcome | Evidence |
|---|---|---|
| `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex` through the TeX Live alias | Exit 0; 15 pages; no overfull or underfull boxes, missing characters or undefined references | `revision_04/build/main.log` (not tracked) |
| `uv run --locked --offline --with matplotlib==3.10.8 python Presentation/2026-11-23/revision_04/render_previews.py` | 15 page images and 3 contact sheets from the final PDF | `revision_04/previews/` |
| Visual inspection of all 15 rendered pages | No clipped text or overlaps introduced by the merge | `revision_04/previews/` |
| `uv run --locked --offline --with matplotlib==3.10.8 python Presentation/2026-11-23/revision_04/check_deck.py` | Passed; details below | `revision_04/validation.json` |

What `check_deck.py` establishes:

- The title page is revision 03's frame with one added option that keeps it out of the slide count. Rendered, 0.008% of its pixels differ from revision 03's page 1.
- Wenhan's preamble and his eight frames are in `main.tex` character for character.
- Yifan's frames 8–13 of revision 03 follow, unchanged apart from the numbers in the comment rules. Nothing comes after them: no appendix and no backup frames.
- The two figures are byte-identical to revision 03's.
- Slides 1–8 (PDF pages 2–9), rendered at 100 dpi and compared with Wenhan's PDF: at most 0.021% of pixels differ on any page.
- Slides 9–14 (PDF pages 10–15), compared with pages 8–13 of revision 03 above the footer: 0.04% to 0.07% of pixels differ, with no shift of the content. Text on these slides is now Wenhan's navy, slightly darker than revision 03's colour, which moves a few edge pixels across the ink threshold.
- The delivered PDF equals the build, and `git status` shows changes only under `revision_04/`, `docs/` and the root README.

The checks above are from the final build, with the title page. The first build of the day, without it, passed the same checks at 14 pages.

## A layout tried and dropped

With Wenhan's title size and title layout applied to slides 9–14, the merger slide overflowed by 21pt. Those six slides therefore keep revision 03's title size and layout.

## Limits and follow-up

- Wenhan's numbers were not rechecked against his saved outputs. The numbers on slides 9–14 were checked in [revision 03](2026-11-22-slide-revision-03.md) and the frames are unchanged.
- Wenhan's slide 4 has an axis label that touches the first date label, and on his slides 5 and 6 the last text line sits just above the footer. Both are in his own PDF and were left alone.
- Slides were inspected as rendered images on this machine, not on the classroom projector.
- No human has rehearsed or timed this version.
- No Mac build was attempted.
