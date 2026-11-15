#!/usr/bin/env python3
"""Dominick's TTI first-pass aggregate logit. No SAS/Stata installation required.

Run: python src/run_logit.py --data-dir '/path/to/Data/Dominick'
All price coefficients use + beta_price * price, so downward demand means beta < 0.
This is an exploratory baseline, not a validated merger model.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import time
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse.csgraph import connected_components

ROOT = Path(__file__).resolve().parents[1]


def codes(s):
    return pd.factorize(s, sort=False)[0]


def absorb(a, groups, tol=1e-10, max_iter=1000):
    """Alternating projections onto complements of categorical fixed effects."""
    a = np.array(a, dtype=float, copy=True)
    if not groups:
        return a, 0, 0.0
    counts = [np.bincount(g) for g in groups]
    for iteration in range(max_iter):
        change = 0.0
        for g, count in zip(groups, counts):
            for k in range(a.shape[1]):
                means = np.bincount(g, weights=a[:, k]) / count
                change = max(change, float(np.max(np.abs(means))))
                a[:, k] -= means[g]
        if change < tol:
            return a, iteration + 1, change
    raise RuntimeError(f'Fixed effect absorption failed: {change}')


def fe_rank(groups):
    if not groups:
        return 0
    if len(groups) == 1:
        return int(groups[0].max() + 1)
    a, b = groups
    na, nb = int(a.max()+1), int(b.max()+1)
    r, c = a, b+na
    graph = sparse.coo_matrix((np.ones(len(r)), (r, c)), shape=(na+nb,na+nb))
    components = connected_components(graph.tocsr(), directed=False, return_labels=False)
    return na + nb - components


def cluster_meat(score, g, n, df):
    ng = int(g.max()+1)
    sums = np.zeros((ng, score.shape[1]))
    np.add.at(sums, g, score)
    return (sums.T @ sums) * (ng/(ng-1)) * ((n-1)/(n-df))


def fit(d, label, iv=None, fe='store_product_week', price='price_pack', controls=('deal',)):
    """2SLS with absorbed FE; CGM two-way store/week cluster covariance.

    First stage reports excluded-IV two-way cluster Wald chi-square and partial R2.
    Wald/number-IV is NOT a Stock-Yogo or Kleibergen-Paap statistic.
    """
    needed = ['y',price,*controls] + ([] if iv is None else iv)
    d = d.dropna(subset=needed).copy()
    if fe in ('store_product_week','store_product_market'):
        time_group=d.week if fe=='store_product_week' else pd.MultiIndex.from_frame(d[['store','week']])
        groups = [codes(pd.MultiIndex.from_frame(d[['store','product_id']])), codes(time_group)]
        names = [price,*controls]
        raw = d[['y',*names,*([] if iv is None else iv)]].to_numpy(float)
        arr, iters, err = absorb(raw,groups)
        rank = fe_rank(groups)
    elif fe == 'none':
        groups = []
        names = [price,*controls,'constant']
        raw = np.column_stack([d.y,d[[price,*controls]],np.ones(len(d))])
        if iv is not None:
            raw = np.column_stack([raw,d[iv]])
        arr, iters, err = raw,0,0.0
        rank = 0
    else:
        raise ValueError(fe)
    y=arr[:,0]; x=arr[:,1:1+len(names)]
    if np.linalg.matrix_rank(x) != x.shape[1]:
        raise ValueError(f'{label}: regressor rank failure')
    z=x if iv is None else np.column_stack([arr[:,1+len(names):],x[:,1:]])
    if np.linalg.matrix_rank(z) != z.shape[1]:
        raise ValueError(f'{label}: instrument rank failure')
    zz=z.T@z; xz=x.T@z
    projection=np.linalg.solve(zz,xz.T)
    bread=np.linalg.inv(xz@projection)
    b=bread@xz@np.linalg.solve(zz,z.T@y)
    u=y-x@b
    xhat=z@projection
    gs,gw=codes(d.store),codes(d.week)
    gsw=codes(pd.MultiIndex.from_frame(d[['store','week']]))
    n=len(d); df=rank+x.shape[1]
    score=xhat*u[:,None]
    meat=cluster_meat(score,gs,n,df)+cluster_meat(score,gw,n,df)-cluster_meat(score,gsw,n,df)
    cov=bread@meat@bread
    se=np.sqrt(np.maximum(np.diag(cov),0))
    beta=float(b[0]); elasticity=beta*d[price].to_numpy()*(1-d.share.to_numpy())
    summary=dict(model=label,method='OLS' if iv is None else '2SLS',fe=fe,
                 price_unit='USD/pack' if price=='price_pack' else 'USD/physical_roll',
                 n=n,stores=int(d.store.nunique()),weeks=int(d.week.nunique()),
                 products=int(d.product_id.nunique()),beta_price=beta,se_price=float(se[0]),
                 median_own_elasticity=float(np.median(elasticity)),
                 share_inelastic=float(np.mean(np.abs(elasticity)<1)),
                 share_upward_sloping=float(np.mean(elasticity>0)),
                 absorption_iterations=iters,absorption_error=err,
                 fe_rank=rank,residual_df=n-df,condition_number=float(np.linalg.cond(xz@projection)))
    summary['negative_variance_components']=int((np.diag(cov)<0).sum())
    coefficients=[dict(model=label,variable=nm,coefficient=float(v),se_two_way_cluster=float(s))
                  for nm,v,s in zip(names,b,se)]
    if iv is not None:
        fs_b=np.linalg.solve(zz,z.T@x[:,0]); fs_u=x[:,0]-z@fs_b
        invzz=np.linalg.inv(zz); fs_score=z*fs_u[:,None]
        fm=(cluster_meat(fs_score,gs,n,rank+z.shape[1])+
            cluster_meat(fs_score,gw,n,rank+z.shape[1])-
            cluster_meat(fs_score,gsw,n,rank+z.shape[1]))
        fc=invzz@fm@invzz
        q=len(iv); wald=float(fs_b[:q]@np.linalg.solve(fc[:q,:q],fs_b[:q]))
        w=x[:,1:]; restricted=x[:,0]-w@np.linalg.lstsq(w,x[:,0],rcond=None)[0] if w.shape[1] else x[:,0]
        summary.update(first_stage_wald_chi2=wald,first_stage_wald_df=q,
                       first_stage_wald_per_iv=wald/q,
                       first_stage_partial_r2=float(1-(fs_u@fs_u)/(restricted@restricted)),
                       instruments=','.join(iv))
        for nm,v,s in zip([*iv,*names[1:]],fs_b,np.sqrt(np.maximum(np.diag(fc),0))):
            coefficients.append(dict(model=label+' FIRST_STAGE',variable=nm,coefficient=float(v),se_two_way_cluster=float(s)))
    return summary,coefficients


def prepare(data_dir, out):
    audit=[]
    def log(stage,n,detail=''):
        audit.append(dict(stage=stage,rows=int(n),detail=detail))
        print(stage,n,detail,flush=True)
    upc=pd.read_csv(ROOT/'inputs/upctti.csv')
    upc.columns=upc.columns.str.lower()
    assert upc.upc.is_unique
    upc['pack_count']=pd.to_numeric(upc['size'].str.extract(r'^\s*(\d+)',expand=False))
    # TTI also contains wet wipes and facial tissue. 40+ counts refer to sheets/wipes.
    upc['excluded_nonroll']=upc.pack_count.ge(40)|upc.descrip.str.contains('WIP|MOIST|SOFKIN|SOFTKINS',case=False,regex=True)
    def brand(text):
        t=text.upper()
        for token,name in [('CHARM','Charmin'),('CHRM','Charmin'),('WHITE CLOUD','White Cloud'),
                           ('DOM','Dominicks'),('HH YLW','Dominicks'),('NORTH','Northern'),
                           ('NRTH','Northern'),('COTT','Cottonelle'),('CNTL','Cottonelle'),
                           ('SCOTT','Scott'),('ANGEL','Angel Soft'),('CORON','Coronet'),
                           ('DELSEY','Delsey'),('KLEENEX','Kleenex'),('KLNX','Kleenex'),
                           ('FOREST','Green Forest'),('GENERIC','Generic'),('GENTLE','Soft N Gentle'),
                           ('VT BATH','Value Time')]:
            if token in t: return name
        return 'UNMAPPED'
    upc['brand']=upc.descrip.map(brand)
    upc['variant']=np.select([upc.descrip.str.contains('DBL|DOUBLE',case=False),
                             upc.descrip.str.contains('ULTRA|ULT',case=False),
                             upc.descrip.str.contains('BIG|SQUEEZE|SQZ',case=False)],
                            ['double','ultra_unspecified','big'],default='regular_or_unspecified')
    upc.to_csv(out/'upc_catalog.csv',index=False)
    m=pd.read_csv(data_dir/'wtti.csv',usecols=['STORE','UPC','WEEK','MOVE','PRICE','QTY','SALE','PROFIT','OK'],dtype={'SALE':'string'})
    m.columns=m.columns.str.lower(); log('raw_movement',len(m)); raw_rows=len(m)
    assert not m.duplicated(['store','upc','week']).any()
    m=m.merge(upc,on='upc',how='left',validate='many_to_one',indicator=True)
    assert m._merge.eq('both').all();m=m.drop(columns='_merge')
    log('nonroll_rows_removed',m.excluded_nonroll.sum())
    m=m.loc[~m.excluded_nonroll].copy()
    log('roll_rows_before_validity',len(m))
    m=m.loc[(m.ok==1)&m.qty.gt(0)&m.move.ge(0)&m.week.between(1,399)].copy()
    log('after_ok_qty_quantity_week',len(m))
    source_zero_fraction=float(m.move.eq(0).mean())
    # Preserve actual reported zero records separately; their prices cannot be recovered
    # merely by adding epsilon to market shares or assuming a previous price persisted.
    m.loc[m.move.eq(0),['store','upc','week','move','price','qty','ok','descrip','size']].to_csv(
        out/'reported_zero_sales_records.csv.gz',index=False,compression='gzip')
    # Do not silently interpret zero price and zero movement as free goods or observed offers.
    log('zero_price_zero_sales',((m.price==0)&(m.move==0)).sum())
    log('positive_sales_nonpositive_price',((m.price<=0)&(m.move>0)).sum())
    m=m.loc[m.price.gt(0)].copy();log('positive_price_records',len(m))
    m['price_pack']=m.price/m.qty
    # Broad prespecified USD/pack sanity band; excluded rows are exported for review.
    anomaly=~m.price_pack.between(0.10,60)
    m.loc[anomaly].to_csv(out/'flagged_price_records.csv',index=False)
    log('price_sanity_band_removed',anomaly.sum(),'USD/pack outside [0.10,60]')
    m=m.loc[~anomaly].copy()
    m['price_roll']=m.price_pack/m.pack_count
    m['deal']=m.sale.fillna('').str.strip().ne('').astype(float)
    m['aac_pack']=m.price_pack*(1-m.profit/100)
    # Negative retail gross margins can be genuine loss-leading promotions.
    # They imply AAC > retail price and are not automatically invalid.
    m.loc[~np.isfinite(m.profit)|m.profit.ge(100)|m.aac_pack.le(0),'aac_pack']=np.nan
    # AAC is an accounting proxy and candidate IV only, not validated marginal cost.
    c=pd.read_stata(data_dir/'ccount.dta',columns=['store','week','date','custcoun'],convert_categoricals=False)
    log('raw_customer_count',len(c))
    c['date_parsed']=pd.to_datetime(c.date.astype(str).str.strip(),format='%y%m%d',errors='coerce')
    c['derived_week']=((c.date_parsed-pd.Timestamp('1989-09-14')).dt.days//7)+1
    valid=(c.store.isin(m.store.unique())&c.week.between(1,399)&c.week.eq(c.derived_week)&
           c.date_parsed.notna()&c.custcoun.gt(0)&np.isclose(c.custcoun,c.custcoun.round()))
    c=c.loc[valid].copy();log('valid_customer_days',len(c))
    assert not c.duplicated(['store','date_parsed']).any()
    traffic=c.groupby(['store','week'],as_index=False).agg(market_size=('custcoun','sum'),
            traffic_days=('date_parsed','nunique'),date_start=('date_parsed','min'),date_end=('date_parsed','max'))
    log('traffic_markets_7_days',(traffic.traffic_days==7).sum())
    traffic=traffic.loc[traffic.traffic_days==7].copy()
    traffic['year']=traffic.date_start.dt.year
    traffic.to_csv(out/'weekly_traffic.csv',index=False)
    m=m.merge(traffic,on=['store','week'],how='inner',validate='many_to_one')
    log('matched_full_week_traffic',len(m))
    m['market_id']=m.store.astype(str)+'_'+m.week.astype(str)
    m['product_id']=m.upc.astype(str)
    totals=m.groupby('market_id').move.sum()
    m['inside_quantity']=m.market_id.map(totals)
    m['share']=m.move/m.market_size
    m['outside_share']=1-m.inside_quantity/m.market_size
    bad=m.outside_share.le(0)|m.outside_share.ge(1)
    log('markets_invalid_outside',m.loc[bad,'market_id'].nunique())
    m.loc[bad,['store','week','market_size','inside_quantity','outside_share']].drop_duplicates().to_csv(
        out/'flagged_invalid_share_markets.csv',index=False)
    m=m.loc[~bad].copy();log('clean_positive_price_panel',len(m))
    # Report observed zero offers. Keep them in panel; never replace with epsilon.
    log('observed_zero_sales_positive_price',m.move.eq(0).sum())
    m['y']=np.where(m.move.gt(0),np.log(m.share.where(m.share.gt(0)))-np.log(m.outside_share),np.nan)
    grouped=m.groupby(['upc','week']).price_pack
    m['other_store_price']=(grouped.transform('sum')-m.price_pack)/(grouped.transform('count')-1)
    m['other_store_count']=grouped.transform('count')-1
    m.loc[m.other_store_count.lt(5),'other_store_price']=np.nan
    # Fixed catalog is descriptive; brand-level merger ownership must be dated separately.
    keep=['store','week','year','date_start','upc','product_id','market_id','brand','variant','descrip','size','pack_count',
          'move','price_pack','price_roll','deal','profit','aac_pack','other_store_price','other_store_count',
          'market_size','traffic_days','inside_quantity','share','outside_share','y']
    m[keep].to_csv(out/'clean_upc_store_week.csv.gz',index=False,compression='gzip')
    source=pd.read_csv(out/'reported_zero_sales_records.csv.gz',usecols=['upc'])
    zeros=m.groupby('upc').agg(n_positive_price_records=('move','size'),total_packs=('move','sum'))
    zeros['source_zero_records_before_traffic_match']=source.groupby('upc').size()
    zeros.merge(upc,on='upc').to_csv(out/'zero_sales_by_upc.csv',index=False)
    # Transparent color aggregation sensitivity: brand x pack count x roll variant.
    m['group_id']=m.brand+'|'+m.pack_count.astype(str)+'|'+m.variant
    # Price weights are fixed pooled positive-sales quantities, renormalized over observed offers.
    weights=m.groupby('upc').move.sum();m['weight']=m.upc.map(weights)
    m['weighted_price']=m.weight*m.price_pack
    m['weighted_deal']=m.weight*m.deal
    m['weighted_aac']=m.weight*m.aac_pack
    m['aac_weight']=m.weight.where(m.aac_pack.notna(),0)
    a=m.groupby(['store','week','group_id'],as_index=False).agg(move=('move','sum'),
       price_num=('weighted_price','sum'),weight=('weight','sum'),deal_num=('weighted_deal','sum'),
       aac_num=('weighted_aac','sum'),aac_weight=('aac_weight','sum'),market_size=('market_size','first'),
       outside_share=('outside_share','first'),year=('year','first'),pack_count=('pack_count','first'),n_upcs=('upc','size'))
    a=a.loc[a.weight.gt(0)].copy()
    a['product_id']=a.group_id;a['price_pack']=a.price_num/a.weight;a['deal']=a.deal_num/a.weight
    a['aac_pack']=a.aac_num/a.aac_weight.replace(0,np.nan)
    a['share']=a.move/a.market_size
    a['y']=np.log(a.share.where(a.share.gt(0)))-np.log(a.outside_share)
    a.to_csv(out/'clean_brand_pack_variant_store_week.csv.gz',index=False,compression='gzip')
    pd.DataFrame(audit).to_csv(out/'cleaning_audit.csv',index=False)
    descriptive=dict(raw_rows=raw_rows,clean_positive_price_rows=len(m),positive_sales_rows=int(m.move.gt(0).sum()),
       source_zero_sales_fraction_before_price_and_traffic_filters=source_zero_fraction,
       zero_sales_fraction=float(m.move.eq(0).mean()),markets=int(m.market_id.nunique()),stores=int(m.store.nunique()),
       products=int(m.upc.nunique()),weeks=int(m.week.nunique()),
       start=str(m.date_start.min().date()),end=str(m.date_end.max().date()),
       outside_share_percentiles=m.drop_duplicates('market_id').outside_share.quantile([0,.05,.5,.95,1]).to_dict(),
       price_pack_percentiles=m.price_pack.quantile([0,.01,.5,.99,1]).to_dict(),
       aggregate_zero_sales_fraction=float(a.move.eq(0).mean()),aggregate_products=int(a.product_id.nunique()))
    (out/'descriptive.json').write_text(json.dumps(descriptive,indent=2))
    # Convert demographic Stata data once for the later RC phase, not used in baseline.
    pd.read_stata(data_dir/'demo.dta',convert_categoricals=False).to_csv(out/'demographics.csv',index=False)
    return m,a


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data-dir',type=Path)
    ap.add_argument('--estimate-only',action='store_true',help='Use the included cleaned CSV.gz files; raw data not needed.')
    ap.add_argument('--output-dir',type=Path,default=ROOT/'results');args=ap.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    if args.estimate_only:
        m=pd.read_csv(args.output_dir/'clean_upc_store_week.csv.gz')
        a=pd.read_csv(args.output_dir/'clean_brand_pack_variant_store_week.csv.gz')
    else:
        if args.data_dir is None:ap.error('--data-dir is required unless --estimate-only is used')
        m,a=prepare(args.data_dir,args.output_dir)
    specs=[(m,'UPC_pooled_OLS',dict(fe='none')),
           (m,'UPC_FE_OLS',{}),
           (m,'UPC_FE_OLS_no_deal',dict(controls=())),
           (m,'UPC_store_product_market_FE_OLS',dict(fe='store_product_market')),
           (m,'UPC_FE_IV_AAC',dict(iv=['aac_pack'])),
           (m,'UPC_FE_IV_other_store_price',dict(iv=['other_store_price'])),
           (m.dropna(subset=['aac_pack','other_store_price']),'UPC_FE_OLS_common_IV_sample',{}),
           (m.dropna(subset=['aac_pack','other_store_price']),'UPC_FE_IV_AAC_common_sample',dict(iv=['aac_pack'])),
           (m.dropna(subset=['aac_pack','other_store_price']),'UPC_FE_IV_other_price_common_sample',dict(iv=['other_store_price'])),
           (m.loc[m.year.between(1991,1992)],'UPC_FE_OLS_1991_1992',{}),
           (m.loc[m.year.between(1991,1992)],'UPC_FE_IV_AAC_1991_1992',dict(iv=['aac_pack'])),
           (m.loc[m.price_pack.between(.25,20)],'UPC_FE_OLS_tighter_price_band',{}),
           (a,'brand_pack_variant_FE_OLS',{}),
           (a,'brand_pack_variant_FE_IV_AAC',dict(iv=['aac_pack']))]
    summaries=[];coefs=[]
    for d,label,kw in specs:
        start=time.time();s,c=fit(d,label,**kw);summaries.append(s);coefs.extend(c)
        print(label, 'beta=',round(s['beta_price'],5),'SE=',round(s['se_price'],5),
              'median elasticity=',round(s['median_own_elasticity'],3),'seconds=',round(time.time()-start,1),flush=True)
        pd.DataFrame(summaries).to_csv(args.output_dir/'estimates.csv',index=False)
        pd.DataFrame(coefs).to_csv(args.output_dir/'coefficients_and_first_stages.csv',index=False)
    from write_summary import write_summary
    write_summary(args.output_dir)
    print('Finished. Results:',args.output_dir,flush=True)


if __name__=='__main__':
    main()
