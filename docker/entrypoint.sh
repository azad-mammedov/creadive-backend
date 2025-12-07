#!/usr/bin/env bash
set -e


python -c "import os; print('Using settings:', os.getenv('DJANGO_SETTINGS_MODULE','backend.settings'))"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Compile translations (safe if none exist yet)
# django-admin compilemessages || true

# Start app
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers=3 --timeout=60 --graceful-timeout=30 --log-level=info
