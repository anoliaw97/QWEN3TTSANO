@echo off
REM Fix Gradio version compatibility issue

echo =========================================
echo   Qwen3-TTS Gradio Update Fix
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

echo [INFO] Activating qwen3-tts environment...
call conda activate qwen3-tts
if %errorlevel% neq 0 (
    echo [ERROR] Environment 'qwen3-tts' not found!
    echo Please create the environment first.
    echo.
    pause
    exit /b 1
)

echo [SUCCESS] Environment activated
echo.
echo [INFO] Current Gradio version:
python -c "import gradio; print('  Gradio version:', gradio.__version__)"
echo.

echo [INFO] Updating Gradio to version 4.20.0 or higher...
pip install --upgrade "gradio>=4.20.0"

if %errorlevel% neq 0 (
    echo [ERROR] Failed to update Gradio
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Gradio updated successfully!
echo.
echo [INFO] New Gradio version:
python -c "import gradio; print('  Gradio version:', gradio.__version__)"
echo.
echo =========================================
echo   Fix Complete!
echo =========================================
echo.
echo You can now run the GUI with:
echo   run_gui_anaconda.bat
echo.
pause
