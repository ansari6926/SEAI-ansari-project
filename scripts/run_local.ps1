$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"
$Backend = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"

Set-Location $Root

if (-not (Test-Path (Join-Path $Root ".venv"))) {
    python -m venv (Join-Path $Root ".venv")
}

$Python -m pip install --upgrade pip
$Python -m pip install -r (Join-Path $Backend "requirements.txt")

Start-Process -WindowStyle Hidden -FilePath $Python -ArgumentList "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" -WorkingDirectory $Backend
Start-Process -WindowStyle Hidden -FilePath "python" -ArgumentList "-m", "http.server", "3000" -WorkingDirectory $Frontend

Write-Host "RoadSense AI is running."
Write-Host "Frontend: http://localhost:3000"
Write-Host "Backend API: http://localhost:8000/docs"
