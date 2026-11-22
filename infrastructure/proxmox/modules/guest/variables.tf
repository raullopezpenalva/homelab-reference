variable "guest" {
  description = "One reviewed guest definition; never a private production inventory."
  type = object({
    name    = string, vm_id = number, address = string, gateway = string,
    vlan_id = number, cores = number, memory_mb = number, os_gib = number, data_gib = number
  })
  validation {
    condition     = can(cidrhost(var.guest.address, 0)) && var.guest.vm_id >= 100 && var.guest.cores >= 1 && var.guest.memory_mb >= 512 && var.guest.os_gib >= 16 && var.guest.data_gib >= 1 && var.guest.vlan_id >= 1 && var.guest.vlan_id <= 4094
    error_message = "Review the guest address, ID, sizing and VLAN."
  }
}
variable "node_name" { type = string }
variable "datastore_id" { type = string }
variable "bridge" { type = string }
variable "template_vm_id" { type = number }
variable "bootstrap_user" { type = string }
variable "ssh_public_keys" { type = list(string) }
variable "dns_servers" { type = list(string) }
variable "operation_approved" {
  type    = bool
  default = false
}
variable "started" {
  type    = bool
  default = false
}
variable "on_boot" {
  type    = bool
  default = false
}
