# Virtualized lab: Proxmox, Terraform, Ansible and services

This is an operator-controlled procedure for **your new disposable lab**. None
of these infrastructure operations was performed while authoring the reference.
Read the architecture and record target, scope, persistence, backup and recovery
before proceeding. Do not point these examples at an existing private setup.

## 1. Prepare the hypervisor and a guest template

Install Proxmox separately using its documented installer. Identify your node,
VM-capable datastore and VLAN-aware bridge. Prepare networking and management
access independently. Do not copy the fictional VLAN values onto a live router.

Create an Ubuntu 24.04 amd64 cloud-init VM template with a small `scsi0` OS disk,
cloud-init drive, serial console, SSH public-key access and Python 3. Install
and enable qemu-guest-agent in that template, and make its OS disk no larger than
the smallest configured guest OS disk. Clean template-specific machine identity
using the distribution's documented cloud-image procedure. Record the template
ID, OS image checksum and a tested console recovery path. Template creation,
physical disks, host installation and bootstrap privileges are not automated.

Create a dedicated, least-privileged API identity scoped to the reviewed node,
template, destination VM IDs and datastore. Determine required privileges from
the pinned provider documentation; no administrator token is supplied here.
Configure trusted HTTPS/CA validation. Do not bypass TLS with `insecure=true`.

## 2. Create private inputs

From the repository root, create an ignored `private/` directory with mode 0700.
Copy [the catalog](../../infrastructure/proxmox/examples/lab.json) to `private/lab.json` and
[the tfvars example](../../infrastructure/proxmox/environments/lab/terraform.tfvars.example)
to `private/lab.tfvars`. Replace every fictional network, node, bridge, storage,
VM ID and template input with values for your disposable lab.

The catalog's `192.0.2.53` is a documentation-only bootstrap DNS placeholder and
must be replaced by a reachable resolver. Do not configure cloud-init to depend
on the foundation DNS server before it exists. Supply only **public** SSH keys.
Never put an API token, private key or password in the catalog or tfvars.

Set `config_file` in your private tfvars to the absolute private catalog path.
Start with `enabled_roles = ["applications"]`; other roles can be added later.
Guest creation requires `operation_approved = true` and public SSH keys. Defaults
keep all guests unselected, stopped and without autostart. Explicitly review
`started` before choosing to boot a guest.

## 3. Validate, review and provision

Install the documented Terraform version on your controller. Run the README's
offline validation first. Then, **only when you authorize a real operation**:

1. Supply a scoped token privately through `TF_VAR_api_token` or the provider's
   supported environment mechanism; use a secure prompt/credential helper rather
   than pasting it into shell history. Clear it after the operation.
2. Initialize the chosen private state location. The example has a local backend;
   on real use, protect state with filesystem permissions and encrypted storage,
   locking and a recovery copy. A sensitive flag alone does not encrypt state.
3. Review a real plan with your absolute private `-var-file`. A plan contacts the
   API and may refresh state. Treat any saved plan/output as private material.
4. Apply only the reviewed plan in that same environment. The module refuses
   destruction and does not automatically reboot guests on configuration updates.
5. Boot the selected guest explicitly if it was created stopped; record its
   observed identity, NIC, OS and data disk before proceeding.

Example commands below are **operational**, not authoring checks:

```sh
terraform -chdir=infrastructure/proxmox/environments/lab plan -var-file=/absolute/private/lab.tfvars -out=/absolute/private/reviewed.plan
terraform -chdir=infrastructure/proxmox/environments/lab apply /absolute/private/reviewed.plan
```

No command in CI runs a real plan or apply. Never use `-target` to bypass the
reviewed inventory and ownership model. The lifecycle safeguard is not a backup.

## 4. Hand off inventory and configure the operating system

After provisioning, save `terraform output -json ansible_inventory` from the
Terraform root into an ignored, mode-0600 private inventory file. It contains
actual environment addresses. For an offline preview only, use:

```sh
python3 operations/provisioning/inventory.py --roles applications
```

The preview reads only JSON. It does not discover VMs or establish connectivity.
Use a verified SSH host-key fingerprint from the console. The Ansible default
inventory is empty and host-key checking is enabled.

Install `operations/validation/requirements.txt` in a separate controller environment and install
the collection from `infrastructure/ansible/requirements.yml`. Copy the
[operation example](../../infrastructure/ansible/examples/operation.example.yml) privately.
Record one exact target, approved scope and a concrete recovery reference, then
set `lab_operation_approved: true` for that operation.

Run from `infrastructure/ansible/`, selecting your private inventory and variables explicitly:

```sh
ansible-playbook -i /absolute/private/inventory.json playbooks/baseline.yml -e @/absolute/private/operation.yml
```

This is a remote change. The controller-side assertion runs before gathering
facts and requires one selected SSH host. `--check` is intentionally rejected:
it is not offline validation. Baseline installs packages, guest support and a
node exporter bound to the guest address. Restrict TCP 9100 to the telemetry host
in your separately reviewed network policy before deploying the exporter.
No SSH account, firewall policy or system reboot is changed by the baseline.

## 5. Prepare data storage and Docker

Using an explicitly reviewed storage procedure, prepare and mount the guest's
separate data disk at `/srv/lab`, persist its mount and record its UUID. This
reference intentionally supplies no automatic formatting command. Verify the
correct disk and recovery path before any manual partitioning.

