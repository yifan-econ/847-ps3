"""Saved-result accounting diagnosis. No estimation or equilibrium solver calls."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import time
import traceback
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[1]
SOURCE = PROJECT / 'Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01'


def digest(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def inventory():
    return {p.relative_to(PROJECT).as_posix(): digest(p)
            for folder in ['Analysis', 'Archive', 'Data', 'Paper']
            for p in (PROJECT/folder).rglob('*')
            if p.is_file() and ROOT not in p.parents and '__pycache__' not in p.parts
            and p.suffix not in ['.pyc', '.pyo']}


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False), encoding='utf-8')


def quantile(x, w, q):
    order = np.argsort(x)
    return float(x[order][np.searchsorted(np.cumsum(w[order]), q*w.sum(), side='left')])


def run(out):
    d = pd.read_csv(SOURCE/'product_inputs.csv.gz')
    cat = pd.read_csv(SOURCE/'ownership_catalog.csv', dtype={'upc': str})
    d['upc'] = d.upc.astype(str)
    d = d.merge(cat[['upc','descrip','corrected_brand']], on='upc', how='left', validate='many_to_one', sort=False)
    assert len(d) == 259986 and d.descrip.notna().all()
    market, names = pd.factorize(d.market_id, sort=False)
    starts = np.r_[0, np.flatnonzero(np.diff(market))+1]
    M = len(starts); assert M == 7996
    total = lambda x: np.add.reduceat(x, starts)
    maximum = lambda x: np.maximum.reduceat(x, starts)
    p=d.price_pack.to_numpy(); s=d.share.to_numpy(); aac=d.aac_pack.to_numpy()
    w=d.move.to_numpy(); q_saved=d.q_percent.to_numpy(); f=d.firm.to_numpy()
    active=f>0; S=total(s); g=market*7+f
    sf=np.bincount(g,weights=s,minlength=M*7)[g]
    market_packages=total(w)
    estimates=pd.read_csv(SOURCE/'estimates_corrected.csv')
    saved_diag=pd.read_csv(SOURCE/'equilibrium_diagnostics.csv').set_index(['cell','retailer'])
    scenarios=[]
    for e in estimates.itertuples():
        for rule in ['dollar']+(['percentage'] if e.rho==0 else []):
            m=pd.read_csv(SOURCE/'cells'/e.model/f'{rule}_markets.csv.gz')
            assert np.array_equal(m.market_id.to_numpy(),names.to_numpy())
            scenarios.append((e,rule,m))
    common=np.logical_and.reduce([m.numerical_ok.to_numpy() for _,_,m in scenarios])
    assert common.sum()==7960
    scopes={'all_input_markets':np.ones(len(d),bool),'common_numerically_valid':common[market]}
    group_maps={'manufacturer':[(str(k),np.asarray(ix)) for k,ix in d[active].groupby('owner',sort=True).groups.items()],
                'upc':[(str(k),np.asarray(ix)) for k,ix in d[active].groupby('upc',sort=True).groups.items()],
                'pack':[('single',np.flatnonzero(active & (d.pack_count.to_numpy()==1))),
                        ('2_to_4',np.flatnonzero(active & d.pack_count.between(2,4).to_numpy())),
                        ('5_plus',np.flatnonzero(active & (d.pack_count.to_numpy()>=5)))],
                'all':[('all_active',np.flatnonzero(active))]}
    agg=[]; stages=[]; markets=[]; thresholds=[]; examples=[]; bridges=[]; margin_rows=[]
    discrepancies={'markup_saved':0.,'cost_saved':0.,'singleton_identity':0.,'dense_markup':0.,'retailer_bridge':0.}
    margin_cases={}
    for e,rule,m in scenarios:
        with np.load(SOURCE/'cells'/e.model/f'{rule}_simulation.npz') as z:
            arr={k:z[k] for k in ['markup','effective_cost','manufacturer_cost','calibrated_cost']}
        h=1/(1-e.rho); A=1+(h-1)/S
        b=np.full(len(d),e.beta_price) if e.form=='linear' else e.beta_price/p
        q=np.ones(len(d)) if rule=='dollar' else q_saved
        base=-q/(h*b)
        # Independent algebra, no import of v5 code: exact ownership-block inverse.
        C=np.bincount(g,weights=s*base,minlength=M*7)
        sf_groups=np.bincount(g,weights=s,minlength=M*7)
        den=1-np.repeat(A/h,7)*sf_groups
        mu=base+(A[market]/h)*(C/den)[g]
        solo_effective=-1/(b*(h-A[market]*s))
        eff=p-mu/q
        manufacturer=aac-mu if rule=='dollar' else q*p-mu
        rawbase=-1/(h*b)
        own_elasticity=p*b*(h-A[market]*s)
        discrepancies['markup_saved']=max(discrepancies['markup_saved'],float(np.max(abs(mu[active]-arr['markup'][active]))))
        discrepancies['cost_saved']=max(discrepancies['cost_saved'],float(np.max(abs(eff[active]-arr['effective_cost'][active]))),float(np.max(abs(manufacturer[active]-arr['manufacturer_cost'][active]))))
        discrepancies['singleton_identity']=max(discrepancies['singleton_identity'],float(np.max(abs(solo_effective[active]/p[active]-1/abs(own_elasticity[active])))))
        assert (mu[active]/q[active] >= solo_effective[active]-1e-10).all()
        for k in [0,M//3,2*M//3,M-1]:
            ix=np.arange(starts[k],starts[k+1] if k<M-1 else len(d))
            J=(h*np.diag(s[ix])-A[k]*np.outer(s[ix],s[ix]))*b[ix][None,:]
            for owner in np.unique(f[ix][f[ix]>0]):
                loc=np.flatnonzero(f[ix]==owner)
                dense=np.linalg.solve(-J[np.ix_(loc,loc)].T,q[ix][loc]*s[ix][loc])
                discrepancies['dense_markup']=max(discrepancies['dense_markup'],float(np.max(abs(dense-mu[ix][loc]))))
        for kind,cost,denominator in [('effective',eff,p*q),('manufacturer',manufacturer,aac if rule=='dollar' else q*p)]:
            negative=active & (cost<0)
            market_negative=maximum(negative)>0
            source_flag=m.effective_cost_ok.to_numpy() if kind=='effective' else m.manufacturer_cost_ok.to_numpy()
            assert np.array_equal(~market_negative,source_flag)
            expected=int((m.numerical_ok & source_flag).sum())
            assert expected==saved_diag.loc[(e.model,rule),f'{kind}_nonnegative']
            cause=np.full(len(d),'nonnegative',dtype=object)
            cause[negative & (p-solo_effective<0)]='own_elasticity_already_insufficient'
            cause[negative & (p-solo_effective>=0) & (eff<0)]='portfolio_crosses_retail_price'
            cause[negative & (eff>=0)]='retailer_wedge_only'
            assert not (negative & (cause=='nonnegative')).any()
            assert (rule=='dollar' and kind=='manufacturer') or not (cause=='retailer_wedge_only').any()
            ratio=mu/denominator
            market_ratio=maximum(np.where(active,ratio,0))
            neg_by_market=total(negative.astype(int))
            for scope,scope_mask in scopes.items():
                valid=scope_mask & active
                market_mask=scope_mask[starts]
                neg_total=float(w[valid & negative].sum())
                all_packages=float(w[valid].sum())
                for label in ['own_elasticity_already_insufficient','portfolio_crosses_retail_price','retailer_wedge_only']:
                    z=valid & (cause==label)
                    stages.append(dict(cell=e.model,retailer=rule,scope=scope,cost_kind=kind,cause=label,
                        rows=int(z.sum()),packages=float(w[z].sum()),fraction_of_active_packages=float(w[z].sum()/all_packages),
                        fraction_of_negative_packages=float(w[z].sum()/neg_total) if neg_total else 0.))
                thresholds.append(dict(cell=e.model,retailer=rule,scope=scope,cost_kind=kind,
                    passing_markets=int((market_mask & ~market_negative).sum()),markets=int(market_mask.sum()),
                    factor_market_median=float(np.median(market_ratio[market_mask])),
                    factor_package_weighted_p50=quantile(market_ratio[market_mask],market_packages[market_mask],.5),
                    factor_package_weighted_p95=quantile(market_ratio[market_mask],market_packages[market_mask],.95),
                    factor_all_markets=float(market_ratio[market_mask].max()),
                    parameter_abs=float(abs(e.beta_price)),threshold_parameter_all=float(abs(e.beta_price)*market_ratio[market_mask].max())))
                for level,groups in group_maps.items():
                    for key,idx in groups:
                        ix=idx[scope_mask[idx]]
                        if not len(ix):continue
                        wn=w[ix]; neg=negative[ix]
                        grouped_negative=np.bincount(market[ix],weights=neg.astype(int),minlength=M)
                        owner_hit=grouped_negative>0
                        row=dict(cell=e.model,retailer=rule,scope=scope,cost_kind=kind,level=level,key=key,
                            rows=len(ix),packages=float(wn.sum()),negative_rows=int(neg.sum()),negative_packages=float(wn[neg].sum()),
                            negative_package_fraction=float(wn[neg].sum()/wn.sum()),
                            share_of_all_negative_packages=float(wn[neg].sum()/neg_total) if neg_total else 0.,
                            markets_present=int(len(np.unique(market[ix]))),markets_with_negative=int(owner_hit.sum()),
                            sole_failing_group_markets=int((owner_hit & (grouped_negative==neg_by_market)).sum()),
                            price_weighted=float(np.average(p[ix],weights=wn)),aac_weighted=float(np.average(aac[ix],weights=wn)),
                            q_weighted=float(np.average(q[ix],weights=wn)),cost_weighted=float(np.average(cost[ix],weights=wn)),
                            base_markup_effective_weighted=float(np.average(rawbase[ix],weights=wn)),
                            singleton_markup_effective_weighted=float(np.average(solo_effective[ix],weights=wn)),
                            portfolio_markup_effective_weighted=float(np.average(mu[ix]/q[ix],weights=wn)),
                            portfolio_increment_weighted=float(np.average(mu[ix]/q[ix]-solo_effective[ix],weights=wn)),
                            retailer_wedge_weighted=float(np.average(p[ix]-aac[ix],weights=wn)),
                            owner_inside_share_weighted=float(np.average(sf[ix]/S[market[ix]],weights=wn)))
                        if level=='upc':
                            z=d.iloc[ix[0]]
                            row.update(upc=z.upc,description=z.descrip,owner=z.owner,pack_count=int(z.pack_count))
                        agg.append(row)
                markets.append(dict(cell=e.model,retailer=rule,scope=scope,cost_kind=kind,
                    failed_markets=int((market_negative & market_mask).sum()),
                    rescued_by_retailer_wedge_rows=int((valid & (eff<0) & (manufacturer>=0)).sum()),
                    negative_packages=neg_total,active_packages=all_packages))
            # Auditable case examples selected by deterministic severity/exposure rules.
            ni=np.flatnonzero(negative & scopes['common_numerically_valid'])
            for method,order in [('lowest_cost',ni[np.argsort(cost[ni])[:20]]),('largest_package_exposure',ni[np.argsort(-w[ni])[:20]])]:
                for rank,j in enumerate(order,1):
                    examples.append(dict(cell=e.model,retailer=rule,cost_kind=kind,selection=method,rank=rank,
                        store=int(d.store.iloc[j]),week=int(d.week.iloc[j]),market_id=str(d.market_id.iloc[j]),upc=d.upc.iloc[j],
                        description=d.descrip.iloc[j],owner=d.owner.iloc[j],pack_count=int(d.pack_count.iloc[j]),
                        packages=float(w[j]),price=float(p[j]),aac=float(aac[j]),q=float(q[j]),share=float(s[j]),
                        inside_share=float(S[market[j]]),owner_inside_share=float(sf[j]/S[market[j]]),
                        own_elasticity=float(own_elasticity[j]),singleton_effective_markup=float(solo_effective[j]),
                        portfolio_effective_markup=float(mu[j]/q[j]),effective_cost=float(eff[j]),manufacturer_cost=float(manufacturer[j]),cause=cause[j]))
        if e.rho==0:
            margin_cases[(e.model,rule)]=(mu,eff,manufacturer)
        print(e.model,rule,'checked',flush=True)
    # Four rho-zero pairs: exact accounting bridge, not new equilibria.
    for e in estimates[estimates.rho.eq(0)].itertuples():
        mu_d,ce_d,cm_d=margin_cases[(e.model,'dollar')]
        mu_p,ce_p,cm_p=margin_cases[(e.model,'percentage')]
        wholesale_shift=q_saved*p-aac
        markup_shift=mu_d-mu_p
        bridge_error=float(np.max(abs((cm_p-cm_d)[active]-(wholesale_shift+markup_shift)[active])))
        effective_error=float(np.max(abs((ce_p-ce_d)[active]-(mu_d-mu_p/q_saved)[active])))
        discrepancies['retailer_bridge']=max(discrepancies['retailer_bridge'],bridge_error,effective_error)
        for scope,sc in scopes.items():
            for level,groups in group_maps.items():
                for key,idx in groups:
                    ix=idx[sc[idx]]
                    if not len(ix):continue
                    wp=w[ix]; negd=cm_d[ix]<0; negp=cm_p[ix]<0
                    bridges.append(dict(cell=e.model,scope=scope,level=level,key=key,packages=float(wp.sum()),
                        dollar_negative_fraction=float(wp[negd].sum()/wp.sum()),percentage_negative_fraction=float(wp[negp].sum()/wp.sum()),
                        rescued_fraction=float(wp[negd & ~negp].sum()/wp.sum()),new_failure_fraction=float(wp[~negd & negp].sum()/wp.sum()),
                        cost_change_weighted=float(np.average((cm_p-cm_d)[ix],weights=wp)),
                        wholesale_level_component=float(np.average(wholesale_shift[ix],weights=wp)),
                        markup_component=float(np.average(markup_shift[ix],weights=wp)),
                        effective_cost_change_weighted=float(np.average((ce_p-ce_d)[ix],weights=wp))))
            for wholesale,baseprice in [('observed_AAC',aac),('median_margin_qp',q_saved*p)]:
                for markup,mu in [('dollar_FOC',mu_d),('percentage_FOC',mu_p)]:
                    neg=active & ((baseprice-mu)<0)
                    ix=sc & active
                    margin_rows.append(dict(cell=e.model,scope=scope,wholesale=wholesale,markup=markup,
                        negative_package_fraction=float(w[ix & neg].sum()/w[ix].sum()),
                        passing_markets=int((sc[starts] & ~(maximum(neg)>0)).sum()),
                        interpretation='saved scenario' if (wholesale=='observed_AAC')==(markup=='dollar_FOC') else 'accounting hybrid only; not a structural scenario'))
    assert all(v<1e-9 for v in discrepancies.values()),discrepancies
    # Group aggregates must exactly partition all active negative package mass.
    df=pd.DataFrame(agg)
    keys=['cell','retailer','scope','cost_kind']
    ref=df[df.level.eq('all')].set_index(keys).negative_packages.sort_index()
    for level in ['upc','manufacturer','pack']:
        check=df[df.level.eq(level)].groupby(keys).negative_packages.sum().sort_index()
        np.testing.assert_allclose(check,ref,rtol=1e-12,atol=1e-6)
    df.to_csv(out/'group_diagnostics.csv',index=False)
    pd.DataFrame(stages).to_csv(out/'failure_decomposition.csv',index=False)
    pd.DataFrame(markets).to_csv(out/'market_summary.csv',index=False)
    pd.DataFrame(thresholds).to_csv(out/'coefficient_thresholds.csv',index=False)
    pd.DataFrame(examples).to_csv(out/'case_examples.csv',index=False)
    pd.DataFrame(bridges).to_csv(out/'retailer_bridge.csv',index=False)
    pd.DataFrame(margin_rows).to_csv(out/'retailer_accounting_2x2.csv',index=False)
    save(out/'validation.json',dict(passed=True,scenarios=len(scenarios),rows=len(d),markets=M,
        common_markets=int(common.sum()),active_upcs=int(d.loc[active,'upc'].nunique()),
        max_discrepancies=discrepancies,group_partition_checks=['manufacturer','upc','pack'],
        numerical_solvers_called=0,estimations_run=0))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run-id',required=True);args=ap.parse_args()
    assert args.run_id and all(c.isalnum() or c in '_-' for c in args.run_id)
    out=ROOT/'runs'/args.run_id;out.mkdir(parents=True,exist_ok=False)
    before=inventory();save(out/'protected_before.json',before)
    shutil.copyfile(__file__,out/'diagnose_code.py')
    save(out/'scope.json',dict(run_id=args.run_id,source_run=SOURCE.relative_to(PROJECT).as_posix(),
        branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip(),
        base_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        collaborator='Yifan / Codex',platform=platform.platform(),python=platform.python_version(),
        code_sha256=digest(Path(__file__)),uv_lock_sha256=digest(PROJECT/'uv.lock'),
        scope='All saved 20 scenarios. No re-estimation, new equilibrium, clipped costs, changed ownership, or data deletion.',
        grouping='Active manufacturers only; UPC, manufacturer and pack; all input markets and common numerical intersection.',
        decomposition='Ordered accounting: singleton retail feasibility, portfolio retail crossing, retailer-wedge-only manufacturer crossing. Not causal attribution.',
        retailer='Four saved rho-zero pairs; exact wholesale-level/markup bridge plus explicitly labeled nonstructural 2x2 accounting hybrids.',
        thresholds='Algebraic price-sensitivity multiplier at fixed shares/rho/form/q; not estimated parameters, uncertainty bounds or recommended adjustments.',
        examples='20 lowest costs and 20 largest negative-cost package exposures per cell/rule/cost kind in common numerical sample.',
        sharing='New diagnosis local, uncommitted/unpushed; source run committed and verified on origin/main at base_commit.'))
    status={'complete':False};start=time.monotonic()
    try:
        run(out);status['complete']=True
    except Exception:
        (out/'traceback.txt').write_text(traceback.format_exc(),encoding='utf-8');raise
    finally:
        after=inventory();changed=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
        save(out/'preservation.json',dict(protected_files=len(before),changed=changed))
        status.update(elapsed_seconds=time.monotonic()-start,baseline_preserved=not changed)
        save(out/'status.json',status)
        assert not changed,changed


if __name__=='__main__':main()
