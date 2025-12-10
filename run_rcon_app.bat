@echo off
REM Activate venv and run the RCON monitor Flask app

REM Change to project directory
cd /d %~dp0

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run your app (adjust filename if needed)
python rcon_app.py

REM Keep window open if something goes wrong
pause