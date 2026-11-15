"""Independent numerical checks for v5 demand, costs, and profit curvature."""
from pathlib import Path
import sys
import unittest
import numpy as np
from scipy.optimize import root
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'Analysis/calibrated_merger_v5/src'))
from model import Demand


class CalibratedMergerTests(unittest.TestCase):
    def data(self, rho=0, form='linear'):
        return Demand(np.zeros(4, int), np.array([1., 1.8, 2.2, 2.5]),
                      np.array([.08, .06, .04, .02]), -2., rho, form)

    def test_derivatives_against_finite_differences(self):
        for form in ['linear', 'log']:
            for rho in [0., .25, .5, .75]:
                d = self.data(rho, form)
                p = d.p0 * 1.07
                eps = 1e-5
                numerical = np.column_stack([(d.state(p + eps*np.eye(4)[k])[0] -
                                              d.state(p - eps*np.eye(4)[k])[0])/(2*eps)
                                             for k in range(4)])
                np.testing.assert_allclose(d.jacobian(p), numerical, rtol=1e-7, atol=1e-10)
                np.testing.assert_allclose(d.state(d.p0)[0], d.s0, atol=1e-14)

    def test_block_markup_inverse_and_baseline(self):
        firm = np.array([1, 1, 2, 0])
        for form in ['linear', 'log']:
            for rho in [0., .25, .5, .75]:
                d = self.data(rho, form)
                for q in [np.ones(4), np.array([.9, .75, .8, 1.])]:
                    mu = d.markups(d.p0, firm, q)
                    J = d.jacobian(d.p0)
                    for owner in [1, 2]:
                        ix = np.flatnonzero(firm == owner)
                        expected = np.linalg.solve(-J[np.ix_(ix, ix)].T, q[ix]*d.s0[ix])
                        np.testing.assert_allclose(mu[ix], expected, atol=1e-12)
                    costs = q*d.p0-mu
                    p, good, *_ = d.solve(firm, q, costs, d.p0*1.02)
                    self.assertTrue(good.all())
                    np.testing.assert_allclose(p, d.p0, atol=1e-8)

    def test_merger_matches_independent_dense_root_and_hessian(self):
        firm = np.array([1, 1, 2, 0]); merged = np.array([1, 1, 1, 0])
        for rho in [0., .5, .75]:
            for form in ['linear', 'log']:
                d = self.data(rho, form);q = np.array([.9, .8, .7, 1.])
                c = q*d.p0-d.markups(d.p0, firm, q)
                def grad(x):
                    p = np.r_[x, d.p0[-1]]
                    s = d.state(p)[0];J=d.jacobian(p)
                    return q[:3]*s[:3]+J[:3,:3].T@(q[:3]*p[:3]-c[:3])
                ref = root(grad, d.p0[:3])
                self.assertTrue(ref.success)
                p, good, *_ = d.solve(merged,q,c,d.p0)
                self.assertTrue(good.all())
                np.testing.assert_allclose(p[:3],ref.x,rtol=1e-7,atol=1e-8)
                eps=1e-5
                H=np.column_stack([(grad(ref.x+eps*np.eye(3)[k])-grad(ref.x-eps*np.eye(3)[k]))/(2*eps) for k in range(3)])
                self.assertLess(np.linalg.eigvalsh((H+H.T)/2).max(),0)
                self.assertTrue(d.curvature(p,merged,q,c).all())

    def test_linear_welfare_derivative_is_minus_share(self):
        for rho in [0., .5, .75]:
            d=self.data(rho);eps=1e-5
            for k in range(4):
                v=(d.state(d.p0+eps*np.eye(4)[k])[2]-d.state(d.p0-eps*np.eye(4)[k])[2])/(2*eps*-d.beta)
                self.assertAlmostEqual(float(v[0]),-d.s0[k],places=8)

    def test_market_batch_independence(self):
        a=self.data(.5,'log')
        b=Demand(np.repeat([0,1],4),np.tile(a.p0,2),np.tile(a.s0,2),a.beta,a.rho,a.form)
        q=np.ones(8);f=np.tile([1,1,2,0],2);mer=np.where(f==2,1,f)
        c=q*b.p0-b.markups(b.p0,f,q)
        p,ok,*_=b.solve(mer,q,c,b.p0)
        self.assertTrue(ok.all());np.testing.assert_allclose(p[:4],p[4:],atol=1e-12)

    def test_retailer_rules_can_diverge_after_merger(self):
        d=Demand(np.zeros(2,int),np.array([2.,2.5]),np.array([.2,.15]),-2.,0.,'linear')
        f=np.array([1,2]);mer=np.array([1,1]);q=np.array([.9,.7])
        cd=d.p0-d.markups(d.p0,f,np.ones(2));cp=q*d.p0-d.markups(d.p0,f,q)
        pd,okd,*_=d.solve(mer,np.ones(2),cd,d.p0)
        pp,okp,*_=d.solve(mer,q,cp,d.p0)
        self.assertTrue(okd.all() and okp.all());self.assertGreater(np.max(abs(pd-pp)),.02)


if __name__ == '__main__':
    unittest.main()
