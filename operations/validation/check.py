#!/usr/bin/env python3
"""Offline release checks; never execute configuration or contact infrastructure."""
from pathlib import Path
import re
import argparse
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PATTERNS = {
    "private key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "GitHub credential": r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})",
    "cloud credential": r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "credential URL": r"://[^\s/:]+:[^\s/@]{8,}@",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-no-remote", action="store_true", help="Check unpublished draft has no remote")
    args = parser.parse_args()
    errors = []
    count = 0
    # Include untracked public candidates: an empty index must not skip scanning.
    for path in sorted(ROOT.rglob("*")):
        rel = path.relative_to(ROOT)
        if ".git" in rel.parts or not path.is_file():
            continue
        if subprocess.run(["git", "check-ignore", "-q", "--", str(rel)],
                          cwd=ROOT, check=False).returncode == 0:
            continue
        count += 1
        content = path.read_text(encoding="utf-8")
        for label, pattern in PATTERNS.items():
            if re.search(pattern, content):
                errors.append(f"{rel}: possible {label}; value suppressed")
        if path.suffix == ".md":
            for target in re.findall(r"\]\(([^)]+)\)", content):
                if re.match(r"^[a-z]+://|^#|^mailto:", target):
                    continue
                link = target.split("#")[0]
                if link and not (path.parent / link).exists():
                    errors.append(f"{rel}: missing relative link target")
    required_public = [
        "docs/README.md", "infrastructure/README.md", "operations/README.md",
        "secrets/README.md", "services/README.md", "AGENTS.md", "00-now.md",
        "operations/backups/postgres-to-restic.sh", "operations/backups/restore-isolated.sh",
        "operations/backups/check_restore.py", "services/starter/.env.example",
        "infrastructure/ansible/inventory/empty.yml",
    ]
    for rel in required_public:
        if not (ROOT / rel).is_file():
            errors.append(f"Required public reference file missing: {rel}")
        elif subprocess.run(["git", "check-ignore", "-q", "--", rel], cwd=ROOT, check=False).returncode == 0:
            errors.append(f"Required reference file is accidentally ignored: {rel}")
    for legacy in ["ansible", "terraform", "examples", "networking", "observability", "scripts", "tests"]:
        if (ROOT / legacy).exists():
            errors.append(f"Legacy top-level directory must be categorized: {legacy}")
    probes = [".env", "nested/.env.prod", "private/inventory.yml", "secrets/key", "operations/backups/private/dump.sql", "infrastructure/ansible/inventory/actual.json",
              "server.key", "server.pem", "terraform.tfstate", "x.tfplan",
              "x.tfvars", "db.sqlite", "backup.dump", "backups/archive.zip"]
    for probe in probes:
        if subprocess.run(["git", "check-ignore", "-q", "--", probe],
                          cwd=ROOT, check=False).returncode != 0:
            errors.append(f"Git exclusion missing: {probe}")
    if args.require_no_remote and subprocess.check_output(["git", "remote"], cwd=ROOT).strip():
        errors.append("Unexpected remote: review before release")
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Checked {count} public candidate files; {len(errors)} findings")
    print("Pattern scan only; not a substitute for Gitleaks and human review")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
