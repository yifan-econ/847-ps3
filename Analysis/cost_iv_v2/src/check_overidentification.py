"""Robust overidentifying moment test, with nuisance-estimation-orthogonal contrast.
A rejection questions the instrument set/model; nonrejection does not establish validity.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.linalg import null_space
from scipy.stats import chi2
from estimator import absorb,codes,cluster_meat,fe_rank
ROOT=Path(__file__).resolve().parents[1]
rows=[]
for sample in ['all_packs','multi_packs']:
 d=pd.read_csv(ROOT/f'data/processed/{sample}_estimation_panel.csv.gz').dropna(subset=['z_pulp_rolls','z_plastic_surface'])
 groups=[codes(pd.MultiIndex.from_frame(d[['store','upc']])),codes(d.week)]
 a,_,_=absorb(d[['y','price_pack','deal','z_pulp_rolls','z_plastic_surface']].to_numpy(),groups)
 y=a[:,0];x=a[:,1:3];z=np.column_stack([a[:,3:],x[:,1]])
 zz=z.T@z;D=z.T@x;A=D.T@np.linalg.solve(zz,D)
 b=np.linalg.solve(A,D.T@np.linalg.solve(zz,z.T@y));u=y-x@b
 # L annihilates D, so estimated beta contributes no first-order term to the tested moment.
 L=null_space(D.T);score=z*u[:,None];n=len(d);df=fe_rank(groups)+x.shape[1]
 gs=codes(d.store);gm=codes(d.month);gsm=codes(pd.MultiIndex.from_frame(d[['store','month']]))
 S=cluster_meat(score,gs,n,df)+cluster_meat(score,gm,n,df)-cluster_meat(score,gsm,n,df)
 v=L.T@S@L;g=L.T@(z.T@u);psd=np.linalg.eigvalsh(v).min()>0
 stat=float(g@np.linalg.solve(v,g)) if psd else np.nan
 rows.append(dict(sample=sample,test='orthogonal overidentifying moment Wald',df=L.shape[1],statistic=stat,p_value=float(chi2.sf(stat,L.shape[1])),covariance_psd=psd,n=n))
pd.DataFrame(rows).to_csv(ROOT/'results/overidentification.csv',index=False)
print(pd.DataFrame(rows).to_string(index=False))
