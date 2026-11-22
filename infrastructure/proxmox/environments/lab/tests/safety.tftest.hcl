mock_provider "proxmox" {}
variables {
  node_name      = "pve-demo"
  datastore_id   = "vm-demo"
  bridge         = "vmbr-demo"
  template_vm_id = 8800
}
run "disabled_by_default" {
  command = plan
  assert {
    condition     = length(output.ansible_inventory.all.children) == 0
    error_message = "Default configuration must not select any guests."
  }
}
run "requires_approval_and_keys" {
  command = plan
  variables { enabled_roles = ["applications"] }
  expect_failures = [var.enabled_roles]
}
run "approved_single_guest" {
  command = plan
  variables {
    enabled_roles      = ["applications"]
    operation_approved = true
    ssh_public_keys    = ["ssh-ed25519 SYNTHETIC-EXAMPLE-NOT-A-KEY"]
  }
  assert {
    condition     = length(output.ansible_inventory.all.children) == 1 && output.ansible_inventory.all.children.applications.hosts.workload01.ansible_host == "10.64.30.21"
    error_message = "Only the selected role may appear in inventory."
  }
}
