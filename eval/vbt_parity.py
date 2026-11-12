#!/usr/bin/env python3
"""Actual vectorbt accounting parity on exact fills, not independent signal validation.

Execution prices already include slippage. Multiply prices by point value so
vectorbt units represent futures contracts. Flat ledger required. Compare each
symbol AND session, not only aggregate PnL; cents tolerance, no percentage escape.
"""
import argparse
import json
import math
from pathlib import Path
import sys

import pandas as pd
import vectorbt as vbt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from instruments import SPECS


def parity(fills, days, tolerance=0.01):
    if not fills or not days:
        raise ValueError('Nonempty fills and session PnL required')
    positions = {}
    groups = {}
    expected_days = {}
    for day in days:
        session, pnl = str(day['session']), float(day['pnl'])
        if session in expected_days or not math.isfinite(pnl):
            raise ValueError('Duplicate or nonfinite session PnL')
        expected_days[session] = pnl
    last_time = None
    for fill in fills:
        symbol, session = fill['symbol'], str(fill['session'])
        spec = SPECS[symbol]
        timestamp = pd.Timestamp(fill['timestamp'])
        q = fill['quantity']
        price, commission = float(fill['price']), float(fill['commission'])
        realized = float(fill['realized_pnl'])
        if (timestamp.tzinfo is None or (last_time is not None and timestamp < last_time)
                or not isinstance(q, int) or isinstance(q, bool) or not q
                or not all(math.isfinite(x) for x in (price, commission, realized))
                or price <= 0 or commission < 0 or session not in expected_days):
            raise ValueError('Invalid fill')
        last_time = timestamp
        old = positions.get(symbol, 0)
        if fill['position_before'] != old or fill['position_after'] != old + q:
            raise ValueError('Inconsistent position chain')
        positions[symbol] = old + q
        groups.setdefault((session, symbol), []).append(fill)
    if any(positions.values()):
        raise ValueError('Open residual positions')
    replay_days = dict.fromkeys(expected_days, 0.)
    checks = []
    for (session, symbol), rows in sorted(groups.items()):
        if sum(f['quantity'] for f in rows):
            raise ValueError('Session not flat')
        prices = pd.Series([float(f['price']) * SPECS[symbol].point_value for f in rows])
        quantities = [f['quantity'] for f in rows]
        fees = [float(f['commission']) for f in rows]
        # Futures margin not simulated: capital only prevents spot-style rejection.
        cash = 1. + sum(abs(q) * p + fee for q, p, fee in zip(quantities, prices, fees))
        pf = vbt.Portfolio.from_orders(
            prices, size=quantities, price=prices, fixed_fees=fees,
            fees=0., slippage=0., init_cash=cash, allow_partial=False, raise_reject=True)
        if len(pf.orders.records) != len(rows):
            raise ValueError('vectorbt dropped fills')
        actual = float(pf.total_profit())
        expected = sum(float(f['realized_pnl']) - float(f['commission']) for f in rows)
        if not math.isfinite(actual):
            raise ValueError('Nonfinite vectorbt PnL')
        checks.append({'session': session, 'symbol': symbol, 'vectorbt_pnl': actual,
                       'sim_pnl': expected, 'difference': actual - expected})
        replay_days[session] += actual
    differences = [abs(c['difference']) for c in checks]
    differences += [abs(replay_days[s] - expected_days[s]) for s in expected_days]
    return {'ok': max(differences) <= tolerance, 'engine': 'vectorbt',
            'version': vbt.__version__, 'tolerance_usd': tolerance,
            'max_difference_usd': max(differences), 'fill_count': len(fills),
            'vectorbt_pnl': sum(replay_days.values()), 'sim_pnl': sum(expected_days.values()),
            'checks': checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ledger', required=True)
    parser.add_argument('--report', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    fills = [json.loads(line) for line in Path(args.ledger).read_text().splitlines() if line.strip()]
    report = json.loads(Path(args.report).read_text())
    result = parity(fills, report['stressed']['days'])
    Path(args.output).write_text(json.dumps(result, allow_nan=False) + '\n')
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
