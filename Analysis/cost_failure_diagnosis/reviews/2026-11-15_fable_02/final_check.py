"""Verify preserved research and corrected documentation after REVIEW-005."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
prior = json.loads((OUT / 'protected_before.json').read_text())
changed = [name for name, digest in prior.items()
           if not (ROOT / name).is_file()
           or hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest]
amended = 'Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01/REPORT.md'
assert changed == [amended], changed
assert hashlib.sha256((OUT / 'prior_review_report.md.txt').read_bytes()).hexdigest() == prior[amended]
whitespace = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
assert whitespace.returncode == 0, whitespace.stdout + whitespace.stderr
docs = [ROOT / 'README.md', *sorted((ROOT / 'docs').rglob('*.md')),
        ROOT / amended, OUT / 'REPORT.md']
missing = []
for p in docs:
    raw = p.read_bytes()
    contents = raw.decode('utf-16' if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig')
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', contents):
        if '://' in target or target.startswith(('#', 'mailto:')):
            continue
        target = unquote(target.split('#')[0]).strip('<>')
        dest = (p.parent / target).resolve()
        if not dest.exists() and dest != OUT / 'final_checks.json':
            missing.append((p.relative_to(ROOT).as_posix(), target))
assert not missing, missing
result = dict(protected_files=len(prior), unchanged_files=len(prior)-1,
              intentional_document_amendments=changed, original_report_archive_hash_matches=True,
              historical_numerical_results_unchanged=True, markdown_files_checked=len(docs),
              missing_local_links=missing, git_diff_check='passed')
with (OUT / 'final_checks.json').open('x', encoding='utf-8') as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
