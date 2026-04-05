# Alterix Backend Startup Script

Write-Host "🚀 Starting Alterix Backend..." -ForegroundColor Cyan

# Check if virtual environment exists
if (-Not (Test-Path "backend\.venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    Set-Location backend
    uv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
    
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    uv pip install -r requirements.txt
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
    Set-Location ..
}

# Start the backend server
Write-Host "Starting FastAPI server on http://localhost:8000..." -ForegroundColor Green
Set-Location backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
