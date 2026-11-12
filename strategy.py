"""v17n-1 experiment 1.
Mechanism: EIA weekly petroleum inventory release creates an initial liquidity shock;
commercial hedging and delayed price discovery may reverse first 15 minutes.
Falsification: stressed PnL or any chronological era is nonpositive.
"""
import numpy as np

FAMILY = "energy-eia-release-initial-shock-reversal"
PARAMS = {"release_ct_second": 34200, "observe_minutes": 15, "hold_minutes": 45}


def signals(panel):
    result = {}
    for symbol, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if symbol != "QM":
            result[symbol] = out
            continue
        sec = df.ct_sec.to_numpy()
        close = df.close.to_numpy()
        session = df.session.astype(str).to_numpy()
        # Wednesday 09:30 CT release. State only uses completed bars in session.
        weekday = df.index.tz_convert("America/Chicago").weekday.to_numpy()
        for indices in df.groupby(session, sort=False).indices.values():
            i = np.asarray(indices)
            candidates = i[(weekday[i] == 2) & (sec[i] == 34200 + 15 * 60)]
            if not len(candidates):
                continue
            end = candidates[0]
            start = end - 15
            if start < i[0] or sec[start] != 34200:
                continue
            side = -int(np.sign(close[end] - close[start]))
            if side:
                active = i[(i > end) & (i <= end + 45) & (sec[i] < 15 * 3600 + 10 * 60)]
                out[active] = side
        result[symbol] = out
    return result


def entry_risk(panel):
    return {symbol: np.full(len(df), 300.0) for symbol, df in panel.items()}
