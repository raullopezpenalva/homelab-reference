# Proxmox: guest resource ownership

| Path | Purpose |
| --- | --- |
| environments/lab/ | Select roles and private environment inputs |
| modules/guest/ | Clone a template, define OS/data disks, NIC and cloud-init |
| examples/lab.json | Fictional common catalog; not a discovered inventory |
| environments/lab/tests/ | Fully mocked provider safety tests |

The default guest selection is empty. Start/autostart are off, destruction is
protected, and selected guests require explicit approval plus public SSH keys.
API identity, node, datastore, bridge, template and actual addresses are supplied
privately. HTTPS verification remains enabled. The module does not install a
hypervisor, create a bridge, configure a router or prepare physical storage.

Read [the VM tutorial](../../docs/getting-started/virtualized.md),
[ownership decision](../../docs/decisions/0002-provisioning-and-data-boundaries.md)
and [validation](../../operations/validation/README.md). Save real Terraform
state/plans and inventory output outside Git with private permissions and a
reviewed encrypted recovery strategy. A valid plan is not permission to apply it.
