# Release notes

## Initial public preview — 2026-11-22

Primary virtualized reference: Proxmox cloning module, Terraform safety operations/validation/tests and
inventory output; guarded Ansible baseline/runtime/DNS and service delivery;
fictional network/VM catalog; NGINX/frontend/Python API and separately managed
PostgreSQL; Prometheus/Grafana; optional private ingress, Jenkins and sandbox;
WireGuard teaching template; offline release validation and encrypted backup/
isolated restore examples. Starter remains an optional Compose introduction.

No release, commit, remote, infrastructure deployment or runtime acceptance is
implied. See the [validation report](docs/release-readiness.md).

### Category organization and AI learning path

Grouped public content under docs, infrastructure, operations, secrets and
services; retained existing executable examples while updating their paths and
CI. Added category/service indexes, AI onboarding, an environment worksheet,
reference inventory, technology rationale including WireGuard and secret custody,
and professional installation/change/recovery procedures. Corrected backup-tool
Git exclusions; actual private material remains excluded. No deployment or
publication is implied.

### Reproducibility and portfolio iteration

Fixed generated-config churn with an explicit service-file manifest; changed
runtime packages to one versioned request with installed-version verification.
Added real temporary-directory Ansible staging regressions, immutable public
image baseline, a consolidated source validator, a guarded hosted application/
encrypted-restore trial, dependency guidance and an engineering case study.
CI execution and disposable Proxmox/Ubuntu acceptance remain pending.
