# Release readiness

Updated: 2026-11-22. Status: initial preview authorized for public publication.
The [case study](portfolio/case-study.md) explains engineering choices. The
[trial guide](getting-started/reproducible-trial.md) separates source, application
and infrastructure evidence. All examples use fictional environment inputs.

## Implemented and locally observed

| Area | Current result | Evidence boundary |
| --- | --- | --- |
| Structure and onboarding | Five responsibility categories, AI handoff, requirements, ADRs and staged runbooks | No private topology or live inventory |
| Core tests | 19 existing tests passed | Inventory, release metadata, API response/redaction, mount and restore guards |
| Ansible regressions | 4 additional tests passed | Actual staging modules on temporary local paths; package request/mismatch contracts |
| Integration harness guards | 7 tests passed | Plan is inert; local/remote contexts and unsafe configs rejected |
| Image baseline consistency | 2 tests passed | Six immutable manifest references and consuming examples agree |
| Consolidated full source profile | 22 checks passed, no skipped regressions | Existing controller tools only; no auto-install/init or managed host |
| Terraform | Format/schema valid; 3 mock-provider tests passed | No real API, state refresh or provisioning |
| Ansible | 4 playbook syntax checks and offline lint passed | No host/runtime execution or actual apt transaction |
| Compose | 8 configurations parsed successfully | No container start/build or image pull |
| YAML, shell and Markdown | Lint passed, including Markdownlint 0.50.1 | Source checks only |
| Container manifest baseline | Six public manifests verified by registry digest; amd64 availability observed | No signature attestation, image vulnerability or runtime acceptance |
| Gitleaks | Zero public-candidate findings in full validation | Pattern scan, no security guarantee |
| Trivy configuration | Zero HIGH/CRITICAL on recognized API Dockerfile/Terraform | Private-input warnings; not image/Compose/Ansible/runtime security coverage |

The local regression suite now has **32 tests**, all passing with the full
validation environment. The basic standard-library path reports optional Ansible
skips; full mode fails if those regressions cannot run. The consolidated report
stores only check IDs/status. [Iteration evidence](evidence/2026-11-22-reproducibility.md)
records the scope and final preservation/privacy checks.

## Hosted application acceptance and remaining VM trials

The hosted `application-trial` job builds the synthetic API from the pinned base,
starts canonical database/application configurations without published ports,
checks frontend/API/SQL and the read-only database role, repeats web delivery,
runs the real encrypted-backup/isolated-restore scripts and cleans its own
resources. It produces a sanitized artifact. Its default local command is a plan;
execution is restricted to a fresh GitHub-hosted Linux runner with the local
Docker endpoint. **The first hosted job passed.** See the [accepted run and sanitized
artifact](evidence/2026-11-22-publication.md). Its result establishes application
integration and encrypted backup/restore mechanics within that isolated runner.

The VM path has not been executed: Proxmox cloning, template compatibility, host
convergence, actual package installation, secret-file permissions, guest startup,
network isolation, VPN/TLS and complete recovery remain unverified. No original
infrastructure, router, SSH endpoint or operational API was contacted. No local
container workload or original-infrastructure operation was performed. Hosted
container/SQL/backup/restore validation and public publication are recorded separately.

## Remaining publication gates

- [x] Correct generated-config churn and package-selection regression.
- [x] Add staging/no-op and version-mismatch regression coverage.
- [x] Fix public example image identities and document update/review boundaries.
- [x] Provide a case study, coherent learning path and consolidated local checks.
- [x] Prepare a guarded hosted application/encrypted-recovery test and evidence artifact.
- [x] Run GitHub CI and inspect its actual result artifacts, including Markdown lint.
- [ ] Scan upstream images and dependencies; review vulnerabilities/provenance.
- [x] Run the hosted application/restore trial successfully, including cleanup.
- [ ] Rehearse induced runtime failure/cleanup paths beyond guard-unit coverage.
- [ ] Accept one disposable Proxmox guest and repeat host/service convergence.
- [ ] Test permitted/denied network flows and off-host recovery; VPN/TLS if selected.
- [x] Owner authorized publication of this MIT-licensed public preview.
- [ ] Obtain an additional independent human privacy/security review.
- [x] Configure GitHub private vulnerability reporting for the public preview.
- [ ] Define supported versions before a supported release.
- [x] Owner explicitly authorized initial repository creation, commit and push.

The initial commit is independent of the private source. No source history or
remote is imported. CI actions are commit-pinned;
its image/tool baselines do not imply a complete software supply-chain audit.
Public code intentionally excludes keys, real inventory, state/plans, data,
backups and actual encrypted-secret metadata. Scan results do not replace human
privacy review. The reference demonstrates professional process while keeping
unobserved deployment claims explicitly out of the portfolio.
