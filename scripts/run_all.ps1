#!/usr/bin/env pwsh
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location (Join-Path $Root 'proyecto_integrado')

$results = Join-Path $Root 'extras/quick_smoke_results.txt'
New-Item -ItemType Directory -Path (Split-Path $results -Parent) -Force | Out-Null
"# Quick smoke run ($(Get-Date -Format o))" | Set-Content -Encoding UTF8 $results

"[check] docker version" | Tee-Object -FilePath $results -Append
docker --version | Tee-Object -FilePath $results -Append

"[check] docker compose version" | Tee-Object -FilePath $results -Append
docker compose version | Tee-Object -FilePath $results -Append

"[up] dev compose (8080/8443)" | Tee-Object -FilePath $results -Append
docker compose up -d --build | Tee-Object -FilePath $results -Append

"[smoke] GET http://localhost:8080/ -> status" | Tee-Object -FilePath $results -Append
try {
  $resp = (Invoke-WebRequest -UseBasicParsing -Uri 'http://localhost:8080/' -Method Head -ErrorAction Stop)
  $code = [int]$resp.StatusCode
} catch {
  $code = 0
}
"dev_status=$code" | Tee-Object -FilePath $results -Append

"[smoke] docs via gateway" | Tee-Object -FilePath $results -Append
try { (Invoke-WebRequest -UseBasicParsing 'http://localhost:8080/api/telemetry/docs').StatusCode | ForEach-Object { "telemetry_docs=$_" } | Tee-Object -FilePath $results -Append } catch {}
try { (Invoke-WebRequest -UseBasicParsing 'http://localhost:8080/api/ids/docs').StatusCode | ForEach-Object { "ids_docs=$_" } | Tee-Object -FilePath $results -Append } catch {}

if (Test-Path '.env') {
  "[up] prod local (80/443)" | Tee-Object -FilePath $results -Append
  docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env up -d --build | Tee-Object -FilePath $results -Append

  "[smoke-prod] HEAD https://localhost/ (insecure)" | Tee-Object -FilePath $results -Append
  try { (curl.exe -k -I https://localhost/) | Tee-Object -FilePath $results -Append } catch {}
}

"[ps] containers" | Tee-Object -FilePath $results -Append
docker compose ps | Tee-Object -FilePath $results -Append

Write-Host "Done. Results at $results"

