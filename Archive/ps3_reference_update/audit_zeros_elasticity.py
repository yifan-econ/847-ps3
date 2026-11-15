"""Read-only audits of recorded zero sales and packaging-related elasticities."""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--data-dir',type=Path,required=True)
    ap.add_argument('--v1-results',type=Path,required=True)
    ap.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent/'Results')
    args=ap.parse_args();out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
    cat=pd.read_csv(args.v1_results/'upc_catalog.csv')
    d=pd.read_csv(args.v1_results/'clean_upc_store_week.csv.gz',
                  usecols=['pack_count','price_pack','share','move','upc'])
    beta=pd.read_csv(args.v1_results/'estimates.csv').set_index('model').loc['UPC_FE_OLS','beta_price']
    d['elasticity']=beta*d.price_pack*(1-d.share)
    d['inelastic']=d.elasticity.abs().lt(1)
    pack=d.groupby('pack_count').agg(rows=('share','size'),inelastic_fraction=('inelastic','mean'),
             median_price_pack=('price_pack','median'),packs=('move','sum'))
    pack.to_csv(out/'elasticity_by_pack_size.csv')
    m=pd.read_csv(args.data_dir/'wtti.csv',usecols=['STORE','UPC','WEEK','MOVE','PRICE','QTY','OK'])
    m.columns=m.columns.str.lower()
    m=m.merge(cat[['upc','excluded_nonroll']],on='upc',validate='many_to_one')
    m=m.loc[(~m.excluded_nonroll)&m.ok.eq(1)&m.qty.gt(0)&m.move.ge(0)&m.week.between(1,399)].copy()
    m=m.sort_values(['store','upc','week'])
    key=[m.store,m.upc]
    positive=m.move.gt(0)&m.price.gt(0)
    pw=m.week.where(positive)
    first=pw.groupby(key).transform('min');last=pw.groupby(key).transform('max')
    m['zero_location']=np.select([first.isna(),m.week.lt(first),m.week.gt(last)],
                  ['never_positive_in_valid_records','before_first_positive_sale','after_last_positive_sale'],default='between_positive_sales')
    z=m.move.eq(0)
    price=(m.price/m.qty).where(positive)
    previous_price=price.groupby(key).ffill();next_price=price.groupby(key).bfill()
    previous_week=pw.groupby(key).ffill();next_week=pw.groupby(key).bfill()
    near=(m.week-previous_week).le(4)&(next_week-m.week).le(4)
    same=pd.Series(np.isclose(previous_price,next_price,equal_nan=False),index=m.index)&previous_price.notna()&next_price.notna()
    locations=m.loc[z].groupby('zero_location').size().rename('rows').to_frame()
    locations['fraction_of_zeros']=locations.rows/locations.rows.sum()
    locations.to_csv(out/'zero_sales_location.csv')
    m['month']=(pd.Timestamp('1989-09-14')+pd.to_timedelta((m.week-1)*7,unit='D')).dt.to_period('M').astype(str)
    monthly=m.groupby(['store','upc','month']).move.sum()
    active=m.week.ge(first)&m.week.le(last)
    active_monthly=m.loc[active].groupby(['store','upc','month']).move.sum()
    audit=dict(zero_records=int(z.sum()),valid_roll_records=len(m),
       zero_and_zero_price=int((z&m.price.eq(0)).sum()),
       within_positive_sales_lifetime=int((z&m.zero_location.eq('between_positive_sales')).sum()),
       zero_with_observed_positive_prices_within_four_weeks_both_sides=int((z&near).sum()),
       zero_with_same_positive_prices_within_four_weeks_both_sides=int((z&near&same).sum()),
       zero_fraction_weekly_recorded=float(z.mean()),
       zero_fraction_monthly_recorded_groups=float(monthly.eq(0).mean()),
       active_window_proxy_records=int(active.sum()),
       zero_fraction_weekly_inside_first_last_positive_sales=float(m.loc[active,'move'].eq(0).mean()),
       zero_fraction_monthly_inside_first_last_positive_sales=float(active_monthly.eq(0).mean()),
       unweighted_inelastic_fraction=float(d.inelastic.mean()),
       package_volume_weighted_inelastic_fraction=float(np.average(d.inelastic,weights=d.move)),
       single_roll_fraction_of_inelastic_records=float(d.loc[d.inelastic,'pack_count'].eq(1).mean()))
    (out/'zero_and_elasticity_audit.json').write_text(json.dumps(audit,indent=2))
    print(json.dumps(audit,indent=2));print(locations.to_string());print(pack.to_string())


if __name__=='__main__':main()
