"""Collect the numbers shown on the revision_03 slides. Reads saved results; fits nothing.

Run from the repository root:
    uv run --locked python Presentation/2026-11-23/revision_03/prepare_tables.py

Every output is opened with mode 'x', so the script refuses to overwrite earlier output.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN = ROOT / 'Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01'
OUT = HERE / 'tables'
OUT.mkdir(exist_ok=False)

d = pd.read_csv(RUN / 'product_inputs.csv.gz')
e = pd.read_csv(RUN / 'estimates_corrected.csv')
w = d.move.to_numpy(float)

# Slides 6-7: first stages and plain-logit estimates (rho = 0).
b = e[e.rho.eq(0)].copy()
co = pd.read_csv(RUN / 'coefficients.csv')
fs = co[co.model.str.endswith('rho00 FIRST_STAGE') & co.variable.eq('_iv')].copy()
fs['model'] = fs.model.str.replace(' FIRST_STAGE', '', regex=False)
fs = fs.merge(b[['model', 'first_stage_partial_r2', 'first_stage_wald_chi2']], on='model')
# One instrument: the cluster-robust first-stage F is the squared t statistic.
fs['first_stage_F'] = (fs.coefficient / fs.se_two_way_cluster) ** 2
assert np.allclose(fs.first_stage_F, fs.first_stage_wald_chi2, rtol=1e-6)
fs.to_csv(OUT / 'first_stage.csv', index=False, mode='x')
b[['model', 'beta_price', 'se_price', 'median_own_elasticity']].to_csv(OUT / 'logit_estimates.csv', index=False, mode='x')

pack = []
beta_dollar = float(b.loc[b.model.eq('linear__aac__rho00'), 'beta_price'].iloc[0])
beta_log = float(b.loc[b.model.eq('log__aac__rho00'), 'beta_price'].iloc[0])
for name, mask in [('1 roll', d.pack_count.eq(1)), ('4 rolls', d.pack_count.eq(4)), ('6+ rolls', d.pack_count.ge(6))]:
    pack.append(dict(group=name, weighted_price=np.average(d.loc[mask, 'price_pack'], weights=d.loc[mask, 'move']),
                     dollar_price_aac=np.average((beta_dollar * d.price_pack * (1 - d.share))[mask], weights=d.loc[mask, 'move']),
                     log_price_aac=np.average((beta_log * (1 - d.share))[mask], weights=d.loc[mask, 'move'])))
pd.DataFrame(pack).to_csv(OUT / 'pack_size_elasticities.csv', index=False, mode='x')

# Slide 4: where price variation sits (descriptive variance shares, not estimates).
p = d.price_pack
total = ((p - p.mean()) ** 2).mean()


def between(keys):
    mean = d.groupby(keys).price_pack.transform('mean')
    return float(((mean - p.mean()) ** 2).mean() / total * 100)


variation = dict(between_store_upc_percent=between(['store', 'upc']),
                 within_store_upc_over_time_percent=100 - between(['store', 'upc']),
                 between_pack_size_percent=between(['pack_count']), between_upc_percent=between(['upc']),
                 between_store_percent=between(['store']),
                 definition='Observation-weighted shares of the variance of package price in dollars.')
(OUT / 'price_variation.json').write_text(json.dumps(variation, indent=2))

# Slide 5: sample counts.
m = d.groupby('market_id').agg(inside=('share', 'sum'), products=('upc', 'size'))
audit = json.loads((RUN / 'sample_audit.json').read_text())
sample = dict(observations=len(d), store_weeks=len(m), stores=int(d.store.nunique()), upcs=int(d.upc.nunique()),
              median_products=float(m.products.median()), median_price=float(d.price_pack.median()),
              single_roll_package_percent=float(d.loc[d.pack_count.eq(1), 'move'].sum() / d.move.sum() * 100),
              median_outside_percent=float((1 - m.inside).median() * 100),
              retained_package_percent=audit['retained_packages_fraction'] * 100)
(OUT / 'sample.json').write_text(json.dumps(sample, indent=2))

# Slide 9: nested logit, all sixteen cells, plus Kimberly-Clark-to-Scott diversion from saved shares.
inside = d.groupby('market_id').share.transform('sum')
scott_share = d.share.where(d.firm.eq(1), 0).groupby(d.market_id).transform('sum')
kc = d.firm.eq(2)
diversion = {}
for rho in [0, .25, .5, .75]:
    h = 1 / (1 - rho)
    A = 1 + (h - 1) / inside
    diversion[rho] = float(np.average((A * scott_share / (h - A * d.share))[kc], weights=d.loc[kc, 'move']))
nest = e[['model', 'form', 'iv', 'rho', 'beta_price', 'se_price', 'median_own_elasticity', 'category_elasticity_median']].copy()
nest['kc_to_scott_diversion'] = nest.rho.map(diversion)
nest.to_csv(OUT / 'nested_results.csv', index=False, mode='x')

# Slides 12-13: merger price effects, and the share of packages with a non-negative implied cost.
r = pd.read_csv(RUN / 'counterfactual_summary.csv')
r = r[r.scope.eq('common_numerically_valid') & r.group.isin(['all', 'Scott', 'Kimberly-Clark'])]
price = r.pivot(index=['cell', 'retailer'], columns='group', values='package_weighted_price_change_pct').reset_index()
price.to_csv(OUT / 'merger_price_effects.csv', index=False, mode='x')
active = d.firm.to_numpy() > 0
scott_single = (d.firm.to_numpy() == 1) & (d.pack_count.to_numpy() == 1)
cost = []
for model in e.model:
    with np.load(RUN / 'cells' / model / 'dollar_simulation.npz') as z:
        negative = z['manufacturer_cost'] < 0
    cost.append(dict(model=model, nonnegative_cost_percent_all_packages=100 * (1 - w[active & negative].sum() / w[active].sum()),
                     negative_cost_percent_scott_single=100 * w[scott_single & negative].sum() / w[scott_single].sum()))
pd.DataFrame(cost).to_csv(OUT / 'cost_check.csv', index=False, mode='x')

# Backup: consumer surplus (price in dollars only), store 124, retailer rules.
cs = pd.read_csv(RUN / 'counterfactual_summary.csv')
cs = cs[cs.scope.eq('common_numerically_valid') & cs.cell.str.startswith('linear') & cs.retailer.eq('dollar') & cs.group.eq('all')]
cs = cs[['cell', 'welfare_per_opportunity', 'welfare_total_dollars', 'markets']].copy()
cs['cents_per_trip'] = -100 * cs.welfare_per_opportunity
cs['loss_thousand_dollars'] = -cs.welfare_total_dollars / 1000
cs.to_csv(OUT / 'consumer_surplus.csv', index=False, mode='x')
s = d[d.store.eq(124) & d.week.eq(110)]
scott39 = s[s.firm.eq(1) & s.price_pack.round(2).eq(.39)]
episode = dict(store=124, week=110, week_beginning=str((pd.Timestamp('1989-09-14') + pd.Timedelta(days=109 * 7)).date()),
               packages=int(s.move.sum()), shopping_trips=float(s.market_size.iloc[0]),
               scott_packages=int(s[s.firm.eq(1)].move.sum()), scott_039_upcs=int(scott39.upc.nunique()),
               scott_039_packages=int(scott39.move.sum()), scott_039_pack_counts=sorted(int(x) for x in scott39.pack_count.unique()))
(OUT / 'store_124.json').write_text(json.dumps(episode, indent=2))

print(fs[['model', 'coefficient', 'se_two_way_cluster', 'first_stage_partial_r2', 'first_stage_F']].round(3).to_string(index=False))
print(pd.DataFrame(pack).round(3).to_string(index=False))
print(json.dumps(variation, indent=1)); print(json.dumps(sample, indent=1))
print(nest.round(3).to_string(index=False))
print(price.round(2).to_string(index=False))
print(pd.DataFrame(cost).round(2).to_string(index=False))
print(cs.round(4).to_string(index=False)); print(json.dumps(episode, indent=1))
