#!/bin/bash
# PreToolUse hook: Block editing generated/locked/sensitive files
#
# Receives JSON via stdin with structure:
# { "tool_name": "Edit", "tool_input": { "file_path": "..." }, ... }
#
# Exit codes:
#   0 = Allow operation
#   2 = Block operation (shows stderr to user)

set -euo pipefail

# Read JSON input from stdin
input=$(cat)

# Extract file_path using Python (avoids jq dependency)
file_path=$(echo "$input" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('file_path', ''))
except:
    print('')
" 2>/dev/null)

# Exit early if no file path
[[ -z "$file_path" ]] && exit 0

# Block Django migrations (should be generated, not hand-edited)
if [[ "$file_path" =~ migrations/[0-9]+.*\.py$ ]]; then
    echo "BLOCKED: Cannot edit Django migration files directly" >&2
    echo "  File: $file_path" >&2
    echo "  Fix: Modify models.py and run 'python manage.py makemigrations'" >&2
    exit 2
fi

# Block __pycache__ files
if [[ "$file_path" == *__pycache__* ]]; then
    echo "BLOCKED: Cannot edit Python cache files (__pycache__)" >&2
    echo "  File: $file_path" >&2
    echo "  Fix: These are generated automatically by Python" >&2
    exit 2
fi

# Block .pyc files
if [[ "$file_path" == *.pyc ]]; then
    echo "BLOCKED: Cannot edit compiled Python files (*.pyc)" >&2
    echo "  File: $file_path" >&2
    exit 2
fi

# Block .env files (security - should be edited manually)
if [[ "$file_path" == *.env ]] || [[ "$file_path" == */.env ]]; then
    echo "BLOCKED: Cannot edit .env files via Claude" >&2
    echo "  File: $file_path" >&2
    echo "  Reason: Security - environment files contain secrets" >&2
    echo "  Fix: Edit .env files manually or use .env.example as template" >&2
    exit 2
fi

# Block poetry.lock / requirements.lock (should be generated)
if [[ "$file_path" == *poetry.lock ]] || [[ "$file_path" == *requirements.lock ]]; then
    echo "BLOCKED: Cannot edit lock files directly" >&2
    echo "  File: $file_path" >&2
    echo "  Fix: Modify pyproject.toml/requirements.txt and run 'poetry lock' or 'pip-compile'" >&2
    exit 2
fi

# Block staticfiles collected directory
if [[ "$file_path" == *staticfiles/* ]]; then
    echo "BLOCKED: Cannot edit collected static files" >&2
    echo "  File: $file_path" >&2
    echo "  Fix: Edit source files in static/ and run 'python manage.py collectstatic'" >&2
    exit 2
fi

# Block node_modules (if any frontend tooling)
if [[ "$file_path" == *node_modules/* ]]; then
    echo "BLOCKED: Cannot edit node_modules files" >&2
    echo "  File: $file_path" >&2
    echo "  Fix: Modify package.json and run 'npm install'" >&2
    exit 2
fi

# Block SSL certificates and keys
if [[ "$file_path" =~ \.(pem|key|crt|cer)$ ]]; then
    echo "BLOCKED: Cannot edit SSL certificate/key files" >&2
    echo "  File: $file_path" >&2
    echo "  Reason: Security - certificates should be managed externally" >&2
    exit 2
fi

# Block database files
if [[ "$file_path" == *.sqlite3 ]] || [[ "$file_path" == *.db ]]; then
    echo "BLOCKED: Cannot edit database files directly" >&2
    echo "  File: $file_path" >&2
    echo "  Fix: Use Django ORM or management commands" >&2
    exit 2
fi

# Allow all other files
exit 0
