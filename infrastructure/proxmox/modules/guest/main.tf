resource "proxmox_virtual_environment_vm" "guest" {
  name                = var.guest.name
  vm_id               = var.guest.vm_id
  node_name           = var.node_name
  description         = "Synthetic homelab reference guest; environment selected by operator"
  tags                = ["reference", "terraform"]
  started             = var.started
  on_boot             = var.on_boot
  reboot_after_update = false
  scsi_hardware       = "virtio-scsi-single"
  boot_order          = ["scsi0"]
  clone {
    vm_id        = var.template_vm_id
    full         = true
    datastore_id = var.datastore_id
  }
  cpu {
    cores = var.guest.cores
    type  = "x86-64-v2-AES"
  }
  memory { dedicated = var.guest.memory_mb }
  agent {
    enabled = true
    wait_for_ip { disabled = true }
  }
  operating_system { type = "l26" }
  serial_device { device = "socket" }
  vga { type = "serial0" }
  disk {
    datastore_id = var.datastore_id
    interface    = "scsi0"
    size         = var.guest.os_gib
  }
  disk {
    datastore_id = var.datastore_id
    interface    = "scsi1"
    size         = var.guest.data_gib
  }
  network_device {
    bridge  = var.bridge
    vlan_id = var.guest.vlan_id
  }
  initialization {
    datastore_id = var.datastore_id
    interface    = "ide2"
    dns { servers = var.dns_servers }
    ip_config {
      ipv4 {
        address = var.guest.address
        gateway = var.guest.gateway
      }
    }
    user_account {
      username = var.bootstrap_user
      keys     = var.ssh_public_keys
    }
  }
  lifecycle {
    prevent_destroy = true
    precondition {
      condition     = var.operation_approved && length(var.ssh_public_keys) > 0 && length(var.dns_servers) > 0 && var.guest.vm_id != var.template_vm_id
      error_message = "Guest creation requires explicit scope approval, public SSH keys, usable bootstrap DNS and a distinct template ID."
    }
  }
}
