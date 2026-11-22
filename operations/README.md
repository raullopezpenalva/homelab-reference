# Operations: how to run and recover a lab

| Category | Contents | Start here |
| --- | --- | --- |
| validation/ | Offline checks, tests and explicit smoke scripts | [Validation guide](validation/README.md) |
| provisioning/ | Offline catalog-to-inventory preview | [Provisioning handoff](provisioning/README.md) |
| deploy/ | Strict offline release metadata checker | [Delivery boundary](deploy/README.md) |
| network/ | Fictional WireGuard template | [Network operations](network/README.md) |
| backups/ | Explicit encrypted DB backup and isolated restore | [Backup guide](backups/README.md) |
| cicd/ | Validation-only Jenkins pipeline example | [CI boundary](cicd/README.md) |

Understanding: [docs](../docs/README.md). First installation:
[staged procedure](../docs/runbooks/first-installation.md). Day-to-day changes:
[change management](../docs/runbooks/change-management.md). Persistent data and
restoration: [runbook](../docs/runbooks/runbook.md).

No task here implies authorization to operate. Record destination, scope,
validation, persistence, backup and recovery before invoking an operational tool.
No new timer, deployment job or infrastructure credential is installed by these
examples. Keep real operation logs and evidence private.
