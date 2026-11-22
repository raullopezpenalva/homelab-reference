# Architecture decisions

Read the rationale before copying a configuration. Each decision is for this
reference, not proof of the author's installation or a requirement for every lab.
Record alternatives and constraints again when adapting it to your own needs.

| ADR | Question |
| --- | --- |
| [0001](0001-incremental-scope.md) | Why is virtualization the primary reference? |
| [0002](0002-provisioning-and-data-boundaries.md) | Who owns provisioning, configuration and persistent data? |
| [0003](0003-wireguard-private-access.md) | Why use WireGuard for private administration? |
| [0004](0004-tool-responsibilities.md) | Why Proxmox, Terraform, Ansible, Compose and these platform services? |
| [0005](0005-secrets-and-custody.md) | Why separate secret custody from the public repository? |
| [0006](0006-release-and-data-lifecycle.md) | Why separate image publication, promotion and database lifecycle? |

For a new ADR include date/status, problem, constraints, options, choice,
consequences, implementation links and the evidence needed to accept it.
Do not mark a design as deployed merely because an ADR is accepted.
