#!/bin/bash
# Piper TTS Voice Trainer Launcher

echo "========================================="
echo "  Piper TTS Voice Trainer"
echo "========================================="
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "[ERROR] Conda not found!"
    echo "Please install Anaconda or Miniconda first"
    echo ""
    exit 1
fi

echo "[INFO] Checking environment..."

# Check if environment exists
if ! conda env list | grep -q "piper-trainer"; then
    echo "[WARNING] Environment 'piper-trainer' not found!"
    echo ""
    echo "Creating environment..."
    conda create -n piper-trainer python=3.10 -y
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create environment"
        exit 1
    fi

    echo "[INFO] Installing dependencies..."
    source activate piper-trainer
    pip install sounddevice soundfile numpy tk
    echo ""
    echo "[INFO] Environment created!"
    echo ""
    echo "NOTE: To enable training, you need to install Piper from source:"
    echo "  1. git clone https://github.com/rhasspy/piper.git"
    echo "  2. cd piper/src/python"
    echo "  3. pip install -e ."
    echo "  4. pip install torch torchaudio onnx onnxruntime"
    echo ""
    echo "For now, you can use the GUI for dataset management and recording."
    echo ""
fi

# Activate environment
echo "[INFO] Activating piper-trainer environment..."
source activate piper-trainer || conda activate piper-trainer

# Check if dependencies are installed
python -c "import sounddevice" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[INFO] Installing dependencies..."
    pip install sounddevice soundfile numpy
fi

echo "[SUCCESS] Environment ready"
echo ""
echo "========================================="
echo "Starting Piper Voice Trainer GUI..."
echo "========================================="
echo ""

# Run the GUI
python piper_trainer_gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to start GUI"
    echo ""
    echo "Make sure you are in the correct directory."
fi
