# ADR 0004: Tool responsibilities and technology choices

Date: 2026-11-22. Status: reference choices; runtime acceptance is separate.

The goal is understandable, reproducible infrastructure with explicit ownership.
Choose tools for separate jobs, and remove optional layers when they do not serve
a need. This table explains the reference rather than claiming a universal stack.

| Choice | Reason in this reference | Trade-off / alternative |
| --- | --- | --- |
| Proxmox with Ubuntu VMs | Separate guest lifecycles and resource budgets on one physical lab | Requires hypervisor capacity and recovery; bare-metal Linux is a simpler first profile |
| Terraform | Review guest-resource intent and lifecycle in code | State is sensitive and plans can contact infrastructure; manual provisioning is acceptable if ownership stays clear |
| Ansible | Configure a selected guest through explicit playbooks and reusable tasks | Idempotence must be observed by repeat execution; it does not replace VM resource ownership |
| Docker Compose inside guests | Keep small service stacks understandable and independently selectable | Host/container isolation and persistence still need design; orchestration is a separate need |
| BIND9 authoritative DNS | Make private naming explicit and teach zone ownership | It is not automatically a recursive resolver; bootstrap DNS must work before this service exists |
| NGINX | Give HTTP routing a defined owner separate from application code | TLS/authentication/renewal need additional decisions; a proxy is not an access-control policy by itself |
| PostgreSQL | Demonstrate persistent application data and a constrained app role | Backup/restore, credential rotation and major upgrades are separate operations |
| Prometheus and Grafana | Separate metric collection/rules from inspection and dashboards | Fresh targets and useful alerts need runtime evidence; they do not prove recovery |
| GitHub Actions | Validate public code without access to the lab | CI success is not deployment acceptance |
| Optional Jenkins | Illustrate a dedicated validation controller and separate agent boundary | Extra runtime, patching and recovery burden; omit it until needed |

Do not introduce a new service merely because it appears in this table.
Terraform owns guest resources, Ansible owns host configuration/delivery, Compose
owns containers, and an operator owns environment promotion. Application source
and artifact builds normally belong to their own repositories; the included
[demo API](../../services/demo-api/README.md) is an educational exception.

Pointers: [Proxmox documentation](https://pve.proxmox.com/pve-docs/),
[Terraform configuration](https://developer.hashicorp.com/terraform/language),
[Ansible playbooks](https://docs.ansible.com/projects/ansible/latest/playbook_guide/),
[Docker Compose](https://docs.docker.com/compose/).
