"""Check the revision_03 deck against the saved numbers. Fits nothing and solves nothing.

Run from the repository root after building the PDF:
    uv run --locked python Presentation/2026-11-23/revision_03/check_deck.py
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
T = HERE / 'tables'
tex = (HERE / 'main.tex').read_text(encoding='utf-8')
log = (HERE / 'build/main.log').read_text(errors='replace')


def need(text):
    assert text in tex, f'not on the slides: {text}'


# Build: page count, layout warnings, delivered copy.
pages = int(re.search(r'Output written on build/main\.pdf \((\d+) pages', log).group(1))
assert pages == 18, pages
assert not re.search(r'Overfull|Underfull|Missing character|undefined references|undefined citations', log)
assert (HERE / 'build/main.pdf').read_bytes() == (HERE / 'presentation.pdf').read_bytes()
main_frames = tex.split('\\appendix')[0].count('\\begin{frame}')
backup_frames = tex.split('\\appendix')[1].count('\\begin{frame}')
assert (main_frames, backup_frames) == (13, 5)

# Slide 5: sample.
s = json.loads((T / 'sample.json').read_text())
for text in [f"{s['store_weeks']:,}", f"{s['stores']} / {s['upcs']}", f"{s['median_products']:.0f}\\\\", f"\\${s['median_price']:.2f}",
             f"{s['single_roll_package_percent']:.1f}\\%", f"{s['median_outside_percent']:.1f}\\%", f"{s['observations']:,} observations",
             f"{s['retained_package_percent']:.0f}\\% of packages sold"]:
    need(text)
v = json.loads((T / 'price_variation.json').read_text())
need(f"{v['between_store_upc_percent']:.1f}\\%")
need(f"{v['within_store_upc_over_time_percent']:.1f}\\%")
need(f"{v['between_store_percent']:.1f}\\%")
assert v['between_pack_size_percent'] > 50  # "most of that is pack size"

# Slide 6: first stage.
for z in pd.read_csv(T / 'first_stage.csv').itertuples():
    row = f"{z.coefficient:.3f} & {z.se_two_way_cluster:.3f} & {z.first_stage_partial_r2:.3f} & {z.first_stage_F:,.0f}"
    need(row.replace('0.', '.'))

# Slide 7: plain-logit estimates and elasticities by pack size.
for z in pd.read_csv(T / 'logit_estimates.csv').itertuples():
    need(f"${z.beta_price:.3f}$ & {z.se_price:.3f}".replace('& 0.', '& .') + f" & ${z.median_own_elasticity:.3f}$")
for z in pd.read_csv(T / 'pack_size_elasticities.csv').itertuples():
    need(f"\\${z.weighted_price:.2f} & ${z.dollar_price_aac:.2f}$ & ${z.log_price_aac:.2f}$")

# Slide 9: nested logit table (AAC instrument).
n = pd.read_csv(T / 'nested_results.csv')
n = n[n.iv.eq('aac')]
for rho, g in n.groupby('rho'):
    d, l = g[g.form.eq('linear')].iloc[0], g[g.form.eq('log')].iloc[0]
    need(f"${d.beta_price:.2f}$ ({d.se_price:.2f}) & ${d.median_own_elasticity:.2f}$ & ${d.category_elasticity_median:.2f}$ & "
         f"${l.beta_price:.2f}$ ({l.se_price:.2f}) & ${l.median_own_elasticity:.2f}$ & ${l.category_elasticity_median:.2f}$ & "
         f"{100 * d.kc_to_scott_diversion:.0f}\\%")

# Slides 2, 12, 13: merger price effects and the cost check.
p = pd.read_csv(T / 'merger_price_effects.csv')
p = p[p.retailer.eq('dollar')]
log_rows, dollar_rows = p[p.cell.str.startswith('log')], p[p.cell.str.startswith('linear')]
rng = lambda x: (x.min(), x.max())
assert [round(x) for x in rng(log_rows['Kimberly-Clark'])] == [1, 11]
assert [round(x) for x in rng(dollar_rows['Kimberly-Clark'])] == [2, 24]
assert [round(x) for x in rng(p['Kimberly-Clark'])] == [1, 24]
assert [round(x, 1) for x in rng(p['all'])] == [0.2, 3.4]
assert [round(x, 1) for x in rng(log_rows['all'])] == [0.2, 1.7]
assert [round(x, 1) for x in rng(p['Scott'])] == [0.3, 4.8]
c = pd.read_csv(T / 'cost_check.csv')
assert [round(x) for x in rng(c[c.model.str.startswith('log')].nonnegative_cost_percent_all_packages)] == [93, 98]
for text in ['0.2--3.4\\%', '1--24\\%', '1--11\\%', '+1\\% to +11\\%', '+2\\% to +24\\%', '+0.3\\% to +4.8\\%', '+0.2\\% to +3.4\\%',
             '93\\% to 98\\%', '1\\% to 11\\%', '0.2\\% to 1.7\\%']:
    need(text)

# Slides 10-11: the markup arithmetic.
beta_dollar = float(n[(n.form == 'linear') & (n.rho == 0)].beta_price.iloc[0])
beta_log = float(n[(n.form == 'log') & (n.rho == 0)].beta_price.iloc[0])
assert f'{1 / abs(beta_dollar):.2f}' == '0.49' and f'{100 / abs(beta_log):.0f}' == '19'
need('1/|\\beta|=\\$0.49')
need('about 19\\%')

# Slide 11: the Scott white example, recomputed from the saved markups. Package-weighted means over
# the store-weeks that solved in every scenario, price in dollars with the AAC instrument.
import numpy as np
RUN = ROOT / 'Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01'
inputs = pd.read_csv(RUN / 'product_inputs.csv.gz')
market = pd.factorize(inputs.market_id)[0]
solved = np.logical_and.reduce([pd.read_csv(f).numerical_ok.to_numpy() for f in sorted((RUN / 'cells').glob('*/*_markets.csv.gz'))])
rows = (inputs.upc.to_numpy() == 5400041500) & solved[market]
weight = inputs.move.to_numpy(float)[rows]
price = np.average(inputs.price_pack.to_numpy()[rows], weights=weight)
aac = np.average(inputs.aac_pack.to_numpy()[rows], weights=weight)
markup = {}
for tag in ['rho00', 'rho75']:
    with np.load(RUN / 'cells' / f'linear__aac__{tag}' / 'dollar_simulation.npz') as z:
        markup[tag] = np.average(z['markup'][rows], weights=weight)
scott_white = dict(price=price, aac=aac, markup_rho0=markup['rho00'], markup_rho75=markup['rho75'],
                   cost_rho0=aac - markup['rho00'], cost_rho75=aac - markup['rho75'])
shown = dict(price=0.52, aac=0.48, markup_rho0=0.58, markup_rho75=1.01, cost_rho0=-0.10, cost_rho75=-0.54)
assert all(round(scott_white[k], 2) == v for k, v in shown.items()), scott_white
for text in ['Retail price & \\$0.52', 'Wholesale price (AAC) & \\$0.48', '$\\rho=0$ & \\$0.58', '$\\rho=0.75$ & \\$1.01', '$-\\$0.10$ to $-\\$0.54$']:
    need(text)

# Backups: retailer rule, store 124, consumer surplus.
both = pd.read_csv(T / 'merger_price_effects.csv')
for cell in ['linear__aac__rho00', 'linear__other_zone__rho00', 'log__aac__rho00', 'log__other_zone__rho00']:
    d, q = (both[both.cell.eq(cell) & both.retailer.eq(r)].iloc[0] for r in ['dollar', 'percentage'])
    need(f"{d['all']:.2f} & {d['Kimberly-Clark']:.2f} & {q['all']:.2f} & {q['Kimberly-Clark']:.2f}")
e = json.loads((T / 'store_124.json').read_text())
for text in [f"{e['shopping_trips']:,.0f}", f"{e['packages']:,}", f"{e['scott_packages']:,}", f"{e['scott_039_packages']:,}", 'October 17, 1991']:
    need(text)
assert e['week_beginning'] == '1991-10-17' and e['scott_039_pack_counts'] == [1]
cs = pd.read_csv(T / 'consumer_surplus.csv').set_index('cell')
for iv, label in [('aac', 'AAC'), ('other_zone', 'Other zone')]:
    a, b = cs.loc[f'linear__{iv}__rho00'], cs.loc[f'linear__{iv}__rho75']
    need(f"{label} & {a.cents_per_trip:.2f} & \\${a.loss_thousand_dollars:.0f} thousand & {b.cents_per_trip:.2f} & \\${b.loss_thousand_dollars:.0f} thousand")

# Nothing outside this folder and docs/ changed; the research files are byte-identical.
before = json.loads((HERE / 'protected_before.json').read_text())
assert all(hashlib.sha256((ROOT / f).read_bytes()).hexdigest() == h for f, h in before.items())
status = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
outside = [x for x in status if not x[3:].startswith(('Presentation/2026-11-23/revision_03/', 'docs/', 'README.md'))]
assert not outside, outside

result = dict(pdf_pages=pages, main_slides=main_frames, backup_slides=backup_frames, layout_warnings=0,
              slide_numbers_match_saved_results=True, scott_white_example={k: round(float(x), 4) for k, x in scott_white.items()},
              protected_research_files=len(before), research_files_unchanged=True,
              tracked_files_outside_revision_03_and_docs_changed=0, estimation_or_solves=0, presenter_rehearsal=False,
              pdf_sha256=hashlib.sha256((HERE / 'presentation.pdf').read_bytes()).hexdigest())
(HERE / 'validation.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
