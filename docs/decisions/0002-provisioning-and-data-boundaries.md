# ADR 0002: Separate provisioning, configuration and persistent data

Date: 2026-11-22. Status: accepted for the reference draft.

Terraform clones Ubuntu guests, defines virtual OS/data disks and emits inventory.
Ansible configures a selected guest and verifies a separately prepared filesystem.
Docker/containerd data roots live on that mount. No playbook formats disks,
reboots hosts or changes a router. VM selection/start/autostart are opt-in.

PostgreSQL has a separate Compose project from the web/API. Application release
inputs cannot request database changes. Backups stream into encrypted independent
storage; restore uses a separately named disposable project without automatic
promotion. CI validates without infrastructure credentials or deployment steps.

Trade-offs: the operator performs additional explicit steps and must manage
secrets/state and disaster recovery. A protected lifecycle or valid manifest
cannot establish a tested backup. These boundaries favor understandable recovery
and prevent an application refresh from becoming an implicit data operation.
