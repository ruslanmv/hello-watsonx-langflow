@echo off
REM ============================================================================
REM LangFlow + watsonx.ai Demo - Windows Batch Script
REM ============================================================================
REM 
REM This batch file provides convenient commands for Windows users.
REM Alternative to run.sh for systems without Git Bash.
REM
REM Usage:
REM   run.bat install    - Install dependencies
REM   run.bat setup      - Setup environment
REM   run.bat demo       - Run interactive demo
REM   run.bat ui         - Start LangFlow UI
REM   run.bat help       - Show help
REM
REM ============================================================================

setlocal enabledelayedexpansion

REM Colors (limited in cmd, but we can use different formatting)
set "HEADER=======================================================================
"

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="setup" goto setup
if "%1"=="demo" goto demo
if "%1"=="simple" goto simple
if "%1"=="ui" goto ui
if "%1"=="test" goto test
if "%1"=="version" goto version
if "%1"=="clean" goto clean

echo Unknown command: %1
echo.
goto help

:help
echo %HEADER%
echo   LangFlow + watsonx.ai Demo - Windows Commands
echo %HEADER%
echo.
echo Installation Commands:
echo   run.bat install      Install all required dependencies
echo   run.bat setup        Setup environment variables
echo.
echo Running Commands:
echo   run.bat demo         Run interactive chat demo
echo   run.bat simple       Run simple demo
echo   run.bat ui           Start LangFlow UI (http://localhost:7860)
echo.
echo Testing:
echo   run.bat test         Test watsonx.ai connection
echo.
echo Utility:
echo   run.bat version      Show version information
echo   run.bat clean        Clean temporary files
echo   run.bat help         Show this help message
echo.
echo Quick Start:
echo   1. run.bat install   ^# Install dependencies
echo   2. run.bat setup     ^# Configure credentials
echo   3. run.bat demo      ^# Start chatting!
echo.
echo Examples:
echo   run.bat install ^&^& run.bat setup ^&^& run.bat demo
echo   run.bat test
echo   run.bat ui
echo.
echo %HEADER%
goto end

:install
echo %HEADER%
echo   Installing Dependencies
echo %HEADER%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.11 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    goto end
)

echo Checking Python version...
python --version
echo.

REM Check if virtual environment exists
if exist venv (
    echo Virtual environment already exists.
    echo Using existing virtual environment.
) else (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        goto end
    )
    echo Virtual environment created successfully!
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies!
    echo Try running as Administrator or check your internet connection.
    goto end
)

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo To activate the environment manually:
echo   venv\Scripts\activate.bat
echo.
echo Next steps:
echo   1. run.bat setup     ^# Configure credentials
echo   2. run.bat demo      ^# Start chatting
echo.
goto end

:setup
echo %HEADER%
echo   Environment Setup
echo %HEADER%
echo.

if exist .env (
    echo .env file already exists.
    set /p "overwrite=Do you want to overwrite it? (y/N): "
    if /i not "!overwrite!"=="y" (
        echo Keeping existing .env file.
        goto end
    )
)

echo.
echo Creating .env file...
echo.
echo Please enter your IBM watsonx.ai credentials:
echo.

set /p "api_key=Enter your IBM Cloud API Key: "
set /p "project_id=Enter your watsonx.ai Project ID: "

echo.
echo Select your region:
echo   1) US South (Dallas) - https://us-south.ml.cloud.ibm.com
echo   2) EU (Frankfurt) - https://eu-de.ml.cloud.ibm.com
echo   3) UK (London) - https://eu-gb.ml.cloud.ibm.com
echo   4) Japan (Tokyo) - https://jp-tok.ml.cloud.ibm.com
echo   5) Australia (Sydney) - https://au-syd.ml.cloud.ibm.com
echo.
set /p "region=Enter choice (1-5) [1]: "

