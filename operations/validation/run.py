#!/usr/bin/env python3
"""Run local source checks; never install tools, start workloads or contact managed hosts."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full', action='store_true', help='Require cached Terraform, lint, Compose and Gitleaks tools')
    parser.add_argument('--draft', action='store_true', help='Also require no configured Git remote')
    parser.add_argument('--report', type=Path, help='Write a sanitized result outside the source tree')
    args = parser.parse_args()
    if args.report and ROOT in args.report.resolve().parents:
        parser.error('Write evidence outside the public source tree')
    if args.full:
        missing = [name for name in ['terraform', 'yamllint', 'ansible-playbook', 'ansible-lint', 'shellcheck', 'docker', 'gitleaks'] if not shutil.which(name)]
        missing += [name for name in ['yaml', 'jinja2'] if importlib.util.find_spec(name) is None]
        if missing:
            parser.exit(2, 'Missing full-check dependencies: ' + ', '.join(missing) + '. No tool was installed.\n')
    commands = [('source-links-exclusions', [sys.executable, 'operations/validation/check.py'] + (['--require-no-remote'] if args.draft else []), ROOT),
                ('regressions', [sys.executable, '-m', 'unittest', 'discover', '-s', 'operations/validation/tests', '-v'], ROOT),
                ('integration-plan-only', [sys.executable, 'operations/validation/integration.py'], ROOT)]
    if args.full:
        tf = '-chdir=infrastructure/proxmox/environments/lab'
        ansible = ROOT / 'infrastructure/ansible'
        commands += [('terraform-format', ['terraform', 'fmt', '-check', '-recursive', 'infrastructure/proxmox'], ROOT),
                     ('terraform-schema', ['terraform', tf, 'validate'], ROOT),
                     ('terraform-mocks', ['terraform', tf, 'test'], ROOT),
                     ('yaml', ['yamllint', '.'], ROOT),
                     ('shell', ['shellcheck'] + [str(p.relative_to(ROOT)) for p in sorted((ROOT / 'operations/validation').glob('*.sh'))] +
                      [str(p.relative_to(ROOT)) for p in sorted((ROOT / 'operations/backups').glob('*.sh'))] + ['services/database/init.sh'], ROOT)]
        for path in sorted((ansible / 'playbooks').glob('*.yml')):
            commands.append(('ansible-syntax-' + path.stem, ['ansible-playbook', '--syntax-check', str(path.relative_to(ansible))], ansible))
        commands.append(('ansible-lint', ['ansible-lint', '--offline'] + [str(p.relative_to(ansible)) for p in sorted((ansible / 'playbooks').glob('*.yml'))], ansible))
        for folder in ['services/starter', 'services/applications', 'services/database', 'services/observability',
                       'services/jenkins', 'services/sandbox', 'services/internal-proxy', 'operations/backups/restore-example']:
            command = ['docker', 'compose', '--project-directory', folder, '--env-file', folder + '/.env.example']
            if folder == 'services/starter':
                command += ['--profile', 'monitoring']
            commands.append(('compose-' + Path(folder).name, command + ['config', '--quiet'], ROOT))
    report = {'schema': 'reference.validation/v1', 'profile': 'full' if args.full else 'basic', 'checks': []}
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    def check(label, command, cwd):
        try:
            result = subprocess.run(command, cwd=cwd, env=environment, capture_output=True, text=True, timeout=180)
            skipped = label == 'regressions' and ('skipped=' in result.stderr or 'skipped=' in result.stdout)
            status = 'failed' if result.returncode or (args.full and skipped) else ('passed-with-skips' if skipped else 'passed')
        except (OSError, subprocess.TimeoutExpired):
            status = 'failed'
        report['checks'].append({'check': label, 'status': status})
        print(label + ': ' + status, flush=True)
    for label, command, cwd in commands:
        check(label, command, cwd)
    if args.full:
        with tempfile.TemporaryDirectory(prefix='reference-validation-export-') as raw:
            target = Path(raw)
            names = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=ROOT).split(b'\0')
            for name in names:
                if not name:
                    continue
                source = ROOT / name.decode()
                if source.is_symlink():
                    parser.exit(2, 'Public symlinks require manual security review\n')
                if source.is_file():
                    destination = target / name.decode()
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, destination)
            check('gitleaks-public-candidate', ['gitleaks', 'dir', str(target), '--redact=100', '--no-banner', '--log-level', 'error'], ROOT)
    report['status'] = 'failed' if any(item['status'] == 'failed' for item in report['checks']) else 'passed'
    report['scope'] = 'Local source/staging checks only. No VM, package installation, container startup or disaster-recovery acceptance.'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print('Result: ' + report['status'])
    return int(report['status'] != 'passed')


if __name__ == '__main__':
    raise SystemExit(main())
