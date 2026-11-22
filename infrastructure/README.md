# Infrastructure: provision guests, configure hosts

- [proxmox/](proxmox/README.md): Terraform environment/module, lockfile and fictional
  catalog. Owns guest resources, not physical hardware or installed services.
- [ansible/](ansible/README.md): baseline, runtime, authoritative DNS and service
  delivery. Owns guest configuration, not VM creation or router policy.

Read the [tool decision](../docs/decisions/0004-tool-responsibilities.md) and
[first installation](../docs/runbooks/first-installation.md) before running anything.
A real plan may contact Proxmox. Ansible check mode may connect to hosts. Use
[offline validation](../operations/validation/README.md) while learning.

No physical disk is selected/formatted here. No actual host inventory, endpoint,
state or key belongs in the public tree. Privately map the fictional roles to
your environment; do not infer that these examples describe another installation.
