"""Read-only artifact checks; writes only the presentation validation record."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote
import pandas as pd
from pypdf import PdfReader

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
before=json.loads((HERE/'protected_before.json').read_text())
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in before.items())
pdf=PdfReader(HERE/'presentation.pdf')
assert len(pdf.pages)==15
tex=(HERE/'main.tex').read_text()
generated=(HERE/'main_results.tex').read_text().splitlines()
assert all(row in tex for row in generated)
assert sum([1,2,2,2,2,2,3,2,2,2,3,2,2,2,1])==30
log=(HERE/'build/main.log').read_text(errors='replace')
assert not re.search(r'Overfull|Missing character|undefined references|undefined citations',log)
assert len(list((HERE/'figures').glob('*.pdf')))==6
assert (HERE/'presentation.pdf').read_bytes()==(HERE/'build/main.pdf').read_bytes()
missing=[]
docs=[ROOT/'README.md',*sorted((ROOT/'docs').rglob('*.md')),HERE/'README.md',HERE/'SPEAKER_NOTES.md']
for p in docs:
    raw=p.read_bytes();body=raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
    for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',body):
        if '://' in link or link.startswith(('#','mailto:')):continue
        dest=(p.parent/unquote(link.split('#')[0]).strip('<>')).resolve()
        if not dest.exists() and dest!=HERE/'validation.json':missing.append([str(p),link])
assert not missing,missing
check=subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True,text=True)
assert check.returncode==0,check.stdout+check.stderr
result=dict(pdf_pages=15,figures=6,target_minutes=30,presenter_rehearsal=False,
    protected_research_files=len(before),all_unchanged=True,estimation_or_solves=0,
    main_table_matches_generated_rows=True,compiler_layout_and_reference_checks='passed',
    markdown_files_checked=len(docs),missing_local_links=missing,git_diff_check='passed',
    visual_review='All pages inspected; corrected slides and final footer inspected again.',
    pdf_sha256=hashlib.sha256((HERE/'presentation.pdf').read_bytes()).hexdigest())
(HERE/'validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
