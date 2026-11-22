#!/usr/bin/env bash
# Explicit operator action only. The encrypted repository must be initialized separately.
set -euo pipefail
: "${REFERENCE_BACKUP_APPROVED:?Set approval after reviewing context, scope and recovery}"
[[ "$REFERENCE_BACKUP_APPROVED" == yes ]] || exit 2
: "${RESTIC_REPOSITORY:?Set external encrypted backup repository}"
: "${RESTIC_PASSWORD_FILE:?Set external password-file path}"
project=${1:?Usage: postgres-to-restic.sh /srv/lab/database}
[[ "$project" = /* && -f "$project/compose.yaml" && -f "$project/.env" ]] || exit 2
# No plaintext dump is written. Pipe failure invalidates acceptance of the snapshot.
docker compose --project-directory "$project" --env-file "$project/.env" exec -T database   pg_dump --username postgres --dbname lab_demo --format custom |
  restic backup --stdin --stdin-filename reference-postgres.dump --tag reference-postgres
