"""v17n-1 experiment 1.
Mechanism: EIA weekly petroleum inventory release (Wed 09:30 CT) creates an initial liquidity
shock; hedger flow and delayed price discovery may partly reverse the first 15 minutes.
Falsification: stressed PnL or any chronological era nonpositive, or <70% positive years.
"""
import numpy as np

FAMILY = "energy-eia-release-initial-shock-reversal"
PARAMS = {"observe_minutes": 15, "hold_minutes": 45, "stop_frac_of_range": 0.5}
PV, FLAT = 500.0, 15 * 3600 + 10 * 60  # QM $/point


def _run(panel):
    sig, risk = {}, {}
    for symbol, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        rk = np.zeros(len(df))
        sig[symbol], risk[symbol] = out, rk
        if symbol != "QM":
            continue
        sec = df.ct_sec.to_numpy()
        close, high, low = (df[c].to_numpy() for c in ("close", "high", "low"))
        session = df.session.astype(str).to_numpy()
        wd = df.index.tz_convert("America/Chicago").weekday.to_numpy()
        for idx in df.groupby(session, sort=False).indices.values():
            i = np.asarray(idx)
            hit = i[(wd[i] == 2) & (sec[i] == 34200 + 14 * 60)]  # last observe bar 09:44
            if not len(hit):
                continue
            end = hit[0]
            start = end - 14
            if start < i[0] or sec[start] != 34200:
                continue
            side = -int(np.sign(close[end] - close[start]))
            rng = high[start:end + 1].max() - low[start:end + 1].min()
            stop = 0.5 * rng
            if not side or stop <= 0 or stop * PV > 300:
                continue
            entry = close[end]  # approx of next open; stop checked on completed closes
            for j in range(end, min(end + 46, i[-1] + 1)):
                if sec[j] >= FLAT or (side * (close[j] - entry) <= -stop and j > end):
                    break
                out[j] = side
                rk[j] = stop * PV
    return sig, risk


def signals(panel):
    return _run(panel)[0]


def entry_risk(panel):
    return _run(panel)[1]
