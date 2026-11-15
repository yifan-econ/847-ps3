"""Presentation summaries only; reads frozen results and never calls an estimator.

Run with uv run --locked. Matplotlib may be supplied by the desktop's bundled
runtime via PYTHONPATH; the project lock and research dependencies are unchanged.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN = ROOT / 'Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01'
REVIEW = ROOT / 'Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01'
OUT = HERE / 'figures'
OUT.mkdir(exist_ok=False)
def inventory():
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for folder in ['Analysis','Archive','Data','Paper'] for p in (ROOT/folder).rglob('*')
        if p.is_file() and '__pycache__' not in p.parts}
before = inventory()
plt.rcParams.update({'font.size':12, 'axes.spines.top':False, 'axes.spines.right':False,
    'axes.labelcolor':'#17324D','text.color':'#17324D','axes.titlesize':13,
    'pdf.fonttype':42,'savefig.bbox':'tight'})
colors = ['#007C83','#17324D','#C27A29','#9265A6']
def save(fig,name,data):
    fig.tight_layout()
    fig.savefig(OUT/f'{name}.pdf')
    fig.savefig(OUT/f'{name}.png',dpi=160)
    data.to_csv(OUT/f'{name}.csv',index=False)
    plt.close(fig)
d=pd.read_csv(RUN/'product_inputs.csv.gz')
catalog=pd.read_csv(RUN/'ownership_catalog.csv')
names={0:'Fringe',1:'Scott',2:'Kimberly-Clark',3:'P&G',4:'James River',5:'Georgia-Pacific',6:'Fort Howard'}
shares=d.groupby('firm').move.sum().reindex(range(7))/d.move.sum()*100
fig,ax=plt.subplots(figsize=(7.9,3.8))
ax.barh([names[x] for x in shares.index],shares,color=[colors[0] if x in [1,2] else '#8C9AA6' for x in shares.index])
ax.set_xlabel('Share of modeled packages sold (%)');ax.invert_yaxis()
for i,v in enumerate(shares):ax.text(v+.4,i,f'{v:.1f}',va='center')
ax.set_xlim(0,shares.max()+7)
save(fig,'manufacturers',shares.rename('package_percent').reset_index())

m=d.groupby('market_id').agg(inside=('share','sum'),products=('upc','size'),store=('store','first'),week=('week','first'))
score=(m.inside-m.inside.median()).abs()/m.inside.std()+(m.products-m.products.median()).abs()/m.products.std()
typical=score.sort_values(kind='stable').index[0]
t=d[d.market_id.eq(typical)].merge(catalog[['upc','descrip']],on='upc').sort_values('share',ascending=False)
top=t.head(7).copy()
labels=['Northern soft prints','Northern white','Northern assorted','Scott white','Cottonelle assorted','Green Forest','Scott pink']
top['label']=[f'{label} ({int(pack)} roll)' for label,pack in zip(labels,top.pack_count)]
plot=pd.DataFrame({'label':top.label,'percent':top.share*100})
plot=pd.concat([plot,pd.DataFrame([{'label':'Other modeled UPCs','percent':t.iloc[7:].share.sum()*100}])],ignore_index=True)
fig,ax=plt.subplots(figsize=(8,4));ax.barh(plot.label,plot.percent,color=colors[0]);ax.invert_yaxis();ax.set_xlabel('Packages / shopping trips (%)')
ax.set_title(f'Store {int(t.store.iloc[0])}, week {int(t.week.iloc[0])}; outside share {100*(1-t.share.sum()):.1f}%')
save(fig,'typical_market',plot)

u=d[d.upc.eq(5400041500)];store=int(u.groupby('store').size().sort_values(ascending=False,kind='stable').index[0]);u=u[u.store.eq(store)].sort_values('week')
u=u.copy();u['date']=pd.Timestamp('1989-09-14')+pd.to_timedelta((u.week-1)*7,unit='D')
import matplotlib.dates as mdates
fig,axes=plt.subplots(2,1,figsize=(8.4,4.1),sharex=True,gridspec_kw={'height_ratios':[1,1]})
axes[0].plot(u.date,u.price_pack,color=colors[0],lw=1.7);axes[0].set_ylabel('Price ($/pack)')
axes[1].plot(u.date,u.share*100,color=colors[1],lw=1.7);axes[1].set_ylabel('Packs/trips (%)');axes[1].set_xlabel('Week beginning');axes[1].xaxis.set_major_locator(mdates.MonthLocator(interval=4));axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
for ax in axes:
    for week in [99,110]:ax.axvline(pd.Timestamp('1989-09-14')+pd.Timedelta(days=(week-1)*7),color='#C27A29',alpha=.5,lw=1)
axes[0].set_title(f'Scott white single roll, store {store}')
save(fig,'promotions',u[['store','week','date','price_pack','share','deal']])

fs=pd.read_csv(RUN/'first_stages.csv');labels=['Linear / AAC','Linear / other zone','Log / AAC','Log / other zone']
fig,ax=plt.subplots(figsize=(8.2,3.7));ax.barh(labels,fs.first_stage_partial_r2,color=[colors[0],colors[1]]*2);ax.invert_yaxis();ax.set_xlim(0,1);ax.set_xlabel('Partial R-squared: excluded instrument after controls and fixed effects')
for i,row in fs.iterrows():ax.text(row.first_stage_partial_r2+.015,i,f'Wald {row.first_stage_wald_chi2:.1f}',va='center',fontsize=11)
save(fig,'first_stages',fs)

r=pd.read_csv(RUN/'counterfactual_summary.csv');r=r[r.scope.eq('common_numerically_valid')].copy()
r[['form','iv','rho_tag']]=r.cell.str.split('__',expand=True);r['rho']=r.rho_tag.str[3:].astype(int)/100
fig,axes=plt.subplots(1,2,figsize=(9.4,3.9))
for ax,group in zip(axes,['all','Kimberly-Clark']):
    for i,((form,iv),z) in enumerate(r[r.retailer.eq('dollar') & r.group.eq(group)].groupby(['form','iv'],sort=False)):
        ax.plot(z.rho,z.package_weighted_price_change_pct,marker='o',color=colors[i],label=f'{form.title()} / '+('AAC' if iv=='aac' else 'other zone'))
    ax.set_xlabel('Calibrated nesting parameter');ax.set_xticks([0,.25,.5,.75]);ax.set_title('All modeled products' if group=='all' else group);ax.set_ylabel('Price change (%)');ax.set_ylim(bottom=0)
axes[0].legend(fontsize=9,frameon=False)
save(fig,'price_sensitivity',r)

c=pd.read_csv(REVIEW/'scott_cost_claim_check.csv');c=c[c.scope.eq('full_input') & c.retailer.eq('dollar')].copy()
c[['form','iv','rho_tag']]=c.cell.str.split('__',expand=True);c['rho']=c.rho_tag.str[3:].astype(int)/100
fig,ax=plt.subplots(figsize=(8.3,3.8))
for i,((form,iv),z) in enumerate(c.groupby(['form','iv'],sort=False)):
    ax.plot(z.rho,z.negative_package_fraction*100,marker='o',color=colors[i],label=f'{form.title()} / '+('AAC' if iv=='aac' else 'other zone'))
ax.set_xlabel('Calibrated nesting parameter');ax.set_ylabel('Volume with negative cost (%)');ax.set_xticks([0,.25,.5,.75]);ax.set_ylim(0,105);ax.legend(frameon=False,fontsize=10)
save(fig,'cost_failures',c)

main=r[r.rho.eq(0)&r.group.isin(['all','Kimberly-Clark'])]
pivot=main.pivot(index=['form','iv'],columns=['group','retailer'],values='package_weighted_price_change_pct')
lines=[]
for (form,iv),z in pivot.iterrows():
    lines.append(f"{form.title()} / {'AAC' if iv=='aac' else 'other zone'} & {z['all','dollar']:.2f} & {z['Kimberly-Clark','dollar']:.2f} & {z['all','percentage']:.2f} & {z['Kimberly-Clark','percentage']:.2f} \\\\")
(HERE/'main_results.tex').write_text('\n'.join(lines),encoding='utf-8')
effects=[]
for group in ['all','Kimberly-Clark']:
    z=r[r.group.eq(group)];base=z[z.retailer.eq('dollar')]
    for lever,keys,col in [('Nesting',['form','iv'],'rho'),('Price form',['iv','rho'],'form'),('Instrument',['form','rho'],'iv')]:
        dif=base.groupby(keys).package_weighted_price_change_pct.agg(lambda x:x.max()-x.min())
        effects.append({'group':group,'assumption':lever,'largest_matched_change_pp':float(dif.max())})
    dif=z[z.rho.eq(0)].groupby(['form','iv']).package_weighted_price_change_pct.agg(lambda x:x.max()-x.min())
    effects.append({'group':group,'assumption':'Retailer rule at rho zero','largest_matched_change_pp':float(dif.max())})
pd.DataFrame(effects).to_csv(HERE/'assumption_comparison.csv',index=False)
stats=dict(rows=len(d),markets=len(m),stores=d.store.nunique(),upcs=d.upc.nunique(),
    median_price=float(d.price_pack.median()),median_aac=float(d.aac_pack.median()),
    median_other_zone_price=float(d.other_zone_price.median()),median_product_share=float(d.share.median()),
    median_products=float(m.products.median()),median_inside_share=float(m.inside.median()),
    single_roll_package_fraction=float(d.loc[d.pack_count.eq(1),'move'].sum()/d.move.sum()),
    deal_row_fraction=float(d.deal.mean()),typical_market=typical,promotion_store=store,
    typical_rule='Nearest to medians of inside share and product count, standardized by sample standard deviations; stable market-ID tie break.',
    promotion_rule='Scott white UPC; store with most observed weeks, ascending store tie break; no outcome-based selection.')
(HERE/'summary_statistics.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
assert before==inventory()
(HERE/'preservation.json').write_text(json.dumps({'protected_files':len(before),'unchanged':True,'estimation_or_solves':0},indent=2))
(HERE/'protected_before.json').write_text(json.dumps(before,indent=2))
print(json.dumps(stats,indent=2));print(pd.DataFrame(effects).to_string(index=False));print('\n'.join(lines))
