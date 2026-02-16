@echo off
setlocal
cd /d "%~dp0"


if not exist ".venv\" (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
)

echo [INFO] Updating dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if exist "requirements.txt" (
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
)


echo.
echo ----------------------------------------------------
echo  Do you want to run a TEST or perform a FINAL BUILD?
echo  [Y] Run test_run.bat
echo  [N] Build EXE (PyInstaller)
echo ----------------------------------------------------
echo.

choice /c YN /m "Select your option:"


if errorlevel 2 goto BUILD
if errorlevel 1 goto TEST

:TEST
echo [ACTION] Starting test_run.bat...
call test_run.bat
goto END

:BUILD
echo [ACTION] Installing PyInstaller in .venv...
".venv\Scripts\python.exe" -m pip install pyinstaller

echo [ACTION] Starting PyInstaller build...
".venv\Scripts\python.exe" -m PyInstaller --noconsole --one-file --collect-all discord botmain.py

if %errorlevel% equ 0 (
    echo [SUCCESS] Build complete! Check the /dist folder.
) else (
    echo [ERROR] Build failed.
)
goto END

:END
pause