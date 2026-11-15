"""Read-only reconciliation of saved sample with raw movement and customer counts."""
from pathlib import Path
import argparse
import shutil
import numpy as np
import pandas as pd
from diagnose import SOURCE, PROJECT, ROOT, inventory, digest, save


def main(out):
    names=['raw_input_audit.json','tail_movement_records.csv','tail_daily_traffic.csv','tail_weekly_audit.csv','audit_inputs_code.py']
    assert not any((out/n).exists() for n in names)
    before=inventory()
    d=pd.read_csv(SOURCE/'product_inputs.csv.gz',dtype={'upc':str})
    keys=['store','upc','week']
    pieces=[]
    for part in pd.read_csv(PROJECT/'Data/Dominick/wtti.csv',usecols=['STORE','UPC','WEEK','MOVE','PRICE','QTY','SALE','PROFIT','OK'],dtype={'UPC':str,'SALE':'string'},chunksize=200000):
        part.columns=part.columns.str.lower()
        part=part.rename(columns={'move':'raw_move'})
        selected=d[keys].merge(part,on=keys,how='inner',validate='one_to_one')
        pieces.append(selected)
    raw=pd.concat(pieces,ignore_index=True)
    assert len(raw)==len(d) and not raw.duplicated(keys).any()
    x=d.merge(raw,on=keys,validate='one_to_one',sort=False)
    assert (x.ok==1).all() and (x.qty>0).all()
    price_error=float(abs(x.price_pack-x.price/x.qty).max())
    aac_error=float(abs(x.aac_pack-x.price/x.qty*(1-x.profit/100)).max())
    quantity_error=float(abs(x.move-x.raw_move).max())
    raw_deal=x.sale.fillna('').str.strip().ne('').astype(int)
    deal_mismatches=int((raw_deal!=x.deal).sum())
    assert price_error<1e-12 and aac_error<1e-12 and quantity_error==0 and deal_mismatches==0
    c=pd.read_stata(PROJECT/'Data/Dominick/ccount.dta',columns=['store','week','date','custcoun'],convert_categoricals=False)
    c['parsed']=pd.to_datetime(c.date.astype(str).str.strip(),format='%y%m%d',errors='coerce')
    c['derived_week']=((c.parsed-pd.Timestamp('1989-09-14')).dt.days//7)+1
    c=c[c.store.isin(d.store.unique()) & c.week.eq(c.derived_week) & c.parsed.notna() & c.custcoun.gt(0) & np.isclose(c.custcoun,c.custcoun.round())].copy()
    assert not c.duplicated(['store','parsed']).any()
    weekly=c.groupby(['store','week'],as_index=False).agg(raw_traffic=('custcoun','sum'),days=('parsed','nunique'),date_start=('parsed','min'))
    selected=d[['store','week','market_size']].drop_duplicates().merge(weekly,on=['store','week'],validate='one_to_one')
    assert len(selected)==7996 and selected.days.eq(7).all()
    traffic_error=float(abs(selected.market_size-selected.raw_traffic).max());assert traffic_error==0
    exposure=pd.read_csv(out/'market_exposure.csv')
    col='log__aac__rho00__dollar__manufacturer_negative_products'
    tail=exposure[exposure[col]>0]
    assert len(tail)==18 and not tail.common_numerically_valid.any()
    tail_keys=tail[['store','week']]
    x.merge(tail_keys,on=['store','week'],validate='many_to_one').to_csv(out/'tail_movement_records.csv',index=False)
    c.merge(tail_keys,on=['store','week'],validate='many_to_one').to_csv(out/'tail_daily_traffic.csv',index=False)
    tail.merge(selected.drop(columns='market_size'),on=['store','week'],validate='one_to_one').to_csv(out/'tail_weekly_audit.csv',index=False)
    assert inventory()==before
    shutil.copyfile(__file__,out/'audit_inputs_code.py')
    save(out/'raw_input_audit.json',dict(passed=True,matched_product_rows=len(x),matched_markets=len(selected),
        max_price_error=price_error,max_aac_error=aac_error,max_quantity_error=quantity_error,
        deal_mismatches=deal_mismatches,max_traffic_error=traffic_error,seven_days_every_market=True,
        tail_markets=len(tail),tail_week_counts={str(k):int(v) for k,v in tail.week.value_counts().items()},
        protected_files=len(before),changed=[],code_sha256=digest(Path(__file__)),
        interpretation='Saved quantities, PRICE/QTY, AAC proxy, deal and seven-day traffic match raw inputs. This verifies provenance, not accuracy of raw data or the one-package-per-shopping-opportunity interpretation.'))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--run-id',required=True);args=ap.parse_args()
    main(ROOT/'runs'/args.run_id)
