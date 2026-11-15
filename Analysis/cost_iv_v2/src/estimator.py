#!/usr/bin/env python3
"""Dominick's TTI first-pass aggregate logit. No SAS/Stata installation required.

Imported by run_analysis.py; adapted from archived v1 estimator.
All price coefficients use + beta_price * price, so downward demand means beta < 0.
This is an exploratory baseline, not a validated merger model.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import time
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse.csgraph import connected_components

ROOT = Path(__file__).resolve().parents[1]


def codes(s):
    return pd.factorize(s, sort=False)[0]


def absorb(a, groups, tol=1e-10, max_iter=1000):
    """Alternating projections onto complements of categorical fixed effects."""
    a = np.array(a, dtype=float, copy=True)
    if not groups:
        return a, 0, 0.0
    counts = [np.bincount(g) for g in groups]
    for iteration in range(max_iter):
        change = 0.0
        for g, count in zip(groups, counts):
            for k in range(a.shape[1]):
                means = np.bincount(g, weights=a[:, k]) / count
                change = max(change, float(np.max(np.abs(means))))
                a[:, k] -= means[g]
        if change < tol:
            return a, iteration + 1, change
    raise RuntimeError(f'Fixed effect absorption failed: {change}')


def fe_rank(groups):
    if not groups:
        return 0
    if len(groups) == 1:
        return int(groups[0].max() + 1)
    a, b = groups
    na, nb = int(a.max()+1), int(b.max()+1)
    r, c = a, b+na
    graph = sparse.coo_matrix((np.ones(len(r)), (r, c)), shape=(na+nb,na+nb))
    components = connected_components(graph.tocsr(), directed=False, return_labels=False)
    return na + nb - components


def cluster_meat(score, g, n, df):
    ng = int(g.max()+1)
    sums = np.zeros((ng, score.shape[1]))
    np.add.at(sums, g, score)
    return (sums.T @ sums) * (ng/(ng-1)) * ((n-1)/(n-df))


def fit(d, label, iv=None, fe='store_product_week', price='price_pack', controls=('deal',)):
    """2SLS with absorbed FE; CGM two-way store/time cluster covariance; cluster_time overrides week.

    First stage reports excluded-IV two-way cluster Wald chi-square and partial R2.
    Wald/number-IV is NOT a Stock-Yogo or Kleibergen-Paap statistic.
    """
    needed = ['y',price,*controls] + ([] if iv is None else iv)
    d = d.dropna(subset=needed).copy()
    if fe in ('store_product_week','store_product_market'):
        time_group=d.week if fe=='store_product_week' else pd.MultiIndex.from_frame(d[['store','week']])
        groups = [codes(pd.MultiIndex.from_frame(d[['store','product_id']])), codes(time_group)]
        names = [price,*controls]
        raw = d[['y',*names,*([] if iv is None else iv)]].to_numpy(float)
        arr, iters, err = absorb(raw,groups)
        rank = fe_rank(groups)
    elif fe == 'none':
        groups = []
        names = [price,*controls,'constant']
        raw = np.column_stack([d.y,d[[price,*controls]],np.ones(len(d))])
        if iv is not None:
            raw = np.column_stack([raw,d[iv]])
        arr, iters, err = raw,0,0.0
        rank = 0
    else:
        raise ValueError(fe)
    y=arr[:,0]; x=arr[:,1:1+len(names)]
    if np.linalg.matrix_rank(x) != x.shape[1]:
        raise ValueError(f'{label}: regressor rank failure')
    z=x if iv is None else np.column_stack([arr[:,1+len(names):],x[:,1:]])
    if np.linalg.matrix_rank(z) != z.shape[1]:
        raise ValueError(f'{label}: instrument rank failure')
    zz=z.T@z; xz=x.T@z
    projection=np.linalg.solve(zz,xz.T)
    bread=np.linalg.inv(xz@projection)
    b=bread@xz@np.linalg.solve(zz,z.T@y)
    u=y-x@b
    xhat=z@projection
    gs,gw=codes(d.store),codes(d.cluster_time if "cluster_time" in d else d.week)
    gsw=codes(pd.MultiIndex.from_frame(d[['store','cluster_time'] if 'cluster_time' in d else ['store','week']]))
    n=len(d); df=rank+x.shape[1]
    score=xhat*u[:,None]
    meat=cluster_meat(score,gs,n,df)+cluster_meat(score,gw,n,df)-cluster_meat(score,gsw,n,df)
    cov=bread@meat@bread
    se=np.sqrt(np.maximum(np.diag(cov),0))
    beta=float(b[0]); elasticity=beta*d[price].to_numpy()*(1-d.share.to_numpy())
    summary=dict(model=label,method='OLS' if iv is None else '2SLS',fe=fe,
                 price_unit='USD/pack' if price=='price_pack' else 'USD/physical_roll',
                 n=n,stores=int(d.store.nunique()),weeks=int(d.week.nunique()),
                 products=int(d.product_id.nunique()),beta_price=beta,se_price=float(se[0]),
                 median_own_elasticity=float(np.median(elasticity)),
                 share_inelastic=float(np.mean(np.abs(elasticity)<1)),
                 share_upward_sloping=float(np.mean(elasticity>0)),
                 absorption_iterations=iters,absorption_error=err,
                 fe_rank=rank,residual_df=n-df,condition_number=float(np.linalg.cond(xz@projection)))
    summary['negative_variance_components']=int((np.diag(cov)<0).sum())
    coefficients=[dict(model=label,variable=nm,coefficient=float(v),se_two_way_cluster=float(s))
                  for nm,v,s in zip(names,b,se)]
    if iv is not None:
        fs_b=np.linalg.solve(zz,z.T@x[:,0]); fs_u=x[:,0]-z@fs_b
        invzz=np.linalg.inv(zz); fs_score=z*fs_u[:,None]
        fm=(cluster_meat(fs_score,gs,n,rank+z.shape[1])+
            cluster_meat(fs_score,gw,n,rank+z.shape[1])-
            cluster_meat(fs_score,gsw,n,rank+z.shape[1]))
        fc=invzz@fm@invzz
        q=len(iv); wald=float(fs_b[:q]@np.linalg.solve(fc[:q,:q],fs_b[:q]))
        w=x[:,1:]; restricted=x[:,0]-w@np.linalg.lstsq(w,x[:,0],rcond=None)[0] if w.shape[1] else x[:,0]
        summary.update(first_stage_wald_chi2=wald,first_stage_wald_df=q,
                       first_stage_wald_per_iv=wald/q,
                       first_stage_partial_r2=float(1-(fs_u@fs_u)/(restricted@restricted)),
                       instruments=','.join(iv))
        for nm,v,s in zip([*iv,*names[1:]],fs_b,np.sqrt(np.maximum(np.diag(fc),0))):
            coefficients.append(dict(model=label+' FIRST_STAGE',variable=nm,coefficient=float(v),se_two_way_cluster=float(s)))
    return summary,coefficients

