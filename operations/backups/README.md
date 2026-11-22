# Backups and restoration

Public scripts belong in this category; actual dumps, repositories, credentials
and evidence do not. Use a separate protected location for backup data. A broad
Git rule must not hide these scripts while leaving a reference incomplete.

- `postgres-to-restic.sh`: explicit PostgreSQL dump stream into an already
  initialized encrypted restic repository; no plaintext dump is saved by it.
- `restore-isolated.sh`: explicit restore to the separately named disposable
  project, with manifest/empty-database checks.
- `check_restore.py`: offline rejection of unsafe project/volume/network/mount
  selections; tested independently and against rendered Compose JSON.
- `restore-example/`: synthetic independent destination, not a production volume.

Review the full [operating and recovery runbook](../../docs/runbooks/runbook.md)
before invoking these tools. Check Docker context, privileges, snapshot, destination,
secret-file paths and recovery intent. Approval environment variables are local
guardrails, not authorization by themselves. No schedule or retention deletion
is configured. Backup/restore scripts have not been integration-tested here.
