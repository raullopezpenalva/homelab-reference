# Provisioning handoff: intent is not discovery

From the repository root, `python3 operations/provisioning/inventory.py --roles applications`
reads the fictional catalog in `infrastructure/proxmox/examples/lab.json` and
prints a preview. No Terraform, SSH or network call is performed. Empty role
selection emits no hosts. This does not prove that any guest exists.

After authorized provisioning, Terraform's `ansible_inventory` output provides
the selected environment's actual handoff. Save it privately with restricted
permissions. Do not commit it, paste it into a public issue or assume that a
rendered IP is an observed VM. Verify identity and trusted SSH separately.
Follow the [VM tutorial](../../docs/getting-started/virtualized.md).
