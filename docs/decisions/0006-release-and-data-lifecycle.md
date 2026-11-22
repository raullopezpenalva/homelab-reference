# ADR 0006: Separate artifacts, environment promotion and data

Date: 2026-11-22. Status: implemented boundaries; runtime procedures untested.

Building/publishing an image should not itself authorize a change to the lab.
Select reviewed image digests and configuration for one environment, record a
recovery reference, deploy through that environment's owner and verify actual
health. A CI status or an offline metadata check cannot prove that an artifact
exists, is compatible or has been deployed correctly.

Keep the database project independent from the application project. A web update
must not implicitly run SQL, restore data or delete a volume. Review schema
compatibility and major database upgrades as separate changes. Restoring an old
image does not undo data changes. Backups count as recoverable only after an
isolated restore check.

The reference provides a validation-only pipeline, a strict offline release
metadata validator and explicit backup/restore tools. It has no unattended
promotion engine, destination transaction journal or production deployment job.
Those require a separate design and acceptance. This narrower implementation
keeps the boundaries visible without pretending that complex automation is done.

See [change management](../runbooks/change-management.md),
[delivery tools](../../operations/deploy/README.md) and
[recovery procedures](../runbooks/runbook.md).
