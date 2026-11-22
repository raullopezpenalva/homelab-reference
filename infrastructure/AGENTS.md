# Infrastructure instructions

Read this category's README and relevant ADR before changing code. Keep VM
resource ownership in proxmox/ and host configuration in ansible/. Preserve the
empty inventory, explicit single-host scope, verified data mount and private
input boundary. Do not infer actual hardware or networks from fictional examples.
Use cached static/schema checks and fully mocked tests during repository work.
Do not initialize a real backend, plan/apply, connect to guests, select/format a
disk or alter router policy without a separate explicit operation request.
