# Creating an Installable App with Piper TTS

Complete guide to building a standalone TTS application with custom Piper voices.

---

## 🎯 **Overview**

This guide shows you how to:
1. ✅ Train a custom Piper voice (or use pre-trained)
2. ✅ Create a Python TTS application
3. ✅ Package it as a standalone installer
4. ✅ Distribute to users (Windows/Mac/Linux)

**Result:** A professional installable app with your custom voice! 🚀

---

## 📋 **Prerequisites**

```bash
# Python 3.10 or 3.11
# Conda or Python venv
# Basic Python knowledge
# Your voice recordings (optional, for custom voice)
```

---

## 🚀 **Quick Start: Using Pre-trained Voices**

### Step 1: Install Piper

```bash
# Create environment
conda create -n piper-app python=3.10 -y
conda activate piper-app

# Install Piper TTS
pip install piper-tts
```

### Step 2: Download a Voice Model

Visit: https://github.com/rhasspy/piper/releases

Download a voice (e.g., `en_US-lessac-medium.onnx`):

```bash
# Download voice and config
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx.json
```

### Step 3: Test the Voice

```bash
# Quick test
echo "Hello world" | piper --model en_US-lessac-medium.onnx --output_file test.wav
```

### Step 4: Run the Example App

```bash
# Use the app we created
python piper_app_example.py
```

**Now you have a working TTS app!** ✅

---

## 🎓 **Advanced: Training Custom Voice**

### Prerequisites for Training

```bash
Hardware:
- CPU: Multi-core (8+ cores recommended)
- RAM: 16 GB minimum, 32 GB recommended
- GPU: Optional (CUDA-capable, speeds up 3-5x)
- Storage: 50-100 GB free

Data Requirements:
- Minimum: 30 minutes clean audio
- Recommended: 1-3 hours
- Ideal: 5-10 hours
- Format: WAV, mono, 22050 Hz
- Quality: No background noise, clear speech
```

### Step 1: Setup Training Environment

```bash
# Create training environment
conda create -n piper-training python=3.10 -y
conda activate piper-training

# Install dependencies
git clone https://github.com/rhasspy/piper.git
cd piper

# Install training tools
pip install -e src/python
pip install onnx onnxruntime
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118  # For CUDA 11.8
# OR for CPU only:
# pip install torch torchaudio
```

### Step 2: Prepare Your Dataset

**Option A: Use piper-sample-generator (Recommended)**

```bash
# Install sample generator
pip install piper-sample-generator

# This tool helps you:
# 1. Record audio systematically
# 2. Transcribe automatically
# 3. Validate quality
# 4. Generate metadata

piper-sample-generator --help
```

**Option B: Prepare Manually**

Create this structure:

```
my_voice_dataset/
├── metadata.csv
├── wavs/
│   ├── audio_0001.wav
│   ├── audio_0002.wav
│   ├── ...
│   └── audio_1000.wav
└── config.json
```

**metadata.csv:**
```csv
audio_0001|This is the first sentence with clear pronunciation.
audio_0002|Another sentence to train the voice model.
audio_0003|Make sure audio quality is consistent throughout.
```

**config.json:**
```json
{
  "audio": {
    "sample_rate": 22050,
    "channels": 1
  },
  "dataset": "my_custom_voice",
  "language": {
    "code": "en-us",
    "family": "en",
    "region": "US"
  }
}
```

**Audio Requirements:**
```python
# Use this script to validate your audio files
import soundfile as sf
import os

def validate_audio(filepath):
    data, sr = sf.read(filepath)

    # Check sample rate
    if sr != 22050:
        print(f"⚠️  {filepath}: Wrong sample rate {sr}, should be 22050")
        return False

    # Check duration (2-15 seconds recommended)
    duration = len(data) / sr
    if duration < 2 or duration > 15:
        print(f"⚠️  {filepath}: Duration {duration:.1f}s not ideal (want 2-15s)")
        return False

    # Check if mono
    if len(data.shape) > 1:
        print(f"⚠️  {filepath}: Not mono audio")
        return False

    print(f"✓ {filepath}: OK ({duration:.1f}s)")
    return True

# Validate all files
for filename in os.listdir("my_voice_dataset/wavs"):
    if filename.endswith(".wav"):
        validate_audio(f"my_voice_dataset/wavs/{filename}")
```

### Step 3: Preprocess Dataset

```bash
cd piper/src/python

# Preprocess for training
python -m piper_train.preprocess \
    --language en-us \
    --input-dir /path/to/my_voice_dataset/wavs \
    --output-dir /path/to/preprocessed \
    --sample-rate 22050 \
    --max-wav-value 32768
```

### Step 4: Train the Model

