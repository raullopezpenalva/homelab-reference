# Reference scope and privacy transformation

Date: 2026-11-22. The primary deliverable is a virtualized IaC reference.

## What informed the design

Read-only inspection of the private source showed provisioning/configuration
boundaries, functional separation between guests, Compose applications,
authoritative DNS, private ingress, PostgreSQL, telemetry, delivery validation,
and backup/recovery procedures. Dated inventory entries are source declarations;
no live service was queried to refresh them. Historical received material is
reference only. This document contains no original guest names, IPs or inventory.

## What is preserved

| Engineering pattern | Independent reference implementation |
| --- | --- |
| Proxmox guests with cloud-init | Parameterized cloning module, virtual OS/data disks, VLAN input |
| Provisioning distinct from host configuration | Terraform inventory handoff and separate Ansible playbooks |
| Service-specific virtual machines | Fictional foundation, workload, telemetry and optional CI/development roles |
| Runtime distinct from services | Guarded exact-version Docker installation on a verified data mount |
| Authoritative DNS / private entry | Native BIND9 role and optional private NGINX ingress bundle |
| Frontend/API/data responsibilities | Independently authored web/API demo and separate PostgreSQL project |
| Observability | Private node metrics, Prometheus rule and provisioned Grafana datasource |
| Delivery ownership | Immutable image inputs, offline metadata validator and validation-only CI |
| Recovery is an operation | Encrypted streaming backup and distinct disposable restore project |

## What is intentionally changed or excluded

Guest identifiers, names, resource allocations, IPs, network segments and
placement were invented. This is not a redacted network map. No original hardware
inventory, public endpoint, domain, DNS record, VLAN, router rule, VPN peer,
service account, SSH identity, token, ciphertext metadata, state, backup, evidence,
CI trigger or private application was imported. No historical repository or
proxy implementation was synchronized. Source/build ownership and environment
promotion remain separate concepts; their private implementations are excluded.

## Implementation boundaries

The virtualized profile now contains executable Terraform and Ansible, rather
than a design-only promise. The Starter profile remains optional. Working code
and parsed configuration do not establish that guest creation, runtime delivery,
network isolation, backups or full application startup have succeeded. See the
[dated validation report](../release-readiness.md).

Router/VPN/TLS policy, ACME/DDNS, IoT software, log aggregation and tracing are
explicit extension areas. They are not represented by empty executable folders
or claims of completion. This scope can grow without reproducing the private
installation or coupling public updates to it.

## Category structure and reader workflow

The public tree follows the same responsibility categories as an operated lab:
[docs](../README.md), [infrastructure](../../infrastructure/README.md),
[operations](../../operations/README.md), [secrets](../../secrets/README.md) and
[services](../../services/README.md). This preserves organization and professional
process, while all actual inventories, policy and identities remain excluded.
The [AI handoff](../getting-started/ai-handoff.md) starts with understanding and
requirements; [decisions](../decisions/README.md) explain choices before commands.
