# Host observability

The telemetry bundle supplies Prometheus, a target-unavailable rule, Grafana datasource and a basic host dashboard. Ansible renders node targets from private inventory; checked-in targets are fictional. No log/tracing stack or external alert delivery is claimed.

Read the [service index](../README.md), [VM guide](../../docs/getting-started/virtualized.md)
and [operating runbook](../../docs/runbooks/runbook.md) before a change.
Public image examples are fixed by digest in the validation image lock. The
operator must still review vulnerabilities and select their own API artifact. Secret contents stay outside Git and
consumer UID/permissions must be verified. No runtime acceptance is implied.

The checked-in Prometheus file supports standalone example parsing only. VM
staging excludes it and renders its sole destination from the inventory template;
a second unchanged stage must not recreate containers. Static rules/datasource/
dashboard files are shipped through the explicit bundle manifest.