```bash
# Train (this takes time!)
python -m piper_train \
    --dataset-dir /path/to/preprocessed \
    --checkpoint-epochs 100 \
    --epochs 1000 \
    --validation-split 0.05 \
    --batch-size 32 \
    --learning-rate 0.0001

# Training time estimates:
# - 30 min audio + GPU: 4-8 hours
# - 1 hour audio + GPU: 12-24 hours
# - 5 hours audio + GPU: 2-5 days
# - CPU only: 3-5x longer
```

**Monitor training:**
```bash
# Check logs
tail -f training.log

# Look for decreasing loss values
# Training loss should go from ~8-10 down to ~1-2
```

### Step 5: Export to ONNX

```bash
# After training completes
python -m piper_train.export_onnx \
    --checkpoint checkpoints/checkpoint_1000.ckpt \
    --output my_custom_voice.onnx \
    --output-json my_custom_voice.onnx.json
```

**Result:**
- `my_custom_voice.onnx` (15-50 MB) - The voice model
- `my_custom_voice.onnx.json` - Configuration file

### Step 6: Test Your Voice

```bash
# Test immediately
echo "This is my custom voice!" | \
    piper --model my_custom_voice.onnx \
    --output_file test_custom.wav

# Listen to test_custom.wav
```

---

## 📦 **Packaging as Installable App**

Now let's turn your app into a distributable installer!

### Method 1: PyInstaller (Windows/Mac/Linux)

```bash
# Install PyInstaller
pip install pyinstaller

# Create standalone executable
pyinstaller --name "MyTTS" \
    --onefile \
    --windowed \
    --add-data "my_custom_voice.onnx:." \
    --add-data "my_custom_voice.onnx.json:." \
    --icon app_icon.ico \
    piper_app_example.py

# Result: dist/MyTTS.exe (Windows) or dist/MyTTS (Linux/Mac)
```

**Folder structure for PyInstaller:**
```
project/
├── piper_app_example.py
├── my_custom_voice.onnx
├── my_custom_voice.onnx.json
├── app_icon.ico
└── requirements.txt
```

**Build on each platform:**
- Windows → MyTTS.exe
- macOS → MyTTS.app
- Linux → MyTTS binary

### Method 2: Inno Setup (Windows Installer)

```bash
# Install Inno Setup from https://jrsoftware.org/isinfo.php

# Create installer script (setup.iss):
```

**setup.iss:**
```ini
[Setup]
AppName=My Custom TTS
AppVersion=1.0
DefaultDirName={pf}\MyTTS
DefaultGroupName=My Custom TTS
OutputDir=installers
OutputBaseFilename=MyTTS_Setup

[Files]
Source: "dist\MyTTS.exe"; DestDir: "{app}"
Source: "my_custom_voice.onnx"; DestDir: "{app}"
Source: "my_custom_voice.onnx.json"; DestDir: "{app}"

[Icons]
Name: "{group}\My Custom TTS"; Filename: "{app}\MyTTS.exe"
Name: "{commondesktop}\My Custom TTS"; Filename: "{app}\MyTTS.exe"
```

Compile with Inno Setup → Get `MyTTS_Setup.exe`!

### Method 3: Electron (Cross-platform, Modern UI)

For web-based UI wrapped as desktop app:

```bash
# Create Electron wrapper
npm install -g electron-packager

# Build for Windows
electron-packager . MyTTS --platform=win32 --arch=x64

# Build for macOS
electron-packager . MyTTS --platform=darwin --arch=x64

# Build for Linux
electron-packager . MyTTS --platform=linux --arch=x64
```

---

## 🎨 **Enhanced App with Better UI**

Here's a more advanced version with Gradio (web-based UI):

```python
# piper_app_gradio.py
import gradio as gr
from piper import PiperVoice
import wave
import tempfile

class PiperTTSApp:
    def __init__(self, model_path):
        self.voice = PiperVoice.load(model_path)

    def generate(self, text):
        """Generate speech from text"""
        if not text.strip():
            return None, "Please enter text"

        try:
            # Generate to temp file
            temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            with wave.open(temp_file.name, "wb") as wav_file:
                self.voice.synthesize(text, wav_file)

            return temp_file.name, "✓ Speech generated!"
        except Exception as e:
            return None, f"Error: {str(e)}"

# Initialize app
app = PiperTTSApp("my_custom_voice.onnx")

# Create Gradio interface
interface = gr.Interface(
    fn=app.generate,
    inputs=gr.Textbox(
        label="Text to Speak",
        placeholder="Enter text here...",
        lines=5
    ),
    outputs=[
        gr.Audio(label="Generated Speech"),
        gr.Textbox(label="Status")
    ],
    title="🎙️ My Custom TTS",
    description="Professional text-to-speech with custom voice",
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    interface.launch()
```

This creates a beautiful web interface that can be packaged!

---

## 📊 **Comparison: Distribution Methods**

