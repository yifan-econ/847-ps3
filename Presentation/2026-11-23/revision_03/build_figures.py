"""Figures for the revision_03 deck. Reads saved results only; fits nothing.

Run from the repository root:
    uv run --locked --with matplotlib==3.10.8 python Presentation/2026-11-23/revision_03/build_figures.py

Figures are drawn at the physical size they take on a 160 mm x 90 mm slide, so the
font sizes below are the sizes the audience sees. The script refuses to overwrite an
existing figures/ folder.
"""
from pathlib import Path
import hashlib
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN = ROOT / 'Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01'
REVIEW = ROOT / 'Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01'
OUT = HERE / 'figures'
OUT.mkdir(exist_ok=False)
WEEK_ONE = pd.Timestamp('1989-09-14')


def inventory():
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for folder in ['Analysis', 'Archive', 'Data', 'Paper'] for p in (ROOT / folder).rglob('*')
            if p.is_file() and '__pycache__' not in p.parts}


before = inventory()
INK = '#17324D'
plt.rcParams.update({'font.size': 8, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.labelcolor': INK, 'text.color': INK, 'xtick.color': INK, 'ytick.color': INK,
                     'axes.edgecolor': INK, 'axes.titlesize': 8.5, 'axes.labelsize': 8,
                     'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5, 'legend.fontsize': 7.5,
                     'pdf.fonttype': 42, 'savefig.bbox': 'tight', 'savefig.pad_inches': 0.02})
colors = ['#007C83', '#17324D', '#C27A29', '#9265A6']
SPEC = {('linear', 'aac'): 'Price in dollars, AAC', ('linear', 'other_zone'): 'Price in dollars, other zone',
        ('log', 'aac'): 'Log price, AAC', ('log', 'other_zone'): 'Log price, other zone'}


def save(fig, name, data):
    fig.savefig(OUT / f'{name}.pdf')
    fig.savefig(OUT / f'{name}.png', dpi=300)
    data.to_csv(OUT / f'{name}.csv', index=False)
    plt.close(fig)


d = pd.read_csv(RUN / 'product_inputs.csv.gz')
catalog = pd.read_csv(RUN / 'ownership_catalog.csv')

# Slide 3: package shares by manufacturer.
names = {0: 'Private label, generics', 1: 'Scott', 2: 'Kimberly-Clark', 3: 'Procter & Gamble',
         4: 'James River', 5: 'Georgia-Pacific', 6: 'Fort Howard'}
shares = d.groupby('firm').move.sum().reindex(range(7)) / d.move.sum() * 100
order = [1, 2, 3, 4, 5, 6, 0]
fig, ax = plt.subplots(figsize=(3.35, 2.15))
ax.barh([names[x] for x in order], shares[order], color=[colors[0] if x in [1, 2] else '#8C9AA6' for x in order])
ax.set_xlabel('Share of packages sold (%)')
ax.invert_yaxis()
for i, x in enumerate(order):
    ax.text(shares[x] + .6, i, f'{shares[x]:.0f}%', va='center', fontsize=8)
ax.set_xlim(0, shares.max() + 8)
fig.tight_layout()
save(fig, 'manufacturers', shares.rename('package_percent').reset_index())

# Backup: a typical market (same selection rule as the earlier drafts).
m = d.groupby('market_id').agg(inside=('share', 'sum'), products=('upc', 'size'), store=('store', 'first'), week=('week', 'first'))
score = (m.inside - m.inside.median()).abs() / m.inside.std() + (m.products - m.products.median()).abs() / m.products.std()
typical = score.sort_values(kind='stable').index[0]
t = d[d.market_id.eq(typical)].merge(catalog[['upc', 'descrip']], on='upc').sort_values('share', ascending=False)
top = t.head(7).copy()
labels = ['Northern soft prints', 'Northern white', 'Northern assorted', 'Scott white', 'Cottonelle assorted', 'Green Forest', 'Scott pink']
top['label'] = [f'{label} ({int(pack)} roll{"s" if pack > 1 else ""})' for label, pack in zip(labels, top.pack_count)]
plot = pd.DataFrame({'label': top.label, 'percent': top.share * 100})
plot = pd.concat([plot, pd.DataFrame([{'label': f'Other {len(t) - 7} UPCs together', 'percent': t.iloc[7:].share.sum() * 100}])], ignore_index=True)
fig, ax = plt.subplots(figsize=(4.9, 2.35))
ax.barh(plot.label, plot.percent, color=[colors[0]] * 7 + ['#8C9AA6'])
ax.invert_yaxis()
ax.set_xlabel('Packages sold per 100 shopping trips')
typical_date = WEEK_ONE + pd.Timedelta(days=(int(t.week.iloc[0]) - 1) * 7)
fig.tight_layout()
save(fig, 'typical_market', plot.assign(store=int(t.store.iloc[0]), week=int(t.week.iloc[0]), week_beginning=str(typical_date.date()),
                                       outside_percent=100 * (1 - t.share.sum()), products=len(t)))

