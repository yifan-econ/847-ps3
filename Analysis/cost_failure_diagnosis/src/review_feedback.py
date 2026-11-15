"""Verify Fable's feedback using saved costs and fixed-residual IV accounting.

No new specification, estimation routine, equilibrium or sample replacement.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
import traceback
import numpy as np
import pandas as pd

PROJECT=Path(__file__).resolve().parents[3]
SOURCE=PROJECT/'Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01'
DIAG=PROJECT/'Analysis/cost_failure_diagnosis/runs/2026-11-15_costdiag_01'
sys.path.insert(0,str(PROJECT/'Analysis/cost_iv_v2/src'))
from estimator import absorb


def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def save(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False),encoding='utf-8')


def inventory(out):
    return {p.relative_to(PROJECT).as_posix():sha(p) for folder in ['Analysis','Archive','Data','Paper']
        for p in (PROJECT/folder).rglob('*') if p.is_file() and out not in p.parents
        and p.resolve()!=Path(__file__).resolve() and '__pycache__' not in p.parts and p.suffix not in ['.pyc','.pyo']}


def review(out):
    d=pd.read_csv(SOURCE/'product_inputs.csv.gz',dtype={'upc':str})
    counts=d.groupby(['store','upc','price_pack']).size().rename('frequency').reset_index()
    mode=counts.sort_values(['store','upc','frequency','price_pack'],ascending=[True,True,False,True]).drop_duplicates(['store','upc'])
    mode=mode[['store','upc','price_pack']].rename(columns={'price_pack':'modal_price'})
    d=d.merge(mode,on=['store','upc'],validate='many_to_one',sort=False)
    mode.to_csv(out/'modal_prices.csv',index=False)
    market,names=pd.factorize(d.market_id,sort=False)
    starts=np.r_[0,np.flatnonzero(np.diff(market))+1];M=len(starts)
    total=lambda a:np.add.reduceat(np.asarray(a),starts)
    p=d.price_pack.to_numpy();s=d.share.to_numpy();w=d.move.to_numpy();aac=d.aac_pack.to_numpy();q=d.q_percent.to_numpy()
    f=d.firm.to_numpy();active=f>0;single=d.pack_count.eq(1).to_numpy();scott=single & (f==1)
    S=total(s);g=market*7+f
    common=pd.read_csv(DIAG/'market_exposure.csv').common_numerically_valid.to_numpy()
    assert M==7996 and common.sum()==7960 and len(d)==259986
    scopes={'full_input':np.ones(len(d),bool),'common_numerical':common[market]}
    below=p<.95*d.modal_price.to_numpy()-1e-10
    strict=p<d.modal_price.to_numpy()-1e-10
    promo_masks={'below_95pct_modal':below,'not_below_95pct_modal':~below,
        'strictly_below_modal':strict,'weeks_99_110':d.week.isin([99,110]).to_numpy()}
    estimates=pd.read_csv(SOURCE/'estimates_corrected.csv')
    cells=[];orders=[];signs=[];elasticities=[];identities=[];promotion_costs=[]
    for e in estimates.itertuples():
        h=1/(1-e.rho);A=1+(h-1)/S;b=np.full(len(d),e.beta_price) if e.form=='linear' else e.beta_price/p
        solo=-1/(b*(h-A[market]*s))
        own=p*b*(h-A[market]*s)
        with np.load(SOURCE/'cells'/e.model/'dollar_simulation.npz') as z:
            mu=z['markup'];cm=z['manufacturer_cost'];ce=z['effective_cost']
        neg=active & (cm<0)
        # Joint inequalities, not sequential causal attribution.
        classification=np.select([solo>p,(solo>aac)&(mu>p),(solo>aac)&(mu<=p),(solo<=aac)&(mu>p),(solo<=aac)&(mu<=p)],
            ['singleton_above_retail','singleton_above_AAC_portfolio_above_retail',
             'singleton_above_AAC_portfolio_at_or_below_retail','singleton_at_or_below_AAC_portfolio_above_retail',
             'singleton_at_or_below_AAC_portfolio_at_or_below_retail'],default='unclassified')
        assert not (neg & (classification=='unclassified')).any()
        for scope,sc in scopes.items():
            bad=neg & sc;volume=float(w[bad].sum())
            for label in ['singleton_above_retail','singleton_above_AAC_portfolio_above_retail',
                          'singleton_above_AAC_portfolio_at_or_below_retail','singleton_at_or_below_AAC_portfolio_above_retail',
                          'singleton_at_or_below_AAC_portfolio_at_or_below_retail']:
                ix=bad & (classification==label)
                cells.append(dict(cell=e.model,scope=scope,classification=label,rows=int(ix.sum()),packages=float(w[ix].sum()),
                    fraction_of_negative_packages=float(w[ix].sum()/volume) if volume else None))
            for order,masks in [('portfolio_then_wedge',[(solo>p),(solo<=p)&(mu>p),(mu<=p)]),
                                ('wedge_then_portfolio',[(solo>p),(solo<=p)&(solo>aac),(solo<=aac)])]:
                # With negative retail margins, singleton>p need not imply singleton>AAC.
                # Give alternate-order comparisons only where AAC<=p; retain all joint cells above.
                eligible=bad & (aac<=p)
                denom=float(w[eligible].sum())
                for stage,mask in zip(['singleton_retail_failure','second_step_crossing','third_step_crossing'],masks):
                    orders.append(dict(cell=e.model,scope=scope,order=order,stage=stage,
                        packages=float(w[eligible&mask].sum()),fraction=float(w[eligible&mask].sum()/denom) if denom else None,
                        eligible_negative_packages=denom,negative_packages_excluded_for_AAC_above_price=float(w[bad&(aac>p)].sum())))
            for group,ix in [('all_single_rolls',sc&single),('active_single_rolls',sc&single&active),('Scott_single_rolls',sc&scott)]:
                elasticities.append(dict(cell=e.model,scope=scope,group=group,packages=float(w[ix].sum()),weighted_own_elasticity=float(np.average(own[ix],weights=w[ix]))))
            if e.rho==0:
                for label,mask in [('below_95pct_modal',below),('not_below_95pct_modal',~below)]:
                    ix=sc&active&mask
                    promotion_costs.append(dict(cell=e.model,scope=scope,group=label,negative_package_incidence=float(w[ix&neg].sum()/w[ix].sum()),
                        contribution_to_all_negative_packages=float(w[ix&neg].sum()/volume) if volume else None,
                        qp_minus_AAC_package_weighted=float(np.average((q*p-aac)[ix],weights=w[ix]))))
        for rule in ['dollar']+(['percentage'] if e.rho==0 else []):
            m=pd.read_csv(SOURCE/'cells'/e.model/f'{rule}_markets.csv.gz')
            if rule=='dollar':cost=cm
            else:
                with np.load(SOURCE/'cells'/e.model/'percentage_simulation.npz') as z:cost=z['manufacturer_cost']
            for scope,sc in {**scopes,'own_numerical':m.numerical_ok.to_numpy()[market]}.items():
                ix=sc&scott;bad=ix&(cost<0)
                signs.append(dict(cell=e.model,retailer=rule,scope=scope,scott_single_rows=int(ix.sum()),
                    negative_scott_single_rows=int(bad.sum()),negative_package_fraction=float(w[bad].sum()/w[ix].sum()),
                    negative_scott_single_markets=int((total(bad)>0).sum())))
        if e.rho==0:
            with np.load(SOURCE/'cells'/e.model/'percentage_simulation.npz') as z:
                mup=z['markup'];cep=z['effective_cost'];cmp=z['manufacturer_cost']
            # Exact general mean identity weights q by s/(-b), not always by s.
            group_s=np.bincount(g,weights=s,minlength=M*7)
            qbar=np.bincount(g,weights=s*q,minlength=M*7)/np.maximum(group_s,1e-300)
            weight=s/(-b)
            qbar_b=np.bincount(g,weights=weight*q,minlength=M*7)/np.maximum(np.bincount(g,weights=weight,minlength=M*7),1e-300)
            mean_d=np.bincount(g,weights=s*mu,minlength=M*7)/np.maximum(group_s,1e-300)
            mean_p=np.bincount(g,weights=s*mup,minlength=M*7)/np.maximum(group_s,1e-300)
            occupied=(group_s>0)&(np.tile(np.arange(7),M)>0)
            general_error=float(np.max(abs(mean_p[occupied]-mean_d[occupied]*qbar_b[occupied])))
            package_error=float(np.max(abs(mean_p[occupied]-mean_d[occupied]*qbar[occupied])))
            assert general_error<1e-10
            if e.form=='linear':assert package_error<1e-10
            assert np.array_equal(cmp[active]<0,cep[active]<0)
            for scope,sc in scopes.items():
                ix=sc&active
                identities.append(dict(cell=e.model,scope=scope,active_rows=int(ix.sum()),effective_sign_flips=int(((ce<0)!=(cep<0))[ix].sum()),
                    mean_identity_general_max_error=general_error,mean_identity_package_q_max_error=package_error,
                    dollar_manufacturer_negative_fraction=float(np.average(cm[ix]<0,weights=w[ix])),
                    percentage_manufacturer_negative_fraction=float(np.average(cmp[ix]<0,weights=w[ix])),
                    same_AAC_percentage_markup_negative_fraction=float(np.average((aac-mup)[ix]<0,weights=w[ix])),
                    dollar_effective_negative_fraction=float(np.average(ce[ix]<0,weights=w[ix])),
                    percentage_effective_negative_fraction=float(np.average(cep[ix]<0,weights=w[ix]))))
    pd.DataFrame(cells).to_csv(out/'joint_cost_classification.csv',index=False)
    pd.DataFrame(orders).to_csv(out/'both_accounting_orders.csv',index=False)
    pd.DataFrame(signs).to_csv(out/'scott_cost_claim_check.csv',index=False)
    pd.DataFrame(elasticities).to_csv(out/'single_roll_elasticities.csv',index=False)
    pd.DataFrame(identities).to_csv(out/'retailer_identity_checks.csv',index=False)
    pd.DataFrame(promotion_costs).to_csv(out/'promotion_costs.csv',index=False)
    # FWL moment reconstruction: same full-sample FE and deal residualization.
    # Subsets sum these fixed residual products; no subgroup reabsorption/refit.
    groups=[pd.factorize(pd.MultiIndex.from_frame(d[['store','upc']]),sort=False)[0],pd.factorize(d.week,sort=False)[0]]
    y=np.log(s)-np.log1p(-S[market])
    contributions=[];coef_errors=[]
    for e in estimates[estimates.rho.eq(0)].itertuples():
        x=p if e.form=='linear' else np.log(p)
        z=d.aac_pack.to_numpy() if e.iv=='aac' else d.other_zone_price.to_numpy()
        if e.form=='log':z=np.log(z)
        residual,iterations,error=absorb(np.column_stack([y,x,z,d.deal.to_numpy()]),groups)
        control=residual[:,3];r=residual[:,:3]-np.outer(control,control@residual[:,:3]/(control@control))
        zy=r[:,2]*r[:,0];zx=r[:,2]*r[:,1]
        ratio=float(zy.sum()/zx.sum());coef_errors.append(abs(ratio-e.beta_price));assert abs(ratio-e.beta_price)<1e-8
        for label,mask in promo_masks.items():
            complement_ratio=float(zy[~mask].sum()/zx[~mask].sum())
            contributions.append(dict(cell=e.model,group=label,rows=int(mask.sum()),row_fraction=float(mask.mean()),
                instrument_price_sum=float(zx[mask].sum()),instrument_outcome_sum=float(zy[mask].sum()),
                fraction_instrument_price_sum=float(zx[mask].sum()/zx.sum()),fraction_instrument_outcome_sum=float(zy[mask].sum()/zy.sum()),
                full_coefficient_reconstructed=ratio,saved_coefficient=e.beta_price,fixed_residual_complement_ratio=complement_ratio,
                absorption_iterations=iterations,absorption_error=error))
    pd.DataFrame(contributions).to_csv(out/'iv_moment_contributions.csv',index=False)
    # Physical rolls per trip are volume diagnostics, not choice shares.
    rolls=w*d.pack_count.to_numpy()
    md=d.iloc[starts][['market_id','store','week','market_size']].reset_index(drop=True)
    md['packages']=total(w);md['rolls']=total(rolls);md['scott_single_packages']=total(np.where(scott,w,0))
    md['other_rolls']=total(np.where(scott,0,rolls))
    md['scott_single_revenue']=total(np.where(scott,w*p,0));md['scott_single_modal_revenue']=total(np.where(scott,w*d.modal_price.to_numpy(),0))
    md['scott_discount_present']=total((scott&below).astype(int))>0
    md['packages_per_trip']=md.packages/md.market_size;md['rolls_per_trip']=md.rolls/md.market_size
    md['common_numerical']=common
    md.to_csv(out/'market_purchase_volume.csv',index=False)
    wk=md.groupby('week',as_index=False).agg(stores=('store','nunique'),traffic=('market_size','sum'),packages=('packages','sum'),rolls=('rolls','sum'),
        scott_single_packages=('scott_single_packages','sum'),other_rolls=('other_rolls','sum'),scott_single_revenue=('scott_single_revenue','sum'),
        scott_single_modal_revenue=('scott_single_modal_revenue','sum'),stores_with_scott_discount=('scott_discount_present','sum'))
    wk['packages_per_trip']=wk.packages/wk.traffic;wk['rolls_per_trip']=wk.rolls/wk.traffic;wk['scott_single_per_trip']=wk.scott_single_packages/wk.traffic
    wk['other_rolls_per_trip']=wk.other_rolls/wk.traffic;wk['scott_single_price']=wk.scott_single_revenue/wk.scott_single_packages
    wk['scott_single_modal_price']=wk.scott_single_modal_revenue/wk.scott_single_packages
    wk.to_csv(out/'weekly_purchase_volume.csv',index=False)
    event=[]
    for week in [99,110]:
        for label,mask in [('eight_weeks_before',wk.week.between(week-8,week-1)),('event_week',wk.week.eq(week)),('eight_weeks_after',wk.week.between(week+1,week+8))]:
            u=wk[mask]
            event.append(dict(event_week=week,window=label,weeks=len(u),scott_single_per_trip=float(u.scott_single_packages.sum()/u.traffic.sum()),
                other_rolls_per_trip=float(u.other_rolls.sum()/u.traffic.sum()),rolls_per_trip=float(u.rolls.sum()/u.traffic.sum())))
    pd.DataFrame(event).to_csv(out/'descriptive_event_windows.csv',index=False)
    summary=dict(passed=True,rows=len(d),markets=M,common_markets=int(common.sum()),
        modal_definition='Full v5 sample store-by-UPC modal package price, lowest price breaks ties; discount <95% of mode minus 1e-10.',
        discount_row_fraction=float(below.mean()),unflagged_discount_package_fraction=float(w[below&d.deal.eq(0).to_numpy()].sum()/w.sum()),
        median_rolls_per_trip=float(md.rolls_per_trip.median()),markets_above_one_roll=int((md.rolls_per_trip>1).sum()),
        markets_above_half_roll=int((md.rolls_per_trip>.5).sum()),weekly_scott_single_median_per_trip=float(wk.scott_single_per_trip.median()),
        excluded_inside_share_min=float(S[~common].min()),included_inside_share_max=float(S[common].max()),
        max_existing_coefficient_reconstruction_error=float(max(coef_errors)),
        new_specifications_estimated=0,equilibrium_solves=0,
        note='Fixed-residual subset ratios are descriptive, not subgroup estimates. Physical rolls/trip are not purchase probabilities. Event windows do not identify stockpiling.')
    save(out/'verification.json',summary)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--review-id',required=True);args=ap.parse_args()
    assert args.review_id and all(c.isalnum() or c in '_-' for c in args.review_id)
    out=PROJECT/'Analysis/cost_failure_diagnosis/reviews'/args.review_id;out.mkdir(parents=True,exist_ok=False)
    before=inventory(out);save(out/'protected_before.json',before);shutil.copyfile(__file__,out/'review_code.py')
    save(out/'scope.json',dict(review_id=args.review_id,branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip(),
        base_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),code_sha256=sha(Path(__file__)),
        scope='Check supplied Fable feedback: joint cost inequalities/both orders, retailer identities, promotion-related fixed-residual moment contributions, package/roll volume and scope of proposed claims. Preserve source runs. No new specification or equilibrium.',
        source_run=SOURCE.relative_to(PROJECT).as_posix(),source_diagnosis=DIAG.relative_to(PROJECT).as_posix()))
    start=time.monotonic();status={'complete':False}
    try:review(out);status['complete']=True
    except Exception:
        (out/'traceback.txt').write_text(traceback.format_exc(),encoding='utf-8');raise
    finally:
        after=inventory(out);changed=sorted(p for p in before.keys()|after.keys() if before.get(p)!=after.get(p))
        save(out/'preservation.json',dict(protected_files=len(before),changed=changed));status.update(elapsed_seconds=time.monotonic()-start,preserved=not changed)
        save(out/'status.json',status);assert not changed,changed


if __name__=='__main__':main()
