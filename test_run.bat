@echo off

cd /d "%~dp0"


if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment '.venv' not found in this directory.
    pause
    exit /b
)


echo Starting botmain.py...
".venv\Scripts\python.exe" botmain.py


pause