@echo off
setlocal
cd /d "%~dp0"

".venv\Scripts\python.exe" -m PyInstaller --noconsole --onefile --collect-all discord botmain.py
