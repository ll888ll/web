#!/bin/bash
set -euo pipefail

SRC_DIRS=("/etc/apache2" "/var/www/html")
DEST_BASE="/var/backups/web"
STAMP=$(date '+%F')
DEST="$DEST_BASE/$STAMP"
LOG_FILE="/var/log/backup_web.log"
RETENTION_DAYS=14

mkdir -p "$DEST" "$(dirname "$LOG_FILE")"

for src in "${SRC_DIRS[@]}"; do
    rsync -a --delete "$src" "$DEST" >> "$LOG_FILE" 2>&1
done

echo "$(date '+%F %T'): Backup completado en $DEST" >> "$LOG_FILE"
find "$DEST_BASE" -mindepth 1 -maxdepth 1 -type d -mtime +$RETENTION_DAYS -exec rm -rf {} +
