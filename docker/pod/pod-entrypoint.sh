#!/bin/bash
# Pod-only entrypoint (PID 1). Initializes the bundled Postgres cluster on the
# mounted volume the FIRST time only, then hands off to supervisord which runs
# Postgres + the Django app side by side. The server deployment does not use
# this script (it uses docker/web/entrypoint.sh).
set -euo pipefail

: "${PGDATA:=/data/pgdata}"
: "${HF_HOME:=/data/hf_cache}"
: "${POSTGRES_USER:?set POSTGRES_USER}"
: "${POSTGRES_PASSWORD:?set POSTGRES_PASSWORD}"
: "${POSTGRES_DB:?set POSTGRES_DB}"

mkdir -p "$HF_HOME" "$(dirname "$PGDATA")"

if [ ! -s "$PGDATA/PG_VERSION" ]; then
  echo "[pod-entrypoint] Initializing fresh Postgres cluster at $PGDATA"
  mkdir -p "$PGDATA"
  chown -R postgres:postgres "$PGDATA" "$HF_HOME"
  # localhost-only DB: trust on 127.0.0.1 is acceptable (nothing outside the
  # container can reach it).
  gosu postgres initdb -D "$PGDATA" --auth-local=peer --auth-host=trust
  gosu postgres pg_ctl -D "$PGDATA" -o "-c listen_addresses='127.0.0.1'" -w start
  gosu postgres psql -v ON_ERROR_STOP=1 --username postgres <<-SQL
    CREATE USER "$POSTGRES_USER" WITH PASSWORD '$POSTGRES_PASSWORD';
    CREATE DATABASE "$POSTGRES_DB" OWNER "$POSTGRES_USER";
SQL
  gosu postgres pg_ctl -D "$PGDATA" -w stop
else
  echo "[pod-entrypoint] Existing cluster at $PGDATA — skipping init"
  chown -R postgres:postgres "$PGDATA"
fi

exec supervisord -n -c /etc/supervisor/supervisord.conf
