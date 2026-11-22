"""Keep all runnable public examples aligned with the immutable manifest baseline."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]


class ImageBaselineTests(unittest.TestCase):
    def setUp(self):
        self.lock = json.loads((ROOT / 'operations/validation/images.lock.json').read_text())['images']

    def test_manifest_references_are_immutable_and_support_reference_architecture(self):
        for record in self.lock.values():
            self.assertRegex(record['image'], r'^[a-zA-Z0-9./:_-]+@sha256:[a-f0-9]{64}$')
            self.assertIn('linux/amd64', record['platforms'])

    def test_consuming_examples_and_api_base_match_the_lock(self):
        keys = {'POSTGRES_IMAGE':'postgres', 'NGINX_IMAGE':'nginx', 'PROXY_IMAGE':'nginx',
                'APP_IMAGE':'nginx', 'PROMETHEUS_IMAGE':'prometheus', 'GRAFANA_IMAGE':'grafana', 'JENKINS_IMAGE':'jenkins'}
        examples = list((ROOT / 'services').rglob('.env.example'))
        examples.append(ROOT / 'operations/backups/restore-example/.env.example')
        for example in examples:
            for line in example.read_text().splitlines():
                key, separator, value = line.partition('=')
                if separator and key in keys:
                    self.assertEqual(value, self.lock[keys[key]]['image'], str(example.relative_to(ROOT)))
        dockerfile = (ROOT / 'services/demo-api/Dockerfile').read_text()
        self.assertIn('ARG PYTHON_IMAGE=' + self.lock['python']['image'], dockerfile)


if __name__ == '__main__':
    unittest.main()
