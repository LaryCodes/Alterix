# Alterix Frontend Startup Script

Write-Host "🎨 Starting Alterix Frontend..." -ForegroundColor Cyan

# Check if node_modules exists
if (-Not (Test-Path "frontend\node_modules")) {
    Write-Host "❌ Dependencies not installed!" -ForegroundColor Red
    Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
    Set-Location ..
}

# Start the frontend server
Write-Host "Starting Next.js server on http://localhost:3000..." -ForegroundColor Green
Set-Location frontend
npm run dev
