"""v17n-1 exp3. Mechanism: weekend geopolitical/news risk is priced into Monday crude
opening flow then fades as physical-market liquidity returns. Fade first 30m CL move at 09:00 CT.
Falsification: stressed PnL or any era nonpositive, or <70% positive years.
"""
import numpy as np
FAMILY = "energy-crude-weekend-risk-liquidity-reversal"
PARAMS = {"observe_minutes": 30, "hold_minutes": 60, "stop_dollars": 280}
PV, START, FLAT = 1000., 9 * 3600, 15 * 3600 + 9 * 60

def _run(panel):
    sig, risk = {}, {}
    for s, d in panel.items():
        out, rk = np.zeros(len(d), dtype=np.int64), np.zeros(len(d)); sig[s], risk[s] = out, rk
        if s != "CL": continue
        sec, c = d.ct_sec.to_numpy(), d.close.to_numpy(); wd=d.index.tz_convert("America/Chicago").weekday.to_numpy()
        for ix in d.groupby(d.session.astype(str), sort=False).indices.values():
            ix=np.asarray(ix); hit=ix[(wd[ix]==0)&(sec[ix]==START+29*60)]
            if not len(hit): continue
            e=hit[0]; a=e-29
            if a < ix[0] or sec[a]!=START: continue
            side=-int(np.sign(c[e]-c[a])); stop=PARAMS['stop_dollars']/PV
            if not side: continue
            for j in range(e,min(e+PARAMS['hold_minutes']+1,ix[-1]+1)):
                if sec[j]>=FLAT or (j>e and side*(c[j]-c[e])<=-stop): break
                out[j]=side; rk[j]=PARAMS['stop_dollars']
    return sig,risk
def signals(panel): return _run(panel)[0]
def entry_risk(panel): return _run(panel)[1]
