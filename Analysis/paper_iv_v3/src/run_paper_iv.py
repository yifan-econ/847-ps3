"""Literature-motivated AAC and leave-own-pricing-zone-out price IV comparisons.
Not an exact replication of single-store GLS or multi-city Hausman-Leonard.
"""
from pathlib import Path
import sys,json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];PROJECT=ROOT.parents[1]
sys.path.insert(0,str(PROJECT/'Analysis/cost_iv_v2/src'))
from estimator import fit
from run_analysis import ar_zero
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
base=pd.read_csv(PROJECT/'Archive/ps3_v1/results/clean_upc_store_week.csv.gz',dtype={'product_id':str})
zone=pd.read_stata(PROJECT/'Data/Dominick/demo.dta',columns=['store','zone'],convert_categoricals=False).dropna()
assert zone.store.is_unique
base=base.merge(zone,on='store',how='left',validate='many_to_one')
missing=base.zone.isna();base.loc[missing,['store']].drop_duplicates().to_csv(OUT/'stores_without_zone.csv',index=False)
known=base.loc[~missing].copy()
# Each donor zone has equal weight. No outcome/sales weights or donor threshold chosen from estimates.
zp=known.groupby(['upc','week','zone'],as_index=False).agg(zone_price=('price_pack','mean'),zone_stores=('store','size'))
zp['sum_zone_prices']=zp.groupby(['upc','week']).zone_price.transform('sum')
zp['other_zone_count']=zp.groupby(['upc','week']).zone_price.transform('size')-1
zp['other_zone_price']=(zp.sum_zone_prices-zp.zone_price)/zp.other_zone_count
zp.loc[zp.other_zone_count.lt(3),'other_zone_price']=np.nan
base=base.merge(zp[['upc','week','zone','other_zone_price','other_zone_count']],on=['upc','week','zone'],how='left',validate='many_to_one')
base['month']=pd.to_datetime(base.date_start).dt.to_period('M').astype(str)
base['cluster_time']=base.month
base['year_from_date']=pd.to_datetime(base.date_start).dt.year
results=[];coefs=[];audits=[]
for sample in ['all_packs','multi_packs']:
 d=base.copy() if sample=='all_packs' else base.loc[base.pack_count.gt(1)].copy()
 # Must define outside using all modeled goods before dropping observations missing IVs.
 d['outside_share']=1-d.groupby('market_id').move.transform('sum')/d.market_size
 d['y']=np.log(d.share)-np.log(d.outside_share)
 assert d.outside_share.between(0,1,inclusive='neither').all()
 for period in ['full','1991_1992']:
  p=d if period=='full' else d.loc[d.year_from_date.between(1991,1992)]
  common=p.dropna(subset=['aac_pack','other_zone_price']).copy()
  audits.append(dict(sample=sample,period=period,before_iv_screen=len(p),common_rows=len(common),stores=int(common.store.nunique()),zones=int(common.zone.nunique()),months=int(common.month.nunique()),min_donor_zones=int(common.other_zone_count.min()),median_donor_zones=float(common.other_zone_count.median()),missing_zone_rows=int(p.zone.isna().sum())))
  for name,iv in [('OLS',None),('AAC_IV',['aac_pack']),('OTHER_ZONE_IV',['other_zone_price'])]:
   label=f'{sample}__{period}__{name}';print('Estimating',label,len(common),flush=True)
   s,c=fit(common,label,iv=iv);s.update(sample=sample,period=period,clustering='store and calendar month',months=int(common.month.nunique()))
   if iv: s.update(ar_zero(common,iv,('deal',)))
   results.append(s);coefs.extend(c)
   pd.DataFrame(results).to_csv(OUT/'estimates.csv',index=False)
   pd.DataFrame(coefs).to_csv(OUT/'coefficients_first_stages.csv',index=False)
   print(label,s['beta_price'],s['se_price'],s.get('first_stage_wald_per_iv'),flush=True)
pd.DataFrame(audits).to_csv(OUT/'sample_audit.csv',index=False)
base[['store','upc','week','zone','other_zone_price','other_zone_count']].to_csv(OUT/'cross_zone_instruments.csv.gz',index=False)
(OUT/'design.json').write_text(json.dumps(dict(donor_rule='Equal weight across other pricing-zone mean prices, same UPC and week; at least three other zones',zone_source='demo.dta: static zone mapping, historical changes unobserved',common_sample='Within packaging and period, OLS/AAC/other-zone share identical observations',outside_share='Recomputed for packaging universe BEFORE IV missingness screening; original traffic denominator',period_design='Full period and 1991-1992 motivated by GLS 2012; pooled stores, not their single-store replication',cautions=['Same chain and Chicago region; not independent cities','Chain-wide brand-week promotions/demand shocks may invalidate price IV','Missing prices/donor assortment can depend on demand','No claim that significance or negative coefficient validates IV']),indent=2))
assert len(results)==12 and all(s['negative_variance_components']==0 for s in results)
print('COMPLETE',flush=True)
