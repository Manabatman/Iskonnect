@echo off
echo ========================================
echo Starting Iskonnect Backend
echo ========================================
echo.

cd /d "%~dp0"

REM Activate venv
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo Creating virtual environment...
    py -3.11 -m venv venv
    call venv\Scripts\activate
)

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Optional: seed local SQLite demo data (set SEED_LOCAL=1 to enable)
if "%SEED_LOCAL%"=="1" (
    echo Seeding local database...
    python seed_data.py
) else (
    echo Skipping seed_data.py ^(set SEED_LOCAL=1 to seed^).
)

REM Start backend server
echo Starting backend server on http://localhost:8000
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
pause
