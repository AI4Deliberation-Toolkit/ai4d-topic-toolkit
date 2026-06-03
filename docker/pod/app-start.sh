#!/bin/bash
# Supervised app process for the pod image. Mirrors docker/web/entrypoint.sh's
# migrate/seed/validate/collectstatic flow, but waits on the in-container
# Postgres (127.0.0.1) instead of a compose 'db' service.
set -euo pipefail

echo "[app] Waiting for local Postgres on 127.0.0.1:5432..."
until nc -z 127.0.0.1 5432; do sleep 0.2; done
echo "[app] Postgres up"

python3 manage.py migrate --noinput
python3 manage.py seed_taxonomy
python3 manage.py validate_taxonomy
python3 manage.py collectstatic --no-input --clear

exec gunicorn -w "${GUNICORN_WORKERS:-2}" -b 0.0.0.0:8000 \
     ai4d_topic_toolkit.wsgi:application --timeout 300
