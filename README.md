# Homelab Reference

A guide and Infrastructure as Code reference for building and operating your own
homelab with an AI coding assistant. It retains the engineering patterns of an
operated lab: clear ownership, documented decisions, virtualization, private
administration, controlled changes, observability and recovery.

For a portfolio overview, read the [engineering case study](docs/portfolio/case-study.md)
and [validation evidence](docs/evidence/2026-11-22-reproducibility.md). They distinguish
measured local results from CI and infrastructure trials that have not run.

**Start with [the AI handoff guide](docs/getting-started/ai-handoff.md).** Give the
whole repository to your assistant, beginning with `AGENTS.md`. Your assistant
should help you understand and design your lab before proposing any deployment.

This is a fictional reference, not a map of its author's installation. Example
names, addresses, IDs and sizing are invented; no original IP, domain, inventory,
secret, history or operational policy is supplied. Your environment's real inputs
belong outside the public tree. No configured service is claimed deployed here.

## Five categories, one responsibility per layer

```text
homelab-reference/
├── README.md                     # Entry point and reading order
├── AGENTS.md                     # Instructions for your AI assistant
├── 00-now.md                     # Current reference status and selected next steps
├── docs/                         # Understanding, decisions, guides and evidence
│   ├── architecture/
│   ├── decisions/
│   ├── evidence/
│   ├── getting-started/
│   ├── network/
│   ├── portfolio/
│   ├── runbooks/
│   ├── security/
│   └── templates/
├── infrastructure/               # Proxmox provisioning and host configuration
│   ├── proxmox/
│   └── ansible/
├── operations/                   # Procedures and tools used to operate the lab
│   ├── backups/
│   ├── cicd/
│   ├── deploy/
│   ├── network/
│   ├── provisioning/
│   └── validation/
├── secrets/                      # Custody policy only; actual material excluded
└── services/                     # Application and platform service definitions
    ├── applications/
    ├── database/
    ├── demo-api/
    ├── internal-proxy/
    ├── jenkins/
    ├── observability/
    ├── sandbox/
    └── starter/
```

CI configuration and contributor/security/license files support these categories.
Each category has a README explaining its contents and boundaries.

## Learn and adapt in order

| Step | Read | Produce for your own lab |
| --- | --- | --- |
| 1. Understand | [Documentation index](docs/README.md), [architecture](docs/architecture/overview.md) | A plain-language explanation of the layers |
| 2. Gather requirements | [Environment worksheet](docs/getting-started/environment.md) | Hardware/capacity, use cases and recovery needs |
| 3. Choose deliberately | [Decision index](docs/decisions/README.md) | Your own decisions and trade-offs |
| 4. Plan privately | [AI workflow](docs/getting-started/ai-handoff.md), [reference inventory](docs/inventory.md) | Private catalog and one approved change plan |
| 5. Validate | [Offline checks](operations/validation/README.md) | Dated static/mock evidence |
| 6. Build incrementally | [First installation](docs/runbooks/first-installation.md) | Verified disposable guest, then selected services |
| 7. Operate and recover | [Operations](docs/runbooks/runbook.md), [change process](docs/runbooks/change-management.md) | Health checks, backup/restore evidence and recovery plan |

## What the reference teaches

Proxmox hosts selectively created Ubuntu VMs. Terraform owns VM resources;
Ansible owns the guest baseline, runtime and service delivery. BIND9 provides
private authoritative DNS. NGINX routes application traffic. The example app has
a frontend, read-only API and independently managed PostgreSQL. Prometheus and
Grafana provide host telemetry. Jenkins is an optional validation controller.
Explicit backup/restore tooling illustrates recovery as a separate operation.

Decisions explain **why**, including [WireGuard for private administration](docs/decisions/0003-wireguard-private-access.md),
[the tool boundaries](docs/decisions/0004-tool-responsibilities.md),
[secret custody](docs/decisions/0005-secrets-and-custody.md) and
[application/data separation](docs/decisions/0006-release-and-data-lifecycle.md).
These choices are examples to evaluate, not universal requirements.

## Validate without deploying

Run from the repository root:

```sh
# Standard library checks; missing optional regression dependencies are reported:
python3 operations/validation/run.py
# With the documented QA tools and cached provider already available:
python3 operations/validation/run.py --full
# Review the isolated CI trial plan; this command starts nothing:
python3 operations/validation/integration.py
```

[Validation prerequisites](operations/validation/README.md) explain the tools and
scope. Local staging regressions exercise the real Ansible file tasks in a
private temporary directory. The CI trial is prepared to test frontend/API/SQL,
read-only access, independent application updates and encrypted backup/restore on
a fresh hosted runner, without published ports or infrastructure credentials.
The [first hosted run passed](docs/evidence/2026-11-22-publication.md). See [the reproducible trial guide](docs/getting-started/reproducible-trial.md).

A real Proxmox plan, host configuration or lab deployment is a separate operation
requiring an explicit destination, scope and recovery plan.

## Status and limits

[00-now.md](00-now.md) records reference work; [inventory](docs/inventory.md)
records code/runtime status; [release readiness](docs/release-readiness.md)
records actual validation. VPN is a teaching template, TLS/router policy are
designs, and real provisioning, convergence and recovery tests remain pending.
The optional Starter is contained under `services/starter/`.

Read [the security audit](docs/security/audit.md), [secrets policy](secrets/README.md),
[contribution guide](CONTRIBUTING.md) and [security policy](SECURITY.md).
Licensed under [MIT](LICENSE). This is an initial public preview: implementation
and measured checks are available, while the VM and complete infrastructure
acceptance gates remain documented.