if "%region%"=="" set region=1
if "%region%"=="1" set "url=https://us-south.ml.cloud.ibm.com"
if "%region%"=="2" set "url=https://eu-de.ml.cloud.ibm.com"
if "%region%"=="3" set "url=https://eu-gb.ml.cloud.ibm.com"
if "%region%"=="4" set "url=https://jp-tok.ml.cloud.ibm.com"
if "%region%"=="5" set "url=https://au-syd.ml.cloud.ibm.com"

REM Create .env file
(
echo # IBM watsonx.ai Configuration
echo WATSONX_APIKEY=%api_key%
echo WATSONX_URL=%url%
echo WATSONX_PROJECT_ID=%project_id%
echo.
echo # Optional: Model Configuration
echo DEFAULT_MODEL=ibm/granite-3-8b-instruct
echo TEMPERATURE=0.7
echo MAX_TOKENS=1000
echo.
echo # Optional: LangFlow Configuration
echo LANGFLOW_PORT=7860
echo LANGFLOW_HOST=0.0.0.0
) > .env

echo.
echo ========================================
echo .env file created successfully!
echo ========================================
echo.
echo Your credentials have been saved to .env
echo.
echo IMPORTANT: Add .env to your .gitignore!
echo.
goto end

:demo
echo %HEADER%
echo   Running Interactive Demo
echo %HEADER%
echo.

if not exist .env (
    echo ERROR: .env file not found!
    echo.
    echo Please run: run.bat setup
    goto end
)

if not exist venv (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run: run.bat install
    goto end
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting interactive demo...
echo.
python agent_langflow.py

goto end

:simple
echo %HEADER%
echo   Running Simple Demo
echo %HEADER%
echo.

if not exist .env (
    echo ERROR: .env file not found!
    echo Please run: run.bat setup
    goto end
)

if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run: run.bat install
    goto end
)

call venv\Scripts\activate.bat
python agent_langflow.py --simple

goto end

:ui
echo %HEADER%
echo   Starting LangFlow UI
echo %HEADER%
echo.
echo LangFlow UI will start at http://localhost:7860
echo Press Ctrl+C to stop the server
echo.

if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run: run.bat install
    goto end
)

call venv\Scripts\activate.bat
langflow run

goto end

:test
echo %HEADER%
echo   Testing watsonx.ai Connection
echo %HEADER%
echo.

if not exist .env (
    echo ERROR: .env file not found!
    echo Please run: run.bat setup
    goto end
)

if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run: run.bat install
    goto end
)

call venv\Scripts\activate.bat
echo Testing connection...
python agent_langflow.py --simple

goto end

:version
echo %HEADER%
echo   Version Information
echo %HEADER%
echo.

echo Python version:
python --version
echo.

if exist venv (
    call venv\Scripts\activate.bat
    
    echo Checking installed packages...
    echo.
    
    pip show langflow 2>nul | findstr "Name Version" || echo LangFlow: Not installed
    pip show langchain-ibm 2>nul | findstr "Name Version" || echo langchain-ibm: Not installed
    pip show python-dotenv 2>nul | findstr "Name Version" || echo python-dotenv: Not installed
) else (
    echo Virtual environment not created yet.
    echo Run: run.bat install
)

echo.
goto end

:clean
echo %HEADER%
echo   Cleaning Temporary Files
echo %HEADER%
echo.

echo Removing temporary files...

if exist __pycache__ rmdir /s /q __pycache__ 2>nul
if exist .pytest_cache rmdir /s /q .pytest_cache 2>nul
if exist .mypy_cache rmdir /s /q .mypy_cache 2>nul
if exist htmlcov rmdir /s /q htmlcov 2>nul
if exist build rmdir /s /q build 2>nul
if exist dist rmdir /s /q dist 2>nul
if exist *.egg-info rmdir /s /q *.egg-info 2>nul
del /q .coverage 2>nul
del /q *.pyc 2>nul

echo.
echo Cleaned!
goto end

:end
endlocal
