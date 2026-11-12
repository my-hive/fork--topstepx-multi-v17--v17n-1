# v17 research contract

This contract supersedes v16. Historical artifacts remain untouched in hive-swarm-task-v16 and archived agent workdirs.

## Objective and unchanged pass bar
Find reproducible TopstepX-style 50K combine strategies across available development futures. Custom evaluator remains combine-rule truth: $3,000 target, $1,000 daily loss, $2,000 EOD trailing maximum loss, $300 maximum entry risk, <=5 standard equivalents, >=2 trading days, best day below 50% total profit; flatten by 15:09 CT minute close. Costs and next-minute execution unchanged from v16. Simulated research, not live trading authorization or broker compliance certification.

## Data and causality
Only /data/dev: 2010-06 through 2023-12, actual symbol availability varies. 49 cache-present roots, no synthesized pre-launch micro history. One-minute OHLCV, UTC minute-start timestamps. Completed-bar signal, next-minute-open fill. Higher-timeframe resampling allowed only after final constituent minute closes. Walk-forward ML training/scaling/feature selection uses past data only. No external services or web research. No sealed data access.

## Scoring and validation
Development score is graded exploration feedback, not eligibility. Final eligibility retains every-year positive stressed PnL, all three chronological era blocks positive, entry diversity and risk, plus frozen 200-seed primary side-null p<=.05. No gate relaxed. Primary statistic worst_three_mean unchanged. Zero statistic or all-tied null is diagnosed as uninformative for side advantage, never promoted. Additional PnL permutation p is exploratory and cannot replace primary null.

Only strategy.py editable. Declare FAMILY and PARAMS. Maximum six independent entry gates; report all free numerical choices honestly. No hidden sweeps. Prefix causality checks remain necessary but not exhaustive proof.

## Roles, collaboration and caps
Six TIER-2 explorers start energy, metals, FX, rates, ags/livestock/crypto, equity-index/cross-asset. First eight experiments independent in seed area. Three TIER-3 analysts reproduce exact peer source SHAs and audit. One TIER-1 gatekeeper coordinates work orders and freezes verified finalists. All markets remain open after seed exploration. Pivot after eight family nonimprovements; stop at total cap: 30 explorer/gatekeeper, 20 analyst. Twelve-hour deadline is ceiling. Write .hive/research-complete before exit. No auto-restarts or identity top-ups.

Every attempt logs source hash, family, symbols, hypothesis, metrics and failures in experiments.jsonl. Share development evidence, attribute adoption, preserve sources before claims. Do not count reproductions as new mechanisms. FAMILY names do not make variants independent. No active novelty bonus. Native leaderboard remains per run; owner family-collapsed board is a summary, not scoring machinery.

## Shared sealed pool and independent parity
Only gatekeeper queues frozen source to v17-validate. Candidate Python runs in a disposable producer sandbox. Fresh scorer process reads numeric outputs only, validates target/risk prefix consistency, and never imports candidate code; candidate cannot monkeypatch scoring. Host first runs development structural screen, then final 200-seed null in dev-only sandbox, then actual vectorbt replay of exact simulator fills with 1-cent per-symbol/session tolerance. Parity checks accounting, not independently generated signals or combine rules. Reject any failed precheck without burning sealed slot. Atomically reserve from shared six-slot pool only after success; evaluate identical frozen bytes on sealed 2024-01 through 2025-08. Return status bits only. No retries of interrupted sealed runs and no quota reset. Do not resubmit tweaked failed sealed families. Owner reviews survivor in Nautilus later; Nautilus is not installed or claimed as completed now.

## Research resources
Installed ML/indicator tools include scipy, scikit-learn, statsmodels, XGBoost, LightGBM, TA-Lib alongside pandas/numpy/numba/vectorbt. Ideas: causal resampled trends, cross-market lead-lag, rates curve relative value, metals ratios, energy inventory response, calendar mechanisms, grains/livestock seasonality, transparent walk-forward regime classification, small constrained expression search. Use economic hypotheses and explicit falsifiers, not arbitrary numeric searches.

## Retained v16 evidence
280 recorded attempts across 42 symbols; no sealed candidates. Turn-of-month index drift: dev .2851, era PnL +2973.25/+30.5/+5728.5, yearly profitability 1.0 but primary statistic zero and null ties. NQ prior-day reversal: .2627, eras all positive, only 9/14 years profitable. Leads only, not winners. MNQ PM momentum/overnight-long previously failed sealed validation: do not rediscover default family.
