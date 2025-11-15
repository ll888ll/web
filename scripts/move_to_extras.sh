#!/usr/bin/env bash
set -euo pipefail

# Move non‑essential evidence/docs to extras/ preserving relative paths.
# Idempotent. Does not touch proyecto_integrado/** except proyecto_integrado/evidence/**

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
cd "$root_dir"

EXTRAS_DIR="extras"
INDEX_MD="$EXTRAS_DIR/EXTRAS_INDEX.md"
MANIFEST_JSON="$EXTRAS_DIR/EXTRAS_MANIFEST.json"

mkdir -p "$EXTRAS_DIR"

# Essential markdown files to keep in place (root)
declare -a ESSENTIAL_MD=(
  "README.md" "arquitectura.md" "funcionalidades.md" "teoria_aplicada.md"
  "seguridad_y_escalabilidad.md" "uso_y_mantenimiento.md" "integracion.md"
  "integracion_con_croody.md" "integracion_con_croody.md" "integracion*.md"
)

is_essential_md() {
  local rel="$1"
  for pat in "${ESSENTIAL_MD[@]}"; do
    if [[ "$rel" == $pat ]]; then return 0; fi
  done
  return 1
}

# Build candidate list
mapfile -t candidates < <( \
  {
    # Evidence-like directories
    find . -path './extras' -prune -o -path './proyecto_integrado' -prune -o -type d \( -iname 'evidence' -o -iname 'archive_legacy' -o -iname 'archive_legacy*' \) -print;
    # Top-level evidence files and audit results
    find . -path './extras' -prune -o -path './proyecto_integrado' -prune -o -type f \
      \( -iname 'AUDIT_*.txt' -o -iname '*_headers.txt' -o -iname '*_results.txt' \
         -o -iname '*_ready.txt' -o -iname '*_check_*.txt' -o -iname 'loadtest*.txt' \
         -o -iname 'compose_*_config.txt' \) -print;
    # Any evidence folder inside proyecto_integrado explicitly allowed
    find ./proyecto_integrado -path './proyecto_integrado/Croody' -prune -o -path './proyecto_integrado/**/evidence' -type d -print 2>/dev/null || true;
    # Non-essential .md at repo root
    for f in ./*.md; do
      [[ -e "$f" ]] || continue
      rel="${f#./}"
      if ! is_essential_md "$rel"; then
        case "$rel" in
          PLAN_CIERRE.md|READY_FOR_PROD.md|EVIDENCE.md|RELEASE_NOTES.md|CHANGELOG.md|CLEANUP_PLAN.md|DEBT.md)
            printf '%s\n' "$f";;
        esac
      fi
    done
    # Text evidence in root not clearly essential
    find . -maxdepth 1 -type f -name '*.txt' \
      \( -iname 'AUDIT_*.txt' -o -iname '*_config.txt' -o -iname '*_headers.txt' -o -iname '*_results.txt' -o -iname '*_ready.txt' -o -iname '*_check_*.txt' -o -iname 'loadtest*.txt' -o -iname 'compose_*_config.txt' \) -print;
    # Root docker-compose files (non-integrated stack)
    find . -maxdepth 1 -type f -name 'docker-compose*.yml' -print;
    # Non-essential top-level directories (exclude core ones)
    for d in */ ; do
      d=${d%/}
      [[ -z "$d" ]] && continue
      case "$d" in
        extras|proyecto_integrado|.github|scripts|tests|.pytest_cache|.git) continue;;
      esac
      # Move duplicates and coursework-like folders away from root
      printf '%s\n' "$d"
    done
  } | sed 's#^\./##' | sort -u
)

# Initialize index and manifest
{
  echo "# Extras Index"
  echo
  echo "| Original Path | New Path | Size (bytes) | Type |"
  echo "|---|---:|---:|---|"
} > "$INDEX_MD"

echo '{"moved":[' > "$MANIFEST_JSON"
first=1

