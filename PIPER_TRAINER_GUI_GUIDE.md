## Piper TTS Voice Trainer GUI - User Guide

Complete guide to using the Piper Voice Trainer GUI application.

---

## 🎯 **Overview**

The Piper Voice Trainer GUI is a comprehensive graphical application that makes training custom Piper TTS voices easy and intuitive.

**Features:**
- 📁 Project management and organization
- 🎤 Built-in audio recording
- 📝 Dataset management and validation
- ⚙️ One-click preprocessing
- 🏋️ Training launcher with live monitoring
- 📦 ONNX model export

---

## 🚀 **Quick Start**

### Installation

```bash
# Create environment
conda create -n piper-trainer python=3.10 -y
conda activate piper-trainer

# Install dependencies
pip install piper-tts sounddevice soundfile numpy

# For training (install Piper from source)
git clone https://github.com/rhasspy/piper.git
cd piper/src/python
pip install -e .

# Install training dependencies
pip install torch torchaudio onnx onnxruntime
```

### Launch the GUI

```bash
python piper_trainer_gui.py
```

---

## 📖 **Step-by-Step Tutorial**

### Step 1: Create a New Project

1. Click **File → New Project**
2. Enter a project name (e.g., "MyCustomVoice")
3. Select a location to save the project
4. Click OK

**Result:** A project folder is created with this structure:
```
MyCustomVoice/
├── project.json          # Project configuration
├── dataset/
│   ├── wavs/            # Audio files go here
│   └── metadata.csv     # Transcripts
└── (preprocessed/)      # Created during preprocessing
```

---

### Step 2: Build Your Dataset

You have **three options** for creating your dataset:

#### Option A: Import Existing Audio Files

**Best for:** If you already have recorded audio

1. Go to **📁 Dataset** tab
2. Click **Import Audio Files** (for individual files)
   - OR **Import Folder** (for a whole directory)
3. Select your .wav files
4. Files are copied to the project

**Requirements:**
- Format: WAV
- Sample rate: 22050 Hz (will be converted if different)
- Channels: Mono
- Duration: 2-15 seconds per file (recommended)

#### Option B: Record Audio in the GUI

**Best for:** Recording from scratch

1. Go to **🎤 Record** tab
2. In the text box, enter the sentence to record
3. Click **🔴 Start Recording**
4. Speak clearly into your microphone
5. Click **⏹️ Stop Recording** when done
6. Click **▶️ Play** to review
7. Click **💾 Save** to add to dataset

**Tips:**
- Speak naturally and clearly
- Record in a quiet environment
- Use a good quality microphone
- Maintain consistent distance from mic
- Record 30+ minutes minimum for basic quality

#### Option C: Batch Recording with Sentence List

**Best for:** Systematic recording of many sentences

1. Create a text file with one sentence per line:
   ```
   The quick brown fox jumps over the lazy dog.
   Machine learning is transforming technology.
   Artificial intelligence helps solve complex problems.
   ...
   ```

2. In **🎤 Record** tab, click **Load Sentence List**
3. Select your sentence file
4. Select a sentence from the list
5. Click "Use Selected Sentence"
6. Record, review, and save
7. Repeat for all sentences

---

### Step 3: Add Transcripts

For imported files without transcripts:

1. Go to **📁 Dataset** tab
2. Double-click any file in the list
3. A dialog opens
4. Type the exact text that was spoken in the audio
5. Click **Save**

**Important:** Transcripts must be accurate! The model learns from these.

---

### Step 4: Validate Your Dataset

Before training, check your audio quality:

1. In **📁 Dataset** tab, click **Validate Audio**
2. The validator checks:
   - ✅ File exists
   - ✅ Sample rate is 22050 Hz
   - ✅ Audio is mono
   - ✅ Duration is reasonable (2-15 seconds)
3. Fix any issues reported

---

### Step 5: Preprocess the Dataset

Preprocessing prepares your audio for training:

1. Go to **⚙️ Preprocess** tab
2. Configure settings:
   - **Language**: en-us (or your language)
   - **Sample Rate**: 22050 (default)
   - **Max WAV Value**: 32768 (default)
   - **Single Speaker**: ✅ (recommended for custom voices)
3. Click **▶️ Run Preprocessing**
4. Wait for completion (shown in the log)

**What it does:**
- Normalizes audio levels
- Extracts phonemes and features
- Creates training-ready data

**Time:** 1-5 minutes depending on dataset size

---

### Step 6: Train Your Voice Model

