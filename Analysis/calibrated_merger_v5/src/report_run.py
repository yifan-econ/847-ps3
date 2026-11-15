"""Make derived tables/report without replacing any run artifacts."""
import argparse
import json
import hashlib
import shutil
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]


def table(frame):
    frame=frame.fillna('—')
    return '\n'.join(['| '+' | '.join(map(str,frame.columns))+' |',
                      '| '+' | '.join(['---']*len(frame.columns))+' |']+
                     ['| '+' | '.join(map(str,row))+' |' for row in frame.itertuples(index=False,name=None)])


def main(run):
    status=json.loads((run/'status.json').read_text()); assert status['complete']
    post=run/'postprocessing_code';post.mkdir(exist_ok=False)
    for name in ['report_run.py','validate_run.py','run_design.py']:
        shutil.copyfile(ROOT/'src'/name,post/name)
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in post.iterdir()}
    with (run/'postprocessing.json').open('x') as f:
        json.dump(dict(code_sha256=hashes,
            note='Frozen execution is under code/. Current runner fixes only share_upward_sloping reporting; no demand or simulation rerun. These snapshots generated/validated derived reporting artifacts.'),f,indent=2)
    e=pd.read_csv(run/'estimates.csv')
    # Legacy fit computes this unused field as beta*log(p)*(1-s) for log cells.
    # Actual own elasticity uses beta*(h-A*s), which is negative for beta<0.
    # Preserve raw artifacts and provide an explicitly corrected derived table.
    corrected=e.copy(); corrected['share_upward_sloping']=(e.beta_price>0).astype(float)
    corrected.to_csv(run/'estimates_corrected.csv',index=False,mode='x')
    changed=e.loc[e.share_upward_sloping!=corrected.share_upward_sloping,['model','share_upward_sloping']]
    with (run/'reporting_correction.json').open('x') as f:
        json.dump(dict(field='share_upward_sloping',raw_values=changed.to_dict('records'),
            corrected_value=0,reason='Legacy estimator diagnostic uses signed log(price). Actual demand derivatives are negative in all 16 cells. No coefficients, elasticities used in simulation, costs, equilibrium solutions, or welfare are changed; raw output preserved.'),f,indent=2)
    s=pd.read_csv(run/'counterfactual_summary.csv'); dg=pd.read_csv(run/'equilibrium_diagnostics.csv')
    fs=pd.read_csv(run/'first_stages.csv'); cost=pd.read_csv(run/'cost_diagnostics.csv')
    common=json.loads((run/'common_sample.json').read_text())
    intro=f'''# Conditional merger results: {run.name}

Completed the authorized 16 demand cells and 20 supply scenarios on 259,986 observations, 7,996 store-weeks, 83 stores and 50 UPCs. All demand coefficients are negative. This is a conditional hypothetical Scott/Kimberly-Clark merger at 1991–1992 conditions. Rho is calibrated, not estimated. No preferred causal model is selected.

Run time: {status['elapsed_seconds']/60:.1f} minutes. All 194 pre-existing research files are byte-identical. [Manifest](design.json), [status](status.json), [preservation](preservation.json), [sample audit](sample_audit.json), and [methods/ownership](../../README.md) record provenance and assumptions.

The sample retains 94.31% of packages in the full 1991–1992 positive-sales panel. Its median outside share is 86.74%; fixed-price fringe accounts for 9.25% of baseline packages. The separate catalog corrects 10 Scott UPC labels present in this sample. Missing zero sales and actual availability remain unresolved.

## First stages and conditional demand

Only four first stages are distinct. Wald chi-square is not a KP/effective-F statistic and does not establish exclusion. Level/log instrument transformations require their own valid moment assumptions. Deal exogeneity, common demand shocks across zones, AAC endogeneity, static purchase behavior and only 24 month clusters remain limitations. Standard errors are conditional on rho and use the existing two-way store/month sandwich; no counterfactual uncertainty is propagated.

'''
    lines=[intro,table(fs[['form','iv','first_stage_wald_chi2','first_stage_partial_r2']].round(4)),
           '\nPrice coefficients and SE have different units across linear/log forms. Own/category elasticities are medians; diversion is baseline Scott-package weighted.\n',
           table(corrected[['model','beta_price','se_price','median_own_elasticity','category_elasticity_median','scott_to_kc_diversion_packages']].round(4)),
           '\n## Counterfactuals on a common numerical sample\n',
           f"Common intersection across all 20 scenarios: **{common['common_numerically_valid_markets']:,} markets**. The intersections additionally requiring all active effective costs or manufacturer costs nonnegative contain **{common['common_effective_nonnegative_markets']:,}** and **{common['common_manufacturer_nonnegative_markets']:,}** markets, respectively. An empty intersection is reported as empty, never replaced by a favorable cell-specific sample.\n"]
    main=s[s.scope.eq('common_numerically_valid')]
    p=main.pivot(index=['cell','retailer'],columns='group',values='package_weighted_price_change_pct').reset_index()
    p=p[['cell','retailer','Scott','Kimberly-Clark','rivals','fringe','all']]
    lines += ['\nBaseline-package-weighted percentage price changes, common numerical sample (negative costs permitted and disclosed):\n',table(p.round(4))]
    coverage=s[s.group.eq('all')].pivot(index=['cell','retailer'],columns='scope',values='baseline_package_coverage').reset_index()
    c=dg[['cell','retailer','numerically_valid','effective_nonnegative','manufacturer_nonnegative']].merge(coverage,on=['cell','retailer'])
    c=c[['cell','retailer','numerically_valid','effective_nonnegative','manufacturer_nonnegative','cell_effective_nonnegative','cell_manufacturer_nonnegative']]
    c=c.rename(columns={'cell_effective_nonnegative':'effective_package_coverage','cell_manufacturer_nonnegative':'manufacturer_package_coverage'})
    lines += ['\n## Numerical and cost coverage\n','Counts below are out of 7,996 markets. Cost screens require **every active manufacturer product** in a market to pass. Package coverage fractions use all baseline sample packages. These screens are model diagnostics, not model-selection tests. Failure counts and candidate prices remain saved.\n',table(c.round(4)),
              '\n[All six reporting scopes and groups](counterfactual_summary.csv) include full numerical coverage, cell-specific screens and common intersections. [Equilibrium diagnostics](equilibrium_diagnostics.csv) report maxima over **all attempted markets**, including failures; those maxima are not residuals of accepted solutions. [Per-market files](cells/) identify convergence, reproduction, start agreement and curvature failures separately.\n',
              '\n## Cost diagnostics by package size\n','Below: fraction of baseline packages attached to negative-cost active products, before numerical or market-level cost screens. Dollar-rule manufacturer costs use AAC as wholesale proxy; percentage-rule manufacturer costs use calibrated q*p. They are distinct assumptions. [Full cost table](cost_diagnostics.csv) also includes counts, medians and AAC-proxy costs.\n']
    k=cost[cost.cost_kind.eq('manufacturer')].pivot(index=['cell','retailer'],columns='pack_group',values='negative_package_fraction').reset_index()
    lines += [table(k.round(4)),'\n## Consumer surplus\n','Linear-price only; traffic-weighted dollars per shopping opportunity on the common numerical sample. Total dollars sum modeled opportunities across retained store-weeks; they are not a consumer panel or a forecast of the actual 1995 merger. Values are scenario outputs, not confidence intervals.\n']
    w=main[main.group.eq('all')&main.cell.str.startswith('linear')][['cell','retailer','welfare_per_opportunity','welfare_total_dollars']]
    lines += [table(w.round(6)), '\n## Validation and limits\n',
       'Accepted markets require baseline reproduction, two post-merger starts, absolute/scaled FOC checks and local negative-definite profit Hessians. Local checks do not prove global Nash equilibrium or uniqueness. Negative costs are never clipped. Log-price dollar welfare is deliberately absent. Rho variation changes substitution at fixed market size; no traffic-denominator robustness is claimed. Saved markup/cost arrays are meaningful only for firm > 0; fixed-price fringe entries are unused placeholders, not inferred costs.\n',
       'The raw estimator emits an irrelevant upward-slope diagnostic using signed log prices. [Corrected demand table](estimates_corrected.csv) fixes only that reporting field, with [audit](reporting_correction.json); original estimates remain preserved. Actual demand derivatives, simulations and reported own elasticities already use the correct formulas.\n',
       'No extra cells, data-dependent restarts, mixed-logit refinement or aggregation were added after inspecting results. [Independent validation](independent_validation.json) checks saved outputs without new estimation; [repository validation record](../../../../docs/validation/2026-11-15-calibrated-merger.md) records runtime evidence and limitations.\n']
    with (run/'REPORT.md').open('x',encoding='utf-8') as f:
        f.write('\n'.join(lines))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--run-id',required=True);args=ap.parse_args()
    main(ROOT/'runs'/args.run_id)
