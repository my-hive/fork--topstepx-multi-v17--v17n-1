"""v17n-1 exp8. Mechanism: Winter heating demand and distillate inventory draw risk create positive daytime HO drift
in Nov-Feb. Long HO 09:00-14:00 CT, fixed $280 stop. Falsification: stressed PnL/era/year checks.
"""
import numpy as np
FAMILY = "energy-gasoline-heating-oil-winter-demand"
PARAMS = {"season_start_month": 11, "season_end_month": 2, "entry_ct_sec": 32400, "stop_dollars": 280}
FLAT = 15 * 3600 + 9 * 60

def _run(panel):
 sig,risk={},{}
 for s,d in panel.items():
  out,rk=np.zeros(len(d),dtype=np.int64),np.zeros(len(d)); sig[s],risk[s]=out,rk
  if s!='HO': continue
  sec,c=d.ct_sec.to_numpy(),d.close.to_numpy(); month=d.index.month.to_numpy()
  for ix in d.groupby(d.session.astype(str),sort=False).indices.values():
   ix=np.asarray(ix); hit=ix[(sec[ix]==32400)&((month[ix]>=11)|(month[ix]<=2))]
   if not len(hit): continue
   e=hit[0]; stop=PARAMS['stop_dollars']/42000
   for j in range(e,ix[-1]+1):
    if sec[j]>=FLAT or (j>e and c[j]-c[e]<=-stop): break
    out[j]=1;rk[j]=PARAMS['stop_dollars']
 return sig,risk
def signals(panel): return _run(panel)[0]
def entry_risk(panel): return _run(panel)[1]
