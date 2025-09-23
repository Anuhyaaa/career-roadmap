@echo off
echo Starting Career Roadmap Generator Backend...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Start the Flask application
echo.
echo Starting Flask server...
echo Server will be available at: http://localhost:5000
echo.
python main.py

pause