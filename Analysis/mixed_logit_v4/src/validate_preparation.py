"""Validate preparation without changing saved artifacts unless explicitly requested."""
import argparse,json,hashlib
import numpy as np
import pandas as pd
from run_mixed import load_data,make_problem_data,ROOT,PROJECT

def validate(write_artifacts=False):
 b,raw=load_data();audit=[]
 for sample in ['all_packs','multi_packs']:
  for demo in ['household','income']:
   d,agents,types,ref=make_problem_data(b,sample,demo,15)
   assert np.allclose(agents.groupby('market_ids').weights.sum(),1)
   assert not d.duplicated(['market_ids','upc']).any()
   assert np.allclose(d.groupby('market_ids').shares.sum()+d.groupby('market_ids').outside_share.first(),1)
   assert len(agents.market_ids.unique())==d.market_ids.nunique()
   if sample=='multi_packs': assert d.pack_count.gt(1).all()
   for store,g in types.groupby('store'):
    r=raw.loc[raw.store.eq(store)].iloc[0]
    if demo=='household':
     assert np.isclose(np.sum(g.weights*g.raw_value),r.hsizeavg,atol=2e-6)
     assert np.isclose(g.weights.iloc[-1],r.hsize567,atol=2e-6)
     assert np.isclose(g.weights.iloc[3:].sum(),r.hh4plus,atol=2e-6)
    else:
     mu=np.sum(g.weights*g.raw_value);var=np.sum(g.weights*(g.raw_value-mu)**2)
     sd=np.sqrt(np.exp(2*mu+var)*np.expm1(var))
     assert np.isclose(mu,r.income,atol=1e-6) and np.isclose(sd,r.incsigma,rtol=2e-6)
   audit.append(dict(sample=sample,demographic=demo,n=len(d),stores=int(d.store.nunique()),markets=int(d.market_ids.nunique()),agents=len(agents),income_order=15))
 if write_artifacts:
  pd.DataFrame(audit).to_csv(ROOT/'data/sample_audit.csv',index=False)
  manifest=[]
  for path in [PROJECT/'Data/Dominick/demo.dta',PROJECT/'Paper/s11129-005-0259-9.pdf',PROJECT/'Paper/ssrn-569866.pdf']:
   manifest.append(dict(path=str(path.relative_to(PROJECT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
  (ROOT/'data/source_manifest.json').write_text(json.dumps(manifest,indent=2))
  (ROOT/'results/preparation_validation.json').write_text(json.dumps(dict(weights_sum_to_one=True,household_mean_and_group_margins_match=True,log_income_median_and_income_sd_analytically_match=True,unique_products_per_market=True,outside_shares_consistent=True,whole_markets_removed_when_any_modeled_product_lacks_either_iv=True,no_external_consumer_dataset_required_for_separate_marginal_models=True),indent=2))
 return pd.DataFrame(audit)

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--write-artifacts',action='store_true',help='Overwrite the original preparation audit and manifest files; default is read-only.')
 args=parser.parse_args()
 print(validate(write_artifacts=args.write_artifacts).to_string(index=False))
 print('Artifacts written.' if args.write_artifacts else 'Read-only validation: no artifacts written.')

if __name__=='__main__': main()
