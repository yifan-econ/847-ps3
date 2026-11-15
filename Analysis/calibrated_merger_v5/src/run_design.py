"""Authorized 16-cell conditional-rho design; all writes in a new run root.

Run: uv run --locked python Analysis/calibrated_merger_v5/src/run_design.py
     --run-id YYYY-MM-DD_16cell_01
Existing run directories are never overwritten. No legacy estimators with IO
are imported. Failure outputs are preserved, not replaced by a preferred fit.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
from pathlib import Path
import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import time
import traceback
from importlib.metadata import version
import sys
import numpy as np
import pandas as pd
from scipy.stats import t
from model import Demand

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[1]
sys.path.insert(0, str(PROJECT / 'Analysis/cost_iv_v2/src'))
from estimator import fit

RHOS = [0., .25, .5, .75]
PREFIX = {'054000': (1, 'Scott'), '036000': (2, 'Kimberly-Clark'),
          '037000': (3, 'Procter & Gamble'), '042000': (4, 'James River'),
          '030400': (5, 'Georgia-Pacific'), '073310': (6, 'Fort Howard'),
          '038281': (0, 'Dominicks private label'), '070524': (0, 'Generic 070524'),
          '075725': (0, 'Generic 075725')}
SOURCE_HL = 'Paper/Hausman_Leonard_2002_public_earlier_version.pdf, pp.5,30-31'
SOURCE_FH = 'https://www.uwgb.edu/UWGBCMS/media/Archives-and-ARC/files/Fort-Howard-company-records.pdf'


def clean(value):
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    if isinstance(value, np.ndarray):
        return clean(value.tolist())
    if isinstance(value, np.generic):
        return clean(value.item())
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def write_json(path, value):
    path.write_text(json.dumps(clean(value), indent=2, allow_nan=False), encoding='utf-8')


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def fingerprint():
    result = {}
    for folder in ['Analysis', 'Archive', 'Data', 'Paper']:
        for path in (PROJECT / folder).rglob('*'):
            if (path.is_file() and ROOT not in path.parents and '__pycache__' not in path.parts
                    and path.suffix not in {'.pyc', '.pyo'}):
                result[path.relative_to(PROJECT).as_posix()] = sha(path)
    return result


def prepare(out):
    b = pd.read_csv(PROJECT / 'Archive/ps3_v1/results/clean_upc_store_week.csv.gz', dtype={'product_id': str})
    b = b[pd.to_datetime(b.date_start).dt.year.between(1991, 1992)].copy()
    keys = pd.read_csv(PROJECT / 'Analysis/mixed_logit_v4/results/all_packs__household__aac/product_results.csv.gz',
                       usecols=['store', 'upc', 'week', 'shares', 'outside_share'])
    keys = keys.rename(columns={'shares': 'saved_share', 'outside_share': 'saved_outside'})
    d = b.merge(keys, on=['store', 'upc', 'week'], validate='one_to_one')
    z = pd.read_csv(PROJECT / 'Analysis/paper_iv_v3/results/cross_zone_instruments.csv.gz',
                    usecols=['store', 'upc', 'week', 'other_zone_price'])
    d = d.merge(z, on=['store', 'upc', 'week'], validate='one_to_one')
    d = d.sort_values(['market_id', 'upc']).reset_index(drop=True)
    assert len(d) == 259986 and d.market_id.nunique() == 7996 and d.store.nunique() == 83
    assert np.allclose(d.share, d.saved_share, atol=1e-14, rtol=0)
    inside = d.groupby('market_id').share.transform('sum')
    assert np.allclose(1 - inside, d.saved_outside, atol=1e-13, rtol=0)
    assert d[['price_pack', 'aac_pack', 'other_zone_price', 'share']].gt(0).all().all()
    assert np.isfinite(d[['price_pack', 'aac_pack', 'other_zone_price', 'share']]).all().all()
    d['month'] = pd.to_datetime(d.date_start).dt.to_period('M').astype(str)
    d['cluster_time'] = d.month
    d['y_base'] = np.log(d.share) - np.log1p(-inside)
    d['within_log'] = np.log(d.share / inside)
    d['prefix'] = d.upc.astype(str).str.zfill(11).str[:6]
    assert set(d.prefix) <= set(PREFIX)
    d['firm'] = d.prefix.map(lambda p: PREFIX[p][0])
    d['owner'] = d.prefix.map(lambda p: PREFIX[p][1])
    d['corrected_brand'] = np.where(d.descrip.str.contains('SCOTT', case=False), 'Scott', d.brand)
    # Median over the prespecified full 1991-92 positive-sales window, before
    # complete-market exclusion; no outcome-dependent margin selection.
    med = b.groupby(['store', 'upc']).profit.median().rename('median_margin_pct')
    d = d.join(med, on=['store', 'upc'], validate='many_to_one')
    d['q_percent'] = 1 - d.median_margin_pct / 100
    assert d.q_percent.between(0, 1, inclusive='right').all()
    catalog = d[['upc', 'prefix', 'descrip', 'brand', 'corrected_brand', 'pack_count', 'firm', 'owner']].drop_duplicates()
    assert catalog.upc.is_unique
    catalog['conduct'] = np.where(catalog.firm > 0, 'Bertrand manufacturer', 'fixed-price fringe')
    catalog['source'] = np.where(catalog.firm.eq(6), SOURCE_FH, SOURCE_HL)
    catalog.loc[catalog.firm.eq(0), 'source'] = 'UPC descriptions; fixed-price conduct assumption, supplier not inferred'
    catalog.to_csv(out / 'ownership_catalog.csv', index=False)
    keep = ['store', 'upc', 'week', 'market_id', 'price_pack', 'share', 'market_size', 'move',
            'pack_count', 'deal', 'aac_pack', 'other_zone_price', 'firm', 'owner', 'q_percent']
    d[keep].to_csv(out / 'product_inputs.csv.gz', index=False)
    audit = {'before_rows': len(b), 'before_markets': b.market_id.nunique(),
             'rows': len(d), 'markets': d.market_id.nunique(), 'stores': d.store.nunique(),
             'upcs': d.upc.nunique(), 'months': d.month.nunique(),
             'retained_packages_fraction': d.move.sum() / b.move.sum(),
             'corrected_label_rows': int((d.brand != d.corrected_brand).sum()),
             'corrected_upcs': int(catalog.loc[catalog.brand != catalog.corrected_brand, 'upc'].nunique()),
             'median_outside': float((1 - inside).groupby(d.market_id).first().median()),
             'unknown_ownership_upcs': 0,
             'fringe_package_fraction': d.loc[d.firm.eq(0), 'move'].sum() / d.move.sum()}
    write_json(out / 'sample_audit.json', audit)
    return d


def assess_scenario(d, dem, firm, q, label, out):
    active = firm > 0
    merged = np.where(firm == 2, 1, firm)
    mu = dem.markups(dem.p0, firm, q)
    costs = q * dem.p0 - mu
    costs[~active] = 0  # No fringe costs are inferred or used in its fixed prices.
    effective = costs / q
    proxy_manufacturer = d.aac_pack.to_numpy() - mu
    # Dollar-rule manufacturer cost is an AAC-based diagnostic; c_eff alone
    # enters predictions. Percentage rule's calibrated manufacturer cost is c.
    manufacturer = proxy_manufacturer if label == 'dollar' else costs
    pre, pre_ok, pre_err, _, pre_iters = dem.solve(firm, q, costs, dem.p0 * 1.02)
    reproduction = dem.maximum(np.abs(pre - dem.p0))
    p1, ok1, err1, abs1, it1 = dem.solve(merged, q, costs, dem.p0)
    p2, ok2, err2, abs2, it2 = dem.solve(merged, q, costs, dem.p0 * 1.10)
    agreement = dem.maximum(np.abs(p1 - p2))
    curv_pre = dem.curvature(dem.p0, firm, q, costs)
    curv_post = dem.curvature(p1, merged, q, costs)
    numerical = pre_ok & ok1 & ok2 & (reproduction < 1e-8) & (agreement < 1e-7) & curv_pre & curv_post
    effective_ok = dem.maximum(active & (effective < 0)) == 0
    manufacturer_ok = dem.maximum(active & (manufacturer < 0)) == 0
    s1, _, logsum1 = dem.state(p1)
    _, _, logsum0 = dem.state(dem.p0)
    welfare = (logsum1 - logsum0) / -dem.beta if dem.form == 'linear' else np.full(dem.M, np.nan)
    market_names = d.market_id.iloc[dem.starts].to_numpy()
    markets = pd.DataFrame({'market_id': market_names, 'numerical_ok': numerical,
        'pre_converged': pre_ok, 'post_start1_converged': ok1, 'post_start2_converged': ok2,
        'pre_curvature_ok': curv_pre, 'post_curvature_ok': curv_post,
        'baseline_price_error': reproduction, 'start_price_difference': agreement,
        'pre_foc_scaled': pre_err, 'post_foc_scaled': np.maximum(err1, err2),
        'post_foc_absolute': np.maximum(abs1, abs2), 'pre_iterations': pre_iters,
        'post_iterations_max': np.maximum(it1, it2), 'effective_cost_ok': effective_ok,
        'manufacturer_cost_ok': manufacturer_ok, 'welfare_per_opportunity': welfare,
        'market_size': d.market_size.iloc[dem.starts].to_numpy()})
    markets.to_csv(out / f'{label}_markets.csv.gz', index=False)
    np.savez_compressed(out / f'{label}_simulation.npz', prices_start1=p1, prices_start2=p2,
        post_shares=s1, markup=mu, calibrated_cost=costs, effective_cost=effective,
        manufacturer_cost=manufacturer, aac_proxy_cost=proxy_manufacturer)
    rows = []
    for pack, mask in [('all', active), ('single', active & d.pack_count.eq(1).to_numpy()),
                       ('2_to_4', active & d.pack_count.between(2, 4).to_numpy()),
                       ('5_plus', active & d.pack_count.ge(5).to_numpy())]:
        for name, value in [('effective', effective), ('manufacturer', manufacturer), ('aac_proxy', proxy_manufacturer)]:
            rows.append({'retailer': label, 'pack_group': pack, 'cost_kind': name,
                         'rows': int(mask.sum()), 'negative_rows': int((mask & (value < 0)).sum()),
                         'negative_package_fraction': float(d.move.to_numpy()[mask & (value < 0)].sum() / d.move.to_numpy()[mask].sum()),
                         'median_cost': float(np.median(value[mask]))})
    return markets, rows


def summarize(out, d, all_scenarios):
    market, _ = pd.factorize(d.market_id, sort=False)
    common_num = np.logical_and.reduce([m.numerical_ok.to_numpy() for _, _, m in all_scenarios])
    common_eff = common_num & np.logical_and.reduce([m.effective_cost_ok.to_numpy() for _, _, m in all_scenarios])
    common_man = common_num & np.logical_and.reduce([m.manufacturer_cost_ok.to_numpy() for _, _, m in all_scenarios])
    rows = []
    for cell, rule, m in all_scenarios:
        arr = np.load(out / 'cells' / cell / f'{rule}_simulation.npz')
        p1 = arr['prices_start1']; change = 100 * (p1 / d.price_pack.to_numpy() - 1)
        masks = {'all_numerically_valid': m.numerical_ok.to_numpy(),
                 'cell_effective_nonnegative': (m.numerical_ok & m.effective_cost_ok).to_numpy(),
                 'cell_manufacturer_nonnegative': (m.numerical_ok & m.manufacturer_cost_ok).to_numpy(),
                 'common_numerically_valid': common_num, 'common_effective_nonnegative': common_eff,
                 'common_manufacturer_nonnegative': common_man}
        for scope, valid in masks.items():
            coverage = d.move.to_numpy()[valid[market]].sum() / d.move.sum()
            for group, select in [('Scott', d.firm.eq(1).to_numpy()),
                                  ('Kimberly-Clark', d.firm.eq(2).to_numpy()),
                                  ('rivals', d.firm.ge(3).to_numpy()),
                                  ('fringe', d.firm.eq(0).to_numpy()),
                                  ('all', np.ones(len(d), bool))]:
                mask = valid[market] & select
                weight = d.move.to_numpy()[mask]
                rows.append({'cell': cell, 'retailer': rule, 'scope': scope, 'group': group,
                    'markets': int(valid.sum()), 'market_fraction': float(valid.mean()),
                    'baseline_package_coverage': float(coverage), 'group_packages': float(weight.sum()),
                    'package_weighted_price_change_pct': float(np.average(change[mask], weights=weight)) if weight.sum() else np.nan,
                    'mean_price_change_pct': float(np.mean(change[mask])) if mask.any() else np.nan,
                    'welfare_per_opportunity': float(np.average(m.loc[valid, 'welfare_per_opportunity'], weights=m.loc[valid, 'market_size'])) if valid.any() else np.nan,
                    'welfare_total_dollars': float(np.sum(m.loc[valid, 'welfare_per_opportunity'] * m.loc[valid, 'market_size'])) if valid.any() and m.welfare_per_opportunity.notna().any() else np.nan})
        arr.close()
    pd.DataFrame(rows).to_csv(out / 'counterfactual_summary.csv', index=False)
    write_json(out / 'common_sample.json', {'scenario_count': len(all_scenarios),
        'common_numerically_valid_markets': common_num.sum(),
        'common_effective_nonnegative_markets': common_eff.sum(),
        'common_manufacturer_nonnegative_markets': common_man.sum()})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-id', required=True)
    ap.add_argument('--smoke-markets', type=int, default=0,
                    help='Synthetic/implementation check only: subset markets; full sample estimates still use all keys.')
    args = ap.parse_args()
    if not args.run_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in args.run_id):
        raise ValueError('run-id must be a simple directory name')
    out = ROOT / 'runs' / args.run_id
    out.mkdir(parents=True, exist_ok=False)
    before = fingerprint()
    write_json(out / 'baseline_before.json', before)
    started = time.monotonic()
    design = {'run_id': args.run_id, 'date': '2026-11-15', 'collaborator': 'Yifan / Codex',
        'branch': subprocess.check_output(['git', 'branch', '--show-current'], cwd=PROJECT, text=True).strip(),
        'base_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=PROJECT, text=True).strip(),
        'starting_git_status': subprocess.check_output(['git', 'status', '--short'], cwd=PROJECT, text=True),
        'python': platform.python_version(), 'platform': platform.platform(),
        'packages': {p: version(p) for p in ['numpy', 'pandas', 'scipy', 'pyblp', 'filelock']},
        'rho_grid': RHOS, 'forms': ['linear', 'log'], 'ivs': ['aac', 'other_zone'],
        'retailer_rules': 'dollar all 16; percentage only rho=0 (4 sensitivity scenarios)',
        'scope': 'hypothetical Scott/Kimberly-Clark merger at 1991-1992 conditions',
        'fringe': 'fixed observed prices; private label/generics remain in the demand system',
        'outputs': out.relative_to(PROJECT).as_posix(), 'smoke_markets': args.smoke_markets,
        'sharing': 'local, uncommitted, unpushed',
        'inference': 'store/month two-way sandwich; only 24 months; conditional on calibrated rho; no overidentification df',
        'iv_assumptions': 'E[z*xi|FE,deal]=0 for level cells and E[log(z)*xi|FE,deal]=0 for log cells; neither established by first stage',
        'solver': {'damping': .5, 'max_iterations': 600, 'starts': ['observed prices', '1.10 times observed prices'],
                   'baseline_start': '1.02 times observed prices', 'scaled_foc_tol': 1e-8,
                   'internal_foc_tol': 1e-10, 'absolute_foc_tol': 1e-8,
                   'baseline_price_tol': 1e-8, 'start_agreement_tol': 1e-7},
        'uncertainty': 'scenario ranges are not confidence intervals; counterfactual parameter uncertainty not propagated'}
    (out / 'code').mkdir()
    for path in [Path(__file__), ROOT / 'src/model.py', PROJECT / 'Analysis/cost_iv_v2/src/estimator.py']:
        shutil.copyfile(path, out / 'code' / path.name)
    design['code_sha256'] = {p.name: sha(p) for p in (out / 'code').iterdir()}
    design['uv_lock_sha256'] = sha(PROJECT / 'uv.lock')
    write_json(out / 'design.json', design)  # Written before inspecting any new estimates.
    status = {'complete': False, 'error': None}
    estimates, first_stages, coefficients, scenarios, cost_rows, diag_rows = [], [], [], [], [], []
    try:
        d = prepare(out)
        for form in ['linear', 'log']:
            for iv in ['aac', 'other_zone']:
                source = d.aac_pack if iv == 'aac' else d.other_zone_price
                d['_price'] = d.price_pack if form == 'linear' else np.log(d.price_pack)
                d['_iv'] = source if form == 'linear' else np.log(source)
                for rho in RHOS:
                    cell = f'{form}__{iv}__rho{int(rho*100):02d}'
                    dest = out / 'cells' / cell
                    dest.mkdir(parents=True)
                    d['y'] = d.y_base - rho * d.within_log
                    est, coef = fit(d, cell, iv=['_iv'], price='_price')
                    est.update(form=form, iv=iv, rho=rho, price_unit='USD/package' if form == 'linear' else 'log USD/package',
                               rho_calibrated=True, overid_df=0)
                    est['price_p_t23'] = float(2*t.sf(abs(est['beta_price']/est['se_price']), 23))
                    coefficients.extend(coef)
                    if rho == 0:
                        first_stages.append({k: est[k] for k in ['form', 'iv', 'n', 'first_stage_wald_chi2', 'first_stage_partial_r2']})
                    if est['beta_price'] >= 0 or not np.isfinite(est['beta_price']):
                        est.update(status='rejected_wrong_sign', median_own_elasticity=None)
                        write_json(dest / 'estimate.json', est)
                        estimates.append(est)
                        print(cell, 'REJECTED WRONG SIGN', flush=True)
                        continue
                    sim = d if not args.smoke_markets else d[d.market_id.isin(d.market_id.drop_duplicates().iloc[:args.smoke_markets])].copy()
                    mid = pd.factorize(sim.market_id, sort=False)[0]
                    dem = Demand(mid, sim.price_pack.to_numpy(), sim.share.to_numpy(), est['beta_price'], rho, form)
                    assert np.max(np.abs(dem.state(dem.p0)[0] - dem.s0)) < 1e-12
                    firm = sim.firm.to_numpy()
                    own, category, diversion = dem.diagnostics(firm)
                    est.update(status='estimated', median_own_elasticity=float(np.median(own)),
                        share_inelastic=float(np.mean(np.abs(own)<1)),
                        share_upward_sloping=float(np.mean(own>0)),
                        category_elasticity_median=float(np.median(category)),
                        scott_to_kc_diversion_packages=float(np.average(diversion[firm==1], weights=sim.move.to_numpy()[firm==1])))
                    estimates.append(est)
                    write_json(dest / 'estimate.json', est)
                    write_json(dest / 'coefficients.json', coef)
                    for rule in ['dollar'] + (['percentage'] if rho == 0 else []):
                        q = np.ones(len(sim)) if rule == 'dollar' else sim.q_percent.to_numpy()
                        m, costs = assess_scenario(sim, dem, firm, q, rule, dest)
                        scenarios.append((cell, rule, m))
                        cost_rows.extend([{'cell': cell, **r} for r in costs])
                        diag = {'cell': cell, 'retailer': rule, 'markets': len(m),
                            'numerically_valid': int(m.numerical_ok.sum()),
                            'effective_nonnegative': int((m.numerical_ok & m.effective_cost_ok).sum()),
                            'manufacturer_nonnegative': int((m.numerical_ok & m.manufacturer_cost_ok).sum()),
                            'max_baseline_error': float(m.baseline_price_error.max()),
                            'max_post_foc_scaled': float(m.post_foc_scaled.max()),
                            'max_start_difference': float(m.start_price_difference.max()),
                            'pre_curvature_failures': int((~m.pre_curvature_ok).sum()),
                            'post_curvature_failures': int((~m.post_curvature_ok).sum())}
                        diag_rows.append(diag)
                        print(cell, rule, json.dumps(diag), flush=True)
                    pd.DataFrame(estimates).to_csv(out / 'estimates.csv', index=False)
                    pd.DataFrame(diag_rows).to_csv(out / 'equilibrium_diagnostics.csv', index=False)
        pd.DataFrame(first_stages).to_csv(out / 'first_stages.csv', index=False)
        pd.DataFrame(coefficients).to_csv(out / 'coefficients.csv', index=False)
        pd.DataFrame(cost_rows).to_csv(out / 'cost_diagnostics.csv', index=False)
        summarize(out, sim, scenarios)
        status.update(complete=True, demand_cells=len(estimates), scenarios=len(scenarios),
                      rejected_demand_cells=sum(e['status'] != 'estimated' for e in estimates))
    except Exception as exc:
        status['error'] = repr(exc)
        (out / 'traceback.txt').write_text(traceback.format_exc(), encoding='utf-8')
        raise
    finally:
        after = fingerprint()
        changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
        write_json(out / 'preservation.json', {'protected_files': len(before), 'changed': changed})
        status['elapsed_seconds'] = time.monotonic() - started
        status['baseline_preserved'] = not changed
        write_json(out / 'status.json', status)
        if changed:
            raise RuntimeError(f'Baseline changed: {changed}')


if __name__ == '__main__':
    main()
