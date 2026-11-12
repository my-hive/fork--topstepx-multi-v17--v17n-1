"""v17n-1 exp6. Mechanism: Thursday 09:30 CT EIA natural-gas storage release. Surprise is
absorbed slowly by hedgers and storage-constrained buyers, so the first 10-minute move continues
(post-announcement drift). QG follows move direction, 60m hold, $280 stop.
Falsification: stressed PnL/era/year checks.
"""
import numpy as np
FAMILY = "energy-ng-storage-release-drift"
PARAMS = {"observe_minutes": 10, "hold_minutes": 60, "stop_dollars": 280}
START, FLAT, PV = 34200, 15 * 3600 + 9 * 60, 2500.

def _run(panel):
    sig, risk = {}, {}
    for s, d in panel.items():
        out, rk = np.zeros(len(d), dtype=np.int64), np.zeros(len(d)); sig[s], risk[s] = out, rk
        if s != "QG": continue
        sec, c = d.ct_sec.to_numpy(), d.close.to_numpy()
        wd = d.index.tz_convert("America/Chicago").weekday.to_numpy()
        for ix in d.groupby(d.session.astype(str), sort=False).indices.values():
            ix = np.asarray(ix); n = PARAMS["observe_minutes"]
            hit = ix[(wd[ix] == 3) & (sec[ix] == START + (n - 1) * 60)]
            if not len(hit): continue
            e = hit[0]; a = e - (n - 1)
            if a < ix[0] or sec[a] != START: continue
            side = int(np.sign(c[e] - c[a - 1])) if a > 0 else 0   # vs 09:29 close (pre-release)
            stop = PARAMS["stop_dollars"] / PV
            if not side: continue
            for j in range(e, min(e + PARAMS["hold_minutes"] + 1, ix[-1] + 1)):
                if sec[j] >= FLAT or (j > e and side * (c[j] - c[e]) <= -stop): break
                out[j] = side; rk[j] = PARAMS["stop_dollars"]
    return sig, risk

def signals(panel): return _run(panel)[0]
def entry_risk(panel): return _run(panel)[1]
