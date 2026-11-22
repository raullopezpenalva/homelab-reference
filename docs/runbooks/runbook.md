# Operations: provision, configure, deliver and recover

Use the [VM guide](../getting-started/virtualized.md) for first installation.
Every operation must record target, scope, validation, persistent data, backup
and recovery. Commands below are for a separately authorized disposable lab;
none were executed against infrastructure during repository authoring.

## Ownership and acceptance

Terraform owns guest resources; Ansible owns OS/runtime and bundle delivery;
Compose owns container projects; application repositories own image builds;
operators own environment promotion and recovery. Do not let two tools format
storage or manage the same VM. Do not copy application code from private repos.

Acceptance requires observed VM identity, trusted SSH, a verified data mount,
repeatable host configuration, expected runtime paths, functional app/SQL checks,
private metrics, denied network flows and a tested recovery path. Repeat baseline
and service playbooks and record convergence; idempotency has not been tested
on real guests here. A parsed config is not a successful deployment.

## Deployment and promotion

Keep guest creation, baseline, runtime, database initialization and application
delivery as separate reviewed operations. Service playbooks refuse multi-host
scope and require image digests. The optional offline release validator at
`operations/deploy/validate.py` checks exact bundle keys, image immutability,
source revision and a recovery reference. It cannot establish artifact existence,
provenance, compatibility or deployment health and never executes a command.

There is no automatic promotion engine or unattended deployment pipeline. A
future service-specific deployer should add a destination lock, durable intent,
health acceptance and a linked recovery record before unattended use. Jenkins
and GitHub Actions examples validate only; they have no infrastructure identity.

## Update an application

Record old image digests, current state and a recovery reference privately.
Review the new image/source, run offline checks, then deliver only the
`applications` bundle. A change to web/API does not invoke the `database` project,
run migrations, restore a database or delete a volume. Verify frontend plus
`/api/message` (actual SQL access), not proxy liveness alone. Roll back only to a
reviewed compatible image combination using the same service procedure. Failure
requires an explicit recovery decision, not re-enabling a historical CI job.

Package changes need exact new versions and review of service restarts. Runtime
storage migration or a changed data UUID is a separate operation. Never re-run
a package role over an unowned existing runtime as a migration technique.

## Database lifecycle

The database has its own Compose project/network/volume. Initialization scripts
run only for an empty volume. Changing a password file does not rotate an
existing database role: coordinate an explicit SQL credential rotation with the
consumer and backup policy. The API role can SELECT only the demo table and has
no schema or administration rights. Do not treat a healthy `pg_isready` result as
proof of application credentials, schema compatibility or backup recoverability.
Major PostgreSQL upgrades require a separate tested dump/restore or supported
upgrade procedure; changing an image tag alone is insufficient.

## Encrypted PostgreSQL backups

`operations/backups/postgres-to-restic.sh` streams a custom-format pg_dump into
an already initialized encrypted restic repository. It requires explicit approval,
a selected project path, `RESTIC_REPOSITORY` and an external
`RESTIC_PASSWORD_FILE`. Restic and Docker must already exist in the chosen
backup environment; no installer or scheduled task is included. The Compose
project path identifies the database; review the Docker context before running.
The script does not delete snapshots or change retention.

Run it on the selected VM with only the needed database/backup privileges. Keep
the restic repository physically separate from the guest/hypervisor and retain
an offline recovery copy. The script uses pipeline failure propagation. If
pg_dump fails, a partial snapshot may still exist; do not accept that snapshot as
a valid backup. Validate a backup by restoring it, not just by its command exit.

## Restore into an isolated destination

1. Copy [the restore project](../../operations/backups/restore-example/compose.yaml) and its env
   example to an isolated host or private working directory. Use reviewed image
   digests matching the source major version and new disposable credentials.
2. Keep the `reference-restore` project name, distinct private network and new
   empty volume. No production ports or data volume may be attached. This
   project omits the reference initialization script, leaving an empty database.
3. Explicitly start that disposable database. Select a reviewed restic snapshot
   by hexadecimal ID, never an implicit moving `latest`.
4. Set `REFERENCE_RESTORE_APPROVED=restore-disposable` and call
   `operations/backups/restore-isolated.sh SNAPSHOT /absolute/restore-project`.
   The script checks project/volume/network identity, rejects host binds or
   container overrides, requires an empty destination, streams the dump and stops on errors.
   It intentionally restores no owners/ACLs and performs no destructive clean.
5. Verify the greeting row, schema and row counts as a disposable administrator.
   Recreate the least-privileged application role privately if rehearsing a full
   application recovery; dumps do not include role passwords or cluster globals.
6. Record snapshot, version, destination identity, result and recovery duration.
   Do not promote this volume automatically. Remove it only after explicit review.

Backups and restores have not been integration-tested here. Restic encryption
protects stored snapshots, not a compromised live database or operator account.

## Other persistence and complete recovery

Grafana and Jenkins have independent named volumes; capture cold copies or
supported application backups with verified permissions and separate encrypted
storage. Terraform state, private catalogs and secret custody require separate
private backup. Metrics may be disposable according to your retention policy;
if retained, test a consistent volume recovery with the matching image.

Complete recovery order: Proxmox/storage/network → template → Terraform state
and selected guests → baseline/data mounts/runtime → external identities →
authoritative DNS → database and application → telemetry → optional CI/sandbox.
Restore a backup into an isolated environment first; changing DNS or public
routing is a separate cutover. No full-machine recovery is claimed verified.

## Troubleshooting

Use the selected VM console, `findmnt --mountpoint /srv/lab`, systemd unit status,
scoped `docker compose ps` and bounded service logs. Treat logs as private before
sharing. API readiness failure may mean missing password-file permissions, DNS,
schema or database availability; it returns a generic error without credentials.
A proxy 502 is not a reason to open a router port. Check explicit backend binds
and reachability. For missing telemetry, inspect rendered inventory targets and
network ACLs. Do not disable certificate/SSH verification to bypass a failure.

For the optional Starter use its [own tutorial](../getting-started/starter.md);
its default project/metrics volume is separate from the virtualized bundles.
