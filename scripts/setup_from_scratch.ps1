#!/usr/bin/env pwsh
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# End-to-end setup on Windows: installs Docker Desktop + Git (via winget),
# clones repo, prepares .env, brings up dev and prod, and performs basic tests.

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

$LogDir = Join-Path $Root 'extras'
$Cmds = Join-Path $LogDir 'manual_commands_windows.txt'
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null

function Log-Cmd($text) { Add-Content -Encoding UTF8 -Path $Cmds -Value $text }
function Run($text) { Log-Cmd $text; Invoke-Expression $text }

# 1) Ensure WSL2 and Docker Desktop
if (-not (Get-Command wsl -ErrorAction SilentlyContinue)) {
  Log-Cmd '# Install/enable WSL2'
  Run 'wsl --install'
  Run 'wsl --set-default-version 2'
}

if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
  Write-Host 'winget not found. Please install Apps Installer from Microsoft Store.' -ForegroundColor Yellow
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Log-Cmd '# Install Git via winget'
  Run 'winget install -e --id Git.Git -h'
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  Log-Cmd '# Install Docker Desktop via winget'
  Run 'winget install -e --id Docker.DockerDesktop -h'
  Write-Host 'Please login once and enable WSL2 backend in Docker Desktop if prompted.' -ForegroundColor Yellow
}

# 2) Clone repo if needed
if (-not (Test-Path '.git')) {
  $GIT_URL = $env:GIT_URL
  if (-not $GIT_URL) { $GIT_URL = 'https://example.com/your/repo.git' }
  Log-Cmd "# Clone repository"
  Run "git clone $GIT_URL repo"
  Set-Location repo
}

# 3) Prepare .env
Set-Location (Join-Path (Get-Location) 'proyecto_integrado')
if (-not (Test-Path '.env')) {
  Log-Cmd '# Prepare .env from sample'
  Run 'Copy-Item .env.production.sample .env'
  (Get-Content .env) -replace '^ENV=.*','ENV=production' | Set-Content .env
  (Get-Content .env) -replace '^ALLOWED_HOSTS=.*','ALLOWED_HOSTS=localhost' | Set-Content .env
  $secret = [Convert]::ToBase64String([byte[]](1..64 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
  Log-Cmd 'SECRET_KEY=***generated***'
  (Get-Content .env) -replace '^SECRET_KEY=.*',"SECRET_KEY=$secret" | Set-Content .env
}

# 4) Bring up dev
Log-Cmd '# Bring up dev compose (8080/8443)'
Run 'docker compose up -d --build'

# 5) Smoke tests (dev)
Log-Cmd '# Smoke test dev homepage'
try { (curl.exe -I http://localhost:8080/) | Tee-Object -FilePath ../extras/smoke_dev.txt -Append } catch {}
Log-Cmd '# Docs endpoints'
try { (Invoke-WebRequest -UseBasicParsing 'http://localhost:8080/api/telemetry/docs').StatusCode | ForEach-Object { "telemetry_docs=$_" } | Tee-Object -FilePath ../extras/smoke_dev.txt -Append } catch {}
try { (Invoke-WebRequest -UseBasicParsing 'http://localhost:8080/api/ids/docs').StatusCode | ForEach-Object { "ids_docs=$_" } | Tee-Object -FilePath ../extras/smoke_dev.txt -Append } catch {}

# 6) Bring up prod (ports 80/443)
Log-Cmd '# Bring up prod local'
Run 'docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env up -d --build'
Log-Cmd '# Smoke test prod homepage https'
try { (curl.exe -k -I https://localhost/) | Tee-Object -FilePath ../extras/smoke_prod.txt -Append } catch {}

Write-Host "Commands recorded in $Cmds"

