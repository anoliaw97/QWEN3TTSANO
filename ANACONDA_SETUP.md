# Running Qwen3-TTS GUI with Anaconda

Complete guide for running the Qwen3-TTS GUI using Anaconda Prompt on Windows.

## Prerequisites

- Anaconda or Miniconda installed
- NVIDIA GPU with CUDA support (recommended, but CPU works too)
- At least 8GB RAM (16GB recommended)

## Step-by-Step Installation

### 1. Open Anaconda Prompt

- **Windows**: Search for "Anaconda Prompt" in Start Menu
- Run as Administrator (recommended for installing packages)

### 2. Create a New Conda Environment

```bash
# Create a new environment named 'qwen3-tts' with Python 3.10
conda create -n qwen3-tts python=3.10 -y

# Activate the environment
conda activate qwen3-tts
```

### 3. Navigate to Project Directory

```bash
# Replace with your actual path
cd C:\path\to\QWEN3TTSANO

# Or if cloned from GitHub:
# git clone <repository-url>
# cd QWEN3TTSANO
```

### 4. Install PyTorch (Important: Choose correct version)

**For GPU (NVIDIA CUDA 11.8):**
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y
```

**For GPU (NVIDIA CUDA 12.1):**
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y
```

**For CPU Only:**
```bash
conda install pytorch torchvision torchaudio cpuonly -c pytorch -y
```

> **Note**: Check your CUDA version with `nvidia-smi` in command prompt if you have NVIDIA GPU.

### 5. Install Other Dependencies

```bash
pip install -r requirements.txt
```

### 6. (Optional) Install FlashAttention for Better Performance

**Only if you have NVIDIA GPU:**
```bash
pip install flash-attn --no-build-isolation
```

> **Note**: This may take 5-10 minutes to compile. If it fails, you can skip it - the GUI will work without it.

## Running the GUI

### Option 1: Gradio Web Interface (Recommended)

```bash
# Make sure environment is activated
conda activate qwen3-tts

# Run the Gradio GUI
python qwen3_tts_gui.py
```

Then open your browser and go to: **http://localhost:7860**

### Option 2: Tkinter Desktop Application

```bash
# Make sure environment is activated
conda activate qwen3-tts

# Run the Tkinter GUI
python qwen3_tts_gui_tkinter.py
```

A desktop window will open directly.

### Option 3: Use Batch Script (Windows)

Double-click `run_gui_anaconda.bat` (created for you)

## Quick Commands Reference

```bash
# Activate environment
conda activate qwen3-tts

# Run Gradio GUI
python qwen3_tts_gui.py

# Run Tkinter GUI
python qwen3_tts_gui_tkinter.py

# Run examples
python example_usage.py

# Deactivate environment when done
conda deactivate
```

## Verifying Installation

Test if everything is installed correctly:

```bash
conda activate qwen3-tts
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}')"
python -c "import gradio; print(f'Gradio: {gradio.__version__}')"
python -c "import qwen_tts; print('qwen-tts: OK')"
```

Expected output:
```
PyTorch: 2.x.x
CUDA Available: True (or False for CPU)
Gradio: 4.x.x
qwen-tts: OK
```

## Troubleshooting

### Issue: "conda: command not found"
**Solution**: Make sure you're using **Anaconda Prompt**, not regular Command Prompt.

### Issue: CUDA out of memory
**Solutions**:
1. Use the 0.6B model instead of 1.7B
2. Close other GPU applications
3. Use CPU mode (slower but works)

### Issue: "No module named 'qwen_tts'"
**Solution**:
```bash
conda activate qwen3-tts
pip install qwen-tts
```

### Issue: FlashAttention installation fails
**Solution**: This is optional - skip it. The GUI works without it:
```bash
# Just continue without FlashAttention
python qwen3_tts_gui.py
```

### Issue: Slow model download
**Solution**: First-time use downloads ~3-7GB model files. This is normal.
- Use a stable internet connection
- Be patient (may take 10-30 minutes depending on speed)

### Issue: Port 7860 already in use
**Solution**: Change the port in the script or kill the process:
```bash
# Edit qwen3_tts_gui.py, find this line:
# interface.launch(server_port=7860)
# Change to:
# interface.launch(server_port=7861)
```

## Environment Management

### List all conda environments
```bash
conda env list
```

### Remove environment (if needed)
```bash
conda deactivate
conda env remove -n qwen3-tts
```

### Export environment for sharing
```bash
conda activate qwen3-tts
conda env export > environment.yml
```

### Create from exported environment
```bash
conda env create -f environment.yml
```

## Performance Tips

1. **GPU vs CPU**: GPU is 10-50x faster. Use CPU only if no NVIDIA GPU available.

2. **Model Selection**:
   - 1.7B models: Better quality, needs ~8GB VRAM
   - 0.6B models: Faster, needs ~4GB VRAM

3. **First Generation**: First audio generation is slower (model initialization). Subsequent generations are faster.

4. **Batch Processing**: Generate multiple audios in one session for efficiency.

## Next Steps

1. ✅ Environment created and activated
2. ✅ Dependencies installed
3. ✅ GUI launched
4. 🎯 Load a model (1.7B-CustomVoice recommended for first try)
5. 🎵 Generate your first TTS audio!

## Support

- Check `README.md` for detailed feature documentation
- Run `python example_usage.py` to see code examples
- Visit [Qwen3-TTS GitHub](https://github.com/QwenLM/Qwen3-TTS) for official documentation
