"""Check rendered deployment settings against the pinned upstream startup guard."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get('PANEL_SOURCE_DIR', ROOT / '.upstream')).resolve()


class ComposeTest(unittest.TestCase):
    def render(self, **overrides):
        values = dict(line.split('=', 1) for line in (ROOT / '.env.example').read_text().splitlines()
                      if line and not line.startswith('#'))
        values.update(LRTMP2_API_TOKEN='a' * 64, SECRET_KEY='b' * 64,
                      PANEL_PASSWORD='validation-only-password')
        values.update(overrides)
        env = {k: v for k, v in os.environ.items() if k not in values}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / '.env'
            path.write_text(''.join(f'{k}={v}\n' for k, v in values.items()))
            result = subprocess.run(['docker', 'compose', '-f', str(ROOT / 'docker-compose.yml'),
                                     '--env-file', str(path), 'config', '--format', 'json'],
                                    env=env, text=True, capture_output=True, check=True)
        return json.loads(result.stdout)['services']['rtmppanel']['environment']

    def validate_upstream(self, settings):
        self.assertTrue((SOURCE / 'config.py').is_file(), 'Pinned upstream source must be available')
        env = {'PATH': os.environ['PATH'], 'PYTHONPATH': str(SOURCE)}
        env.update(settings)
        return subprocess.run(['python3', '-c', 'import config'], env=env, cwd=SOURCE,
                              capture_output=True, text=True)

    def test_defaults_pass_real_upstream_startup_validation(self):
        settings = self.render()
        self.assertEqual(settings['GUNICORN_WORKERS'], '1')
        self.assertEqual(settings['ALLOW_INSECURE_NO_LOGIN'], '0')
        self.assertEqual(settings['LRTMP2_STATS_URL'], 'http://localhost:8090')
        result = self.validate_upstream(settings)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_independent_custom_api_and_browser_urls(self):
        settings = self.render(LRTMP2_API_URL='http://host.docker.internal:9190',
                               LRTMP2_STATS_URL='https://stream.example.com:9443')
        self.assertEqual(settings['LRTMP2_API_URL'], 'http://host.docker.internal:9190')
        self.assertEqual(settings['LRTMP2_STATS_URL'], 'https://stream.example.com:9443')
        self.assertNotIn('RTMP_API_PORT', (ROOT / '.env.example').read_text())

    def test_no_login_requires_explicit_acknowledgement(self):
        denied = self.validate_upstream(self.render(REQUIRE_LOGIN='False'))
        self.assertNotEqual(denied.returncode, 0)
        self.assertIn('ALLOW_INSECURE_NO_LOGIN', denied.stderr)
        allowed = self.validate_upstream(self.render(REQUIRE_LOGIN='False', ALLOW_INSECURE_NO_LOGIN='1'))
        self.assertEqual(allowed.returncode, 0, allowed.stderr)

    def test_multiple_workers_require_shared_backend(self):
        denied = self.validate_upstream(self.render(GUNICORN_WORKERS='2'))
        self.assertNotEqual(denied.returncode, 0)
        self.assertIn('multiple Gunicorn workers', denied.stderr)
        allowed = self.validate_upstream(self.render(GUNICORN_WORKERS='2',
                                                     RATELIMIT_STORAGE_URI='redis://redis:6379/0'))
        self.assertEqual(allowed.returncode, 0, allowed.stderr)

    def test_entrypoint_defaults_to_one_worker(self):
        with tempfile.TemporaryDirectory() as tmp:
            stub = Path(tmp) / 'gunicorn'
            stub.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\n')
            stub.chmod(0o755)
            env = {'PATH': tmp + ':' + os.environ['PATH'], 'SECRET_KEY': 'b' * 64,
                   'PANEL_DB_PATH': str(Path(tmp) / 'panel.db')}
            result = subprocess.run(['sh', str(ROOT / 'entrypoint.sh')], env=env,
                                    text=True, capture_output=True, check=True)
            args = result.stdout.splitlines()
            self.assertEqual(args[args.index('--workers') + 1], '1')


if __name__ == '__main__':
    unittest.main()
