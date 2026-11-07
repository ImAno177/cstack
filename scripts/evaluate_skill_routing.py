from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter
from pathlib import Path


def load_cases(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding='utf-8'))
    if data.get('version') != 1 or not isinstance(data.get('cases'), list):
        raise ValueError('cases must have version=1 and cases array')
    cases = {}
    for case in data['cases']:
        case_id = case['id']
        if not case_id or case_id in cases or not isinstance(case.get('primary'), str):
            raise ValueError(f'duplicate or invalid case: {case_id!r}')
        cases[case_id] = case
    return cases


def load_results(path: Path, cases: dict[str, dict]) -> dict[tuple[str, int], dict]:
    rows: dict[tuple[str, int], dict] = {}
    for lineno, text in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not text.strip():
            continue
        item = json.loads(text)
        case_id = item.get('id')
        run = item.get('run')
        if case_id not in cases or type(run) is not int or run < 1:
            raise ValueError(f'{path}:{lineno}: unknown case or invalid run')
        key = (case_id, run)
        if key in rows:
            raise ValueError(f'{path}:{lineno}: duplicate id/run: {key}')
        if not isinstance(item.get('primary'), str) or type(item.get('success')) is not bool:
            raise ValueError(f'{path}:{lineno}: primary and boolean success required')
        supporting = item.get('supporting', [])
        if not isinstance(supporting, list) or not all(isinstance(x, str) for x in supporting):
            raise ValueError(f'{path}:{lineno}: supporting must be a skill-name list')
        if item['primary'] in supporting or len(supporting) != len(set(supporting)):
            raise ValueError(f'{path}:{lineno}: repeated skill activation')
        for metric in ('tokens', 'latency_ms'):
            value = item.get(metric)
            if type(value) not in (int, float) or value < 0:
                raise ValueError(f'{path}:{lineno}: {metric} must be nonnegative')
        rows[key] = item
    if not rows:
        raise ValueError(f'{path}: no result rows')
    return rows


def score(rows: dict[tuple[str, int], dict], cases: dict[str, dict]) -> dict:
    results = list(rows.values())
    routing = [row['primary'] == cases[row['id']]['primary'] for row in results]
    supporting = [
        all(name in cases[row['id']].get('allowed_support', []) for name in row.get('supporting', []))
        for row in results
    ]
    mistakes = Counter(
        (cases[row['id']]['primary'], row['primary'])
        for row in results if row['primary'] != cases[row['id']]['primary']
    )
    runs = Counter(row['id'] for row in results)
    return {
        'runs': len(results),
        'cases_covered': len(runs),
        'cases_total': len(cases),
        'min_runs_per_covered_case': min(runs.values()),
        'primary_accuracy': round(statistics.mean(routing), 4),
        'supporting_precision': round(statistics.mean(supporting), 4),
        'outcome_success': round(statistics.mean(row['success'] for row in results), 4),
        'avg_tokens': round(statistics.mean(row['tokens'] for row in results), 2),
        'avg_latency_ms': round(statistics.mean(row['latency_ms'] for row in results), 2),
        'top_confusions': [
            {'expected': expected, 'actual': actual, 'count': count}
            for (expected, actual), count in mistakes.most_common(10)
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description='Score real cstack routing traces; no simulated model results.')
    parser.add_argument('--cases', type=Path, default=Path('benchmarks/skill-routing/cases.json'))
    parser.add_argument('--candidate', type=Path)
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    cases = load_cases(args.cases)
    if not args.candidate:
        if args.baseline:
            parser.error('--baseline requires --candidate')
        for case in cases.values():
            print(f"{case['id']}\t{case['primary']}\t{case['prompt']}")
        print(f'\n{len(cases)} cases; collect >=3 real runs/case before scoring.')
        return 0

    candidate = load_results(args.candidate, cases)
    report = {'candidate': score(candidate, cases)}
    if args.baseline:
        baseline = load_results(args.baseline, cases)
        if set(baseline) != set(candidate):
            raise ValueError('baseline and candidate must contain identical (id, run) pairs')
        before = score(baseline, cases)
        report['baseline'] = before
        report['delta_candidate_minus_baseline'] = {
            name: round(report['candidate'][name] - before[name], 4)
            for name in ('primary_accuracy', 'supporting_precision', 'outcome_success', 'avg_tokens', 'avg_latency_ms')
        }
    report['note'] = 'Only real traces are scored. A routing pass does not prove task completion.'
    serialized = json.dumps(report, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding='utf-8')
    print(serialized, end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
