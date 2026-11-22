#!/usr/bin/env bash
# Restore only to the separate, disposable restore project described in the runbook.
set -euo pipefail
[[ "${REFERENCE_RESTORE_APPROVED:-}" == restore-disposable ]] || exit 2
: "${RESTIC_REPOSITORY:?Set encrypted backup repository}"
: "${RESTIC_PASSWORD_FILE:?Set external password-file path}"
snapshot=${1:?Usage: restore-isolated.sh snapshot-id /absolute/restore-project}
project=${2:?Select the disposable restore project}
[[ "$snapshot" =~ ^[a-f0-9]{8,64}$ && "$project" = /* && -f "$project/compose.yaml" ]] || exit 2
# Independent project identity prevents the production/reference DB from being selected.
helper_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
docker compose --project-directory "$project" --env-file "$project/.env" config --format json |
  python3 "$helper_dir/check_restore.py"
# The independent project must have no application table before loading a dump.
tables=$(docker compose --project-directory "$project" --env-file "$project/.env" exec -T database \
  psql --username postgres --dbname lab_demo --tuples-only --no-align \
  --command "SELECT count(*) FROM pg_tables WHERE schemaname = 'public'")
[[ "$tables" == 0 ]] || { echo 'Restore database is not empty' >&2; exit 2; }
restic dump "$snapshot" /reference-postgres.dump |
  docker compose --project-directory "$project" --env-file "$project/.env" exec -T database     pg_restore --username postgres --dbname lab_demo --no-owner --no-acl --exit-on-error
