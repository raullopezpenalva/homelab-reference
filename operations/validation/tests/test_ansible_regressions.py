"""Run only file-staging tasks in a temporary local directory; never apt or Docker."""
import copy
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

try:
    import yaml
    from jinja2 import Environment, StrictUndefined
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[3]
BUNDLE = ROOT / 'infrastructure/ansible/roles/bundle'


@unittest.skipUnless(yaml is not None, 'Install validation requirements for Ansible regression tests')
class RuntimePackageTests(unittest.TestCase):
    def setUp(self):
        self.tasks = yaml.safe_load((ROOT / 'infrastructure/ansible/roles/runtime/tasks/main.yml').read_text())
        self.versions = {name: '1.0.0-reference' for name in [
            'docker-ce', 'docker-ce-cli', 'containerd.io', 'docker-buildx-plugin', 'docker-compose-plugin']}
        self.env = Environment(undefined=StrictUndefined)

    def test_all_reviewed_versions_are_requested_in_one_transaction(self):
        installs = [task for task in self.tasks if 'ansible.builtin.apt' in task]
        self.assertEqual(len(installs), 1)
        self.assertNotIn('loop', installs[0])
        expression = installs[0]['ansible.builtin.apt']['name'].strip()[2:-2].strip()
        specs = self.env.compile_expression(expression)(lab_runtime_versions=self.versions)
        self.assertEqual(set(specs), {f'{key}={version}' for key, version in self.versions.items()})

    def test_wrong_installed_version_is_rejected_before_runtime_start(self):
        index = next(i for i, task in enumerate(self.tasks) if task['name'].startswith('Require installed runtime versions'))
        start = next(i for i, task in enumerate(self.tasks) if task['name'] == 'Start reference runtimes')
        self.assertLess(index, start)
        conditions = self.tasks[index]['ansible.builtin.assert']['that']
        item = {'key': 'docker-ce', 'value': '1.0.0-reference'}
        def accepted(version):
            facts = {'packages': {'docker-ce': [{'version': version}]}}
            return all(self.env.compile_expression(expr)(item=item, ansible_facts=facts) for expr in conditions)
        self.assertTrue(accepted(item['value']))
        self.assertFalse(accepted('different-version'))


@unittest.skipUnless(yaml is not None and shutil.which('ansible-playbook'), 'Ansible and validation requirements required')
class BundleStagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='reference-staging-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / 'source'
        shutil.copytree(ROOT / 'services/observability', self.source / 'observability')
        self.destination = self.base / 'destination'
        tasks = copy.deepcopy(yaml.safe_load((BUNDLE / 'tasks/stage.yml').read_text()))
        # Preserve the shipping loop/templates from the real role. Redirect only
        # filesystem roots and ownership so the test never touches /srv or root files.
        for task in tasks:
            for key in ['ansible.builtin.file', 'ansible.builtin.copy', 'ansible.builtin.template']:
                if key not in task:
                    continue
                options = task[key]
                options.pop('owner', None)
                options.pop('group', None)
                for field in ['path', 'dest']:
                    if field in options:
                        options[field] = options[field].replace('/srv/lab', str(self.destination))
                if key == 'ansible.builtin.copy':
                    options['src'] = options['src'].replace('{{ playbook_dir }}/../../../services', str(self.source))
                if key == 'ansible.builtin.template':
                    options['src'] = str(BUNDLE / 'templates' / options['src'])
        variables = yaml.safe_load((BUNDLE / 'vars/main.yml').read_text())
        variables.update(lab_bundle='telemetry', lab_secret_dir='/unused-reference-test',
                         lab_images={'PROMETHEUS_IMAGE': 'example.com/prometheus@sha256:' + 'a' * 64,
                                     'GRAFANA_IMAGE': 'example.com/grafana@sha256:' + 'b' * 64})
        self.playbook = self.base / 'stage.yml'
        self.playbook.write_text(yaml.safe_dump([{'name': 'Temporary local staging regression',
                                                  'hosts': 'localhost', 'gather_facts': False,
                                                  'become': False, 'vars': variables, 'tasks': tasks}], sort_keys=False))
        self.inventory = self.base / 'inventory.yml'
        self.write_inventory('10.64.20.31')

    def write_inventory(self, address):
        self.inventory.write_text(yaml.safe_dump({'all': {'hosts': {
            'localhost': {'ansible_connection': 'local', 'ansible_python_interpreter': sys.executable,
                          'ansible_host': '127.0.0.1', 'lab_role': 'telemetry'},
            'synthetic-guest': {'ansible_host': address, 'lab_role': 'telemetry'}}}}))

    def stage(self):
        environment = dict(os.environ, ANSIBLE_LOCAL_TEMP=str(self.base / 'ansible-tmp'),
                           ANSIBLE_NOCOLOR='1', ANSIBLE_CONFIG=str(ROOT / 'infrastructure/ansible/ansible.cfg'))
        result = subprocess.run(['ansible-playbook', '-i', str(self.inventory), str(self.playbook)],
                                env=environment, capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout[-5000:] + result.stderr[-2000:])
        recap = re.findall(r'changed=(\d+)', result.stdout)
        self.assertTrue(recap, 'Missing play recap')
        return int(recap[-1])

    def test_second_staging_and_readme_changes_are_noop(self):
        self.assertGreater(self.stage(), 0)
        self.assertEqual(self.stage(), 0)
        source = self.source / 'observability'
        (source / 'README.md').write_text('Changed documentation only\n')
        (source / '.env').write_text('LOCAL_ONLY=SYNTHETIC-NOT-FOR-DELIVERY\n')
        self.assertEqual(self.stage(), 0)
        self.assertNotIn('LOCAL_ONLY', (self.destination / 'telemetry/.env').read_text())
        self.assertFalse((self.destination / 'telemetry/README.md').exists())

    def test_static_and_inventory_changes_are_delivered(self):
        self.stage()
        self.write_inventory('10.64.20.32')
        self.assertGreater(self.stage(), 0)
        self.assertIn('10.64.20.32', (self.destination / 'telemetry/prometheus.yml').read_text())
        rules = self.source / 'observability/rules.yml'
        rules.write_text(rules.read_text() + '\n# Synthetic reviewed change\n')
        self.assertGreater(self.stage(), 0)
        self.assertEqual(rules.read_text(), (self.destination / 'telemetry/rules.yml').read_text())
        self.assertEqual(self.stage(), 0)


if __name__ == '__main__':
    unittest.main()
