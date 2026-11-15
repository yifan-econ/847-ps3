"""Reproducible positive-sales aggregate logit; exploratory external-cost instruments."""
from pathlib import Path
import sys,json,hashlib,urllib.request
import numpy as np
import pandas as pd
from scipy.stats import chi2
from estimator import fit,absorb,codes,cluster_meat,fe_rank
ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[1]
OUT=ROOT/'results'
OUT.mkdir(exist_ok=True,parents=True)

def download():
    manifest=[]
    for sid in ['WPU0911','WPU072205']:
        path=ROOT/f'data/raw/{sid}.csv'
        url=f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd=1988-01-01&coed=1998-12-31'
        if not path.exists(): path.write_bytes(urllib.request.urlopen(url,timeout=60).read())
        q=pd.read_csv(path,na_values='.')
        manifest.append(dict(series=sid,url=url,source='BLS via FRED',retrieved_date='2026-11-14',sha256=hashlib.sha256(path.read_bytes()).hexdigest(),first=q.iloc[0,0],last=q.iloc[-1,0],nonmissing=int(q[sid].notna().sum())))
    (ROOT/'data/raw/manifest.json').write_text(json.dumps(manifest,indent=2))

def ar_zero(d,ivs,controls):
    """Anderson-Rubin test of beta_price=0; two-way store/month cluster Wald."""
    groups=[codes(pd.MultiIndex.from_frame(d[['store','product_id']])),codes(d.week)]
    a,_,_=absorb(d[['y',*ivs,*controls]].to_numpy(float),groups)
    y=a[:,0];z=a[:,1:];b=np.linalg.lstsq(z,y,rcond=None)[0];u=y-z@b
    inv=np.linalg.inv(z.T@z);n=len(d);df=fe_rank(groups)+z.shape[1]
    gs=codes(d.store);gt=codes(d.cluster_time);gst=codes(pd.MultiIndex.from_frame(d[['store','cluster_time']]))
    score=z*u[:,None]
    meat=cluster_meat(score,gs,n,df)+cluster_meat(score,gt,n,df)-cluster_meat(score,gst,n,df)
    cov=inv@meat@inv;q=len(ivs);v=cov[:q,:q]
    if np.linalg.eigvalsh(v).min()<=0: return dict(ar_beta0_chi2=np.nan,ar_beta0_p=np.nan,ar_covariance_psd=False)
    stat=float(b[:q]@np.linalg.solve(v,b[:q]))
    return dict(ar_beta0_chi2=stat,ar_beta0_p=float(chi2.sf(stat,q)),ar_covariance_psd=True)

