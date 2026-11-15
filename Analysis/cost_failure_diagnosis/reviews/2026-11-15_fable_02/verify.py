"""Read saved arrays/flags; no estimation or equilibrium calls. Outputs must be new."""
from pathlib import Path
import hashlib
import json
import platform
import sys
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
RUN = ROOT / 'Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01'

def inventory():
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for folder in ['Analysis', 'Archive', 'Data', 'Paper']
            for p in (ROOT / folder).rglob('*')
            if p.is_file() and OUT not in p.parents and '__pycache__' not in p.parts}

def save(name, obj):
    with (OUT / name).open('x', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)

before = inventory()
save('protected_before.json', before)
d = pd.read_csv(RUN / 'product_inputs.csv.gz')
ids = d.market_id.drop_duplicates().to_numpy()
active = d.firm.gt(0).to_numpy()
scott = (d.firm.eq(1) & d.pack_count.eq(1)).to_numpy()
largest = d[d.firm.gt(0)].groupby(['market_id', 'firm']).share.sum().groupby('market_id').max()
rows = []
for path in sorted((RUN / 'cells').glob('*/*_markets.csv.gz')):
    cell = path.parent.name
    rule = path.name.split('_')[0]
    m = pd.read_csv(path)
    assert np.array_equal(ids, m.market_id)
    a = np.load(path.parent / f'{rule}_simulation.npz')
    for cost, flag in [('effective_cost', 'effective_cost_ok'), ('manufacturer_cost', 'manufacturer_cost_ok')]:
        negative = active & (a[cost] < 0)
        expected = ~pd.Series(negative).groupby(d.market_id).any().reindex(ids).to_numpy()
        assert np.array_equal(expected, m[flag])
    ok = m.numerical_ok.to_numpy()
    eff = m.effective_cost_ok.to_numpy()
    man = m.manufacturer_cost_ok.to_numpy()
    fs = largest.reindex(ids).to_numpy()
    assert fs[ok].max() < fs[~ok].min()
    sn = scott & (a['manufacturer_cost'] < 0)
    snmarkets = set(d.loc[sn, 'market_id'])
    beta = json.loads((path.parent / 'estimate.json').read_text())['beta_price']
    rows.append(dict(cell=cell, retailer=rule, rejected=int((~ok).sum()),
        rejected_effective_nonnegative=int((~ok & eff).sum()),
        accepted_effective_negative=int((ok & ~eff).sum()),
        accepted_manufacturer_negative=int((ok & ~man).sum()),
        max_accepted_firm_share=float(fs[ok].max()), min_rejected_firm_share=float(fs[~ok].min()),
        rejected_pre_not_converged=int((~ok & ~m.pre_converged).sum()),
        rejected_baseline_error=int((~ok & m.baseline_price_error.ge(1e-8)).sum()),
        rejected_pre_curvature_fail=int((~ok & ~m.pre_curvature_ok).sum()),
        rejected_post_curvature_fail=int((~ok & ~m.post_curvature_ok).sum()),
        scott_negative_markets=len(snmarkets),
        scott_negative_accepted_markets=len(snmarkets & set(m.loc[ok, 'market_id'])),
        scott_negative_package_fraction=float(d.loc[sn, 'move'].sum() / d.loc[scott, 'move'].sum()),
        beta=beta,
        singleton_log_iteration_threshold=(3 + 1 / abs(beta)) / 4 if cell.startswith('log') else None,
        singleton_log_cost_threshold=1 - 1 / abs(beta) if cell.startswith('log') else None))
    if rule == 'percentage':
        assert np.array_equal(a['effective_cost'][active] < 0, a['manufacturer_cost'][active] < 0)
    if cell.startswith('log') and cell.endswith('rho00'):
        assert np.array_equal(ok, eff)
t = pd.DataFrame(rows)
assert len(t) == 20
assert (t.rejected_effective_nonnegative == 0).all()
assert (t.rejected_baseline_error == t.rejected).all()
assert (t[['rejected_pre_curvature_fail', 'rejected_post_curvature_fail']] == 0).all().all()
old = pd.read_csv(OUT.parent / '2026-11-15_fable_01/scott_cost_claim_check.csv')
check = t.merge(old[old.scope.eq('full_input')], on=['cell', 'retailer'])
assert np.max(np.abs(check.scott_negative_package_fraction - check.negative_package_fraction)) < 1e-14
t.to_csv(OUT / 'scenario_crosschecks.csv', index=False, mode='x')

b = pd.read_csv(ROOT / 'Archive/ps3_v1/results/clean_upc_store_week.csv.gz')
b = b[pd.to_datetime(b.date_start).dt.year.between(1991, 1992)].copy()
b['market_id'] = b.store.astype(str) + '_' + b.week.astype(str)
b['rolls'] = b.move * b.pack_count
v = b.groupby('market_id').agg(store=('store', 'first'), week=('week', 'first'),
    packages=('move', 'sum'), rolls=('rolls', 'sum'), traffic=('market_size', 'first'))
v['kept'] = v.index.isin(ids)
v['packages_per_trip'] = v.packages / v.traffic
v['rolls_per_trip'] = v.rolls / v.traffic
v.to_csv(OUT / 'sample_coverage.csv', mode='x')
coverage = []
for kept, z in v.groupby('kept'):
    coverage.append(dict(kept=bool(kept), markets=len(z), week105_stores=int(z[z.week.eq(105)].store.nunique()),
        median_packages_per_trip=float(z.packages_per_trip.median()),
        median_rolls_per_trip=float(z.rolls_per_trip.median()),
        pooled_packages_per_trip=float(z.packages.sum()/z.traffic.sum()),
        pooled_rolls_per_trip=float(z.rolls.sum()/z.traffic.sum())))
save('sample_summary.json', coverage)
after = inventory()
assert before == after
save('verification.json', dict(python=sys.version, platform=platform.platform(), scenarios=20,
    protected_files=len(before), unchanged=True, saved_flags_match_arrays=True,
    all_scenarios_share_separated=True, log_rho0_numerical_equals_effective_nonnegative=True,
    estimation_or_equilibrium_calls=0))
print(t.to_string(index=False))
print(json.dumps(coverage))
print(f'Protected {len(before)} files unchanged.')
