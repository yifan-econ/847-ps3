"""Render build/main.pdf to one PNG per slide and to contact sheets of six slides.

Run from the repository root, with pdftoppm (Poppler) on PATH:
    uv run --locked --with matplotlib==3.10.8 python Presentation/2026-11-23/revision_03/render_previews.py

Pillow comes with the plotting environment; the project lock is unchanged.
rendered/ holds single slides (ignored by git); previews/ holds the contact sheets.
"""
from pathlib import Path
import shutil
import subprocess
from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
pdf = HERE / 'build/main.pdf'
tool = shutil.which('pdftoppm')
assert tool, 'pdftoppm not found on PATH'
rendered = HERE / 'rendered'
previews = HERE / 'previews'
for folder in (rendered, previews):
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir()
subprocess.run([tool, '-r', '200', '-png', str(pdf), str(rendered / 'slide')], check=True)
pages = sorted(rendered.glob('slide-*.png'))
images = [Image.open(p).convert('RGB') for p in pages]
for start in range(0, len(images), 6):
    sheet = Image.new('RGB', (2000, 1730), '#dddddd')
    for i, im in enumerate(images[start:start + 6]):
        sheet.paste(ImageOps.contain(im, (990, 557)), (i % 2 * 1010, i // 2 * 577))
    sheet.save(previews / f'slides_{start + 1:02}_{min(start + 6, len(images)):02}.png')
print(len(images), 'slides rendered;', len(list(previews.glob('*.png'))), 'contact sheets')
