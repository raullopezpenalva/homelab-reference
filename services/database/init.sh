#!/bin/sh
# Called by the upstream entrypoint only for a new, empty data volume.
set -eu
APP_PASSWORD=$(cat /run/secrets/database_app)
export APP_PASSWORD
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<'SQL'
\getenv app_password APP_PASSWORD
CREATE ROLE reference_reader LOGIN PASSWORD :'app_password';
CREATE TABLE public.greeting (id integer PRIMARY KEY, message text NOT NULL);
INSERT INTO public.greeting VALUES (1, 'Hello from the reference database');
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT CONNECT ON DATABASE lab_demo TO reference_reader;
GRANT USAGE ON SCHEMA public TO reference_reader;
GRANT SELECT ON public.greeting TO reference_reader;
SQL
unset APP_PASSWORD
