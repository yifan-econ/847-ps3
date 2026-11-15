"""Resolve feedback's weekly sample and post-event summary definitions."""
from pathlib import Path
import json
import pandas as pd

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[3]
b=pd.read_csv(PROJECT/'Archive/ps3_v1/results/clean_upc_store_week.csv.gz')
b=b[pd.to_datetime(b.date_start).dt.year.between(1991,1992)]
wk=pd.read_csv(OUT/'weekly_purchase_volume.csv')
rows=[]
for week in [99,105,110]:
    u=b[b.week.eq(week)];sc=u.descrip.str.contains('SCOTT',case=False)&u.pack_count.eq(1)
    traffic=u.groupby('store').market_size.first().sum()
    rows.append(dict(sample='v1_positive_1991_1992',week=week,stores=u.store.nunique(),
        scott_single_per_trip=u.loc[sc,'move'].sum()/traffic,rolls_per_trip=(u.move*u.pack_count).sum()/traffic))
    z=wk[wk.week.eq(week)].iloc[0]
    rows.append(dict(sample='v4_keys_used_by_v5',week=week,stores=int(z.stores),
        scott_single_per_trip=z.scott_single_per_trip,rolls_per_trip=z.rolls_per_trip))
pd.DataFrame(rows).to_csv(OUT/'weekly_scope_comparison.csv',index=False,mode='x')
post=[]
for event in [99,110]:
    u=wk[wk.week.between(event+1,event+8)]
    post.append(dict(event_week=event,window='next_8_weeks',mean_weekly_rate=u.scott_single_per_trip.mean(),
        median_weekly_rate=u.scott_single_per_trip.median(),pooled_rate=u.scott_single_packages.sum()/u.traffic.sum(),
        max_weekly_rate=u.scott_single_per_trip.max(),max_week=int(u.loc[u.scott_single_per_trip.idxmax(),'week'])))
pd.DataFrame(post).to_csv(OUT/'post_event_definitions.csv',index=False,mode='x')
with (OUT/'scope_supplement.json').open('x',encoding='utf-8') as f:
    json.dump(dict(broader_v1_rows=len(b),broader_v1_stores=int(b.store.nunique()),
        note='Fable weekly store counts and 46/44 rates reproduce on the broader v1 panel. Primary review uses v5 estimation keys throughout. Post-event summaries depend on aggregation and secondary promotions; no inventory recoupment is identified.'),f,indent=2)
