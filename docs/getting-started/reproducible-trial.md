# A reproducible trial, with explicit evidence boundaries

There are three different paths. Choose the one appropriate to your stage.

| Path | Command or guide | What it proves |
| --- | --- | --- |
| Local source/staging | `python3 operations/validation/run.py --full` | Static/mock correctness and repeatable local file delivery |
| Hosted application trial | CI job `application-trial` | When executed successfully: frontend/API/SQL, privileges, independent web repeat and encrypted recovery |
| Disposable VM trial | [Virtualized guide](virtualized.md) | Only after actual checks: Proxmox resources, guest configuration and environment behavior |

## 1. Prepare your controller

Use Git, Python and the pinned validation requirements in a private virtual
environment. For full checks provide Terraform, Docker Compose CLI, ShellCheck,
Gitleaks and the validation tools. Install the Ansible collection from
`infrastructure/ansible/requirements.yml`. Initialize only the public provider
with `terraform init -backend=false` as documented in the validation guide.
These are explicit dependency setup steps, not actions performed by the checker.

Run from the repository root:

```sh
python3 operations/validation/run.py --full --report /absolute/private/validation.json
```

The report contains check IDs/status, not raw logs or credentials. Full mode fails
if required tools are missing or optional regression tests were skipped. Basic
mode reports skips rather than implying full coverage. No tool auto-installs,
real backend initializes, workload starts or managed host is contacted.

The Ansible staging regressions deliberately operate on a temporary directory
through a local connection. They do not run the host/runtime role, sudo, apt,
Docker, DNS or systemd. Their evidence is file-delivery convergence only.

## 2. Understand the hosted application trial

`python3 operations/validation/integration.py` is a plan-only command. Read the
result without Docker access. The CI job runs `--execute` only on a fresh
GitHub-hosted Linux runner. The harness refuses a developer machine, self-hosted
runner, named Docker context or remote Docker endpoint. These checks are scope
guardrails, not a new authorization to operate a lab.

The trial uses the canonical app/database/restore manifests, immutable public
images from `operations/validation/images.lock.json`, a locally built demo API,
new random test credentials and no published host ports. It verifies:

1. The frontend/API can read the initialized PostgreSQL greeting through NGINX.
2. The app role cannot insert data, independently of the API's read-only setting.
3. Repeating the app project leaves the separate database container identity intact.
4. The actual backup script creates an encrypted synthetic restic snapshot.
5. The actual guarded restore script restores that snapshot into the isolated,
   initially empty restore project; the recovered row matches the source.
6. Only this test's projects/volumes/image are cleaned up, including on failure.

Generated secret files stay under a private temporary parent; file-backed mounts
allow each assigned container UID to read only its mounted test file. No real
credential, inventory, endpoint, published image or lab SSH identity is involved.
The report artifact contains only fixed check names/results, public image digests
and a completion time. Raw Docker/SQL/restic output is never copied to it.

The [first hosted trial passed](../evidence/2026-11-22-publication.md). Passing
unit tests for its guards alone is not a successful application trial. When you
run CI for a later revision,
inspect the result artifact and job status; do not infer success from the plan.
The encrypted test repository is temporary and local to the runner: this tests
backup-format/restore mechanics, not off-host or disaster recovery durability.

## 3. Accept your own VM environment

Complete the private environment worksheet, choose a single disposable guest,
prepare trusted access and recovery, and follow the [VM guide](virtualized.md).
Record before/after identity, data UUID, actual package versions, repeated guest
convergence, functional app/SQL checks and permitted/denied network flows.
Use a separately approved operation for formatting, router/VPN/TLS changes or a
restore. This repository supplies no bare-metal installer or automated disk
formatter. See the [change record](../templates/change-record.example.md).
