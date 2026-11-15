"""Numerical checks against explicit dummies and statsmodels' independent 2SLS."""
import numpy as np
import pandas as pd
from statsmodels.sandbox.regression.gmm import IV2SLS
from statsmodels.stats.sandwich_covariance import cov_cluster_2groups
import statsmodels.api as sm
from run_logit import fit

rng=np.random.default_rng(847)
d=pd.MultiIndex.from_product([range(15),range(4),range(12)],names=['store','product_id','week']).to_frame(index=False)
d['sp']=d.store.astype(str)+'_'+d.product_id.astype(str)
n=len(d);z=rng.normal(size=n);v=rng.normal(size=n)
sp=rng.normal(size=60)[pd.factorize(d.sp)[0]]
wk=rng.normal(size=12)[d.week]
d['price_pack']=2+z+.5*v+.2*sp
d['deal']=rng.integers(0,2,n)
d['y']=-1.5*d.price_pack+.4*d.deal+sp+wk+.5*v+rng.normal(size=n)
d['z']=z;d['share']=.01
dummy=pd.get_dummies(d[['sp','week']].astype(str),drop_first=True,dtype=float)
base=np.column_stack([np.ones(n),dummy.to_numpy()])
x=np.column_stack([d.price_pack,d.deal,base])
zz=np.column_stack([d.z,d.deal,base])
for iv in [False,True]:
    summary,coefs=fit(d,'check',iv=['z'] if iv else None)
    reference=IV2SLS(d.y,x,zz).fit() if iv else sm.OLS(d.y,x).fit()
    err=np.max(np.abs(np.array([c['coefficient'] for c in coefs[:2]])-reference.params[:2]))
    assert err<1e-9,(iv,err)
    if not iv:
        cov=cov_cluster_2groups(reference,d.store,d.week)[0]
        se_err=np.max(np.abs(np.array([c['se_two_way_cluster'] for c in coefs[:2]])-np.sqrt(np.diag(cov)[:2])))
        assert se_err<1e-9,se_err
    print(('2SLS' if iv else 'OLS'),'explicit-dummy maximum coefficient error:',err)
print('PASS: absorbed FE estimates match explicit dummies; two-way OLS SE matches statsmodels.')