Now the exciting part!

1. Go to **🏋️ Train** tab
2. Configure training settings:
   - **Epochs**: 1000 (recommended)
   - **Batch Size**: 32 (or 16 if low on VRAM)
   - **Learning Rate**: 0.0001 (default)
   - **Checkpoint Every**: 100 epochs
   - **Validation Split**: 0.05 (5%)
3. Click **▶️ Start Training**

**Training Time Estimates:**

| Dataset Size | GPU | Time |
|-------------|-----|------|
| 30 min | RTX 3060 | 4-8 hours |
| 1 hour | RTX 3060 | 12-24 hours |
| 5 hours | RTX 3060 | 2-5 days |
| 30 min | CPU only | 12-24 hours |

**Monitoring:**
- Watch the training log for progress
- Loss should decrease over time
- Training loss ~1-2 is good
- You can stop early if loss plateaus

**Checkpoints:**
- Saved every 100 epochs by default
- Located in `preprocessed/checkpoints/`
- You can resume training from any checkpoint

---

### Step 7: Export Your Model

Convert the trained model to ONNX for use in applications:

1. Go to **📦 Export** tab
2. Click **Browse** next to "Checkpoint"
3. Select a checkpoint file (e.g., `checkpoint_1000.ckpt`)
   - Usually located in `preprocessed/checkpoints/`
4. Click **Browse** next to "Output"
5. Choose where to save (e.g., `my_voice.onnx`)
6. Click **📦 Export to ONNX**
7. Wait for export to complete

**Result:**
- `my_voice.onnx` - Your trained voice model (15-50 MB)
- `my_voice.onnx.json` - Configuration file

**You can now use this model in any Piper TTS application!**

---

## 🎓 **Best Practices**

### For Best Voice Quality

1. **Data Quality:**
   - 📌 Clear, noise-free recordings
   - 📌 Consistent audio levels
   - 📌 Natural speech patterns
   - 📌 No background music or noise
   - 📌 Good microphone quality

2. **Data Quantity:**
   - 📌 Minimum: 30 minutes (basic quality)
   - 📌 Recommended: 1-3 hours (good quality)
   - 📌 Ideal: 5-10 hours (excellent quality)
   - 📌 More data = better quality

3. **Data Diversity:**
   - 📌 Variety of sentences
   - 📌 Different sentence lengths
   - 📌 Various punctuation and intonations
   - 📌 Cover common words and sounds

4. **Recording Environment:**
   - 📌 Quiet room
   - 📌 Soft furnishings (reduce echo)
   - 📌 Consistent distance from microphone
   - 📌 Same equipment throughout

5. **Training Settings:**
   - 📌 Start with defaults
   - 📌 Train for 1000+ epochs minimum
   - 📌 Monitor loss - should decrease steadily
   - 📌 Use validation to check overfitting

---

## 🔧 **Troubleshooting**

### Recording Issues

**Problem:** No microphone detected
```
Solution:
1. Check microphone is connected
2. Select correct input device in system settings
3. Install: pip install sounddevice soundfile
```

**Problem:** Poor audio quality
```
Solution:
1. Use a better microphone
2. Record in a quiet room
3. Add soft materials to reduce echo
4. Check recording levels (not too loud/quiet)
```

### Dataset Issues

**Problem:** "Not mono audio" error
```
Solution:
1. Convert audio to mono using:
   ffmpeg -i input.wav -ac 1 output.wav
2. Or use audacity: Tracks → Stereo to Mono
```

**Problem:** "Wrong sample rate" warning
```
Solution:
1. Convert to 22050 Hz:
   ffmpeg -i input.wav -ar 22050 output.wav
2. Preprocessing will handle this automatically
```

**Problem:** Audio too long/short
```
Solution:
1. Ideal: 2-15 seconds per clip
2. Split longer audio into shorter clips
3. Combine very short clips if needed
```

### Training Issues

**Problem:** Training is very slow
```
Solution:
1. Use a GPU (CUDA-capable NVIDIA card)
2. Reduce batch size if out of memory
3. Use fewer training samples for testing
4. Be patient - training takes time!
```

**Problem:** Loss not decreasing
```
Solution:
1. Check data quality
2. Ensure transcripts are accurate
3. Try lower learning rate (0.00005)
4. Train for more epochs
5. Add more training data
```

**Problem:** Out of memory error
```
Solution:
1. Reduce batch size (try 16 or 8)
2. Close other GPU applications
3. Use CPU training (slower)
4. Use smaller dataset for testing
```

