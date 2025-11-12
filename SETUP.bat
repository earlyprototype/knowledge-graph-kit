@echo off
REM Knowledge Graph Kit - Windows Setup Launcher
REM Double-click this file to run the setup wizard

echo.
echo ============================================================
echo   Knowledge Graph Kit - Setup Wizard
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

REM Check if PyYAML is installed
python -c "import yaml" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Run setup wizard
python setup_wizard.py

pause

