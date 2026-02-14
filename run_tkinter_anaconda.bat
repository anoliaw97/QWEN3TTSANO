@echo off
REM Qwen3-TTS Tkinter GUI Launcher for Anaconda (Windows)

echo =========================================
echo   Qwen3-TTS Tkinter GUI (Anaconda)
echo =========================================
echo.

REM Check if conda is available
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Conda not found!
    echo Please run this script from Anaconda Prompt
    echo.
    pause
    exit /b 1
)

echo [INFO] Conda found
echo.

REM Activate environment
echo [INFO] Activating qwen3-tts environment...
call conda activate qwen3-tts
if %errorlevel% neq 0 (
    echo [ERROR] Environment 'qwen3-tts' not found!
    echo.
    echo Please create the environment first:
    echo   conda create -n qwen3-tts python=3.10 -y
    echo   conda activate qwen3-tts
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [SUCCESS] Environment activated
echo.

REM Check if qwen-tts is installed
python -c "import qwen_tts" >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] qwen-tts package not found
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [INFO] All dependencies found
echo.
echo =========================================
echo Starting Qwen3-TTS Desktop GUI...
echo =========================================
echo.

REM Run the Tkinter GUI
python qwen3_tts_gui_tkinter.py

pause
