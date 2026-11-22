"""Validate the integration harness guardrails without starting any workload."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('integration', ROOT / 'operations/validation/integration.py')
integration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(integration)


class IntegrationPlanTests(unittest.TestCase):
    def test_default_plan_has_no_process_or_docker_call(self):
        with patch.object(integration.subprocess, 'run', side_effect=AssertionError('No execution permitted')):
            plan = integration.plan()
        self.assertEqual(plan['status'], 'planned-not-executed')
        self.assertEqual(plan['published_ports'], [])
        self.assertEqual(set(plan['images']), {'python', 'postgres', 'nginx'})

    def test_execution_rejects_a_developer_machine(self):
        with self.assertRaises(integration.TrialError):
            integration.require_ci({})

    def test_execution_rejects_remote_docker_even_in_ci(self):
        with self.assertRaises(integration.TrialError):
            integration.require_ci({'GITHUB_ACTIONS':'true', 'RUNNER_ENVIRONMENT':'github-hosted', 'RUNNER_OS':'Linux',
                                    'DOCKER_HOST':'tcp://192.0.2.10:2376'})

    def test_execution_rejects_an_inherited_named_context(self):
        with self.assertRaises(integration.TrialError):
            integration.require_ci({'GITHUB_ACTIONS':'true', 'RUNNER_ENVIRONMENT':'github-hosted', 'RUNNER_OS':'Linux',
                                    'DOCKER_CONTEXT':'synthetic-other-environment'})

    def test_port_removal_and_project_volume_isolation(self):
        original = {'services':{'api':{'ports':['8080:8000'], 'restart':'always'}},
                    'networks':{'app_data':{'name':'reference-app-data'}, 'http':{}},
                    'volumes':{'database':{}}}
        result = integration.isolate(original, 'reference-test-example', 'reference-test-data')
        self.assertNotIn('ports', result['services']['api'])
        self.assertEqual(result['networks']['app_data']['name'], 'reference-test-data')
        self.assertEqual(result['volumes']['database']['name'], 'reference-test-example_database')
        self.assertIn('ports', original['services']['api'])

    def test_existing_external_volumes_are_rejected(self):
        with self.assertRaises(integration.TrialError):
            integration.isolate({'services':{}, 'volumes':{'database':{'external':True}}}, 'test', 'test-data')

    def test_privileged_service_is_rejected(self):
        with self.assertRaises(integration.TrialError):
            integration.isolate({'services':{'api':{'privileged':True}}}, 'test', 'test-data')


if __name__ == '__main__':
    unittest.main()
