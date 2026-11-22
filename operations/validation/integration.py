#!/usr/bin/env python3
"""Plan an isolated application/recovery trial; execution is restricted to hosted CI."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
LOCK = ROOT / 'operations/validation/images.lock.json'
STEPS = ['build-api', 'start-database', 'start-application', 'frontend-api-sql',
         'read-only-database-role', 'independent-web-repeat', 'encrypted-backup',
         'isolated-restore', 'restored-data', 'cleanup']


class TrialError(Exception):
    """Only a fixed step identifier is safe to expose in reports."""


def plan():
    lock = json.loads(LOCK.read_text())
    required = ['python', 'postgres', 'nginx']
    images = {name: lock['images'][name]['image'] for name in required}
    if any(not re.fullmatch(r'[a-zA-Z0-9./:_-]+@sha256:[a-f0-9]{64}', image) for image in images.values()):
        raise TrialError('invalid-image-lock')
    return {'schema': 'reference.integration/v1', 'status': 'planned-not-executed',
            'target': 'fresh-github-hosted-linux-runner-local-docker', 'steps': STEPS,
            'images': images, 'data': 'new-synthetic-only', 'published_ports': [],
            'scope_limit': 'Container integration only; no VM provisioning, host convergence or off-host disaster recovery'}


def require_ci(environment):
    if environment.get('GITHUB_ACTIONS') != 'true' or environment.get('RUNNER_ENVIRONMENT') != 'github-hosted' or environment.get('RUNNER_OS') != 'Linux':
        raise TrialError('execution-requires-fresh-github-hosted-runner')
    if environment.get('DOCKER_HOST', 'unix:///var/run/docker.sock') != 'unix:///var/run/docker.sock':
        raise TrialError('remote-docker-endpoint-rejected')
    if environment.get('DOCKER_CONTEXT', 'default') != 'default':
        raise TrialError('nondefault-docker-context-rejected')


def isolate(config, project, data_network):
    """Adapt rendered canonical Compose data; do not maintain a parallel stack."""
    result = json.loads(json.dumps(config))
    result['name'] = project
    for service in result['services'].values():
        service.pop('ports', None)
        if service.get('privileged') or service.get('network_mode') or service.get('container_name'):
            raise TrialError('unsafe-service-identity')
        service['restart'] = 'no'
    for key, network in result.get('networks', {}).items():
        network['name'] = data_network if key == 'app_data' else project + '_' + key
    for key, volume in result.get('volumes', {}).items():
        if volume.get('external'):
            raise TrialError('external-volume-rejected')
        volume['name'] = project + '_' + key
    return result


class Runner:
    def __init__(self, environment):
        self.environment = environment

    def run(self, command, step, timeout=240, input_bytes=None):
        try:
            result = subprocess.run(command, env=self.environment, input=input_bytes,
                                    capture_output=True, timeout=timeout)
        except (OSError, subprocess.TimeoutExpired):
            raise TrialError(step) from None
        if result.returncode:
            # Tool errors may contain paths, SQL or credential-bearing diagnostics.
            # Never propagate raw stdout/stderr into public evidence.
            raise TrialError(step)
        return result.stdout


def execute(report):
    require_ci(os.environ)
    if any(shutil.which(tool) is None for tool in ['docker', 'restic', 'bash']):
        raise TrialError('missing-ci-tools')
    environment = dict(os.environ, DOCKER_DEFAULT_PLATFORM='linux/amd64')
    runner = Runner(environment)
    context = json.loads(runner.run(['docker', 'context', 'inspect', 'default'], 'inspect-docker-context'))
    if context[0]['Endpoints']['docker']['Host'] != 'unix:///var/run/docker.sock':
        raise TrialError('remote-docker-context-rejected')
    # The restore tool deliberately has a fixed disposable identity. Do not adopt
    # any existing project/volume/network, even on a hosted runner.
    existing = runner.run(['docker', 'ps', '-aq', '--filter', 'label=com.docker.compose.project=reference-restore'], 'check-restore-identity')
    volumes = runner.run(['docker', 'volume', 'ls', '-q', '--filter', 'name=^reference-restore_database$'], 'check-restore-volume')
    networks = runner.run(['docker', 'network', 'ls', '-q', '--filter', 'name=^reference-restore-data$'], 'check-restore-network')
    if existing.strip() or volumes.strip() or networks.strip():
        raise TrialError('restore-resources-already-exist')
    prefix = 'reference-test-' + secrets.token_hex(6)
    api_image = prefix + '-api:local'
    projects = []
    built = False
    report.update(status='running', checks={step: 'not-run' for step in STEPS})
    with tempfile.TemporaryDirectory(prefix='reference-integration-') as raw:
        temp = Path(raw)
        secret_dir = temp / 'credentials'
        secret_dir.mkdir(mode=0o700)
        # Generated test values are never printed. Host directory is private;
        # bound files are readable by the distinct, unprivileged container UIDs.
        for name in ['database_admin', 'database_app', 'restic_password']:
            path = secret_dir / name
            path.write_text(secrets.token_hex(32) + '\n')
            path.chmod(0o644 if name != 'restic_password' else 0o600)
        environment.update(LAB_SECRET_DIR=str(secret_dir), POSTGRES_IMAGE=report['images']['postgres'],
                           NGINX_IMAGE=report['images']['nginx'], API_IMAGE=api_image,
                           LAB_BIND_ADDRESS='127.0.0.1', RESTIC_REPOSITORY=str(temp / 'encrypted-backup'),
                           RESTIC_PASSWORD_FILE=str(secret_dir / 'restic_password'),
                           REFERENCE_BACKUP_APPROVED='yes', REFERENCE_RESTORE_APPROVED='restore-disposable')
        try:
            runner.run(['docker', 'build', '--build-arg', 'PYTHON_IMAGE=' + report['images']['python'],
                        '--tag', api_image, str(ROOT / 'services/demo-api')], 'build-api', timeout=600)
            built = True
            report['checks']['build-api'] = 'passed'
            definitions = [('database', ROOT / 'services/database', prefix + '-database', prefix + '-data'),
                           ('application', ROOT / 'services/applications', prefix + '-application', prefix + '-data'),
                           ('restore', ROOT / 'operations/backups/restore-example', 'reference-restore', 'reference-restore-data')]
            commands = {}
            for label, source, name, network in definitions:
                empty_env = temp / 'empty.env'
                empty_env.touch()
                rendered = json.loads(runner.run(['docker', 'compose', '--project-directory', str(source),
                                                 '--env-file', str(empty_env), '--project-name', name,
                                                 'config', '--format', 'json'], 'render-' + label))
                config = isolate(rendered, name, network)
                if label == 'restore':
                    spec = importlib.util.spec_from_file_location('restore_guard', ROOT / 'operations/backups/check_restore.py')
                    guard = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(guard)
                    guard.validate(config)
                directory = temp / label
                directory.mkdir(mode=0o700)
                (directory / 'compose.yaml').write_text(json.dumps(config))
                (directory / '.env').touch(mode=0o600)
                commands[label] = (['docker', 'compose', '--project-directory', str(directory),
                                    '--env-file', str(directory / '.env')], directory)
            for label in ['database', 'application']:
                command, _ = commands[label]
                projects.append(command)
                step = 'start-' + label
                runner.run(command + ['up', '-d', '--wait', '--wait-timeout', '180'], step)
                report['checks'][step] = 'passed'
            app, _ = commands['application']
            database, db_dir = commands['database']
            probe = ("import json,urllib.request; "
                     "assert 'Reference application' in urllib.request.urlopen('http://proxy:8080/',timeout=5).read().decode(); "
                     "assert json.load(urllib.request.urlopen('http://proxy:8080/api/message',timeout=5))['message'] == 'Hello from the reference database'")
            runner.run(app + ['exec', '-T', 'api', 'python', '-c', probe], 'frontend-api-sql')
            report['checks']['frontend-api-sql'] = 'passed'
            privilege_probe = '''import os,psycopg
from pathlib import Path
with psycopg.connect(host=os.environ['DB_HOST'],dbname=os.environ['DB_NAME'],user=os.environ['DB_USER'],password=Path(os.environ['DB_PASSWORD_FILE']).read_text().strip(),connect_timeout=5) as db:
    try:
        db.execute("INSERT INTO public.greeting VALUES (2, 'synthetic test')")
    except psycopg.errors.InsufficientPrivilege:
        pass
    else:
        raise AssertionError('Application role unexpectedly has write privileges')
'''
            runner.run(app + ['exec', '-T', 'api', 'python', '-c', privilege_probe], 'read-only-database-role')
            report['checks']['read-only-database-role'] = 'passed'
            before = runner.run(database + ['ps', '-q', 'database'], 'database-identity')
            runner.run(app + ['up', '-d', '--wait'], 'independent-web-repeat')
            if before != runner.run(database + ['ps', '-q', 'database'], 'database-identity'):
                raise TrialError('database-container-changed-during-web-repeat')
            report['checks']['independent-web-repeat'] = 'passed'
            runner.run(['restic', 'init'], 'initialize-encrypted-backup')
            runner.run(['bash', str(ROOT / 'operations/backups/postgres-to-restic.sh'), str(db_dir)], 'encrypted-backup')
            report['checks']['encrypted-backup'] = 'passed'
            snapshots = json.loads(runner.run(['restic', 'snapshots', '--json', '--tag', 'reference-postgres'], 'select-snapshot'))
            if len(snapshots) != 1:
                raise TrialError('unexpected-backup-count')
            restore, restore_dir = commands['restore']
            projects.append(restore)
            runner.run(restore + ['up', '-d', '--wait', '--wait-timeout', '180'], 'start-restore')
            runner.run(['bash', str(ROOT / 'operations/backups/restore-isolated.sh'), snapshots[0]['id'], str(restore_dir)], 'isolated-restore')
            report['checks']['isolated-restore'] = 'passed'
            value = runner.run(restore + ['exec', '-T', 'database', 'psql', '-U', 'postgres', '-d', 'lab_demo', '-At',
                                         '-c', 'SELECT message FROM public.greeting WHERE id = 1'], 'restored-data')
            if value.strip() != b'Hello from the reference database':
                raise TrialError('restored-data')
            runner.run(app + ['exec', '-T', 'api', 'python', '-c', probe], 'source-application-after-restore')
            report['checks']['restored-data'] = 'passed'
            report['status'] = 'passed'
        finally:
            failed = False
            for command in reversed(projects):
                try:
                    runner.run(command + ['down', '--volumes', '--remove-orphans'], 'cleanup')
                except TrialError:
                    failed = True
            if built:
                try:
                    runner.run(['docker', 'image', 'rm', api_image], 'cleanup-image')
                except TrialError:
                    failed = True
            report['checks']['cleanup'] = 'failed' if failed else 'passed'
            if failed:
                raise TrialError('cleanup')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true', help='Run only on a fresh GitHub-hosted runner')
    parser.add_argument('--report', type=Path, help='Sanitized result path outside the public source tree')
    args = parser.parse_args()
    if args.report and ROOT in args.report.resolve().parents:
        parser.error('Write execution evidence outside the public source tree')
    report = plan()
    code = 0
    if args.execute:
        try:
            execute(report)
        except TrialError as error:
            report.update(status='failed', failed_step=str(error))
            code = 1
        except (AssertionError, ValueError, KeyError, IndexError, TypeError, OSError):
            report.update(status='failed', failed_step='integration-assertion')
            code = 1
        report['completed_at'] = datetime.now(timezone.utc).isoformat()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
