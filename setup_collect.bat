@echo off
setlocal

echo ============================================
echo  SLT - Data Collection Setup (Windows)
echo ============================================
echo.

REM ── Check Python version ──────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo         Download Python 3.10+ from https://www.python.org/downloads/
    echo         Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo Found Python %PYVER%

REM ── Create virtual environment ────────────────────────────
if not exist "venv_collect" (
    echo.
    echo Creating virtual environment...
    python -m venv venv_collect
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo Virtual environment already exists, skipping creation.
)

REM ── Activate and install dependencies ─────────────────────
echo.
echo Installing dependencies...
call venv_collect\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements_collect.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Setup complete! Running data collection...
echo ============================================
echo.

REM ── Run the script ────────────────────────────────────────
python src\collect_data.py

echo.
echo Done.
pause