# Slide 4: one UPC in one store over time.
u = d[d.upc.eq(5400041500)]
store = int(u.groupby('store').size().sort_values(ascending=False, kind='stable').index[0])
u = u[u.store.eq(store)].sort_values('week').copy()
u['date'] = WEEK_ONE + pd.to_timedelta((u.week - 1) * 7, unit='D')
fig, axes = plt.subplots(2, 1, figsize=(3.45, 2.45), sharex=True)
axes[0].plot(u.date, u.price_pack, color=colors[0], lw=1.1)
axes[0].set_ylabel('Price ($)')
axes[1].plot(u.date, u.share * 100, color=colors[1], lw=1.1)
axes[1].set_ylabel('Sold per 100 trips')
axes[1].xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
axes[0].set_title(f'Scott white single roll, store {store}')
fig.tight_layout(h_pad=.6)
save(fig, 'promotions', u[['store', 'week', 'date', 'price_pack', 'share', 'deal']])

# Slide 12: merger price effects by specification and nesting value.
r = pd.read_csv(RUN / 'counterfactual_summary.csv')
r = r[r.scope.eq('common_numerically_valid')].copy()
r[['form', 'iv', 'rho_tag']] = r.cell.str.split('__', expand=True)
r['rho'] = r.rho_tag.str[3:].astype(int) / 100
fig, axes = plt.subplots(1, 2, figsize=(3.45, 2.3))
for ax, group, title in zip(axes, ['Kimberly-Clark', 'all'], ['Kimberly-Clark products', 'All tissue products']):
    z = r[r.retailer.eq('dollar') & r.group.eq(group)]
    for i, ((form, iv), g) in enumerate(z.groupby(['form', 'iv'], sort=False)):
        ax.plot(g.rho, g.package_weighted_price_change_pct, marker='o', ms=2.8, lw=1.1, color=colors[i], label=SPEC[form, iv])
    ax.set_xlabel(r'Nesting parameter $\rho$')
    ax.set_xticks([0, .25, .5, .75])
    ax.set_xticklabels(['0', '.25', '.5', '.75'])
    ax.set_title(title)
    ax.set_ylim(bottom=0)
axes[0].set_ylabel('Price increase (%)')
handles, lab = axes[0].get_legend_handles_labels()
fig.tight_layout(rect=(0, .16, 1, 1), w_pad=1.0)
fig.legend(handles, lab, loc='lower center', ncol=2, frameon=False, columnspacing=1.2, handlelength=1.6)
save(fig, 'price_sensitivity', r)

# Slide 11: share of Scott single-roll packages with a negative implied cost.
c = pd.read_csv(REVIEW / 'scott_cost_claim_check.csv')
c = c[c.scope.eq('full_input') & c.retailer.eq('dollar')].copy()
c[['form', 'iv', 'rho_tag']] = c.cell.str.split('__', expand=True)
c['rho'] = c.rho_tag.str[3:].astype(int) / 100
fig, ax = plt.subplots(figsize=(3.1, 2.05))
for i, ((form, iv), g) in enumerate(c.groupby(['form', 'iv'], sort=False)):
    ax.plot(g.rho, g.negative_package_fraction * 100, marker='o', ms=3, lw=1.2, color=colors[i], label=SPEC[form, iv])
ax.set_xlabel(r'Nesting parameter $\rho$')
ax.set_ylabel('Negative implied cost (%)')
ax.set_xticks([0, .25, .5, .75])
ax.set_xticklabels(['0', '.25', '.5', '.75'])
ax.set_ylim(0, 108)
# Label the lines directly; a legend box would sit on top of the rising line.
ax.text(.75, 91, 'Price in dollars, AAC', color=colors[0], ha='right', va='top', fontsize=8)
ax.text(.01, 62, 'Price in dollars,\nother zone', color=colors[1], ha='left', va='center', fontsize=8)
ax.text(.75, 24, 'Log price, both instruments', color=colors[3], ha='right', va='bottom', fontsize=8)
fig.tight_layout()
save(fig, 'cost_failures', c)

assert before == inventory()
(HERE / 'preservation.json').write_text(json.dumps({'protected_files': len(before), 'unchanged': True, 'estimation_or_solves': 0}, indent=2))
(HERE / 'protected_before.json').write_text(json.dumps(before, indent=2))
print('figures written:', sorted(p.name for p in OUT.glob('*.pdf')))
print('typical market', typical, 'week beginning', typical_date.date(), 'outside %.1f%%' % (100 * (1 - t.share.sum())), 'products', len(t))
print('promotion store', store)
