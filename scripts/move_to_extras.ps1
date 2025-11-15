#!/usr/bin/env pwsh
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Move non-essential evidence/docs to extras/ preserving relative paths.
# Idempotent. Does not touch proyecto_integrado/** except proyecto_integrado/evidence/**

Start-Transcript -Path "extras/move_to_extras.transcript.txt" -Append -ErrorAction SilentlyContinue | Out-Null

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

$extras = Join-Path $Root 'extras'
New-Item -ItemType Directory -Path $extras -Force | Out-Null

$indexMd = Join-Path $extras 'EXTRAS_INDEX.md'
$manifestJson = Join-Path $extras 'EXTRAS_MANIFEST.json'

$essentialMd = @(
  'README.md','arquitectura.md','funcionalidades.md','teoria_aplicada.md',
  'seguridad_y_escalabilidad.md','uso_y_mantenimiento.md','integracion.md',
  'integracion_con_croody.md','integracion*.md'
)

function Is-EssentialMd([string]$rel) {
  foreach ($pat in $essentialMd) {
    if ($rel -like $pat) { return $true }
  }
  return $false
}

$candidates = New-Object System.Collections.Generic.List[string]

# Evidence-like directories
Get-ChildItem -Recurse -Directory -Name | Where-Object {
  $_ -notlike 'extras*' -and $_ -notlike 'proyecto_integrado*' -and (
    (Split-Path $_ -Leaf) -like 'evidence' -or (Split-Path $_ -Leaf) -like 'archive_legacy*'
  )
} | ForEach-Object { $candidates.Add($_) }

# Evidence-like files at root
Get-ChildItem -File -Name | Where-Object {
  $_ -like 'AUDIT_*.txt' -or $_ -like '*_headers.txt' -or $_ -like '*_results.txt' -or $_ -like '*_ready.txt' -or $_ -like '*_check_*.txt' -or $_ -like 'loadtest*.txt' -or $_ -like 'compose_*_config.txt'
} | ForEach-Object { $candidates.Add($_) }

# Root docker-compose files (non-integrated stack)
Get-ChildItem -File -Name 'docker-compose*.yml' | ForEach-Object { $candidates.Add($_.ToString()) }

# Non essential md at root
Get-ChildItem -File -Name *.md | ForEach-Object {
  if (-not (Is-EssentialMd $_)) {
    if ($_ -in @('PLAN_CIERRE.md','READY_FOR_PROD.md','EVIDENCE.md','RELEASE_NOTES.md','CHANGELOG.md','CLEANUP_PLAN.md','DEBT.md')) {
      $candidates.Add($_)
    }
  }
}

# evidence inside proyecto_integrado explicitly allowed
Get-ChildItem -Recurse -Directory proyecto_integrado 2>$null | Where-Object {
  $_.FullName -notlike '*\\Croody*' -and $_.Name -like 'evidence*'
} | ForEach-Object { $candidates.Add($_.FullName.Substring($Root.Length+1)) }

# Prepare index
@(
  '# Extras Index','',
  '| Original Path | New Path | Size (bytes) | Type |',
  '|---|---:|---:|---|'
) | Set-Content -Encoding UTF8 $indexMd

$manifest = [System.Collections.Generic.List[object]]::new()

function Add-ManifestEntry($original, $newPath) {
  $fi = Get-Item $newPath -Force
  $size = if ($fi -is [System.IO.FileInfo]) { $fi.Length } else { 0 }
  $type = if ($fi -is [System.IO.FileInfo]) { (Get-Content -Raw $newPath | Out-Null; 'file') } else { 'dir' }
  $sha256 = if ($fi -is [System.IO.FileInfo]) {
    (Get-FileHash -Algorithm SHA256 $newPath).Hash.ToLower()
  } else { '' }
  $manifest.Add([pscustomobject]@{ original=$original; new=$newPath; size=$size; sha256=$sha256; type=$type }) | Out-Null
  $row = "| $original | $newPath | $size | $type |"
  Add-Content -Encoding UTF8 -Path $indexMd -Value $row
}

foreach ($rel in ($candidates | Sort-Object -Unique)) {
  if (-not (Test-Path $rel)) { continue }
  if ($rel -like 'extras*') { continue }
  if ($rel -like 'proyecto_integrado*') {
    if ($rel -notlike 'proyecto_integrado*evidence*') { continue }
  }
  $src = Join-Path $Root $rel
  $dst = Join-Path $extras $rel
  $dstDir = Split-Path -Parent $dst
  New-Item -ItemType Directory -Path $dstDir -Force | Out-Null

  if (Test-Path $src -PathType Container) {
    # Move dir contents
    New-Item -ItemType Directory -Path $dst -Force | Out-Null
    Get-ChildItem -Force $src | ForEach-Object {
      Move-Item -Force $_.FullName (Join-Path $dst $_.Name)
    }
    try { Remove-Item -Force -Recurse $src } catch {}
  } else {
    if (-not (Test-Path $dst)) { Move-Item -Force $src $dst }
  }
  Add-ManifestEntry $rel $dst
}

$manifest | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 $manifestJson

Write-Host "Done. Index written to $indexMd"
Write-Host "Manifest written to $manifestJson"

Stop-Transcript | Out-Null
# Prepare index
# Add non-essential top-level directories (exclude core ones)
Get-ChildItem -Directory -Name | ForEach-Object {
  switch -Wildcard ($_) {
    'extras' { break }
    'proyecto_integrado' { break }
    '.github' { break }
    'scripts' { break }
    'tests' { break }
    '.pytest_cache' { break }
    '.git' { break }
    default { $candidates.Add($_) }
  }
}

# Prepare index
