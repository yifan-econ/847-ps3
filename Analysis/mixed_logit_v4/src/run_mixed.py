"""Demographic mixed logit using observed store marginal distributions.
Separate household-size / log-income models avoid assuming a joint demographic distribution.
Negative-exponential price slopes: -exp(theta0 + thetaD * demo). Sigma=0; demographic mixing.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import sys,argparse,json,pickle,time,gzip,fcntl
import numpy as np
import pandas as pd
import pyblp
from numpy.polynomial.hermite import hermgauss
ROOT=Path(__file__).resolve().parents[1];PROJECT=ROOT.parents[1]
sys.path.insert(0,str(PROJECT/'Analysis/cost_iv_v2/src'))
from estimator import fit,codes,cluster_meat,fe_rank
pyblp.options.verbose=True
pyblp.options.digits=5
pyblp.options.flush_output=True

def load_data():
 b=pd.read_csv(PROJECT/'Archive/ps3_v1/results/clean_upc_store_week.csv.gz',dtype={'product_id':str})
 b=b.loc[pd.to_datetime(b.date_start).dt.year.between(1991,1992)].copy()
 z=pd.read_csv(PROJECT/'Analysis/paper_iv_v3/results/cross_zone_instruments.csv.gz',usecols=['store','upc','week','other_zone_price'])
 b=b.merge(z,on=['store','upc','week'],validate='one_to_one')
 demo=pd.read_stata(PROJECT/'Data/Dominick/demo.dta',columns=['store','income','incsigma','hsizeavg','hsize1','hsize2','hsize34','hsize567','hh4plus'],convert_categoricals=False).dropna()
 assert demo.store.is_unique
 b=b.merge(demo,on='store',validate='many_to_one')
 return b,demo

def demographic_types(b,demographic,order):
 d=b.drop_duplicates('store').sort_values('store')
 mu_ref=float(d.income.mean())
 rows=[]
 for _,r in d.iterrows():
  if demographic=='household':
   p4=float(r.hh4plus-r.hsize567);p3=float(r.hsize34-p4)
   weights=np.array([r.hsize1,r.hsize2,p3,p4,r.hsize567],float);weights/=weights.sum()
   tail=(r.hsizeavg-np.dot(weights[:4],[1,2,3,4]))/weights[4]
   assert weights.min()>0 and tail>=5
   values=np.array([1,2,3,4,tail]);demo_values=values-2.7
  else:
   # Income is log(median), incsigma is SD in levels. Match both under lognormal assumption.
   ratio=(r.incsigma/np.exp(r.income))**2
   sigma=np.sqrt(np.log((1+np.sqrt(1+4*ratio))/2))
   nodes,weights=hermgauss(order);weights=weights/np.sqrt(np.pi)
   values=r.income+np.sqrt(2)*sigma*nodes
   demo_values=(values-mu_ref)/0.3
  for i,(v,w,dd) in enumerate(zip(values,weights,demo_values)):
   rows.append(dict(store=int(r.store),type_id=i,raw_value=float(v),weights=float(w),demo=float(dd),nodes0=0.0))
 a=pd.DataFrame(rows)
 assert np.allclose(a.groupby('store').weights.sum(),1)
 moments=a.groupby('store').apply(lambda g:pd.Series({'demo_mean':np.sum(g.weights*g.demo),'demo_variance':np.sum(g.weights*(g.demo-np.sum(g.weights*g.demo))**2)}),include_groups=False).reset_index()
 for c in ['demo_mean','demo_variance']: moments[c]-=moments[c].mean()
 return a,moments,mu_ref

def make_problem_data(b,sample,demographic,order):
 d=b.copy() if sample=='all_packs' else b.loc[b.pack_count.gt(1)].copy()
 d['outside_share']=1-d.groupby('market_id').move.transform('sum')/d.market_size
 d['share']=d.move/d.market_size;d['y']=np.log(d.share)-np.log(d.outside_share)
 # Shares defined before dropping unavailable IV observations; same sample across IV families.
 bad=d[['aac_pack','other_zone_price']].isna().any(axis=1).groupby(d.market_id).transform('any')
 d=d.loc[~bad].copy()
 types,moments,mu_ref=demographic_types(b.dropna(subset=['aac_pack','other_zone_price']),demographic,order)
 d=d.merge(moments,on='store',validate='many_to_one').sort_values(['market_id','upc']).reset_index(drop=True)
 d['market_ids']=d.market_id;d['prices']=d.price_pack;d['shares']=d.share
 d['store_product']=d.store.astype(int).astype(str)+'_'+d.product_id
 d['clustering_ids']=d.store
 d['month']=pd.to_datetime(d.date_start).dt.to_period('M').astype(str);d['cluster_time']=d.month
 markets=d[['market_ids','store']].drop_duplicates()
 agents=markets.merge(types,on='store',validate='many_to_many').sort_values(['market_ids','type_id']).reset_index(drop=True)
 assert d.shares.gt(0).all() and d.groupby('market_ids').shares.sum().lt(1).all()
 assert np.allclose(d.groupby('market_ids').shares.sum()+d.groupby('market_ids').outside_share.first(),1)
 return d,agents,types,mu_ref

def two_way_cov(res,d):
 # Same full parameter order as PyBLP: nonlinear theta, concentrated linear beta.
 Z=np.asarray(res.problem.products.ZD);xi=np.asarray(res.xi).ravel();G=np.asarray(res.moments_jacobian);W=np.asarray(res.W)
 score=Z*xi[:,None];score-=score.mean(axis=0)
 gs=codes(d.store);gm=codes(d.month);gsm=codes(pd.MultiIndex.from_frame(d[['store','month']]))
 n=len(d)
 # Cluster-count correction only; no absorbed-FE df correction, reported explicitly.
 S=cluster_meat(score,gs,n,1)+cluster_meat(score,gm,n,1)-cluster_meat(score,gsm,n,1)
 B=np.linalg.pinv(G.T@W@G);V=B@G.T@W@(S/n**2)@W@G@B
 eig=np.linalg.eigvalsh(V)
 return V,np.sqrt(np.maximum(np.diag(V),0)),float(eig.min())

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--sample',choices=['all_packs','multi_packs'],required=True)
 ap.add_argument('--demographic',choices=['household','income'],required=True);ap.add_argument('--iv',choices=['aac','other_zone'],required=True)
 ap.add_argument('--start',type=float,default=.1);ap.add_argument('--income-order',type=int,default=15);ap.add_argument('--workers',type=int,default=1)
 ap.add_argument('--force',action='store_true')
 ap.add_argument('--evaluate-only',action='store_true')
 ap.add_argument('--tag',default='')
 args=ap.parse_args();label=f'{args.sample}__{args.demographic}__{args.iv}'
 out=ROOT/'results'/label
 if args.tag:out=out/args.tag
 out.mkdir(parents=True,exist_ok=True)
 lock=open(out/'run.lock','w');fcntl.flock(lock,fcntl.LOCK_EX)
 if not args.force and (out/'summary.json').exists() and (out/'pyblp_results.pkl.gz').exists():
  print('CACHED',label,flush=True);return
 (out/'process.json').write_text(json.dumps(dict(pid=os.getpid(),parent_pid=os.getppid())))
 b,demodata=load_data();d,agents,types,mu_ref=make_problem_data(b,args.sample,args.demographic,args.income_order)
 source='aac_pack' if args.iv=='aac' else 'other_zone_price'
 for k,arr in enumerate([d[source],d[source]*d.demo_mean,d[source]*d.demo_variance]):
  d[f'demand_instruments{k}']=(arr-arr.mean())/arr.std()
 types.to_csv(ROOT/f'data/{args.demographic}_types.csv',index=False)
 controls=('deal',);ivs=[f'demand_instruments{k}' for k in range(3)]
 baseline,bc=fit(d,label+'__logit_same_instruments',iv=ivs,controls=controls)
 (out/'logit_comparison.json').write_text(json.dumps(baseline,indent=2))
 formulation=(pyblp.Formulation('0 + deal',absorb='C(store_product) + C(week)'),pyblp.Formulation('0 + I(-prices)'))
 problem=pyblp.Problem(formulation,d,agent_formulation=pyblp.Formulation('1 + demo'),agent_data=agents,rc_types=['log'])
 initial_pi=np.array([[np.log(2),args.start]])
 seed=out/'optimization_seed.json'
 if seed.exists(): initial_pi=np.array(json.loads(seed.read_text()))
 prior=out/'pyblp_results.pkl.gz'
 if prior.exists():
  with gzip.open(prior,'rb') as f: initial_pi=pickle.load(f).pi
 t=time.time()
 with pyblp.parallel(args.workers):
  res=problem.solve(sigma=np.zeros((1,1)),pi=initial_pi,method='1s',
   optimization=(pyblp.Optimization('return') if args.evaluate_only else pyblp.Optimization('bfgs',{'maxiter':70,'gtol':1e-3,'hess_inv0':np.eye(2)*0.01})),
   iteration=pyblp.Iteration('lm',{'ftol':1e-11,'xtol':1e-11,'gtol':1e-11,'maxiter':500},compute_jacobian=True),
   W_type='clustered',se_type='clustered',error_behavior='revert',error_punishment=10000,check_optimality='both')
  # Row diagonals follow input order within each market.
  elas=res.extract_diagonals(res.compute_elasticities()).ravel()
  predicted=res.compute_shares().ravel()
 V,se,mineig=two_way_cov(res,d)
 slope=-np.exp(float(res.pi[0,0])+float(res.pi[0,1])*types.demo)
 pos=float(np.sum(types.weights*(slope>0))/types.store.nunique())
 if np.max(np.abs(predicted-d.shares))>=1e-8:
  failure=dict(model=label,status='rejected',reason='Final shares fail inversion accuracy check',max_share_error=float(np.max(np.abs(predicted-d.shares))),theta_intercept=float(res.pi[0,0]),theta_demo=float(res.pi[0,1]),gradient_norm=float(res.projected_gradient_norm))
  (out/'rejected_fit.json').write_text(json.dumps(failure,indent=2))
  print('REJECTED',json.dumps(failure),flush=True);return
 summary=dict(model=label,demographic=args.demographic,iv_family=args.iv,n=len(d),stores=int(d.store.nunique()),markets=int(d.market_ids.nunique()),months=int(d.month.nunique()),beta_price=-float(np.exp(res.pi[0,0])),theta_intercept=float(res.pi[0,0]),pi_demo=float(res.pi[0,1]),sigma=0.,se_pi_two_way=float(se[1]),se_beta_two_way=float(np.exp(res.pi[0,0])*se[0]),covariance_min_eigenvalue=mineig,objective=float(res.objective),converged=bool(res.converged and not args.evaluate_only),diagnostic_endpoint_only=bool(args.evaluate_only),projected_gradient_norm=float(res.projected_gradient_norm),min_reduced_hessian_eigenvalue=float(np.linalg.eigvalsh(res.reduced_hessian).min()),median_own_elasticity=float(np.median(elas)),share_inelastic=float(np.mean(np.abs(elas)<1)),share_upward_sloping_products=float(np.mean(elas>0)),positive_individual_price_slopes=pos,max_share_error=float(np.max(np.abs(predicted-d.shares))),elapsed_seconds=time.time()-t,price_unit='USD per package',income_reference_logmedian=mu_ref,income_quadrature_order=args.income_order,parameter_order=['theta_intercept','theta_demo','beta_deal'],price_distribution='negative exponential link; finite household mixture or income-induced lognormal mixing',near_numerical_bound=False,uncertainty='store and month two-way clustered sandwich; 24 months; count correction only',logit_same_iv_beta=baseline['beta_price'],logit_same_iv_elasticity=baseline['median_own_elasticity'])
 (out/'summary.json').write_text(json.dumps(summary,indent=2))
 np.savez_compressed(out/'diagnostics.npz',parameters=res.parameters,covariance=V,moments=res.moments,moments_jacobian=res.moments_jacobian,xi=res.xi)
 d[['store','upc','week','market_ids','prices','shares','outside_share']].assign(elasticity=elas,predicted_share=predicted).to_csv(out/'product_results.csv.gz',index=False)
 temp=out/f'pyblp_results.{os.getpid()}.tmp.gz'
 with gzip.open(temp,'wb',compresslevel=3) as f:pickle.dump(res,f)
 os.replace(temp,out/'pyblp_results.pkl.gz')
 print('FINAL_SUMMARY',json.dumps(summary),flush=True)
if __name__=='__main__': main()
