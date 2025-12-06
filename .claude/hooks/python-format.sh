#!/bin/bash
# PostToolUse hook: Auto-format Python files after Edit/Write
#
# Receives JSON via stdin with structure:
# { "tool_name": "Edit", "tool_input": { "file_path": "..." }, ... }
#
# Requires: black, isort (pip install black isort)

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

# Exit early if no file path or not a Python file
[[ -z "$file_path" ]] && exit 0
[[ "$file_path" != *.py ]] && exit 0

# Skip generated/cache files
[[ "$file_path" == *__pycache__* ]] && exit 0
[[ "$file_path" == *migrations/0* ]] && exit 0
[[ "$file_path" == *.pyc ]] && exit 0

# Skip virtual environments
[[ "$file_path" == *venv/* ]] && exit 0
[[ "$file_path" == *.venv/* ]] && exit 0
[[ "$file_path" == *env/* ]] && exit 0

# Format the file silently with black and isort
if [[ -f "$file_path" ]]; then
    # Run isort first (import ordering)
    isort --profile black --quiet "$file_path" 2>/dev/null || true

    # Then black (code formatting)
    black --quiet "$file_path" 2>/dev/null || true
fi

exit 0
