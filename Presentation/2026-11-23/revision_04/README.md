# Presentation, version 4

Built November 23, 2026, the day of the talk. [PDF](presentation.pdf), [source](main.tex), [speaker notes for slides 9–14](SPEAKER_NOTES.md), preview sheets in `previews/`.

Fourteen slides, no backups:

- **Slides 1–8, Wenhan.** The preamble and the eight frames of [his file](../Version-Wenhan/PS3_Wenhan_8slides.tex), character for character.
- **Slides 9–14, Yifan.** Slides 8–13 of [revision 03](../revision_03/main.tex), unchanged, with the two figures they use.

`Version-Wenhan/` and `revision_03/` are not modified.

## What differs between the two halves

- Yifan's slides keep their sentence titles at the smaller title size and their original title position. At Wenhan's title size and position the merger slide overflowed by 21pt.
- The footer text "ECON 847 PS3" is on Wenhan's slides only. Yifan's slides show the slide number alone, as in revision 03.
- Text and bullet colours on slides 9–14 are Wenhan's navy and blue.
- There is no title slide; the deck opens on Wenhan's Overview.

The two halves come from different runs. The differences an audience can see (log price, sample size, the second instrument's name, two reused symbols) are listed in the [speaker notes](SPEAKER_NOTES.md).

## Rebuild

In this folder, with the local TeX setup named in AGENTS.md:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

Copy `build/main.pdf` to `presentation.pdf`, then from the repository root, with `pdftoppm` and `pdfinfo` on PATH:

```sh
uv run --locked --offline --with matplotlib==3.10.8 python Presentation/2026-11-23/revision_04/render_previews.py
uv run --locked --offline --with matplotlib==3.10.8 python Presentation/2026-11-23/revision_04/check_deck.py
```

`check_deck.py` confirms that both sets of frames are in `main.tex` unchanged, compares the rendered pages with Wenhan's PDF and with revision 03, and writes [validation.json](validation.json).