### Export Issues

**Problem:** "Cannot find checkpoint"
```
Solution:
1. Make sure training completed
2. Check preprocessed/checkpoints/ folder
3. Select the right checkpoint file (.ckpt or .pt)
```

**Problem:** Export fails
```
Solution:
1. Install: pip install onnx onnxruntime
2. Make sure checkpoint is from completed training
3. Check export log for specific errors
```

---

## 📊 **Understanding Training Metrics**

### What to Look For

**Training Loss:**
- Starts high (~8-10)
- Should decrease steadily
- Target: ~1-2 for good quality
- If stuck high: check data quality

**Validation Loss:**
- Should track training loss
- If much higher: overfitting
- Solution: more data or early stopping

**Checkpoints:**
- Saved periodically (every 100 epochs default)
- Each is a snapshot of the model
- You can test different checkpoints
- Usually the latest is best

---

## 💡 **Tips and Tricks**

### Efficient Recording

1. **Use a script:** Prepare sentences beforehand
2. **Batch record:** Do many in one session
3. **Stay consistent:** Same time of day, same energy level
4. **Take breaks:** Vocal fatigue affects quality
5. **Review later:** Listen to all recordings before training

### Dataset Organization

1. **Start small:** Test with 10-20 clips first
2. **Validate early:** Check quality before recording more
3. **Backup:** Keep original recordings separate
4. **Document:** Note recording conditions

### Training Strategy

1. **Test run:** Train on small dataset first (100 clips)
2. **Quick validation:** Export after 500 epochs to test
3. **Full training:** Once satisfied, train on full dataset
4. **Multiple checkpoints:** Test different epochs (800, 900, 1000)
5. **Fine-tune:** Adjust based on results

---

## 📚 **Example Workflow**

### Complete Project Timeline

**Day 1: Setup and Recording**
1. Create project (5 min)
2. Prepare sentence list (30 min)
3. Record audio (2-4 hours for 1-2 hours of audio)
4. Validate dataset (10 min)

**Day 2: Preprocessing and Training Start**
1. Review and fix any audio issues (30 min)
2. Add/verify transcripts (1 hour)
3. Run preprocessing (5 min)
4. Start training (5 min to setup)

**Days 3-5: Training**
1. Monitor training progress
2. Let it run (12 hours - 5 days depending on data)

**Day 6: Export and Testing**
1. Export model (5 min)
2. Test in Piper TTS app
3. Generate sample audio
4. Evaluate quality

**If needed: Iteration**
1. Record more data for weak areas
2. Retrain with expanded dataset
3. Compare results

---

## 🎯 **Success Checklist**

Before training:
- ✅ 30+ minutes of audio (1+ hour recommended)
- ✅ All audio is 22050 Hz, mono, WAV
- ✅ Transcripts are accurate and complete
- ✅ Audio quality validated
- ✅ Preprocessing completed successfully

During training:
- ✅ Loss is decreasing
- ✅ No error messages
- ✅ Checkpoints being saved
- ✅ Enough disk space for checkpoints

After training:
- ✅ Training completed (or loss plateaued)
- ✅ Model exported to ONNX
- ✅ Both .onnx and .onnx.json files created
- ✅ Model tested and sounds good

---

## 🚀 **Next Steps After Training**

Once you have your ONNX model:

1. **Test it:**
   ```bash
   echo "Hello, this is my custom voice" | \
       piper --model my_voice.onnx --output test.wav
   ```

2. **Use in applications:**
   - Load in `piper_app_example.py`
   - Bundle with your software
   - Distribute to users

3. **Share:**
   - Share with community (if permitted)
   - Contribute to Piper voice library
   - Help others learn

4. **Iterate:**
   - Record more data for weak sounds
   - Retrain for better quality
   - Create variations (different styles)

---

## 📞 **Getting Help**

**Resources:**
- Piper GitHub: https://github.com/rhasspy/piper
- Training docs: https://github.com/rhasspy/piper/blob/master/TRAINING.md
- Community: Piper Discord/Forums

**Common Questions:**
- Check PIPER_APP_GUIDE.md for detailed training info
- See PIPER_VS_QWEN3_COMPARISON.md for alternatives
- Refer to Piper's official documentation

---

## 🎉 **Congratulations!**

You now have a powerful tool for creating custom TTS voices!

**Remember:**
- Quality data = quality voice
- Patience is key (training takes time)
- Iterate and improve
- Share your success!

**Happy voice training!** 🎙️
