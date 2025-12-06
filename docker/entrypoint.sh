#!/usr/bin/env bash
set -e

echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
for i in {1..30}; do
  if pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" > /dev/null 2>&1; then
    echo "Postgres is ready"
    break
  fi
  echo -n "."
  sleep 1
done


python -c "import os; print('Using settings:', os.getenv('DJANGO_SETTINGS_MODULE','backend.settings'))"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Compile translations (safe if none exist yet)
# django-admin compilemessages || true

# Start app
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers=3 --timeout=60 --graceful-timeout=30 --log-level=info
