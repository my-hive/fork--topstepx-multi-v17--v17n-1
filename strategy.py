"""v17n-1 exp5. Mechanism: refinery utilization and gasoline demand create a daily
crack-spread inventory-balance signal. When prior session RB outperforms CL, RB continuation
at 09:00 CT captures persistent product tightness. Falsification: stressed PnL/era/year checks.
"""
import numpy as np
FAMILY = "energy-prior-session-crack-spread-continuation"
PARAMS = {"entry_ct_sec": 32400, "hold_minutes": 120, "stop_dollars": 280}
FLAT=15*3600+9*60

def _run(p):
 sig={s:np.zeros(len(d),dtype=np.int64) for s,d in p.items()}; risk={s:np.zeros(len(d)) for s,d in p.items()}
 rb,cl=p['RB'],p['CL']; sec=rb.ct_sec.to_numpy(); c=rb.close.to_numpy(); sess=rb.session.astype(str).to_numpy()
 rbclose=rb.close.groupby(sess).last(); clclose=cl.close.reindex(rb.index).groupby(sess).last(); spread=np.log(rbclose).diff()-np.log(clclose).diff()
 groups=list(rb.groupby(sess,sort=False).indices.values())
 for k in range(1,len(groups)):
  v=spread.iloc[k-1]; side=0 if np.isnan(v) else int(np.sign(v)); ix=np.asarray(groups[k]); hit=ix[sec[ix]==PARAMS['entry_ct_sec']]
  if not side or not len(hit): continue
  e=hit[0]; stop=PARAMS['stop_dollars']/42000
  for j in range(e,min(e+PARAMS['hold_minutes']+1,ix[-1]+1)):
   if sec[j]>=FLAT or (j>e and side*(c[j]-c[e])<=-stop): break
   sig['RB'][j]=side; risk['RB'][j]=PARAMS['stop_dollars']
 return sig,risk
def signals(panel): return _run(panel)[0]
def entry_risk(panel): return _run(panel)[1]
