# Start Backend Server
# This script uses the parent directory's venv to avoid reinstalling heavy dependencies

Write-Host "Starting Resume ATS API Backend..." -ForegroundColor Green

# Check if parent venv exists
$parentVenv = "..\venv"
if (Test-Path $parentVenv) {
    Write-Host "Using parent virtual environment..." -ForegroundColor Cyan
    & "$parentVenv\Scripts\Activate.ps1"
} else {
    Write-Host "Warning: Parent venv not found. Using current environment..." -ForegroundColor Yellow
}

# Install only FastAPI if not already installed
$fastapi = python -c "import fastapi" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing FastAPI and dependencies..." -ForegroundColor Cyan
    pip install fastapi uvicorn[standard] python-multipart python-dotenv toml firebase-admin
}

# Start server
Write-Host "`nServer starting at http://localhost:8000" -ForegroundColor Green
Write-Host "API Docs: http://localhost:8000/docs`n" -ForegroundColor Cyan

python start_server.py
