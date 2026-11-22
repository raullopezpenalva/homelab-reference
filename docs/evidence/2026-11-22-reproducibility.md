# Reproducibility iteration: observed local evidence

Date: 2026-11-22. Scope: independently authored local source and temporary staging.

## Fixes under test

- Generated Prometheus config has one owner. The static manifest excludes it,
  documentation and local env/private material.
- A single apt request contains all selected package/version pairs; observed
  package facts must match before runtime startup.
- Six public image manifest references are fixed by digest. Registry manifest
  bytes and Linux amd64 availability were checked without pulling images.
- A guarded, plan-by-default CI application/SQL/encrypted-restore harness and its
  result artifact are implemented. Execution has not been performed.

## Observed regression results

The initial focused run passed 23 tests: the existing 19 tests plus four Ansible
regressions. Two of those regressions run the real staging file tasks through a
local connection with temporary paths/ownership. A second pass and README/local
source-env changes produce changed=0; inventory/static file changes propagate and
then converge to changed=0. No runtime/package/service task was executed.
Seven additional integration-harness tests passed: plan performs no subprocess
call, execution rejects developer/remote/named contexts, port/project isolation
works, and privileged/external-volume configurations are rejected.

A consolidated final validation result and privacy/preservation review follow
below after the final check run. CI workload success, package transaction success,
VM convergence and real backup/restore acceptance are deliberately not inferred
from these local regressions or source checks.

## Consolidated observed result

The full local validation profile passed all 22 checks with no skipped
regressions: source/links/exclusions, the 32-test regression suite, inert integration
plan, Terraform format/schema and three mocks, YAML/ShellCheck, four Ansible syntax
checks and offline lint, eight Compose configurations, and fresh Gitleaks on the
public candidate. Trivy's cached Dockerfile/Terraform configuration scan reported
zero HIGH/CRITICAL findings, with expected absent-private-input warnings.
No CI workload, real package transaction or Proxmox operation was run. A temporary
local QA environment was used for linting and source/staging tests only.

Markdownlint 0.50.1 passed locally with the repository's compact-table policy.
The CI source job now selects Node 24 explicitly for that tool. YAML/ShellCheck,
all explicit shipping-manifest paths, and rendered BIND configuration/zone also
passed. Public image examples and the API base agree with the lock. No container
image was built or pulled locally, and no package transaction was executed.

## Final preservation and disclosure check

The original source file set/content hashes, Git HEAD and pre-existing status
remained unchanged. A targeted comparison found no reviewed private-source name
or address in the public candidate. All public JSON parsed and no trailing
whitespace issue was found. A final default-rule Gitleaks scan covered the current
public candidate, including new helpers/tests/manifests, with zero findings.
The reference remains uncommitted, without tags/remotes or publication. Actual
image vulnerability, hosted integration and VM/recovery acceptance remain open.