sha256_of() { sha256sum "$1" 2>/dev/null | awk '{print $1}'; }
mime_of() { file -b --mime-type "$1" 2>/dev/null || echo "unknown"; }

move_one() {
  local src_rel="$1"
  local src="$root_dir/$src_rel"
  local dst_rel="$EXTRAS_DIR/$src_rel"
  local dst_dir
  dst_dir="$(dirname "$dst_rel")"

  # Skip if already under extras
  [[ "$src_rel" == extras/* ]] && return 0

  # Skip most of proyecto_integrado except its evidence dirs
  if [[ "$src_rel" == proyecto_integrado/* ]]; then
    if [[ "$(basename "$src_rel")" != evidence && "$src_rel" != proyecto_integrado/*/evidence* && "$src_rel" != proyecto_integrado/evidence* ]]; then
      return 0
    fi
  fi

  # If it's a directory, move the whole tree
  if [[ -d "$src" ]]; then
    mkdir -p "$dst_dir"
    if [[ ! -e "$dst_rel" ]]; then
      # Fast path: move the whole directory if destination doesn't exist
      mv "$src" "$dst_rel"
      # Index and manifest for the directory itself
      size=0; ftype="dir"
      printf "| %s | %s | %s | %s |\n" "$src_rel" "$dst_rel" "$size" "$ftype" >> "$INDEX_MD"
      if [[ $first -eq 0 ]]; then echo "," >> "$MANIFEST_JSON"; fi
      first=0
      printf '{"original":"%s","new":"%s","size":%s,"sha256":"","type":"%s"}' \
        "$src_rel" "$dst_rel" "$size" "$ftype" >> "$MANIFEST_JSON"
    else
      # Destination exists: attempt rsync to preserve structure and empty source
      if command -v rsync >/dev/null 2>&1; then
        rsync -a --remove-source-files "$src"/ "$dst_rel"/
        # Clean up any empty directories left behind
        find "$src" -type d -empty -delete 2>/dev/null || true
      else
        # Fallback to iterative move
        shopt -s dotglob
        for item in "$src"/*; do
          [[ -e "$item" ]] || continue
          rel_child="${item#$root_dir/}"
          move_one "$rel_child"
        done
        rmdir "$src" 2>/dev/null || true
      fi
      # Index entry for the directory path
      printf "| %s | %s | %s | %s |\n" "$src_rel" "$dst_rel" 0 dir >> "$INDEX_MD"
      if [[ $first -eq 0 ]]; then echo "," >> "$MANIFEST_JSON"; fi
      first=0
      printf '{"original":"%s","new":"%s","size":%s,"sha256":"","type":"dir"}' \
        "$src_rel" "$dst_rel" 0 >> "$MANIFEST_JSON"
    fi
    return 0
  fi

  # If it's a file, move preserving path
  mkdir -p "$dst_dir"
  if [[ ! -e "$dst_rel" ]]; then
    mv "$src" "$dst_rel"
  fi

  # Index row
  size=$(stat -c '%s' "$dst_rel" 2>/dev/null || echo 0)
  ftype=$(mime_of "$dst_rel")
  printf "| %s | %s | %s | %s |\n" "$src_rel" "$dst_rel" "$size" "$ftype" >> "$INDEX_MD"

  # Manifest entry
  sum=$(sha256_of "$dst_rel")
  if [[ $first -eq 0 ]]; then echo "," >> "$MANIFEST_JSON"; fi
  first=0
  printf '{"original":"%s","new":"%s","size":%s,"sha256":"%s","type":"%s"}' \
    "$src_rel" "$dst_rel" "$size" "$sum" "$ftype" >> "$MANIFEST_JSON"
}

for rel in "${candidates[@]}"; do
  [[ -e "$rel" ]] || continue
  move_one "$rel"
done

echo ']}' >> "$MANIFEST_JSON"

echo "Done. Index written to $INDEX_MD"
echo "Manifest written to $MANIFEST_JSON"
