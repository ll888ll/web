#!/bin/bash
set -e

# ========================================
# ENTRYPOINT SCRIPT - Production (ECS/Fargate)
# ========================================

echo "=== Croody Production Startup ==="
echo "Environment: PRODUCTION"
echo "Django Settings: ${DJANGO_SETTINGS_MODULE}"

# Function to wait for database
wait_for_db() {
    local max_attempts=30
    local attempt=1

    echo "Waiting for database connection..."

    while [ $attempt -le $max_attempts ]; do
        if python -c "
import django
django.setup()
from django.db import connection
try:
    connection.ensure_connection()
    print('Database connection successful!')
    exit(0)
except Exception as e:
    print(f'Attempt failed: {e}')
    exit(1)
" 2>/dev/null; then
            return 0
        fi

        echo "Database unavailable - attempt $attempt/$max_attempts - sleeping 3s"
        sleep 3
        attempt=$((attempt + 1))
    done

    echo "ERROR: Could not connect to database after $max_attempts attempts"
    exit 1
}

# Function to run Django checks
run_checks() {
    echo "Running Django system checks..."
    python manage.py check --deploy || {
        echo "WARNING: Some deployment checks failed. Review the output above."
    }
}

# Function to run migrations safely
run_migrations() {
    echo "Running database migrations..."
    python manage.py migrate --noinput

    if [ $? -ne 0 ]; then
        echo "ERROR: Migrations failed!"
        exit 1
    fi
    echo "Migrations completed successfully."
}

# Function to collect static files
collect_static() {
    echo "Collecting static files..."
    python manage.py collectstatic --noinput --clear

    if [ $? -ne 0 ]; then
        echo "WARNING: Static file collection had issues."
    fi
    echo "Static files collected."
}

# Function to compile translations
compile_messages() {
    echo "Compiling translation messages..."
    python manage.py compilemessages 2>/dev/null || {
        echo "INFO: Message compilation skipped or had warnings."
    }
}

# Main execution
main() {
    # Wait for database
    wait_for_db

    # Run deployment checks
    run_checks

    # Run migrations (only if not explicitly disabled)
    if [ "${SKIP_MIGRATIONS}" != "true" ]; then
        run_migrations
    else
        echo "Skipping migrations (SKIP_MIGRATIONS=true)"
    fi

    # Collect static files
    collect_static

    # Compile translations
    compile_messages

    echo "=== Startup complete. Launching application... ==="

    # Execute the main command (gunicorn)
    exec "$@"
}

# Run main function
main "$@"
