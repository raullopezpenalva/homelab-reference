# Now: reference project

Updated: 2026-11-22. This file tracks selected reference work, not anyone's live
infrastructure or an application backlog.

## Current scope

The five public categories are docs, infrastructure, operations, secrets and
services. Proxmox/VM provisioning and Ansible configuration remain the primary
reference. Documentation now provides an ordered handoff for a new owner and an
AI assistant, including explanations of technology choices and operating process.

## Current reproducibility work

The two reviewed regressions are corrected: static/template ownership and one
package-version transaction with post-install checks. Public images are fixed by
digest. Local staging regressions now measure repeat delivery; a separate hosted
application/recovery trial has passed its first hosted run. See the
[case study](docs/portfolio/case-study.md) and [evidence](docs/evidence/2026-11-22-reproducibility.md).

## Next selected steps

1. A new owner reads the [AI handoff](docs/getting-started/ai-handoff.md) and
   completes the [environment worksheet](docs/getting-started/environment.md).
2. Record that owner's decisions and keep environment-specific inputs privately.
3. Validate offline, then obtain approval for one disposable-lab operation.
4. Record actual deployment/convergence, network and restore evidence before
   accepting that environment. Do not mark these complete from static checks.

The [reference inventory](docs/inventory.md) owns status by component. The
[release report](docs/release-readiness.md) owns validation/publication limits.
No operation, deployment, publication, commit or push is authorized by this list.
