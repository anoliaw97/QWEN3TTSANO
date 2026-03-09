@echo off
REM Piper TTS Voice Trainer Launcher

echo =========================================
echo   Piper TTS Voice Trainer
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

echo [INFO] Checking environment...

REM Check if environment exists
conda env list | findstr "piper-trainer" >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Environment 'piper-trainer' not found!
    echo.
    echo Creating environment...
    call conda create -n piper-trainer python=3.10 -y
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create environment
        pause
        exit /b 1
    )

    echo [INFO] Installing dependencies...
    call conda activate piper-trainer
    pip install sounddevice soundfile numpy tk
    echo.
    echo [INFO] Environment created!
    echo.
    echo NOTE: To enable training, you need to install Piper from source:
    echo   1. git clone https://github.com/rhasspy/piper.git
    echo   2. cd piper/src/python
    echo   3. pip install -e .
    echo   4. pip install torch torchaudio onnx onnxruntime
    echo.
    echo For now, you can use the GUI for dataset management and recording.
    echo.
)

REM Activate environment
echo [INFO] Activating piper-trainer environment...
call conda activate piper-trainer

REM Check if dependencies are installed
python -c "import sounddevice" >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Installing dependencies...
    pip install sounddevice soundfile numpy
)

echo [SUCCESS] Environment ready
echo.
echo =========================================
echo Starting Piper Voice Trainer GUI...
echo =========================================
echo.

REM Run the GUI
python piper_trainer_gui.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to start GUI
    echo.
    echo Make sure you are in the correct directory.
    pause
)
