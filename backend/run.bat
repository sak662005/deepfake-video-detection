@echo off
REM Windows batch file to start the development server
REM Set the path to the Python executable (adjust if needed)
set PYTHON=C:\Python314\python.exe

REM If Python is not found at that path, try to find it in PATH
if not exist "%PYTHON%" (
    for /f "delims=" %%i in ('where python.exe') do set PYTHON=%%i
)

echo Starting Deepfake Video Detection API...
echo Python: %PYTHON%
cd /d "%~dp0"
%PYTHON% run.py --reload
pause
