"""v17n-1 exp4. Mechanism: products first, crude follows. Refinery demand and EPA blending
rules transmit product moves into crude with 5-minute lag. QM follows RB+HO 5m signed shock
composite at 3x threshold, 15m holding and $280 stop. Falsification: stressed PnL/era/year checks.
"""
import numpy as np
FAMILY = "energy-product-led-crude-liquidity"
PARAMS = {"lookback_minutes": 5, "threshold": 0.0015, "hold_minutes": 15, "stop_dollars": 280}
START, FLAT = 30600, 15 * 3600 + 9 * 60

def _run(panel):
    sig, risk = {}, {}
    for s, d in panel.items():
        out, rk = np.zeros(len(d), dtype=np.int64), np.zeros(len(d)); sig[s], risk[s] = out, rk
    df = panel["QM"]; sec, c = df.ct_sec.to_numpy(), df.close.to_numpy(); sess = df.session.astype(str).to_numpy()
    rb = panel["RB"].close.reindex(df.index); ho = panel["HO"].close.reindex(df.index)
    rb_ret = (rb / rb.shift(5) - 1).to_numpy(); ho_ret = (ho / ho.shift(5) - 1).to_numpy()
    composite = np.where(np.isfinite(rb_ret) & np.isfinite(ho_ret), (rb_ret + ho_ret) / 2, np.nan)
    for ix in df.groupby(sess, sort=False).indices.values():
        ix = np.asarray(ix)
        valid = ix[(ix >= 5) & (sec[ix] >= START) & (sec[ix] < FLAT)]
        sides = np.sign(composite[valid]); sides[np.abs(composite[valid]) < PARAMS["threshold"]] = 0
        stop = PARAMS["stop_dollars"] / 500.
        for e, side in zip(valid, sides):
            if not side: continue
            # numba-like causal loop: entry at current completed bar, flat within 15m or stop.
            for j in range(e, min(e + PARAMS["hold_minutes"] + 1, ix[-1] + 1)):
                if sec[j] >= FLAT or (j > e and side * (c[j] - c[e]) <= -stop): break
                sig["QM"][j] = int(side); risk["QM"][j] = PARAMS["stop_dollars"]
    return sig, risk

def signals(panel): return _run(panel)[0]
def entry_risk(panel): return _run(panel)[1]
