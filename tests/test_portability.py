"""Exercise locking and cached execution using disposable paths only."""
import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from filelock import FileLock

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / 'Analysis/mixed_logit_v4/src'))
import run_mixed
import validate_preparation


class PortabilityTests(unittest.TestCase):
    def setUp(self):
        scratch = PROJECT / '.local' / 'tests'
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.label = 'all_packs__income__aac'
        self.out = self.root / 'results' / self.label
        self.out.mkdir(parents=True)
        self.path = self.out / 'run.lock'
        self.argv = ['run_mixed.py', '--sample', 'all_packs', '--demographic', 'income', '--iv', 'aac']

    def child(self, code):
        return subprocess.run(
            [sys.executable, '-c', code, str(self.path)], capture_output=True,
            text=True, timeout=30,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
        )

    def test_other_process_is_excluded_then_can_acquire(self):
        code = """import sys
from filelock import FileLock, Timeout
try:
    with FileLock(sys.argv[1], timeout=0):
        print('acquired')
except Timeout:
    sys.exit(3)
"""
        with FileLock(self.path):
            blocked = self.child(code)
            self.assertEqual(blocked.returncode, 3, blocked.stderr)
        released = self.child(code)
        self.assertEqual(released.returncode, 0, released.stderr)
        self.assertIn('acquired', released.stdout)

    def test_abrupt_exit_releases_os_lock(self):
        ended = self.child("import os, sys; from filelock import FileLock; lock=FileLock(sys.argv[1]); lock.acquire(); os._exit(0)")
        self.assertEqual(ended.returncode, 0, ended.stderr)
        with FileLock(self.path, timeout=0):
            pass

    def test_stale_marker_does_not_block(self):
        self.path.write_text('historical marker', encoding='utf-8')
        with FileLock(self.path, timeout=0):
            pass

    def test_cached_runner_does_not_estimate_or_change_saved_files(self):
        saved = {'summary.json': b'{"cached": true}', 'pyblp_results.pkl.gz': b'not opened by cached runner'}
        for name, content in saved.items():
            (self.out / name).write_bytes(content)
        with patch.object(run_mixed, 'ROOT', self.root), patch.object(sys, 'argv', self.argv), \
             patch.object(run_mixed, 'load_data', side_effect=AssertionError('must not estimate')), \
             contextlib.redirect_stdout(io.StringIO()) as stdout:
            run_mixed.main()
        self.assertIn('CACHED', stdout.getvalue())
        for name, content in saved.items():
            self.assertEqual((self.out / name).read_bytes(), content)
        self.assertFalse((self.out / 'process.json').exists())
        with FileLock(self.path, timeout=0):
            pass

    def test_runner_exception_releases_lock(self):
        with patch.object(run_mixed, 'ROOT', self.root), patch.object(sys, 'argv', self.argv), \
             patch.object(run_mixed, 'run_locked', side_effect=RuntimeError('test failure')):
            with self.assertRaisesRegex(RuntimeError, 'test failure'):
                run_mixed.main()
        with FileLock(self.path, timeout=0):
            pass

    def test_preparation_cli_defaults_to_no_writes(self):
        with patch.object(sys, 'argv', ['validate_preparation.py']), \
             patch.object(validate_preparation, 'validate') as validate, \
             contextlib.redirect_stdout(io.StringIO()):
            validate.return_value.to_string.return_value = 'audit'
            validate_preparation.main()
        validate.assert_called_once_with(write_artifacts=False)


if __name__ == '__main__':
    unittest.main()
