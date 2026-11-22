# Reference inventory and evidence status

Updated: 2026-11-22. This is an inventory of the **reference implementation**, not
an operational inventory of the author or a new owner. No real host, endpoint,
network range, account or deployment is listed here.

| Category | Component | Available artifact | Runtime acceptance |
| --- | --- | --- | --- |
| infrastructure | Proxmox VMs | Terraform module, fictional catalog and mock tests | Not deployed |
| infrastructure | Guest configuration | Baseline, data/runtime guards, DNS and service playbooks | No guest convergence tested |
| services | Application/data | Frontend, read-only demo API and separate PostgreSQL project | Hosted synthetic frontend/API/SQL trial passed |
| services | Private ingress | NGINX HTTP example | No network/TLS acceptance |
| services | Observability | Prometheus, Grafana datasource/dashboard and host exporter | No live targets verified |
| services | Optional CI/development | Jenkins controller and sandbox definitions | Not installed |
| operations | Delivery/validation | Offline metadata checker, tests, smoke scripts and CI examples | No automatic deployment engine |
| operations | Recovery | Explicit encrypted backup and isolated restore tooling | Hosted encrypted backup/isolated restore passed; off-host recovery pending |
| operations | Hosted integration | Canonical app/SQL/encrypted-restore harness, CI job and guard tests | First hosted application/restore run passed |
| operations | Private access | Fictional WireGuard template | No tunnel/router configuration |
| secrets | Custody | Policy and private-file workflow | No identity or credential included |

Actual local check results belong in [release readiness](release-readiness.md).
A component can be implemented and statically checked without being runtime-tested.

For your environment, maintain a separate private inventory with role, actual
identity, date, observed check/result, persistent data, recovery reference and
remaining unknowns. Refer to that private record without copying its values into
this public tree. `00-now.md` tracks selected work; decisions explain why;
runbooks explain how; evidence establishes what actually happened.

Local staging convergence is observed only for temporary file delivery; it is not
whole-guest convergence. The public image baseline is digest-fixed and registry
verified, while vulnerability and runtime acceptance remain separate gates.
