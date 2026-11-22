# Ansible: configure one selected guest

Run from this directory when following the [VM guide](../../docs/getting-started/virtualized.md).
The default `inventory/empty.yml` has no hosts. Actual inventories belong privately
outside this tree. `examples/` contains invalid markers and fictional inputs only.

| Playbook | Responsibility | Before executing |
| --- | --- | --- |
| baseline.yml | Guest support and node exporter | One target, trusted SSH, external metrics policy |
| runtime.yml | Reviewed Docker/containerd packages and dedicated data roots | Exact versions, key checksum, verified data UUID and recovery |
| dns.yml | Authoritative-only BIND9 | Explicit query clients, zone/serial and DNS checks |
| services.yml | One selected service bundle | Correct role, image digests, data mount, private secrets and binds |

The controller assertion precedes SSH facts and requires one selected target,
a declared scope and recovery plan. These are guardrails, not a substitute for
operator authorization. The playbooks do not format storage, reboot systems or
change routers. Actual idempotence needs repeat convergence in a trial environment.

Service names and remote project paths remain stable while the source is grouped
by category. `roles/bundle/vars/main.yml` maps logical bundle keys to the source
directories listed in [services](../../services/README.md). Never change the
inventory role to bypass the mapping. See [offline checks](../../operations/validation/README.md).

The service role ships only files listed in `bundle_static_files`; generated
Prometheus config is template-owned and local README/env files are excluded.
Local regression tests verify staging convergence. Runtime package selection is
one versioned apt request with post-install facts checked before startup; the
actual package transaction still needs a disposable-guest trial.
