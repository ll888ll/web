#!/usr/bin/env bash
set -euo pipefail

cd /app

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn croody.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers ${GUNICORN_WORKERS:-3} \
  --threads ${GUNICORN_THREADS:-4} \
  --timeout ${GUNICORN_TIMEOUT:-60}

