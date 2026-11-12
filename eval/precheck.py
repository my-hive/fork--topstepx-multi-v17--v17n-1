"""Slot-free dev screen, then frozen final null + ledger; no sealed mount."""
import argparse
import json
from pathlib import Path
import sys
import sim


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ('candidate', 'data', 'symbols', 'output'):
        parser.add_argument('--' + key, required=True)
    args = parser.parse_args()
    symbols = json.loads(args.symbols)
    if not isinstance(symbols, list) or not symbols or not all(isinstance(s, str) for s in symbols):
        raise ValueError('Nonempty symbol list required')
    base = ['sim.py', '--strategy', args.candidate, '--data', args.data,
            '--symbols', *symbols, '--output', args.output]
    # Reject structurally weak candidates without spending 200 permutation runs.
    sys.argv = base + ['--null-seeds', '0', '--mode', 'final']
    sim.main()
    report = json.loads(Path(args.output).read_text())
    stressed = report['stressed']
    checks = stressed['eligibility']['checks']
    if stressed['worst_three_mean'] <= 0 or any(
            value is not True for key, value in checks.items() if key != 'side_null_p_le_0_05'):
        return
    sys.argv = base + ['--ledger', '/results/fills.jsonl', '--null-seeds', '200', '--mode', 'final']
    sim.main()


if __name__ == '__main__':
    main()
