"""Single-inside-nest demand and manufacturer FOCs; no file IO.

Price derivatives use beta < 0. Fringe (firm=0) has fixed prices.
All arrays are sorted by market. Retail profit is sum (q*p-c)*share,
where q=1 gives dollar margins with retail-equivalent costs, and
q=1-m gives fixed percentage margins with manufacturer costs.
"""
from dataclasses import dataclass
import numpy as np
from scipy.special import expit


@dataclass
class Demand:
    market: np.ndarray
    p0: np.ndarray
    s0: np.ndarray
    beta: float
    rho: float
    form: str

    def __post_init__(self):
        self.market = np.asarray(self.market, dtype=int)
        self.starts = np.r_[0, np.flatnonzero(np.diff(self.market)) + 1]
        self.M = len(self.starts)
        assert np.array_equal(np.unique(self.market), np.arange(self.M))
        assert self.beta < 0 and 0 <= self.rho < 1
        assert (self.p0 > 0).all() and (self.s0 > 0).all()
        inside = self.sum(self.s0)
        assert (inside < 1).all()
        self.h = 1 / (1 - self.rho)
        self.delta = (np.log(self.s0) - np.log1p(-inside[self.market])
                      - self.rho * np.log(self.s0 / inside[self.market]))

    def sum(self, values):
        return np.add.reduceat(values, self.starts)

    def maximum(self, values):
        return np.maximum.reduceat(values, self.starts)

    def state(self, prices):
        change = prices - self.p0 if self.form == 'linear' else np.log(prices / self.p0)
        v = (self.delta + self.beta * change) * self.h
        mx = self.maximum(v)
        ld = mx + np.log(self.sum(np.exp(v - mx[self.market])))
        log_inside_odds = ld / self.h
        inside = expit(log_inside_odds)
        shares = np.exp(v - ld[self.market]) * inside[self.market]
        return shares, inside, np.logaddexp(0, log_inside_odds)

    def slopes(self, prices):
        return np.full(len(prices), self.beta) if self.form == 'linear' else self.beta / prices

    def jacobian(self, prices):
        """Dense Jacobian for a single market (tests and independent checks)."""
        assert self.M == 1
        s, S, _ = self.state(prices)
        b = self.slopes(prices)
        A = 1 + (self.h - 1) / S[0]
        return (self.h * np.diag(s) - A * np.outer(s, s)) * b[None, :]

    def markups(self, prices, firm, q):
        """Exact inverse of the ownership-block Jacobian, all rho/forms."""
        s, S, _ = self.state(prices)
        b = self.slopes(prices)
        g = self.market * 7 + firm
        A = 1 + (self.h - 1) / S
        sf = np.bincount(g, weights=s, minlength=self.M * 7)
        base = -q / (self.h * b)
        numerator = np.bincount(g, weights=s * base, minlength=self.M * 7)
        den = 1 - np.repeat(A / self.h, 7) * sf
        C = numerator / den
        return base + A[self.market] / self.h * C[g]

    def foc(self, prices, firm, q, costs):
        """Retail-price profit gradient, plus scale-invariant FOC residual."""
        s, S, _ = self.state(prices)
        b = self.slopes(prices)
        g = self.market * 7 + firm
        margin = q * prices - costs
        C = np.bincount(g, weights=s * margin, minlength=self.M * 7)
        A = 1 + (self.h - 1) / S
        R = q + b * (self.h * margin - A[self.market] * C[g])
        R = np.where(firm > 0, R, 0)
        return s * R, R / q

    def curvature(self, prices, firm, q, costs):
        """FOC-point firm Hessian: negative diagonal plus a rank-one term.

        Returns a sufficient/exact negative-definiteness check for positive
        firm profit C at a stationary point. FOC accuracy is checked separately.
        Curvature is for retail-price coordinates; a positive diagonal change
        to wholesale coordinates preserves definiteness.
        """
        s, S, _ = self.state(prices)
        b = self.slopes(prices)
        g = self.market * 7 + firm
        bp_over_b = np.zeros(len(prices)) if self.form == 'linear' else -1 / prices
        diag = s * q * (self.h * b - bp_over_b)
        C = np.bincount(g, weights=s * (q * prices - costs), minlength=self.M * 7)
        k = np.repeat((self.h - 1) * (1 - S) / S**2, 7) * C
        bad_diag = np.bincount(g, weights=(diag >= 0) & (firm > 0), minlength=self.M * 7)
        ratios = np.bincount(g, weights=(s * b)**2 / np.maximum(-diag, 1e-300), minlength=self.M * 7)
        occupied = np.bincount(g, minlength=self.M * 7) > 0
        active = occupied & (np.tile(np.arange(7), self.M) > 0)
        good = ((bad_diag == 0) & (1 - k * ratios > 1e-7) & (C >= 0)) | ~active
        return good.reshape(self.M, 7).all(axis=1)

    def solve(self, firm, q, costs, start, max_iterations=600):
        """Prespecified damped markup iteration, no data-dependent restarts.

        Two starts are called by the runner. Freeze converged markets, retain
        failures. Price positivity is maintained by step shortening, never by
        changing a recovered cost or an accepted equilibrium.
        """
        p = np.array(start, copy=True)
        p[firm == 0] = self.p0[firm == 0]
        done = np.zeros(self.M, bool)
        failed = np.zeros(self.M, bool)
        iterations = np.zeros(self.M, int)
        for it in range(1, max_iterations + 1):
            mu = self.markups(p, firm, q)
            target = (costs + mu) / q
            new = .5 * p + .5 * target
            new = np.maximum(new, .5 * p)
            new[firm == 0] = self.p0[firm == 0]
            live = ~(done | failed)
            new[~live[self.market]] = p[~live[self.market]]
            p = new
            if it % 5 == 0 or it == max_iterations:
                invalid = self.maximum((~np.isfinite(p)) | (p < 1e-12) | (p > 1e6 * self.p0)) > 0
                failed |= invalid
                # Keep invalid markets finite solely to finish other markets.
                p[invalid[self.market]] = self.p0[invalid[self.market]]
                _, R = self.foc(p, firm, q, costs)
                error = self.maximum(np.abs(R))
                newly = (error < 1e-10) & live & ~failed
                iterations[newly] = it
                done |= newly
                if (done | failed).all():
                    break
        iterations[~done] = max_iterations
        grad, R = self.foc(p, firm, q, costs)
        error = self.maximum(np.abs(R))
        absolute = self.maximum(np.abs(grad))
        good = done & ~failed & (error < 1e-8) & (absolute < 1e-8)
        return p, good, error, absolute, iterations

    def diagnostics(self, firm):
        s, S, _ = self.state(self.p0)
        b = self.slopes(self.p0)
        A = 1 + (self.h - 1) / S
        own = self.p0 * b * (self.h - A[self.market] * s)
        # All inside prices increase by the same proportion; outside unchanged.
        category = (1 - S) * self.sum(s * b * self.p0) / S
        kcshare = self.sum(np.where(firm == 2, s, 0))
        diversion = A[self.market] * kcshare[self.market] / (self.h - A[self.market] * s)
        return own, category, np.where(firm == 1, diversion, np.nan)
