#!/bin/sh
set -e

if [ -z "$SECRET_KEY" ]; then
  echo "ERROR: SECRET_KEY must be set to a stable random value. It is used to encrypt stored stream keys." >&2
  exit 1
fi

mkdir -p "$(dirname "${PANEL_DB_PATH:-/data/panel.db}")"

exec gunicorn --bind 0.0.0.0:8000 --workers "${GUNICORN_WORKERS:-2}" app:app
