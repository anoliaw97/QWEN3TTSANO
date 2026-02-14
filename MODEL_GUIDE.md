# Qwen3-TTS Model Guide

Quick reference for choosing the right model for your needs.

## 📋 Model Types Overview

Qwen3-TTS has **three different model types**, each designed for specific use cases:

### 1. 🎯 CustomVoice Models
**Files:** `*-CustomVoice`
- ✅ Best for: Quick TTS with pre-made high-quality voices
- ✅ Voices: 9 predefined speakers (Ryan, Vivian, Serena, etc.)
- ✅ Use case: Natural-sounding TTS without providing reference audio
- ✅ GUI Tab: **Custom Voice**

**Available models:**
- `Qwen3-TTS-12Hz-1.7B-CustomVoice` (recommended - better quality)
- `Qwen3-TTS-12Hz-0.6B-CustomVoice` (faster - lower memory)

### 2. 🎨 VoiceDesign Model
**Files:** `*-VoiceDesign`
- ✅ Best for: Creating custom voices from text descriptions
- ✅ Input: Text description of desired voice characteristics
- ✅ Example: "A deep, calm male voice with British accent"
- ✅ GUI Tab: **Voice Design**

**Available models:**
- `Qwen3-TTS-12Hz-1.7B-VoiceDesign` (only this size available)

### 3. 🔊 Base Models (Voice Cloning)
**Files:** `*-Base`
- ✅ Best for: Cloning voices from audio samples
- ✅ Input: 3+ seconds of reference audio + transcript
- ✅ Use case: Replicate a specific person's voice
- ✅ GUI Tab: **Voice Clone**

**Available models:**
- `Qwen3-TTS-12Hz-1.7B-Base` (recommended - better quality)
- `Qwen3-TTS-12Hz-0.6B-Base` (faster - lower memory)

---

## 🎯 Which Model Should I Use?

### For Beginners: Start Here! 👇

**First time using Qwen3-TTS?**
```
✅ Load: Qwen3-TTS-12Hz-1.7B-CustomVoice
✅ Go to: Custom Voice tab
✅ Try: Generate text with "Ryan" or "Vivian" voice
```

This gives you immediate results with high-quality voices!

---

## 📊 Feature Comparison

| Model Type | Predefined Voices | Custom Voice Design | Voice Cloning | Speed | Quality |
|------------|------------------|---------------------|---------------|-------|---------|
| **CustomVoice** | ✅ 9 speakers | ❌ | ❌ | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ |
| **VoiceDesign** | ❌ | ✅ | ❌ | ⚡⚡ | ⭐⭐⭐⭐ |
| **Base** | ❌ | ❌ | ✅ | ⚡⚡ | ⭐⭐⭐⭐⭐ |

---

## 🚫 Common Mistakes

### ❌ Wrong Model for Feature

**Error:** Loading `CustomVoice` model but trying to use Voice Clone tab
```
❌ Error: model does not support generate_voice_clone
```

**Solution:** Load the correct model:
- Voice Clone needs `*-Base` model
- Voice Design needs `*-VoiceDesign` model
- Custom Voice needs `*-CustomVoice` model

### ❌ Model Size Confusion

**1.7B vs 0.6B - What's the difference?**

| Size | Parameters | VRAM | Quality | Speed | When to Use |
|------|-----------|------|---------|-------|-------------|
| **1.7B** | 1.7 billion | ~8GB | ⭐⭐⭐⭐⭐ | ⚡⚡ | Default choice |
| **0.6B** | 0.6 billion | ~4GB | ⭐⭐⭐⭐ | ⚡⚡⚡ | Low VRAM / CPU |

**Recommendation:**
- Have 8GB+ VRAM? → Use **1.7B**
- Have 4-6GB VRAM or using CPU? → Use **0.6B**

---

## 🎭 Available Speakers (CustomVoice Models)

When using **CustomVoice** models, you get these 9 voices:

### English Speakers
1. **Ryan** - Young male, bright, energetic (English)
2. **Chloe** - Young female, bright (English)
3. **Jessica** - Mature female, neutral (English)

### Chinese Speakers
4. **Vivian** - Young female, bright, edgy (Chinese)
5. **Serena** - Young female, warm, gentle (Chinese)
6. **Emily** - Young female, calm, soft (Chinese)
7. **Luna** - Young female, bright, clear (Chinese)
8. **Alice** - Young female, cheerful, energetic (Chinese)
9. **Bella** - Young female, sweet, expressive (Chinese)

---

## 💡 Use Case Examples

### Example 1: Audiobook Narration
**Goal:** Natural-sounding narration in English
```
✅ Model: Qwen3-TTS-12Hz-1.7B-CustomVoice
✅ Tab: Custom Voice
✅ Speaker: Jessica (mature, neutral)
✅ Text: Your book content
```

### Example 2: Clone Your Own Voice
**Goal:** Make AI speak in your voice
```
✅ Model: Qwen3-TTS-12Hz-1.7B-Base
✅ Tab: Voice Clone
✅ Upload: 3+ seconds of your voice
✅ Transcript: What you said in the audio
✅ Text: What you want AI to say
```

### Example 3: Create Unique Character Voice
**Goal:** Design a specific voice for a character
```
✅ Model: Qwen3-TTS-12Hz-1.7B-VoiceDesign
✅ Tab: Voice Design
✅ Instruction: "A deep, mysterious male voice with a slight echo"
✅ Text: Your character's dialogue
```

### Example 4: Multilingual Content
**Goal:** Generate speech in multiple languages
```
✅ Model: Any CustomVoice or Base model
✅ Language: Auto (or specify: en, zh, ja, etc.)
✅ Works with: Chinese, English, Japanese, Korean, and more!
```

---

## 🔄 Switching Models

You can load different models during the same session:

1. Click "🔄 Load Model" with a new selection
2. Wait for download/loading (first time takes longer)
3. Use the appropriate tab for the new model

**Note:** Loading a new model clears the previous one from memory.

---

## 📦 Model Download Sizes

**First-time download sizes** (one-time):

| Model | Download Size | Disk Space |
|-------|--------------|------------|
| 1.7B-CustomVoice | ~6.5 GB | ~7 GB |
| 0.6B-CustomVoice | ~2.5 GB | ~3 GB |
| 1.7B-VoiceDesign | ~6.5 GB | ~7 GB |
| 1.7B-Base | ~6.5 GB | ~7 GB |
| 0.6B-Base | ~2.5 GB | ~3 GB |

Models are cached in `~/.cache/huggingface/hub/` and reused.

---

## 🎯 Quick Decision Tree

```
START
  │
  ├─ Need predefined voices? ──YES──> CustomVoice model
  │                             │      → Use Custom Voice tab
  │                             │
  ├─ Want to design a voice? ──YES──> VoiceDesign model
  │                             │      → Use Voice Design tab
  │                             │
  └─ Want to clone a voice? ────YES──> Base model
                                │      → Use Voice Clone tab
```

---

## 🆘 Troubleshooting

### Model won't load
- Check internet connection (first download)
- Ensure enough disk space (see sizes above)
- Check VRAM/RAM availability

### Wrong model error
- Check which tab you're using
- Load the matching model type
- See the table at the top of this guide

### Out of memory
- Try 0.6B version instead of 1.7B
- Close other GPU applications
- Use CPU mode (slower but works)

---

## 📚 Further Reading

- **README.md** - Full feature documentation
- **ANACONDA_SETUP.md** - Installation guide
- **example_usage.py** - Code examples
- [Qwen3-TTS Official Docs](https://github.com/QwenLM/Qwen3-TTS)

---

**Happy voice generation! 🎵**
