# Presentation, revision 03

Built November 22, 2026 from [the slide revision notes](SLIDE_REVISION_NOTES.md). [PDF](presentation.pdf), [source](main.tex), [speaker notes](SPEAKER_NOTES.md), preview sheets in `previews/`.

Thirteen main slides (Wenhan 1–7, Yifan 8–13) and five backups. [Revision 02](../revision_02/README.md) and the [first draft](../README.md) are untouched.

## What changed from revision 02

- Nested logit has its own two slides (8 and 9).
- The supply slide shows the lecture's markup formula, says what AAC is, and defines implied cost as AAC minus markup.
- The cost slide states in one paragraph why costs turn negative with price in dollars.
- The merger slide lists what changes, what is re-solved, what is held fixed, and the algorithm.
- The conclusion uses the cost check: the log-price model passes it, so its range is the one we report first.
- "Linear" is now "price in dollars". Internal labels and defensive footnotes are gone. One caption line per slide at most.
- Figures are redrawn at slide size with readable labels. No number changed.

## Rebuild

From the repository root. The two extraction scripts refuse to overwrite `tables/` and `figures/`; delete those folders first to regenerate them.

```sh
uv run --locked python Presentation/2026-11-23/revision_03/prepare_tables.py
uv run --locked --with matplotlib==3.10.8 python Presentation/2026-11-23/revision_03/build_figures.py
```

Then, in this folder, with the local TeX setup named in AGENTS.md:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

Copy `build/main.pdf` to `presentation.pdf`, then from the repository root:

```sh
uv run --locked --with matplotlib==3.10.8 python Presentation/2026-11-23/revision_03/render_previews.py
uv run --locked python Presentation/2026-11-23/revision_03/check_deck.py
```

`render_previews.py` needs `pdftoppm` on PATH. `check_deck.py` compares every number on the slides with `tables/` and writes [validation.json](validation.json).

No estimation and no price solve ran for this revision.

## Still open

- Wenhan has not agreed to this split or to the new conclusion slide.
- Nobody has rehearsed this version with a timer.
