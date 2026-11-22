variable "endpoint" {
  type        = string
  description = "Private Proxmox HTTPS API endpoint; CA trust must be configured externally."
  default     = "https://pve.example.com:8006/"
  validation {
    condition     = startswith(var.endpoint, "https://")
    error_message = "Use HTTPS with certificate verification."
  }
}
variable "api_token" {
  type      = string
  sensitive = true
  ephemeral = true
  default   = null
}
variable "config_file" {
  description = "Path to a private JSON catalog; null selects the fictional example."
  type        = string
  default     = null
}
variable "enabled_roles" {
  type    = set(string)
  default = []
  validation {
    condition     = length(var.enabled_roles) == 0 || (var.operation_approved && length(var.ssh_public_keys) > 0)
    error_message = "Selecting guests requires explicit approval and bootstrap public keys."
  }
  validation {
    condition     = length(setsubtract(var.enabled_roles, ["foundation", "applications", "telemetry", "automation", "sandbox"])) == 0
    error_message = "Select only documented role keys."
  }
}
variable "node_name" { type = string }
variable "datastore_id" { type = string }
variable "bridge" { type = string }
variable "template_vm_id" { type = number }
variable "ssh_public_keys" {
  type    = list(string)
  default = []
}
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
