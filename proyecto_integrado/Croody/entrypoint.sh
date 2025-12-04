#!/bin/bash
set -e

# ========================================
# ENTRYPOINT SCRIPT - Development
# ========================================

echo "Starting Croody development server..."

# Wait for database to be ready (if using external DB)
if [ -n "$DATABASE_URL" ] || [ -n "$DB_HOST" ]; then
    echo "Waiting for database..."
    while ! python -c "
import os
import sys
try:
    import django
    django.setup()
    from django.db import connection
    connection.ensure_connection()
    print('Database ready!')
except Exception as e:
    print(f'Database not ready: {e}')
    sys.exit(1)
" 2>/dev/null; do
        echo "Database unavailable - sleeping"
        sleep 2
    done
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Compile messages
echo "Compiling translations..."
python manage.py compilemessages || true

# Create superuser if credentials provided
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput || true
fi

echo "Starting development server..."
exec "$@"
