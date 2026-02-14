# Qwen3-TTS GUI

A comprehensive graphical user interface for the Qwen3-TTS text-to-speech models.

## Features

🎯 **Custom Voice Mode**
- Use 9 premium predefined voices
- Support for multiple languages and dialects
- Optional style/emotion control via natural language instructions

🎨 **Voice Design Mode**
- Create unique voices from text descriptions
- Design custom character voices
- Control tone, age, gender, and emotional characteristics

🔊 **Voice Clone Mode**
- Clone any voice from a 3-second audio sample
- High-fidelity voice replication
- Support for X-Vector only mode for faster generation

## Quick Start

### For Windows Users with Anaconda (Easiest!)

**🚀 Automated Setup:**
1. Open Anaconda Prompt
2. Navigate to project folder: `cd C:\path\to\QWEN3TTSANO`
3. Run: `setup_anaconda.bat`
4. Follow the prompts
5. Run the GUI: `run_gui_anaconda.bat`

**📖 See `ANACONDA_SETUP.md` for detailed Anaconda instructions**
**📋 See `QUICKSTART_ANACONDA.txt` for quick reference**

---

### For Linux/Mac or Standard Python

#### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd QWEN3TTSANO
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional but recommended) Install FlashAttention for better performance:
```bash
pip install flash-attn --no-build-isolation
```

#### Usage

**Method 1: Direct Python**
```bash
python qwen3_tts_gui.py
```

**Method 2: Using the launcher**
```bash
chmod +x run_gui.sh
./run_gui.sh
```

The GUI will be accessible at `http://localhost:7860`

## System Requirements

### Minimum
- Python 3.8+
- 4GB RAM
- CPU inference supported (slower)

### Recommended
- Python 3.10+
- NVIDIA GPU with 8GB+ VRAM
- CUDA 11.8 or higher
- 16GB RAM

## Model Selection

The GUI supports multiple Qwen3-TTS models:

| Model | Size | Use Case | VRAM |
|-------|------|----------|------|
| Qwen3-TTS-12Hz-1.7B-CustomVoice | 1.7B | Best quality custom voices | ~8GB |
| Qwen3-TTS-12Hz-0.6B-CustomVoice | 0.6B | Faster custom voices | ~4GB |
| Qwen3-TTS-12Hz-1.7B-VoiceDesign | 1.7B | Voice design from descriptions | ~8GB |
| Qwen3-TTS-12Hz-1.7B-Base | 1.7B | Best quality voice cloning | ~8GB |
| Qwen3-TTS-12Hz-0.6B-Base | 0.6B | Faster voice cloning | ~4GB |

## Supported Languages

- Chinese (including Beijing and Sichuan dialects)
- English
- Japanese
- Korean
- German
- French
- Russian
- Portuguese
- Spanish
- Italian

## Available Speakers (Custom Voice Mode)

| Speaker | Description | Native Language |
|---------|-------------|-----------------|
| Vivian | Bright, slightly edgy young female voice | Chinese |
| Serena | Warm, gentle young female voice | Chinese |
| Uncle_Fu | Seasoned male voice with low, mellow timbre | Chinese |
| Dylan | Youthful Beijing male voice | Chinese (Beijing) |
| Eric | Lively Chengdu male voice | Chinese (Sichuan) |
| Ryan | Dynamic male voice with strong rhythmic drive | English |
| Aiden | Sunny American male voice | English |
| Ono_Anna | Playful Japanese female voice | Japanese |
| Sohee | Warm Korean female voice | Korean |

## Tips for Best Results

### Custom Voice Mode
- Use each speaker's native language for best quality
- Keep style instructions concise and clear
- Examples: "angry tone", "very happy", "whisper"

### Voice Design Mode
- Be specific about voice characteristics (age, gender, tone)
- Describe emotional qualities and speaking style
- Include pitch/timbre details if desired
- Example: "A warm, gentle female voice with slight huskiness, age around 30, speaking calmly"

### Voice Clone Mode
- Use clean, noise-free reference audio
- Minimum 3 seconds of reference audio recommended
- Provide accurate transcript for best quality
- Use X-Vector only mode for faster (but lower quality) results

## Troubleshooting

### Model Download Issues
Models are automatically downloaded from Hugging Face. If you're in mainland China, you may want to set:
```bash
export HF_ENDPOINT=https://hf-mirror.com
```

### CUDA Out of Memory
- Try using the 0.6B models instead of 1.7B
- Reduce batch size
- Close other GPU applications
- Use CPU inference (slower)

### Audio Quality Issues
- Ensure reference audio is clear and noise-free
- Check that the language setting matches your text
- Try adjusting the style instructions
- Verify your audio drivers and output device

## Credits

This GUI is built on top of the amazing [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) project by the Alibaba Qwen team.

## License

This project follows the same license as Qwen3-TTS (Apache 2.0).

## Resources

- [Qwen3-TTS GitHub](https://github.com/QwenLM/Qwen3-TTS)
- [Qwen3-TTS Paper](https://arxiv.org/abs/2601.15621)
- [Hugging Face Models](https://huggingface.co/collections/Qwen/qwen3-tts)
- [ModelScope Models](https://modelscope.cn/collections/Qwen/Qwen3-TTS)
