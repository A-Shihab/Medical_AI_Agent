@echo off
REM Medical AI Agent - Quick Start Script for Windows

echo ======================================
echo 🧠 Medical AI Agent - Quick Start
echo ======================================
echo.

REM Check Python installation
echo ✓ Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo   Found Python %PYTHON_VERSION%

REM Create virtual environment
echo.
echo ✓ Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo   Virtual environment created
) else (
    echo   Virtual environment already exists
)

REM Activate virtual environment
echo.
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo ✓ Installing dependencies...
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo   Dependencies installed

REM Check .env file
echo.
echo ✓ Checking configuration...
if not exist ".env" (
    echo   ⚠️  .env file not found
    echo   Creating from template...
    copy .env.template .env
    echo.
    echo   🔑 IMPORTANT: Edit .env file and add your API keys:
    echo      - OPENAI_API_KEY
    echo      - TAVILY_API_KEY
    echo      - KAGGLE_USERNAME
    echo      - KAGGLE_KEY
    echo.
    echo   Then run this script again.
    pause
    exit /b 0
) else (
    echo   .env file found
)

REM Check Kaggle credentials
echo.
echo ✓ Checking Kaggle credentials...
if not exist "%USERPROFILE%\.kaggle\kaggle.json" (
    echo   ⚠️  Kaggle credentials not found
    echo   Please place kaggle.json in %USERPROFILE%\.kaggle\
    echo   Get it from: https://www.kaggle.com/settings/account
    pause
    exit /b 1
) else (
    echo   Kaggle credentials found
)

REM All checks passed
echo.
echo ======================================
echo ✅ Setup Complete!
echo ======================================
echo.
echo Choose how to run:
echo.
echo Option 1 - Jupyter Notebook (Interactive):
echo   jupyter notebook medical_ai_agent.ipynb
echo.
echo Option 2 - Python Script (Direct):
echo   python medical_agent.py
echo.
echo Option 3 - Gradio Only (Web Interface):
echo   python -c "from medical_agent import *; demo = create_gradio_interface(initialize_system()); demo.launch()"
echo.
pause