| Method | Size | Ease | Cross-Platform | UI Quality |
|--------|------|------|----------------|------------|
| **PyInstaller** | ~100 MB | ⭐⭐⭐ | ✅ | Basic |
| **Inno Setup** | ~100 MB | ⭐⭐ | ❌ Windows only | Basic |
| **Electron** | ~200 MB | ⭐⭐⭐⭐ | ✅ | Beautiful |
| **Gradio + PyInstaller** | ~150 MB | ⭐⭐⭐⭐⭐ | ✅ | Modern web UI |

**Recommendation:** Gradio + PyInstaller for best results! 🏆

---

## 🔒 **Protecting Your Custom Voice**

If your custom voice is proprietary:

### Option 1: Encrypt the Model

```python
from cryptography.fernet import Fernet

# Generate key (keep secret!)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt model
with open("my_custom_voice.onnx", "rb") as f:
    encrypted = cipher.encrypt(f.read())

with open("my_custom_voice.onnx.encrypted", "wb") as f:
    f.write(encrypted)

# In app, decrypt before loading
with open("my_custom_voice.onnx.encrypted", "rb") as f:
    encrypted_data = f.read()

decrypted_data = cipher.decrypt(encrypted_data)
# Load from decrypted bytes
```

### Option 2: License Keys

```python
# Simple license validation
def check_license(license_key):
    valid_licenses = load_valid_licenses()  # From server or embedded
    return license_key in valid_licenses

if not check_license(user_license):
    show_activation_dialog()
```

---

## 📦 **Complete Build Process**

Here's the full workflow:

```bash
# 1. Train or download voice
python -m piper_train ...
# OR
wget https://github.com/rhasspy/piper/releases/download/.../voice.onnx

# 2. Create your app
# (use piper_app_example.py or piper_app_gradio.py)

# 3. Test locally
python piper_app_gradio.py

# 4. Install packaging tools
pip install pyinstaller

# 5. Bundle everything
pyinstaller --onefile --windowed \
    --add-data "my_custom_voice.onnx:." \
    --add-data "my_custom_voice.onnx.json:." \
    --name "MyTTS" \
    piper_app_gradio.py

# 6. Test executable
./dist/MyTTS

# 7. Create installer (Windows)
iscc setup.iss

# 8. Distribute!
# Result: MyTTS_Setup.exe ready to ship!
```

---

## 💰 **Commercial Considerations**

### Licensing

**Piper TTS:**
- ✅ MIT License - use commercially
- ✅ Can modify and distribute
- ✅ No attribution required (but appreciated)

**Your voice:**
- ✅ You own the voice model you train
- ✅ Can license however you want
- ⚠️  Ensure voice actor consents if using someone else's voice

### Distribution

You can:
- ✅ Sell your app commercially
- ✅ Bundle with proprietary software
- ✅ Offer as SaaS
- ✅ Include in commercial products

---

## 🎯 **Example Use Cases**

### 1. Accessibility App
```
Custom voice for visually impaired users
- Screen reader with personalized voice
- Portable, offline capability
```

### 2. Audiobook Creator
```
Convert ebooks to audiobooks with consistent voice
- Batch processing
- Save as MP3/M4B
```

### 3. Language Learning
```
Pronunciation practice with native voice
- Custom word lists
- Repetition exercises
```

### 4. Brand Voice Assistant
```
Company's branded TTS voice
- Support chatbots
- IVR systems
- Product demos
```

---

## 🆘 **Troubleshooting**

### Training Issues

**Problem:** Training loss not decreasing
```
Solution:
- Check audio quality (no noise)
- Ensure consistent volume levels
- Verify transcripts are accurate
- Try lower learning rate (0.00005)
```

**Problem:** Model sounds robotic
```
Solution:
- Train longer (more epochs)
- Add more training data
- Check audio sample rate (must be 22050 Hz)
- Ensure natural speech patterns in data
```

### Packaging Issues

**Problem:** PyInstaller can't find modules
```
Solution:
- Use --hidden-import flag
- Add all dependencies to spec file
- Use --collect-all piper
```

**Problem:** Large executable size
```
Solution:
- Use --exclude-module for unused packages
- Don't include development tools
- Compress with UPX (use carefully)
```

---

## 📚 **Resources**

- **Piper GitHub**: https://github.com/rhasspy/piper
- **Pre-trained voices**: https://rhasspy.github.io/piper-samples/
- **Training guide**: https://github.com/rhasspy/piper/blob/master/TRAINING.md
- **PyInstaller docs**: https://pyinstaller.org/
- **Inno Setup**: https://jrsoftware.org/isinfo.php

---

## 🎉 **Next Steps**

1. ✅ Choose: Use pre-trained voice or train custom?
2. ✅ Test: Run `piper_app_example.py`
3. ✅ Customize: Modify UI, add features
4. ✅ Package: Build with PyInstaller
5. ✅ Distribute: Share your TTS app!

**You now have everything needed to create a professional TTS app!** 🚀
