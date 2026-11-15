"""Read-only research checks; evidence defaults to ignored .local/validation/."""
import gzip
import argparse
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import pickle
import platform
import subprocess
import sys
import time
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / 'Analysis/mixed_logit_v4/src'))
import numpy as np
import pandas as pd
import pyblp
from validate_preparation import validate


def fingerprint():
    """Hash research files, excluding only Python's disposable bytecode cache."""
    files = {}
    for folder in ['Analysis', 'Archive', 'Data', 'Paper']:
        for path in sorted((PROJECT / folder).rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts or path.suffix in {'.pyc', '.pyo'}:
                continue
            with path.open('rb') as stream:
                files[path.relative_to(PROJECT).as_posix()] = hashlib.file_digest(stream, 'sha256').hexdigest()
    return files


def main():
    if not __debug__:
        raise RuntimeError('Run without -O: preparation validation uses assertions.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', help='New isolated evidence directory outside protected research folders; refuses an existing directory.')
    args = parser.parse_args()
    evidence = (PROJECT / args.output_dir).resolve() if args.output_dir else PROJECT / '.local/validation'
    if any((PROJECT / name).resolve() == evidence or (PROJECT / name).resolve() in evidence.parents
           for name in ['Analysis', 'Archive', 'Data', 'Paper']):
        raise ValueError('Evidence must be outside protected research folders to avoid changing the preservation inventory.')
    evidence.mkdir(parents=True, exist_ok=args.output_dir is None)
    report = {'platform': platform.platform(), 'python': platform.python_version(),
              'packages': {name: version(name) for name in ['numpy', 'pandas', 'scipy', 'pyblp', 'statsmodels', 'filelock']},
              'estimation_run': False}
    start = time.monotonic()
    before = fingerprint()
    (evidence / 'artifacts-before.json').write_text(json.dumps(before, indent=2), encoding='utf-8')
    try:
        completed = subprocess.run(
            [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=PROJECT,
            capture_output=True, text=True, timeout=120,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
        )
        (evidence / 'portability-tests.txt').write_text(completed.stdout + completed.stderr, encoding='utf-8')
        print(completed.stdout + completed.stderr, flush=True)
        completed.check_returncode()
        report['portability_tests_passed'] = True

        # Prevent accidental estimation if later changes introduce a solve call.
        with patch.object(pyblp.Problem, 'solve', side_effect=AssertionError('Estimation is forbidden in this check')):
            audit = validate(write_artifacts=False)
            saved = pd.read_csv(PROJECT / 'Analysis/mixed_logit_v4/data/sample_audit.csv')
            keys = ['sample', 'demographic']
            pd.testing.assert_frame_equal(audit.sort_values(keys).reset_index(drop=True),
                                          saved.sort_values(keys).reset_index(drop=True), check_dtype=False)
            report['preparation'] = audit.to_dict(orient='records')
            print(audit.to_string(index=False), flush=True)

            # Load one trusted repository result and predict one market at saved parameters.
            # No optimizer, re-estimation, or saved-result writes are involved.
            folder = PROJECT / 'Analysis/mixed_logit_v4/results/all_packs__household__aac'
            with gzip.open(folder / 'pyblp_results.pkl.gz', 'rb') as stream:
                result = pickle.load(stream)
            pyblp.options.verbose = False
            market = result.problem.unique_market_ids[0]
            predicted = result.compute_shares(market_id=market).ravel()
            ids = np.asarray(result.problem.products.market_ids).ravel()
            expected = np.asarray(result.problem.products.shares).ravel()[ids == market]
            error = float(np.max(np.abs(predicted - expected)))
            if error >= 1e-8:
                raise AssertionError(f'Saved-market share mismatch: {error}')
            report['saved_result'] = {'model': folder.name, 'market': str(market),
                                      'products': len(expected), 'max_share_error': error}
        report['passed'] = True
    except BaseException as error:
        report['passed'] = False
        report['error'] = f'{type(error).__name__}: {error}'
        raise
    finally:
        after = fingerprint()
        changed = sorted(key for key in before.keys() | after.keys() if before.get(key) != after.get(key))
        report['protected_file_count'] = len(before)
        report['changed_research_files'] = changed
        report['elapsed_seconds'] = round(time.monotonic() - start, 2)
        if changed:
            report['passed'] = False
        (evidence / 'artifacts-after.json').write_text(json.dumps(after, indent=2), encoding='utf-8')
        (evidence / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(json.dumps(report, indent=2), flush=True)
        if changed:
            raise RuntimeError(f'Research files changed during validation: {changed}')


if __name__ == '__main__':
    main()
