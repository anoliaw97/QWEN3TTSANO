#!/usr/bin/env python3
"""
Qwen3-TTS Example Usage
Simple examples demonstrating the three main TTS modes
"""

import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel


def example_custom_voice():
    """Example: Generate speech with custom voice"""
    print("=" * 60)
    print("Example 1: Custom Voice")
    print("=" * 60)

    # Load model
    print("Loading CustomVoice model...")
    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
        device_map="cuda:0" if torch.cuda.is_available() else "cpu",
        dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
    )

    # Generate speech
    print("Generating speech...")
    wavs, sr = model.generate_custom_voice(
        text="Hello! This is a demonstration of Qwen3-TTS custom voice.",
        language="English",
        speaker="Ryan",
        instruct="Speak with enthusiasm",
    )

    # Save audio
    output_file = "example_custom_voice.wav"
    sf.write(output_file, wavs[0], sr)
    print(f"✅ Audio saved to: {output_file}")
    print(f"   Duration: {len(wavs[0])/sr:.2f}s")
    print()


def example_voice_design():
    """Example: Generate speech with voice design"""
    print("=" * 60)
    print("Example 2: Voice Design")
    print("=" * 60)

    # Load model
    print("Loading VoiceDesign model...")
    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
        device_map="cuda:0" if torch.cuda.is_available() else "cpu",
        dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
    )

    # Generate speech
    print("Generating speech with custom voice design...")
    wavs, sr = model.generate_voice_design(
        text="This is an example of voice design with Qwen3-TTS.",
        language="English",
        instruct="A warm, friendly female voice, age around 25, speaking cheerfully",
    )

    # Save audio
    output_file = "example_voice_design.wav"
    sf.write(output_file, wavs[0], sr)
    print(f"✅ Audio saved to: {output_file}")
    print(f"   Duration: {len(wavs[0])/sr:.2f}s")
    print()


def example_voice_clone():
    """Example: Generate speech with voice clone"""
    print("=" * 60)
    print("Example 3: Voice Clone")
    print("=" * 60)

    # Load model
    print("Loading Base model for voice cloning...")
    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
        device_map="cuda:0" if torch.cuda.is_available() else "cpu",
        dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
    )

    # Use a reference audio URL (or provide your own file path)
    ref_audio = "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-TTS-Repo/clone.wav"
    ref_text = "Okay. Yeah. I resent you. I love you. I respect you. But you know what? You blew it! And thanks to you."

    # Generate speech
    print("Generating speech with cloned voice...")
    wavs, sr = model.generate_voice_clone(
        text="This is a demonstration of voice cloning with Qwen3-TTS.",
        language="English",
        ref_audio=ref_audio,
        ref_text=ref_text,
    )

    # Save audio
    output_file = "example_voice_clone.wav"
    sf.write(output_file, wavs[0], sr)
    print(f"✅ Audio saved to: {output_file}")
    print(f"   Duration: {len(wavs[0])/sr:.2f}s")
    print()


def main():
    """Run all examples"""
    print("\n🎙️  Qwen3-TTS Example Usage\n")
    print("This script demonstrates the three main TTS modes.")
    print("Note: Models will be downloaded on first run.\n")

    try:
        # Run examples
        example_custom_voice()
        example_voice_design()
        example_voice_clone()

        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