def main():
    download()
    base=pd.read_csv(PROJECT/'Archive/ps3_v1/results/clean_upc_store_week.csv.gz',dtype={'product_id':str})
    assert not base.duplicated(['store','upc','week']).any()
    assert base.move.gt(0).all() and base.price_pack.gt(0).all()
    # Retain original traffic denominator; single-roll purchases become outside in multi sample.
    costs=None
    for sid in ['WPU0911','WPU072205']:
        a=pd.read_csv(ROOT/f'data/raw/{sid}.csv',na_values='.')
        a['month']=pd.to_datetime(a.iloc[:,0]).dt.to_period('M').astype(str)
        a=a[['month',sid]]
        costs=a if costs is None else costs.merge(a,on='month',how='outer',validate='one_to_one')
    costs.to_csv(ROOT/'data/processed/monthly_cost_indices.csv',index=False)
    base['month']=pd.to_datetime(base.date_start).dt.to_period('M').astype(str)
    base=base.merge(costs,on='month',how='left',validate='many_to_one')
    # Actual week-start month; no interpolation or backfilling of missing plastics series.
    base['z_pulp_rolls']=base.WPU0911/100*base.pack_count
    # Rough surface-area scaling of wrapping with package volume; a sensitivity proxy only.
    base['z_plastic_surface']=base.WPU072205/100*base.pack_count.pow(2/3)
    base['cluster_time']=base.month
    base['trend']=(base.week-base.week.min())/52
    summaries=[];coeff=[];audit=[]
    for sample in ['all_packs','multi_packs']:
        d=base.copy() if sample=='all_packs' else base.loc[base.pack_count.gt(1)].copy()
        total=d.groupby('market_id').move.transform('sum')
        d['inside_quantity']=total;d['outside_share']=1-total/d.market_size
        d['share']=d.move/d.market_size
        assert d.outside_share.between(0,1,inclusive='neither').all()
        d['y']=np.log(d.share)-np.log(d.outside_share)
        assert np.allclose(d.groupby('market_id').share.sum()+d.groupby('market_id').outside_share.first(),1)
        audit.append(dict(sample=sample,n=len(d),products=int(d.upc.nunique()),months=int(d.month.nunique()),first=d.date_start.min(),last=d.date_start.max(),plastic_missing_rows=int(d.WPU072205.isna().sum()),single_roll_purchases_inside=bool(d.pack_count.eq(1).any())))
        specs=[('OLS',None,d,('deal',)),('AAC_IV',['aac_pack'],d,('deal',)),('PULP_IV',['z_pulp_rolls'],d,('deal',))]
        joint=d.dropna(subset=['z_pulp_rolls','z_plastic_surface']).copy()
        specs.extend([('OLS_joint_sample',None,joint,('deal',)),('PULP_IV_joint_sample',['z_pulp_rolls'],joint,('deal',)),('PULP_PLASTIC_IV',['z_pulp_rolls','z_plastic_surface'],joint,('deal',))])
        # Within-pack linear trends sensitivity to size-specific demand trends.
        for pack in sorted(d.pack_count.unique())[1:]: d[f'trend_pack_{int(pack)}']=d.trend*d.pack_count.eq(pack)
        tc=tuple(['deal']+[c for c in d if c.startswith('trend_pack_')])
        specs.append(('PULP_IV_pack_trends',['z_pulp_rolls'],d,tc))
        savecols=['store','week','upc','month','pack_count','price_pack','share','outside_share','y','deal','aac_pack','WPU0911','WPU072205','z_pulp_rolls','z_plastic_surface']
        d[savecols].to_csv(ROOT/f'data/processed/{sample}_estimation_panel.csv.gz',index=False)
        for name,iv,data,controls in specs:
            label=sample+'__'+name
            print('Estimating',label,len(data),flush=True)
            needed=['y','price_pack',*controls]+([] if iv is None else iv)
            dd=data.dropna(subset=needed).copy()
            s,c=fit(dd,label,iv=iv,controls=controls)
            s.update(sample=sample,clustering='store and calendar month',months=int(dd.month.nunique()))
            if iv:
                s['first_stage_wald_p']=float(chi2.sf(s['first_stage_wald_chi2'],len(iv))) if s['first_stage_wald_chi2']>=0 else np.nan
                s.update(ar_zero(dd,iv,controls))
            summaries.append(s);coeff.extend(c)
            pd.DataFrame(summaries).to_csv(OUT/'estimates.csv',index=False)
            pd.DataFrame(coeff).to_csv(OUT/'coefficients_first_stages.csv',index=False)
            print(label,'beta',s['beta_price'],'se',s['se_price'],'F-like',s.get('first_stage_wald_per_iv'),flush=True)
    pd.DataFrame(audit).to_csv(OUT/'sample_audit.csv',index=False)
    # Original output is a comparison target, not evidence of fresh raw-data reproduction.
    old=pd.read_csv(PROJECT/'Archive/ps3_v1/results/estimates.csv').set_index('model').loc['UPC_FE_OLS','beta_price']
    new=next(s['beta_price'] for s in summaries if s['model']=='all_packs__OLS')
    assert abs(old-new)<1e-7,(old,new)
    (OUT/'validation.json').write_text(json.dumps(dict(original_ols_beta=float(old),replicated_ols_beta=new,unique_product_market=True,shares_sum_to_one=True,raw_data_unchanged=True,base_panel_source='archived v1 cleaned panel; not freshly regenerated from movement data',zero_sales_policy='Preserve source zero records; exclude from log-share estimation, availability unresolved'),indent=2))
    print('COMPLETE',flush=True)
if __name__=='__main__': main()
