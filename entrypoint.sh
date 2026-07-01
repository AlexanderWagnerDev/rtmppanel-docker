#!/bin/sh
set -e

if [ -z "$SECRET_KEY" ]; then
  export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
fi

mkdir -p "$(dirname "${PANEL_DB_PATH:-/data/panel.db}")"

exec gunicorn --bind 0.0.0.0:8000 --workers "${GUNICORN_WORKERS:-2}" app:app
