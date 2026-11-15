"""Check and render the revised presentation; no estimation or simulation."""
from pathlib import Path
import hashlib,json,re,subprocess
from urllib.parse import unquote
import pandas as pd
from pypdf import PdfReader
import pypdfium2 as pdfium
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
before=json.loads((HERE/'protected_before.json').read_text())
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in before.items())
old=json.loads((HERE.parent/'validation.json').read_text())
assert hashlib.sha256((HERE.parent/'presentation.pdf').read_bytes()).hexdigest()==old['pdf_sha256']
pdf=PdfReader(HERE/'presentation.pdf');assert len(pdf.pages)==18
assert not pdf.is_encrypted
assert (HERE/'build/main.pdf').read_bytes()==(HERE/'presentation.pdf').read_bytes()
tex=(HERE/'main.tex').read_text();log=(HERE/'build/main.log').read_text(errors='replace')
assert not re.search(r'Overfull|Missing character|undefined references|undefined citations',log)
est=pd.read_csv(HERE/'demand_estimates.csv')
for z in est.itertuples():
    assert f'${z.beta_price:.3f}$ & {z.se_price:.3f}'.replace(' & 0.',' & .') in tex
    assert f'${z.median_own_elasticity:.3f}$' in tex
pack=pd.read_csv(HERE/'pack_size_detail.csv')
for z in pack.itertuples():
    assert f'${z.linear_aac:.2f}$ & ${z.log_aac:.2f}$' in tex
timing=[.5,1.5,1.5,1.5,1,1.5,2,2,2.5,2,1.5,2,2.5,2,1.5]
assert sum(timing)==25.5
assert pd.Timestamp('1989-09-14')+pd.Timedelta(days=109*7)==pd.Timestamp('1991-10-17')
out=HERE/'rendered';out.mkdir(exist_ok=True)
preview=HERE/'previews';preview.mkdir(exist_ok=True)
doc=pdfium.PdfDocument(str(HERE/'presentation.pdf'))
pages=[p.render(scale=2).to_pil().convert('RGB') for p in doc]
for i,im in enumerate(pages):im.save(out/f'slide_{i+1:02}.png')
for start in range(0,len(pages),6):
    sheet=Image.new('RGB',(1600,1350),'#dddddd')
    for i,im in enumerate(pages[start:start+6]):sheet.paste(ImageOps.contain(im,(800,430)),(i%2*800,i//2*450))
    sheet.save(preview/f'slides_{start+1:02}_{start+6:02}.png')
missing=[];docs=[ROOT/'README.md',*sorted((ROOT/'docs').rglob('*.md')),HERE/'README.md',HERE/'SPEAKER_NOTES.md']
for p in docs:
    raw=p.read_bytes();body=raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
    for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',body):
        if '://' in link or link.startswith(('#','mailto:')):continue
        dest=(p.parent/unquote(link.split('#')[0]).strip('<>')).resolve()
        if not dest.exists() and dest!=HERE/'validation.json':missing.append([str(p),link])
assert not missing,missing
check=subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True,text=True);assert check.returncode==0,check.stdout+check.stderr
result=dict(pdf_pages=18,main_slides=15,backup_slides=3,target_minutes=sum(timing),presenter_rehearsal=False,
    protected_research_files=len(before),all_unchanged=True,first_draft_pdf_unchanged=True,
    pdf_encrypted=False,estimation_or_solves=0,demand_and_pack_tables_checked=True,
    compiler_layout_and_reference_checks='passed',missing_local_links=missing,git_diff_check='passed',
    pdf_sha256=hashlib.sha256((HERE/'presentation.pdf').read_bytes()).hexdigest())
(HERE/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
