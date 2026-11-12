"""v17n-1 exp2. Mechanism: natural-gas trend persistence from slow storage/weather information
diffusion and producer-hedger pressure. Sign of trailing 5-session return (completed session
closes) is held intraday 08:30-14:50 CT in QG with hard stop. Falsification: stressed PnL or any
era nonpositive, or <70% positive years -> trend not harvestable intraday after costs.
"""
import numpy as np

FAMILY = "energy-ng-multisession-trend-intraday"
PARAMS = {"lookback_sessions": 5, "entry_ct_sec": 30600, "stop_dollars": 280}
PV = 2500.0
FLAT = 15 * 3600 + 9 * 60


def _run(panel):
    sig, risk = {}, {}
    for symbol, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        rk = np.zeros(len(df))
        sig[symbol], risk[symbol] = out, rk
        if symbol != "QG":
            continue
        sec = df.ct_sec.to_numpy()
        close = df.close.to_numpy()
        groups = list(df.groupby(df.session.astype(str), sort=False).indices.values())
        last = [g[-1] for g in groups]
        stop = PARAMS["stop_dollars"] / PV
        for k in range(PARAMS["lookback_sessions"], len(groups)):
            ret = close[last[k - 1]] - close[last[k - 1 - PARAMS["lookback_sessions"]]]
            side = int(np.sign(ret))
            g = np.asarray(groups[k])
            ent = g[sec[g] == PARAMS["entry_ct_sec"]]
            if not side or not len(ent):
                continue
            e = ent[0]
            entry = close[e]
            for j in range(e, g[-1] + 1):
                if sec[j] >= FLAT or (j > e and side * (close[j] - entry) <= -stop):
                    break
                out[j] = side
                rk[j] = PARAMS["stop_dollars"]
    return sig, risk


def signals(panel):
    return _run(panel)[0]


def entry_risk(panel):
    return _run(panel)[1]
