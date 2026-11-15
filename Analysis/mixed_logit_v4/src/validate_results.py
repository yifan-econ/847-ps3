"""Independent checks of elasticities, logit nesting, and covariance scaling."""
from pathlib import Path
import gzip,pickle,json
import numpy as np
import pandas as pd
from scipy.linalg import null_space
from scipy.stats import chi2
from numpy.polynomial.hermite import hermgauss
from run_mixed import ROOT,load_data,make_problem_data
import pyblp
pyblp.options.verbose=False
rows=[]
for folder in sorted((ROOT/'results').iterdir()):
 if not folder.is_dir() or not (folder/'summary.json').exists(): continue
 s=json.loads((folder/'summary.json').read_text());fn=folder/'pyblp_results.pkl.gz'
 if not fn.exists(): continue
 with gzip.open(fn,'rb') as f:r=pickle.load(f)
 # All matrices preserve original product-data order.
 p=np.asarray(r.problem.products.prices).ravel();shares=np.asarray(r.problem.products.shares).ravel()
 ids=np.asarray(r.problem.products.market_ids).ravel();aid=np.asarray(r.problem.agents.market_ids).ravel()
 dem=np.asarray(r.problem.agents.demographics);aw=np.asarray(r.problem.agents.weights).ravel()
 probs=r.compute_probabilities()
 manual=np.empty(len(shares))
 pg=pd.Series(np.arange(len(ids))).groupby(ids).indices
 agroups=pd.Series(np.arange(len(aid))).groupby(aid).indices
 for mid in r.problem.unique_market_ids:
  ix=pg[mid];ag=agroups[mid]
  alpha=-np.exp(dem[ag]@np.asarray(r.pi).ravel())
  pr=probs[ix,:len(ag)]
  manual[ix]=p[ix]/shares[ix]*np.sum(aw[ag][None,:]*alpha[None,:]*pr*(1-pr),axis=1)
 saved=pd.read_csv(folder/'product_results.csv.gz')
 err=float(np.max(np.abs(manual-saved.elasticity)))
 assert err<1e-7,(s['model'],err)
 # Independent nested logit shares: set each consumer demographic index to zero.
 agframe=pd.DataFrame({'market_ids':aid,'weights':aw,'nodes0':np.zeros(len(aid)),'demo':np.zeros(len(aid))})
 inside=pd.Series(shares).groupby(ids).transform('sum').to_numpy()
 logit_delta=np.log(shares)-np.log1p(-inside)+np.exp(r.pi[0,0])*p
 pred=r.compute_shares(delta=logit_delta[:,None],agent_data=agframe).ravel()
 nested_error=float(np.max(np.abs(pred-shares)));assert nested_error<1e-10
 quad_error=np.nan;quad_relative_p99=np.nan
 if s['demographic']=='income':
  nodes31,w31=hermgauss(31);w31=w31/np.sqrt(np.pi);frames=[]
  for mid in r.problem.unique_market_ids:
   ag=agroups[mid];dv=dem[ag,1];mu=np.sum(aw[ag]*dv);sd=np.sqrt(np.sum(aw[ag]*(dv-mu)**2))
   frames.append(pd.DataFrame(dict(market_ids=np.repeat(mid,31),weights=w31,nodes0=np.zeros(31),demo=mu+np.sqrt(2)*sd*nodes31)))
  newagents=pd.concat(frames,ignore_index=True)
  refined=r.compute_shares(agent_data=newagents).ravel()
  quad_error=float(np.max(np.abs(refined-shares)));quad_relative_p99=float(np.quantile(np.abs(refined/shares-1),.99))
 # Check sandwich scaling against PyBLP's one-way store-clustered covariance.
 Z=np.asarray(r.problem.products.ZD);e=np.asarray(r.xi).ravel();score=Z*e[:,None];score-=score.mean(0)
 cid=np.asarray(r.problem.products.clustering_ids).ravel();_,ic=np.unique(cid,return_inverse=True)
 sums=np.zeros((ic.max()+1,Z.shape[1]));np.add.at(sums,ic,score)
 S=sums.T@sums/len(shares);G=np.asarray(r.moments_jacobian);W=np.asarray(r.W)
 B=np.linalg.pinv(G.T@W@G);V=B@G.T@W@S@W@G@B/len(shares)
 reference=np.asarray(r.parameter_covariances)/len(shares)
 cerr=float(np.max(np.abs(V-reference)));assert np.allclose(V,reference,rtol=1e-5,atol=1e-7),(s['model'],cerr)
 # Summaries of moment Jacobian column collinearity, not formal weak-IV diagnostics.
 norms=np.linalg.norm(G,axis=0);Gn=G/np.maximum(norms,1e-30)
 sv=np.linalg.svd(Gn,compute_uv=False)
 month=(pd.Timestamp('1989-09-14')+pd.to_timedelta((saved.week-1)*7,unit='D')).dt.to_period('M').astype(str)
 def meat(ids):
  groups=pd.factorize(ids)[0];sums=np.zeros((groups.max()+1,score.shape[1]));np.add.at(sums,groups,score)
  return sums.T@sums*(len(sums)/(len(sums)-1))
 Ssum=meat(saved.store)+meat(month)-meat(pd.MultiIndex.from_arrays([saved.store,month]))
 L=null_space(G.T); contrast=L.T@np.asarray(r.moments);CV=L.T@Ssum@L/len(shares)**2
 stat=float((contrast.T@np.linalg.solve(CV,contrast)).item()) if np.linalg.eigvalsh(CV).min()>0 else np.nan
 op=float(chi2.sf(stat,L.shape[1])) if np.isfinite(stat) else np.nan
 rows.append(dict(model=s['model'],overid_moment_chi2=stat,overid_df=L.shape[1],overid_p_asymptotic=op,income_31point_max_share_difference=quad_error,income_31point_relative_share_difference_p99=quad_relative_p99,manual_elasticity_error=err,logit_nesting_error=nested_error,one_way_covariance_check_error=cerr,normalized_moment_jacobian_min_singular=float(sv.min()),normalized_moment_jacobian_condition=float(sv.max()/sv.min()),moment_jacobian_rank=int(np.linalg.matrix_rank(G))))
 pd.DataFrame(rows).to_csv(ROOT/'results/independent_validation.csv',index=False)
 print(s['model'],'validated',flush=True)
