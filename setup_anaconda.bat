@echo off
REM Qwen3-TTS Setup Script for Anaconda (Windows)

echo =========================================
echo   Qwen3-TTS Setup (Anaconda)
echo =========================================
echo.

REM Check if conda is available
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Conda not found!
    echo Please install Anaconda or Miniconda first
    echo Download from: https://www.anaconda.com/download
    echo.
    pause
    exit /b 1
)

echo [INFO] Conda found:
conda --version
echo.

REM Check if environment already exists
conda env list | findstr "qwen3-tts" >nul 2>nul
if %errorlevel% equ 0 (
    echo [WARNING] Environment 'qwen3-tts' already exists
    echo.
    set /p RECREATE="Do you want to remove and recreate it? (y/N): "
    if /i "%RECREATE%"=="y" (
        echo [INFO] Removing existing environment...
        call conda deactivate
        call conda env remove -n qwen3-tts -y
    ) else (
        echo [INFO] Using existing environment
        goto INSTALL_DEPS
    )
)

echo =========================================
echo Step 1: Creating Conda Environment
echo =========================================
echo.
echo [INFO] Creating environment 'qwen3-tts' with Python 3.10...
call conda create -n qwen3-tts python=3.10 -y
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create environment
    pause
    exit /b 1
)
echo [SUCCESS] Environment created
echo.

:INSTALL_DEPS
echo =========================================
echo Step 2: Installing PyTorch
echo =========================================
echo.
echo Select your hardware:
echo   1. NVIDIA GPU with CUDA 11.8
echo   2. NVIDIA GPU with CUDA 12.1
echo   3. CPU Only (slower)
echo.
set /p HARDWARE="Enter choice (1/2/3): "

call conda activate qwen3-tts

if "%HARDWARE%"=="1" (
    echo [INFO] Installing PyTorch with CUDA 11.8...
    call conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y
) else if "%HARDWARE%"=="2" (
    echo [INFO] Installing PyTorch with CUDA 12.1...
    call conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y
) else if "%HARDWARE%"=="3" (
    echo [INFO] Installing PyTorch (CPU only)...
    call conda install pytorch torchvision torchaudio cpuonly -c pytorch -y
) else (
    echo [ERROR] Invalid choice
    pause
    exit /b 1
)

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install PyTorch
    pause
    exit /b 1
)
echo [SUCCESS] PyTorch installed
echo.

echo =========================================
echo Step 3: Installing Dependencies
echo =========================================
echo.
echo [INFO] Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [SUCCESS] Dependencies installed
echo.

echo =========================================
echo Step 4: (Optional) FlashAttention
echo =========================================
echo.
echo FlashAttention improves performance but takes time to compile
echo Only works with NVIDIA GPU
echo.
set /p FLASH="Install FlashAttention? (y/N): "
if /i "%FLASH%"=="y" (
    echo [INFO] Installing FlashAttention (this may take 5-10 minutes)...
    pip install flash-attn --no-build-isolation
    if %errorlevel% neq 0 (
        echo [WARNING] FlashAttention installation failed (optional, can skip)
    ) else (
        echo [SUCCESS] FlashAttention installed
    )
)
echo.

echo =========================================
echo Step 5: Verification
echo =========================================
echo.
echo [INFO] Verifying installation...
echo.

python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA Available:', torch.cuda.is_available())"
python -c "import gradio; print('Gradio:', gradio.__version__)"
python -c "import qwen_tts; print('qwen-tts: OK')"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Verification failed
    pause
    exit /b 1
)

echo.
echo =========================================
echo   Setup Complete!
echo =========================================
echo.
echo To run the GUI:
echo   1. Double-click 'run_gui_anaconda.bat' (Web interface)
echo   2. Double-click 'run_tkinter_anaconda.bat' (Desktop app)
echo.
echo Or from Anaconda Prompt:
echo   conda activate qwen3-tts
echo   python qwen3_tts_gui.py
echo.
echo See ANACONDA_SETUP.md for detailed instructions
echo.
pause
