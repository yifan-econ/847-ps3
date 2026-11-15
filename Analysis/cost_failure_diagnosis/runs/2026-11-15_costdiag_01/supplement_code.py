"""Trace cost failures excluded from the common numerical intersection.

Uses saved arrays only; adds fresh files and refuses overwrites.
"""
from pathlib import Path
import argparse
import json
import shutil
import numpy as np
import pandas as pd
from diagnose import SOURCE, ROOT, inventory, save, digest


def main(out):
    targets=['market_exposure.csv','all_input_examples.csv','supplement_validation.json','supplement_code.py']
    assert not any((out/f).exists() for f in targets)
    before=inventory()
    d=pd.read_csv(SOURCE/'product_inputs.csv.gz',dtype={'upc':str})
    cat=pd.read_csv(SOURCE/'ownership_catalog.csv',dtype={'upc':str})
    d=d.merge(cat[['upc','descrip']],on='upc',sort=False,validate='many_to_one')
    mid,names=pd.factorize(d.market_id,sort=False)
    starts=np.r_[0,np.flatnonzero(np.diff(mid))+1]
    total=lambda a:np.add.reduceat(np.asarray(a),starts)
    active=d.firm.gt(0).to_numpy();scott=d.firm.eq(1).to_numpy()
    w=d.move.to_numpy();p=d.price_pack.to_numpy();s=d.share.to_numpy()
    base=d.iloc[starts][['market_id','store','week','market_size']].reset_index(drop=True)
    assert d.groupby('market_id').market_size.nunique().max()==1
    base['packages']=total(w);base['inside_share']=total(s)
    base['scott_share']=total(np.where(scott,s,0))
    base['scott_inside_fraction']=base.scott_share/base.inside_share
    sw=total(np.where(scott,w,0))
    base['scott_price_package_weighted']=total(np.where(scott,w*p,0))/np.where(sw>0,sw,np.nan)
    base['deal_package_fraction']=total(w*d.deal.to_numpy())/base.packages
    flags=[];examples=[]
    for e in pd.read_csv(SOURCE/'estimates_corrected.csv').itertuples():
        for rule in ['dollar']+(['percentage'] if e.rho==0 else []):
            folder=SOURCE/'cells'/e.model
            m=pd.read_csv(folder/f'{rule}_markets.csv.gz')
            flags.append(m.numerical_ok.to_numpy())
            with np.load(folder/f'{rule}_simulation.npz') as a:
                mu=a['markup'];eff=a['effective_cost'];man=a['manufacturer_cost']
            prefix=e.model+'__'+rule
            base[prefix+'__numerical_ok']=m.numerical_ok
            for kind,cost in [('effective',eff),('manufacturer',man)]:
                negative=active & (cost<0)
                base[prefix+'__'+kind+'_negative_products']=total(negative.astype(int))
                ix=np.flatnonzero(negative)
                for label,chosen in [('lowest_cost',ix[np.argsort(cost[ix])[:20]]),('largest_package_exposure',ix[np.argsort(-w[ix])[:20]])]:
                    for rank,j in enumerate(chosen,1):
                        examples.append(dict(cell=e.model,retailer=rule,cost_kind=kind,selection=label,rank=rank,
                            market_id=d.market_id.iloc[j],store=int(d.store.iloc[j]),week=int(d.week.iloc[j]),upc=d.upc.iloc[j],
                            description=d.descrip.iloc[j],owner=d.owner.iloc[j],pack_count=int(d.pack_count.iloc[j]),
                            deal=int(d.deal.iloc[j]),packages=float(w[j]),price=float(p[j]),aac=float(d.aac_pack.iloc[j]),
                            q=float(1 if rule=='dollar' else d.q_percent.iloc[j]),markup=float(mu[j]),
                            effective_cost=float(eff[j]),manufacturer_cost=float(man[j]),
                            market_inside_share=float(base.inside_share.iloc[mid[j]]),
                            scott_market_share=float(base.scott_share.iloc[mid[j]]),
                            numerical_ok=bool(m.numerical_ok.iloc[mid[j]])))
    common=np.logical_and.reduce(flags)
    base['common_numerically_valid']=common
    ex=pd.DataFrame(examples)
    lookup=dict(zip(base.market_id,common))
    ex['common_numerically_valid']=ex.market_id.map(lookup)
    base.to_csv(out/'market_exposure.csv',index=False)
    ex.to_csv(out/'all_input_examples.csv',index=False)
    assert common.sum()==7960
    after=inventory();assert before==after
    shutil.copyfile(__file__,out/'supplement_code.py')
    save(out/'supplement_validation.json',dict(passed=True,protected_files=len(before),changed=[],
        code_sha256=digest(Path(__file__)),rows=len(base),common_markets=int(common.sum()),
        examples=len(ex),reason='Primary diagnosis showed log-price cost failures can disappear on the common numerical sample. Trace excluded markets and all-input cases without estimating or selecting a new sample.'))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--run-id',required=True);args=ap.parse_args()
    main(ROOT/'runs'/args.run_id)