Select exact Docker vendor package versions for Ubuntu noble/amd64 and the
public repository signing-key checksum. Supply them in the private operation
file. Choose a compatible set from the vendor repository, including a matching
engine/CLI pair; do not substitute `latest` or a version wildcard. See the
[dependency procedure](../runbooks/dependency-updates.md). Run `playbooks/runtime.yml`
with the same single-host procedure. The role
checks the exact mount and rejects unowned runtime files/packages rather than
migrating them. All selected versions are requested in one package transaction
and checked against installed package facts before service startup. Docker and
containerd store data separately under `/srv/lab`;
their startup requires the data mount. No Docker TCP API or user-group grant is
created. Do not change disk UUID or runtime ownership as an upgrade shortcut.

## 6. Build the example API and deliver bundles

The API source is [demo API source](../../services/demo-api/app.py).
Its image is not prepublished. In your explicitly selected build environment:

```sh
docker build -t reference-api:local services/demo-api
```

For a VM, publish to a registry you control and record the immutable digest.
The public upstream examples are fixed in `operations/validation/images.lock.json`.
Their manifests were verified, but vulnerability/runtime acceptance is separate.
Review that baseline or deliberately choose and record new digests for your lab. Use the exact `lab_images` keys
from [the image example](../../infrastructure/ansible/examples/images.example.yml), replacing
its deliberately invalid placeholders with reviewed digests.

Create strong independent `database_admin` and `database_app` password files
outside Git at your private `lab_secret_dir`. Do not print them. PostgreSQL's
entrypoint reads the admin file, creates a read-only application role on first
initialization, and grants SELECT on one demo table. The API receives only its
own password file. On the VM, secret-file permissions must allow the consuming
container UID: the API runs as 10001. Compose file-backed secrets use host bind
permissions; declared secret modes are not a substitute for verifying ownership.
Use a protected parent directory and narrowly readable files; test this first in
a disposable environment.

Run `playbooks/services.yml` twice, each as a separate reviewed operation:

1. `lab_bundle: database`, `lab_role: applications`, and `POSTGRES_IMAGE` only.
   This creates the private data network and initializes an empty DB volume.
2. `lab_bundle: applications`, same guest role, and `NGINX_IMAGE` plus `API_IMAGE`.
   This joins the existing data network and starts the API/proxy. It never runs
   database lifecycle commands. The DB must already be healthy.

`lab_bundle` is an operation input; `lab_role` comes from the private inventory.
Do not overwrite the inventory role to make a bundle fit. Services require the
same verified data UUID as the runtime. No service bundle deletes volumes or
adopts another project. Start with `lab_bind_address: 127.0.0.1`, then run
`sh operations/validation/smoke-virtualized.sh` on the workload guest or through an approved
SSH tunnel. Success checks the frontend, API and actual SQL read path.

## 7. Add foundation and telemetry

Enable the chosen additional guest roles in your private Terraform input,
review/apply their plans, regenerate inventory and configure their baselines.
On the foundation guest run `playbooks/dns.yml` with a reviewed copy of the
[DNS inputs](../../infrastructure/ansible/examples/dns.example.yml). Increase the SOA serial
for zone changes. `named-checkzone` and `named-checkconf` validate generated files.
Test allowed and denied queries, and no-recursion behavior, before clients use it.

Prepare telemetry storage/runtime and create an external `grafana_admin` file
readable by Grafana's container UID (commonly 472; verify your selected image).
Deploy `lab_bundle: telemetry` with the two required image digests. The playbook
renders node targets from your inventory; the checked-in targets are fictional.
Use a private tunnel to Grafana 3000 or Prometheus 9090 and check target freshness.
Do not claim alert delivery: no notification route is configured.

## 8. Optional private ingress, CI and development

The foundation's `ingress` bundle can route Host-based HTTP to selected workload,
Grafana and CI backends. Supply `lab_application_upstream`,
`lab_grafana_upstream`, `lab_ci_upstream` and `lab_domain`. Leave it on loopback
for tunnel use first. Cross-VM routing requires explicit private backend binds
and independently tested ACLs. This bundle does not issue TLS certificates.
Never expose it to an untrusted network before designing TLS/authentication.

Optional automation uses its own VM and persistent controller volume. Keep
Jenkins on loopback, complete its setup wizard privately, and provision a
separate `reference-validation` agent with the validation tools. The sample
Jenkinsfile performs checks only, with no timer, deployment job or credentials.
The sandbox bundle is a separate private demo, not a shared application runtime.
VPN, TLS renewal, notification delivery, centralized logging and IoT software
remain separate extensions. See [operations](../runbooks/runbook.md).

## Upstream contracts

- [Pinned Proxmox VM provider reference](https://github.com/bpg/terraform-provider-proxmox/blob/v0.114.0/docs/resources/virtual_environment_vm.md)
- [Terraform mocked-provider testing](https://developer.hashicorp.com/terraform/language/tests/mocking)
- [Ansible Compose v2 module](https://docs.ansible.com/projects/ansible/latest/collections/community/docker/docker_compose_v2_module.html)
- [Docker Ubuntu package installation](https://docs.docker.com/engine/install/ubuntu/)

Review the contracts for your selected versions before accepting an operation.
