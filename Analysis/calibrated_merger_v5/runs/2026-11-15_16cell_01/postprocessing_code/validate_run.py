"""Read saved outputs; independently check dense FOCs on deterministic markets."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import logsumexp, expit

PROJECT = Path(__file__).resolve().parents[3]


def validate(run):
    status = json.loads((run / 'status.json').read_text())
    assert status['complete'] and status['demand_cells'] == 16 and status['scenarios'] == 20
    assert status['baseline_preserved'] and status['rejected_demand_cells'] == 0
    design=json.loads((run/'design.json').read_text())
    for name, expected in design['code_sha256'].items():
        with (run/'code'/name).open('rb') as f:
            assert hashlib.file_digest(f,'sha256').hexdigest()==expected
    baseline = json.loads((run / 'baseline_before.json').read_text())
    for name, expected in baseline.items():
        with (PROJECT / name).open('rb') as f:
            assert hashlib.file_digest(f, 'sha256').hexdigest() == expected, name
    d = pd.read_csv(run / 'product_inputs.csv.gz')
    assert len(d) == 259986 and d.market_id.nunique() == 7996
    assert not d.duplicated(['store', 'upc', 'week']).any()
    groups = list(d.groupby('market_id', sort=False).indices.values())
    estimates = pd.read_csv(run / 'estimates.csv')
    maxima = dict(markup_error=0., baseline_dense_foc=0., post_dense_foc=0.,
                  jacobian_error=0., largest_hessian_eigenvalue=-np.inf,
                  share_error=0., price_summary_error=0.)
    checks = []
    common = []
    summary = pd.read_csv(run / 'counterfactual_summary.csv')
    for e in estimates.itertuples():
        for rule in ['dollar'] + (['percentage'] if e.rho == 0 else []):
            cell = run / 'cells' / e.model
            a = np.load(cell / f'{rule}_simulation.npz')
            m = pd.read_csv(cell / f'{rule}_markets.csv.gz')
            assert list(m.market_id) == list(d.market_id.drop_duplicates())
            valid = m.numerical_ok.to_numpy()
            active=d.firm.gt(0).to_numpy()
            q_all=np.ones(len(d)) if rule=='dollar' else d.q_percent.to_numpy()
            np.testing.assert_allclose(a['calibrated_cost'][active],
                (q_all*d.price_pack.to_numpy()-a['markup'])[active],atol=1e-12,rtol=0)
            np.testing.assert_allclose(a['effective_cost'][active],
                (a['calibrated_cost']/q_all)[active],atol=1e-12,rtol=0)
            expected_manufacturer=d.aac_pack.to_numpy()-a['markup'] if rule=='dollar' else a['calibrated_cost']
            np.testing.assert_allclose(a['manufacturer_cost'][active],expected_manufacturer[active],atol=1e-12,rtol=0)
            for name,column in [('effective_cost','effective_cost_ok'),('manufacturer_cost','manufacturer_cost_ok')]:
                expected=np.array([not np.any((a[name][ix]<0)&active[ix]) for ix in groups])
                assert np.array_equal(expected,m[column].to_numpy())
            common.append(valid)
            fringe = d.firm.eq(0).to_numpy()
            assert np.array_equal(a['prices_start1'][fringe], a['prices_start2'][fringe])
            np.testing.assert_allclose(a['prices_start1'][fringe],d.price_pack.to_numpy()[fringe],atol=1e-12,rtol=0)
            assert np.isfinite(a['post_shares']).all() and (a['post_shares'] >= 0).all()
            assert m.loc[valid, 'baseline_price_error'].max() < 1e-8
            assert m.loc[valid, 'start_price_difference'].max() < 1e-7
            assert m.loc[valid, 'post_foc_scaled'].max() < 1e-8
            assert m.loc[valid, 'post_foc_absolute'].max() < 1e-8
            assert m.welfare_per_opportunity.isna().all() if e.form == 'log' else m.welfare_per_opportunity.notna().all()
            # Equally spaced accepted markets, fixed selection rule.
            vi = np.flatnonzero(valid)
            chosen = np.unique(vi[np.linspace(0, len(vi)-1, 12).astype(int)])
            for k in chosen:
                ix = groups[k]
                x = d.iloc[ix]
                p0 = x.price_pack.to_numpy(); s0 = x.share.to_numpy()
                q = np.ones(len(ix)) if rule == 'dollar' else x.q_percent.to_numpy()
                firm = x.firm.to_numpy(); merged = np.where(firm == 2, 1, firm)
                cost = a['calibrated_cost'][ix]
                h = 1 / (1-e.rho)
                delta = np.log(s0/(1-s0.sum())) - e.rho*np.log(s0/s0.sum())

                def shares(p):
                    v = h*(delta + e.beta_price*(p-p0 if e.form == 'linear' else np.log(p/p0)))
                    ld = logsumexp(v)
                    return np.exp(v-ld)*expit(ld/h)

                def jac(p):
                    s = shares(p); S = s.sum()
                    b = np.full(len(p), e.beta_price) if e.form == 'linear' else e.beta_price/p
                    return (h*np.diag(s) - (1+(h-1)/S)*np.outer(s,s))*b[None,:]

                def grad(p, own, f):
                    mask = own == f
                    return q[mask]*shares(p)[mask] + jac(p)[np.ix_(mask, mask)].T @ (q*p-cost)[mask]

                p1 = a['prices_start1'][ix]
                maxima['share_error'] = max(maxima['share_error'], np.max(abs(shares(p1)-a['post_shares'][ix])))
                for own, p, label in [(firm,p0,'baseline_dense_foc'), (merged,p1,'post_dense_foc')]:
                    for f in np.unique(own[own>0]):
                        mask = own == f
                        residual = np.max(abs(grad(p,own,f)))
                        maxima[label] = max(maxima[label],residual)
                        assert residual < 1e-8
                        if label == 'baseline_dense_foc':
                            mu = np.linalg.solve(-jac(p)[np.ix_(mask,mask)].T, q[mask]*shares(p)[mask])
                            error = np.max(abs(mu-a['markup'][ix][mask]))
                            maxima['markup_error'] = max(maxima['markup_error'],error)
                            assert error < 1e-8
                        else:
                            cols = np.flatnonzero(mask); H = np.empty((len(cols),len(cols)))
                            for j, col in enumerate(cols):
                                step = 1e-5*p[col]; plus=p.copy(); minus=p.copy()
                                plus[col]+=step; minus[col]-=step
                                H[:,j]=(grad(plus,own,f)-grad(minus,own,f))/(2*step)
                            eig = np.linalg.eigvalsh((H+H.T)/2).max()
                            maxima['largest_hessian_eigenvalue']=max(maxima['largest_hessian_eigenvalue'],eig)
                            assert eig < 1e-8
                J = np.empty((len(ix),len(ix)))
                for col in range(len(ix)):
                    step=1e-5*p1[col]; plus=p1.copy(); minus=p1.copy()
                    plus[col]+=step; minus[col]-=step
                    J[:,col]=(shares(plus)-shares(minus))/(2*step)
                err=np.max(abs(J-jac(p1)))
                maxima['jacobian_error']=max(maxima['jacobian_error'],err)
                assert err < 1e-7
            rows = np.concatenate([groups[k] for k in vi])
            price_change=np.average(100*(a['prices_start1'][rows]/d.price_pack.to_numpy()[rows]-1),weights=d.move.to_numpy()[rows])
            reported=summary.loc[(summary.cell==e.model)&(summary.retailer==rule)&(summary.scope=='all_numerically_valid')&(summary.group=='all'),'package_weighted_price_change_pct'].item()
            maxima['price_summary_error']=max(maxima['price_summary_error'],abs(price_change-reported))
            assert abs(price_change-reported)<1e-10
            checks.append(dict(cell=e.model,retailer=rule,accepted_markets=int(valid.sum()),dense_markets=len(chosen)))
            a.close()
    assert np.logical_and.reduce(common).sum() == json.loads((run/'common_sample.json').read_text())['common_numerically_valid_markets']
    return dict(passed=True,protected_files=len(baseline),scenarios=checks,maxima=maxima,
                method='Independent dense Jacobian/inversion, numerical differentiation and profit Hessians on 12 deterministic accepted markets per scenario; full saved-flag and summary checks. No new estimation or equilibrium search.')


if __name__ == '__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--run-id',required=True); args=ap.parse_args()
    run=PROJECT/'Analysis/calibrated_merger_v5/runs'/args.run_id
    result=validate(run)
    dest=run/'independent_validation.json'
    with dest.open('x',encoding='utf-8') as f:
        json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
