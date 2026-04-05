@echo off
REM Alterix Quick Installation Script for Windows
REM This script sets up both backend and frontend

echo.
echo Starting Alterix Installation...
echo.

REM Check Python
echo Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    exit /b 1
)
echo Python found

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed
    exit /b 1
)
echo Node.js found

echo.
echo Setting up Backend...
cd backend

REM Create virtual environment
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt --quiet

REM Check for .env file
if not exist ".env" (
    echo WARNING: .env file not found
    if exist ".env.example" (
        echo Creating .env from .env.example...
        copy .env.example .env
        echo WARNING: Please edit backend\.env with your configuration
    ) else (
        echo ERROR: .env.example not found
    )
)

echo Backend setup complete
cd ..

echo.
echo Setting up Frontend...
cd frontend

REM Install dependencies
echo Installing Node.js dependencies...
call npm install --silent

REM Check for .env.local file
if not exist ".env.local" (
    echo WARNING: .env.local file not found
    if exist ".env.local.example" (
        echo Creating .env.local from .env.local.example...
        copy .env.local.example .env.local
        echo WARNING: Please edit frontend\.env.local with your configuration
    ) else (
        echo ERROR: .env.local.example not found
    )
)

echo Frontend setup complete
cd ..

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Configure backend\.env with your Supabase and API keys
echo 2. Configure frontend\.env.local with your API URL
echo 3. Set up your database schema (see SETUP_GUIDE.md)
echo.
echo To start the application:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   .venv\Scripts\activate
echo   uvicorn app.main:app --reload
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then visit: http://localhost:3000
echo.
pause
