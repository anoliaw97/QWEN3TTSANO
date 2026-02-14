#!/bin/bash

# Qwen3-TTS GUI Launcher Script

echo "========================================="
echo "  Qwen3-TTS GUI Launcher"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if qwen-tts is installed
if ! python3 -c "import qwen_tts" 2>/dev/null; then
    echo "⚠️  Warning: qwen-tts package not found"
    echo "Installing required packages..."
    pip install -r requirements.txt
else
    echo "✅ qwen-tts package is installed"
fi

echo ""
echo "🚀 Starting Qwen3-TTS GUI..."
echo "The interface will be available at: http://localhost:7860"
echo "Press Ctrl+C to stop the server"
echo ""

# Launch the GUI
python3 qwen3_tts_gui.py
