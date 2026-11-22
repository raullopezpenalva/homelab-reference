# Validation: local evidence before an operation

Run from the repository root. Python tests need only the standard library.
The optional lint dependencies are listed in `requirements.txt` in this category.
Use already available tools or explicitly prepare your own controller environment;
none of the checks installs tools or contacts managed hosts on its own.

```sh
python3 operations/validation/check.py
python3 -m unittest discover -s operations/validation/tests -v
terraform fmt -check -recursive infrastructure/proxmox
terraform -chdir=infrastructure/proxmox/environments/lab validate
terraform -chdir=infrastructure/proxmox/environments/lab test
```

Schema validation/mock tests require the pinned public provider already cached.
If absent, a separately chosen dependency-setup step is
`terraform -chdir=infrastructure/proxmox/environments/lab init -backend=false -input=false`.
It downloads public dependencies; never substitute a real plan for a mock test.
Ansible syntax/lint requires the collection in
`infrastructure/ansible/requirements.yml` already installed in your controller.
Do not install dependencies automatically merely to edit a document.

The checker includes untracked public candidates, secret patterns, relative
Markdown links, five-category consistency and Git exclusions. It can additionally
check an unpublished draft with `--require-no-remote`; regular contributor/CI
checkouts naturally have a public remote. It is not equivalent to Gitleaks.

Additional checks: YAML lint, ShellCheck, Ansible syntax/offline lint, Compose
config for all service examples, rendered BIND config/zone, fresh Gitleaks and a
scoped Trivy configuration scan. The CI workflow uses these categories and has
no infrastructure identity or deployment step. The [release report](../../docs/release-readiness.md)
records which checks actually ran and their limits.

`smoke-starter.sh` and `smoke-virtualized.sh` query a selected local application;
run them only against an explicitly chosen trial/tunnel after deployment. The
virtualized check verifies proxy, frontend, API and a real SQL read. Neither
script provisions a host or proves recovery.

## Consolidated entry points

`python3 operations/validation/run.py` runs the basic checks and reports optional
skips. `--full` requires the documented tools/cached provider and fails on skipped
regressions; `--report /absolute/private/result.json` saves a sanitized summary
outside the source tree. `--draft` additionally checks there is no Git remote.
The wrapper installs/initializes nothing and does not run workload integration.

`python3 operations/validation/integration.py` prints a plan only. The separate
CI job executes the guarded synthetic container/SQL/encrypted-recovery trial on
a fresh hosted runner, without published ports or lab credentials. See the
[trial guide](../../docs/getting-started/reproducible-trial.md). The
[first hosted trial passed](../../docs/evidence/2026-11-22-publication.md).

`images.lock.json` fixes the public image baseline. Its registry verification is
not a vulnerability scan. The API build and a real VM still need their own
acceptance. Staging tests use a temporary local Ansible connection; they never
install packages or manage services. Verify repeat convergence on the real guest
only in a separately approved operation.
