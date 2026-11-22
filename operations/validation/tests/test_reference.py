import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded

inventory = module("inventory", "operations/provisioning/inventory.py")
release = module("release", "operations/deploy/validate.py")
api = module("api", "services/demo-api/app.py")
storage = module("storage", "infrastructure/ansible/roles/runtime/files/storage-check.py")
restore = module("restore", "operations/backups/check_restore.py")

class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT/"infrastructure/proxmox/examples/lab.json").read_text())

    def test_empty_selection_has_no_hosts(self):
        self.assertEqual(inventory.render(self.config, [])["all"]["children"], {})

    def test_only_selected_role_is_rendered(self):
        result = inventory.render(self.config, ["applications"])
        self.assertEqual(set(result["all"]["children"]), {"applications"})

    def test_unknown_role_rejected(self):
        with self.assertRaises(ValueError):
            inventory.render(self.config, ["unknown"])

    def test_duplicate_identity_rejected(self):
        self.config["guests"]["telemetry"]["vm_id"] = self.config["guests"]["applications"]["vm_id"]
        with self.assertRaises(ValueError):
            inventory.render(self.config, ["telemetry"])

class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.doc = {"schema":"reference.release/v1", "bundle":"applications",
                    "images":{"NGINX_IMAGE":"example.com/proxy@sha256:" + "a"*64,
                              "API_IMAGE":"example.com/api@sha256:" + "b"*64},
                    "revision":"c"*40, "recovery":"isolated-test-recovery-record"}

    def test_digest_metadata_does_not_claim_deployment(self):
        self.assertEqual(release.validate(self.doc)["status"], "metadata-valid-not-deployed")

    def test_commands_rejected(self):
        self.doc["command"] = "forbidden"
        with self.assertRaises(ValueError): release.validate(self.doc)

    def test_mutable_tag_rejected(self):
        self.doc["images"]["API_IMAGE"] = "example.com/api:latest"
        with self.assertRaises(ValueError): release.validate(self.doc)

    def test_database_cannot_be_promoted_as_web(self):
        self.doc["images"]["POSTGRES_IMAGE"] = "example.com/db@sha256:" + "d"*64
        with self.assertRaises(ValueError): release.validate(self.doc)

    def test_synthetic_zero_digest_rejected(self):
        self.doc["images"]["API_IMAGE"] = "example.com/api@sha256:" + "0"*64
        with self.assertRaises(ValueError): release.validate(self.doc)

class ApiTests(unittest.TestCase):
    def test_liveness_does_not_need_database(self):
        self.assertEqual(api.response('/health/live', lambda: self.fail('database called'))[0], 200)

    def test_readiness_fails_closed_and_redacts_error(self):
        def unavailable(): raise RuntimeError('synthetic-private-connection-details')
        status, body = api.response('/health/ready', unavailable)
        self.assertEqual(status, 503)
        self.assertNotIn('synthetic-private', json.dumps(body))

    def test_message_uses_database_reader(self):
        self.assertEqual(api.response('/api/message', lambda: 'test greeting'), (200, {'message':'test greeting'}))

    def test_unknown_route_does_not_query(self):
        self.assertEqual(api.response('/unknown', lambda: self.fail('database called'))[0], 404)

class StorageTests(unittest.TestCase):
    def test_missing_or_root_filesystem_rejected(self):
        self.assertFalse(storage.accepted('synthetic-data-uuid', ''))
        self.assertFalse(storage.accepted('synthetic-data-uuid', 'synthetic-root-uuid'))

    def test_exact_filesystem_accepted(self):
        self.assertTrue(storage.accepted('synthetic-data-uuid', 'synthetic-data-uuid\n'))

class RestoreTests(unittest.TestCase):
    def setUp(self):
        self.config = {"name":"reference-restore", "services":{"database":{"volumes":[{"type":"volume", "source":"database"}]}},
                       "volumes":{"database":{"name":"reference-restore_database"}},
                       "networks":{"app_data":{"name":"reference-restore-data", "internal":True}}}

    def test_isolated_manifest_accepted(self):
        restore.validate(self.config)

    def test_existing_volume_rejected(self):
        self.config['volumes']['database']['name'] = 'reference-database_database'
        with self.assertRaises(ValueError): restore.validate(self.config)

    def test_host_bind_rejected(self):
        self.config['services']['database']['volumes'][0]['type'] = 'bind'
        with self.assertRaises(ValueError): restore.validate(self.config)

    def test_explicit_container_identity_rejected(self):
        self.config['services']['database']['container_name'] = 'existing-database'
        with self.assertRaises(ValueError): restore.validate(self.config)

if __name__ == '__main__': unittest.main()
