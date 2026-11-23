"""Check that version 4 is the title page, Wenhan's eight slides and Yifan's six, and nothing else.

Run from the repository root after the LaTeX build, with pdftoppm and pdfinfo (Poppler) on PATH:
    uv run --locked --offline --with matplotlib==3.10.8 python Presentation/2026-11-23/revision_04/check_deck.py

It reads the sources and PDFs of Version-Wenhan and revision_03 and writes only
revision_04/validation.json and revision_04/build/compare/. It runs no estimation.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
WENHAN = HERE.parent / 'Version-Wenhan'
REV03 = HERE.parent / 'revision_03'


def text(path):
    return path.read_text(encoding='utf-8').replace('\r\n', '\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pages(pdf):
    out = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True, check=True).stdout
    return int(re.search(r'Pages:\s+(\d+)', out).group(1))


def render(pdf, name):
    folder = HERE / 'build/compare' / name
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)
    subprocess.run(['pdftoppm', '-r', '100', '-gray', '-png', str(pdf), str(folder / 'p')], check=True)
    return [np.asarray(Image.open(p).convert('L')) < 200 for p in sorted(folder.glob('p-*.png'))]


def differing(a, b, rows):
    """Percent of pixels, in the given rows, that are ink in one image and paper in the other."""
    assert a.shape == b.shape
    return 100 * float((a[rows] != b[rows]).mean())


main = text(HERE / 'main.tex')
wenhan = text(WENHAN / 'PS3_Wenhan_8slides.tex')
rev03 = text(REV03 / 'main.tex')

# Source: Wenhan's preamble and frames are in main.tex character for character.
w_preamble, w_rest = wenhan.split('\\begin{document}\n', 1)
w_frames = w_rest.split('\\end{document}', 1)[0]
assert w_frames.count('\\begin{frame}') == 8
assert w_preamble in main and w_frames in main
assert main.index(w_preamble) < main.index(w_frames)

# Source: the title page is revision 03's, kept out of the slide count so Wenhan's slides stay 1 to 8.
t_start = rev03.index('\\begin{frame}[plain]')
title = rev03[t_start:rev03.index('\\end{frame}', t_start) + len('\\end{frame}')]
title = title.replace('[plain]', '[plain,noframenumbering]', 1)
assert main.count(title) == 1
assert main.index('\\begin{document}') < main.index(title) < main.index(w_frames)

# Source: Yifan's frames 8 to 13 of revision 03 follow, unchanged apart from the numbers in the comment rules.
rule = r'% -{64} \d+ \(Yifan\)\n'
start = rev03.index('% ' + '-' * 64 + ' 8 (Yifan)')
y_frames = re.sub(rule, '', rev03[start:rev03.index('% ' + '-' * 64 + ' Backup')]).strip()
assert y_frames.count('\\begin{frame}') == 6
after_wenhan = re.sub(rule, '', main[main.index(w_frames) + len(w_frames):])
assert y_frames in after_wenhan
assert after_wenhan.rstrip().endswith(y_frames + '\n\\end{document}')

# No backups, a title page and fourteen slides, fifteen pages, clean log, delivered PDF is the build.
assert main.count('\\begin{frame}') == 15 and '\\appendix' not in main and 'Backup' not in main
assert pages(HERE / 'build/main.pdf') == 15
log = (HERE / 'build/main.log').read_text(encoding='latin-1')
for warning in ('Overfull', 'Underfull', 'Missing character', 'undefined'):
    assert warning not in log, warning
assert sha(HERE / 'presentation.pdf') == sha(HERE / 'build/main.pdf')

# Figures are the files checked in revision 03.
for name in ('cost_failures.pdf', 'price_sensitivity.pdf'):
    assert sha(HERE / 'figures' / name) == sha(REV03 / 'figures' / name)
assert sorted(p.name for p in (HERE / 'figures').iterdir()) == ['cost_failures.pdf', 'price_sensitivity.pdf']

# Rendered pages: 1 to 8 against Wenhan's PDF, 9 to 14 against pages 8 to 13 of revision 03.
new = render(HERE / 'build/main.pdf', 'version_04')
his = render(WENHAN / 'PS3_Wenhan_8slides.pdf', 'wenhan')
old = render(REV03 / 'presentation.pdf', 'revision_03')
assert len(his) == 8 and len(old) == 18
height = new[0].shape[0]
whole = slice(0, height)
body = slice(0, int(height * 0.92))  # the footer differs on Yifan's slides: page number and its position
title_diff = round(differing(new[0], old[0], whole), 4)
wenhan_diff = [round(differing(new[1 + i], his[i], whole), 4) for i in range(8)]
yifan_diff = [round(differing(new[9 + i], old[7 + i], body), 4) for i in range(6)]
assert title_diff < 0.1, title_diff
assert max(wenhan_diff) < 0.05, wenhan_diff
# Text here is Wenhan's navy, slightly darker than revision 03's, so a few edge pixels cross the threshold.
assert max(yifan_diff) < 0.1, yifan_diff

# Nothing outside revision_04, docs and the root README changed; the two source folders are untouched.
status = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True, check=True).stdout
changed = [line[3:].strip('"') for line in status.splitlines()]
allowed = ('Presentation/2026-11-23/revision_04/', 'docs/', 'README.md')
assert all(path.startswith(allowed) for path in changed), changed

result = {
    'pages': 15,
    'title_page_verbatim': True,
    'percent_pixels_differing_from_revision_03_title_page': title_diff,
    'wenhan_frames_verbatim': True,
    'yifan_frames_verbatim': True,
    'layout_warnings': 0,
    'percent_pixels_differing_from_wenhan_pdf_pages_1_8': wenhan_diff,
    'percent_pixels_differing_from_revision_03_pages_8_13_above_footer': yifan_diff,
    'pdf_sha256': sha(HERE / 'presentation.pdf'),
    'wenhan_tex_sha256': sha(WENHAN / 'PS3_Wenhan_8slides.tex'),
    'wenhan_pdf_sha256': sha(WENHAN / 'PS3_Wenhan_8slides.pdf'),
    'revision_03_pdf_sha256': sha(REV03 / 'presentation.pdf'),
}
(HERE / 'validation.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps(result, indent=2))
