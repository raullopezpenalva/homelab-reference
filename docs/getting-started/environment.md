# Your environment worksheet

Complete this before editing the example catalog. Share only information you are
comfortable giving the assistant. Actual endpoints, inventories and identities
belong in ignored private files or a separate private workspace, never in this
public worksheet or a public issue. Never paste credentials into chat.

## Goals and capacity

- What do you want to learn or host first? What can wait?
- What CPU architecture, RAM and disk capacity are available for a disposable lab?
- Can you reinstall the machine? Is any existing data or service at risk?
- How much resource must remain available for the hypervisor and recovery?
- Which services need persistent data, and how much growth is expected?

## Access and network capabilities

- Is the lab local-only, remotely administered or intentionally public?
- Does your router/switch support the segmentation you want? You can describe
  capabilities without sharing its real address, vendor account or rule export.
- Can you reach a VPN endpoint, or do NAT/provider constraints need another design?
- Which clients need DNS, administration, an app or IoT access? These are separate
  authorizations; do not grant a whole network because one service is needed.
- Who owns DNS, certificates, routing and router policy in the new environment?

## Persistence, secrets and recovery

- What can be rebuilt from code, and what data must be restored?
- Where will encrypted backups live independently of the hypervisor?
- What data loss and recovery time are acceptable for each service?
- How will an operator recover keys/state if the usual laptop or DNS is unavailable?
- Which password manager and encrypted-file custody model can you operate reliably?

## Record the decisions

Choose only the smallest useful profile. Write your reasons using the
[decision index](../decisions/README.md), document the adaptation in a private
[change record](../templates/change-record.example.md), and keep a private map
from role names to your actual environment. Do not infer any of these answers
from the fictional IDs, networks or sizes checked into this repository.
