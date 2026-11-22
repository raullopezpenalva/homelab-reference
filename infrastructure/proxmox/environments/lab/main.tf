provider "proxmox" {
  endpoint  = var.endpoint
  api_token = var.api_token
  insecure  = false
}
locals {
  config   = jsondecode(file(var.config_file == null ? "${path.module}/../../examples/lab.json" : var.config_file))
  selected = { for role, guest in local.config.guests : role => guest if contains(var.enabled_roles, role) }
}
module "guests" {
  source             = "../../modules/guest"
  for_each           = local.selected
  guest              = each.value
  node_name          = var.node_name
  datastore_id       = var.datastore_id
  bridge             = var.bridge
  template_vm_id     = var.template_vm_id
  ssh_public_keys    = var.ssh_public_keys
  dns_servers        = local.config.dns_servers
  bootstrap_user     = local.config.bootstrap_user
  operation_approved = var.operation_approved
  started            = var.started
  on_boot            = var.on_boot
}
output "ansible_inventory" {
  description = "Private environment handoff; persist only under ignored private/."
  precondition {
    condition     = length(local.selected) == length(var.enabled_roles) && length(distinct([for g in values(local.config.guests) : g.vm_id])) == length(local.config.guests) && length(distinct([for g in values(local.config.guests) : g.address])) == length(local.config.guests) && length(distinct([for g in values(local.config.guests) : g.name])) == length(local.config.guests)
    error_message = "Catalog must contain each selected role and unique guest IDs, addresses and names."
  }
  value = {
    all = {
      vars = {
        ansible_user = local.config.bootstrap_user
        lab_domain   = local.config.domain
      }
      children = {
        for role, guest in local.selected : role => {
          hosts = { (guest.name) = { ansible_host = split("/", guest.address)[0], lab_role = role } }
        }
      }
    }
  }
}
