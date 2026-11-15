"""Extract saved estimates and descriptive slide values, without fitting models."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
RUN=ROOT/'Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01'
d=pd.read_csv(RUN/'product_inputs.csv.gz')
e=pd.read_csv(RUN/'estimates_corrected.csv')
b=e[e.rho.eq(0)].copy()
b.to_csv(HERE/'demand_estimates.csv',index=False,mode='x')
co=pd.read_csv(RUN/'coefficients.csv')
fs=co[co.model.str.endswith('rho00 FIRST_STAGE') & co.variable.eq('_iv')].copy()
fs['model']=fs.model.str.replace(' FIRST_STAGE','',regex=False)
fs=fs.merge(b[['model','first_stage_partial_r2','first_stage_wald_chi2']],on='model')
fs.to_csv(HERE/'first_stage_estimates.csv',index=False,mode='x')
el=[]
for z in b.itertuples():
    own=z.beta_price*(1-d.share)*(d.price_pack if z.form=='linear' else 1)
    for name,mask in [('Single roll',d.pack_count.eq(1)),('Multipack',d.pack_count.gt(1))]:
        el.append(dict(model=z.model,group=name,weighted_price=np.average(d.loc[mask,'price_pack'],weights=d.loc[mask,'move']),weighted_elasticity=np.average(own[mask],weights=d.loc[mask,'move'])))
pd.DataFrame(el).to_csv(HERE/'pack_elasticities.csv',index=False,mode='x')
pack=[]
for name,mask in [('1 roll',d.pack_count.eq(1)),('4 rolls',d.pack_count.eq(4)),('6+ rolls',d.pack_count.ge(6))]:
    pack.append(dict(group=name,weighted_price=np.average(d.loc[mask,'price_pack'],weights=d.loc[mask,'move']),
        linear_aac=np.average((-2.028040536973842*d.price_pack*(1-d.share))[mask],weights=d.loc[mask,'move']),
        log_aac=np.average((-5.387947996262146*(1-d.share))[mask],weights=d.loc[mask,'move'])))
pd.DataFrame(pack).to_csv(HERE/'pack_size_detail.csv',index=False,mode='x')
mean=d.groupby(['store','upc']).price_pack.transform('mean')
total=np.mean((d.price_pack-d.price_pack.mean())**2)
within=np.mean((d.price_pack-mean)**2);between=np.mean((mean-d.price_pack.mean())**2)
assert abs(total-within-between)<1e-12
prices=dict(between_store_upc_percent=between/total*100,within_store_upc_over_time_percent=within/total*100,
    definition='Observation-weighted decomposition of level-price variance into store-UPC means and within-store-UPC deviations over weeks; not residual IV variation.')
(HERE/'price_variation.json').write_text(json.dumps(prices,indent=2))
r=pd.read_csv(RUN/'counterfactual_summary.csv')
r=r[r.scope.eq('common_numerically_valid')]
main=r[r.cell.str.endswith('rho00')&r.retailer.eq('dollar')&r.group.isin(['all','Scott','Kimberly-Clark'])]
main.pivot(index='cell',columns='group',values='package_weighted_price_change_pct').to_csv(HERE/'main_price_table.csv',mode='x')
linear=r[r.cell.str.startswith('linear')&r.retailer.eq('dollar')&r.group.eq('all')]
linear[['cell','welfare_per_opportunity','welfare_total_dollars']].to_csv(HERE/'welfare_backup.csv',index=False,mode='x')
inside=d.groupby('market_id').share.transform('sum');sc=d.share.where(d.firm.eq(1),0).groupby(d.market_id).transform('sum');kc=d.firm.eq(2)
div=[]
for rho in [0,.25,.5,.75]:
    h=1/(1-rho);A=1+(h-1)/inside
    value=A*sc/(h-A*d.share)
    div.append(dict(rho=rho,kc_to_scott_package_weighted=np.average(value[kc],weights=d.loc[kc,'move'])))
pd.DataFrame(div).to_csv(HERE/'diversion_backup.csv',index=False,mode='x')
print(b[['model','beta_price','se_price','median_own_elasticity']].to_string(index=False))
print(fs.to_string(index=False));print(pd.DataFrame(el).to_string(index=False));print(prices)
print(main.pivot(index='cell',columns='group',values='package_weighted_price_change_pct').to_string())
print(linear[['cell','welfare_per_opportunity']].to_string(index=False));print(div)
