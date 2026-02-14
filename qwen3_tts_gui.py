#!/usr/bin/env python3
"""
Qwen3-TTS GUI Application
A comprehensive graphical user interface for Qwen3-TTS models
Supports Custom Voice, Voice Design, and Voice Clone modes
"""

import os
import gradio as gr
import torch
import soundfile as sf
import tempfile
import traceback
from typing import Optional, Tuple
import warnings
warnings.filterwarnings("ignore")


class Qwen3TTSGUI:
    """Main GUI class for Qwen3-TTS"""

    def __init__(self):
        self.model = None
        self.model_type = None
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        # Check if flash-attention is available
        self.has_flash_attn = False
        try:
            import flash_attn
            self.has_flash_attn = True
        except ImportError:
            print("ℹ️ flash-attn not installed. Using standard attention (slower but works fine).")
            self.has_flash_attn = False

        # Supported speakers for CustomVoice model
        self.speakers = {
            "Vivian": "Bright, slightly edgy young female voice (Chinese)",
            "Serena": "Warm, gentle young female voice (Chinese)",
            "Uncle_Fu": "Seasoned male voice with low, mellow timbre (Chinese)",
            "Dylan": "Youthful Beijing male voice (Chinese - Beijing Dialect)",
            "Eric": "Lively Chengdu male voice (Chinese - Sichuan Dialect)",
            "Ryan": "Dynamic male voice with strong rhythmic drive (English)",
            "Aiden": "Sunny American male voice (English)",
            "Ono_Anna": "Playful Japanese female voice (Japanese)",
            "Sohee": "Warm Korean female voice (Korean)"
        }

        # Supported languages
        self.languages = [
            "Auto", "Chinese", "English", "Japanese", "Korean",
            "German", "French", "Russian", "Portuguese", "Spanish", "Italian"
        ]

    def load_model(self, model_name: str, progress=gr.Progress()) -> str:
        """Load the selected TTS model"""
        try:
            progress(0, desc="Loading model...")

            # Import here to avoid issues if qwen_tts is not installed
            from qwen_tts import Qwen3TTSModel

            # Determine model type
            if "CustomVoice" in model_name:
                self.model_type = "custom_voice"
            elif "VoiceDesign" in model_name:
                self.model_type = "voice_design"
            elif "Base" in model_name:
                self.model_type = "voice_clone"
            else:
                return "❌ Unknown model type"

            progress(0.3, desc=f"Loading {model_name}...")

            # Determine attention implementation
            # Use FlashAttention2 only if available and on CUDA
            if torch.cuda.is_available() and self.has_flash_attn:
                attn_impl = "flash_attention_2"
                print("✓ Using FlashAttention2 for better performance")
            elif torch.cuda.is_available():
                attn_impl = "sdpa"  # Scaled Dot Product Attention (PyTorch native, fast)
                print("✓ Using SDPA (PyTorch native attention)")
            else:
                attn_impl = "eager"  # Standard attention for CPU
                print("✓ Using eager attention (CPU mode)")

            # Load model with appropriate settings
            self.model = Qwen3TTSModel.from_pretrained(
                model_name,
                device_map=self.device,
                dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
                attn_implementation=attn_impl,
            )

            progress(1.0, desc="Model loaded!")
            return f"✅ Model loaded successfully: {model_name}\nType: {self.model_type}\nDevice: {self.device}"

        except Exception as e:
            error_msg = f"❌ Error loading model: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            return error_msg

    def generate_custom_voice(
        self,
        text: str,
        language: str,
        speaker: str,
        instruct: str = "",
        progress=gr.Progress()
    ) -> Tuple[Optional[str], str]:
        """Generate speech using CustomVoice model"""
        try:
            if self.model is None:
                return None, "❌ Please load a model first"

            # Check if correct model type is loaded
            if self.model_type != "custom_voice":
                return None, (
                    "❌ Wrong model loaded!\n\n"
                    "Custom Voice requires a **CustomVoice** model.\n"
                    "Current model type: " + self.model_type + "\n\n"
                    "Please load one of these models:\n"
                    "• Qwen3-TTS-12Hz-1.7B-CustomVoice (recommended)\n"
                    "• Qwen3-TTS-12Hz-0.6B-CustomVoice (faster)\n\n"
                    "Then try again!"
                )

            if not text.strip():
                return None, "❌ Please enter text to synthesize"

            progress(0, desc="Generating speech...")

            # Convert Auto to None for auto-detection
            lang = None if language == "Auto" else language

            # Generate audio
            wavs, sr = self.model.generate_custom_voice(
                text=text,
                language=lang,
                speaker=speaker,
                instruct=instruct if instruct.strip() else None,
            )

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                sf.write(f.name, wavs[0], sr)
                progress(1.0, desc="Speech generated!")
                return f.name, f"✅ Speech generated successfully!\nSample rate: {sr} Hz\nDuration: {len(wavs[0])/sr:.2f}s"

        except Exception as e:
            error_msg = f"❌ Error generating speech: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            return None, error_msg

    def generate_voice_design(
        self,
        text: str,
        language: str,
        instruct: str,
        progress=gr.Progress()
    ) -> Tuple[Optional[str], str]:
        """Generate speech using VoiceDesign model"""
        try:
            if self.model is None:
                return None, "❌ Please load a model first"

            # Check if correct model type is loaded
            if self.model_type != "voice_design":
                return None, (
                    "❌ Wrong model loaded!\n\n"
                    "Voice Design requires the **VoiceDesign** model.\n"
                    "Current model type: " + self.model_type + "\n\n"
                    "Please load:\n"
                    "• Qwen3-TTS-12Hz-1.7B-VoiceDesign\n\n"
                    "Then try again!"
                )

            if not text.strip():
                return None, "❌ Please enter text to synthesize"

            if not instruct.strip():
                return None, "❌ Please provide voice design instructions"

            progress(0, desc="Designing voice and generating speech...")

            # Convert Auto to None for auto-detection
            lang = None if language == "Auto" else language

            # Generate audio
            wavs, sr = self.model.generate_voice_design(
                text=text,
                language=lang,
                instruct=instruct,
            )

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                sf.write(f.name, wavs[0], sr)
                progress(1.0, desc="Speech generated!")
                return f.name, f"✅ Speech generated successfully!\nSample rate: {sr} Hz\nDuration: {len(wavs[0])/sr:.2f}s"

        except Exception as e:
            error_msg = f"❌ Error generating speech: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            return None, error_msg

    def generate_voice_clone(
        self,
        text: str,
        language: str,
        ref_audio,
        ref_text: str,
        x_vector_only: bool,
        progress=gr.Progress()
    ) -> Tuple[Optional[str], str]:
        """Generate speech using VoiceClone model"""
        try:
            if self.model is None:
                return None, "❌ Please load a model first"

            # Check if correct model type is loaded
            if self.model_type != "voice_clone":
                return None, (
                    "❌ Wrong model loaded!\n\n"
                    "Voice Clone requires a **Base** model.\n"
                    "Current model type: " + self.model_type + "\n\n"
                    "Please load one of these models:\n"
                    "• Qwen3-TTS-12Hz-1.7B-Base (better quality)\n"
                    "• Qwen3-TTS-12Hz-0.6B-Base (faster)\n\n"
                    "Then try again!"
                )

            if not text.strip():
                return None, "❌ Please enter text to synthesize"

            if ref_audio is None:
                return None, "❌ Please provide reference audio"

            if not x_vector_only and not ref_text.strip():
                return None, "❌ Please provide reference text or enable X-Vector Only mode"

            progress(0, desc="Cloning voice and generating speech...")

            # Convert Auto to None for auto-detection
            lang = None if language == "Auto" else language

            # Generate audio
            wavs, sr = self.model.generate_voice_clone(
                text=text,
                language=lang,
                ref_audio=ref_audio,
                ref_text=ref_text if not x_vector_only else None,
                x_vector_only_mode=x_vector_only,
            )

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                sf.write(f.name, wavs[0], sr)
                progress(1.0, desc="Speech generated!")
                return f.name, f"✅ Speech generated successfully!\nSample rate: {sr} Hz\nDuration: {len(wavs[0])/sr:.2f}s"

        except Exception as e:
            error_msg = f"❌ Error generating speech: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            return None, error_msg

    def create_interface(self):
        """Create the Gradio interface"""

        with gr.Blocks(title="Qwen3-TTS GUI", theme=gr.themes.Soft()) as interface:
            gr.Markdown("""
            # 🎙️ Qwen3-TTS GUI

            A comprehensive interface for Qwen3-TTS text-to-speech models.

            **Features:**
            - 🎯 **Custom Voice**: Use predefined high-quality voices (9 speakers)
            - 🎨 **Voice Design**: Create custom voices from text descriptions
            - 🔊 **Voice Clone**: Clone any voice from audio samples

            ---

            ### 📌 Which Model to Use?

            | Feature | Required Model | Purpose |
            |---------|---------------|---------|
            | **Custom Voice** | `*-CustomVoice` | Use 9 pre-made voices (Ryan, Vivian, etc.) |
            | **Voice Design** | `*-VoiceDesign` | Design custom voices with descriptions |
            | **Voice Clone** | `*-Base` | Clone voices from your audio files |

            ⚠️ **Important**: Each tab requires its specific model type to work!
            """)

            # Model Loading Section
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 📥 Load Model")
                    model_selector = gr.Dropdown(
                        choices=[
                            "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
                            "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
                            "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
                            "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
                            "Qwen/Qwen3-TTS-12Hz-0.6B-Base",
                        ],
                        value="Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
                        label="Select Model"
                    )
                    gr.Markdown("""
                    **Model Guide:**
                    - `*-CustomVoice` → Use **Custom Voice** tab
                    - `*-VoiceDesign` → Use **Voice Design** tab
                    - `*-Base` → Use **Voice Clone** tab
                    """)
                    load_btn = gr.Button("🔄 Load Model", variant="primary")
                    model_status = gr.Textbox(label="Model Status", lines=3)

            load_btn.click(
                fn=self.load_model,
                inputs=[model_selector],
                outputs=[model_status]
            )

            gr.Markdown("---")

            # TTS Generation Tabs
            with gr.Tabs():
                # Custom Voice Tab
                with gr.Tab("🎯 Custom Voice"):
                    gr.Markdown("""
                    Generate speech using predefined premium voices with optional style control.
                    **Best for**: Quick, high-quality TTS with consistent voices
                    """)

                    with gr.Row():
                        with gr.Column():
                            cv_text = gr.Textbox(
                                label="Text to Synthesize",
                                placeholder="Enter the text you want to convert to speech...",
                                lines=5
                            )
                            cv_language = gr.Dropdown(
                                choices=self.languages,
                                value="Auto",
                                label="Language"
                            )
                            cv_speaker = gr.Dropdown(
                                choices=list(self.speakers.keys()),
                                value="Vivian",
                                label="Speaker"
                            )
                            cv_speaker_info = gr.Markdown("**Vivian**: Bright, slightly edgy young female voice (Chinese)")
                            cv_instruct = gr.Textbox(
                                label="Style Instruction (Optional)",
                                placeholder="e.g., 'Speak with an angry tone' or 'Very happy'",
                                lines=2
                            )
                            cv_generate_btn = gr.Button("🎵 Generate Speech", variant="primary")

                        with gr.Column():
                            cv_audio = gr.Audio(label="Generated Audio", type="filepath")
                            cv_status = gr.Textbox(label="Status", lines=3)

                    # Update speaker info when speaker changes
                    cv_speaker.change(
                        fn=lambda x: f"**{x}**: {self.speakers[x]}",
                        inputs=[cv_speaker],
                        outputs=[cv_speaker_info]
                    )

                    cv_generate_btn.click(
                        fn=self.generate_custom_voice,
                        inputs=[cv_text, cv_language, cv_speaker, cv_instruct],
                        outputs=[cv_audio, cv_status]
                    )

                # Voice Design Tab
                with gr.Tab("🎨 Voice Design"):
                    gr.Markdown("""
                    Create custom voices from natural language descriptions.
                    **Best for**: Creating unique character voices or specific vocal characteristics
                    """)

                    with gr.Row():
                        with gr.Column():
                            vd_text = gr.Textbox(
                                label="Text to Synthesize",
                                placeholder="Enter the text you want to convert to speech...",
                                lines=5
                            )
                            vd_language = gr.Dropdown(
                                choices=self.languages,
                                value="Auto",
                                label="Language"
                            )
                            vd_instruct = gr.Textbox(
                                label="Voice Design Instructions",
                                placeholder="Describe the voice characteristics you want...\ne.g., 'A warm, gentle female voice with slight huskiness, age around 30'",
                                lines=4
                            )

                            gr.Examples(
                                examples=[
                                    ["Hello! How are you doing today?", "English", "A cheerful young female voice, bright and energetic, with a slight British accent"],
                                    ["哥哥，你回来啦！", "Chinese", "体现撒娇稚嫩的萝莉女声，音调偏高且起伏明显"],
                                    ["This is incredible!", "English", "Speak in an excited tone with enthusiasm and joy"],
                                ],
                                inputs=[vd_text, vd_language, vd_instruct],
                                label="Example Prompts"
                            )

                            vd_generate_btn = gr.Button("🎵 Generate Speech", variant="primary")

                        with gr.Column():
                            vd_audio = gr.Audio(label="Generated Audio", type="filepath")
                            vd_status = gr.Textbox(label="Status", lines=3)

                    vd_generate_btn.click(
                        fn=self.generate_voice_design,
                        inputs=[vd_text, vd_language, vd_instruct],
                        outputs=[vd_audio, vd_status]
                    )

                # Voice Clone Tab
                with gr.Tab("🔊 Voice Clone"):
                    gr.Markdown("""
                    Clone any voice from a 3-second audio sample.
                    **Best for**: Replicating specific voices or maintaining voice consistency
                    """)

                    with gr.Row():
                        with gr.Column():
                            vc_text = gr.Textbox(
                                label="Text to Synthesize",
                                placeholder="Enter the text you want to convert to speech...",
                                lines=5
                            )
                            vc_language = gr.Dropdown(
                                choices=self.languages,
                                value="Auto",
                                label="Language"
                            )
                            vc_ref_audio = gr.Audio(
                                label="Reference Audio (Upload 3+ second sample)",
                                type="filepath"
                            )
                            vc_ref_text = gr.Textbox(
                                label="Reference Audio Transcript",
                                placeholder="Transcript of the reference audio (required unless X-Vector Only mode is enabled)",
                                lines=3
                            )
                            vc_x_vector = gr.Checkbox(
                                label="X-Vector Only Mode (faster but lower quality)",
                                value=False
                            )
                            vc_generate_btn = gr.Button("🎵 Generate Speech", variant="primary")

                        with gr.Column():
                            vc_audio = gr.Audio(label="Generated Audio", type="filepath")
                            vc_status = gr.Textbox(label="Status", lines=3)

                    vc_generate_btn.click(
                        fn=self.generate_voice_clone,
                        inputs=[vc_text, vc_language, vc_ref_audio, vc_ref_text, vc_x_vector],
                        outputs=[vc_audio, vc_status]
                    )

            gr.Markdown("""
            ---
            ### 📚 Tips
            - **Custom Voice**: Best for quick results with professional voices
            - **Voice Design**: Experiment with detailed descriptions for unique voices
            - **Voice Clone**: Use clear, noise-free reference audio for best results

            ### ⚙️ Requirements
            - GPU with CUDA support recommended for faster generation
            - At least 8GB VRAM for 1.7B models, 4GB for 0.6B models
            - `qwen-tts` package installed (`pip install qwen-tts`)

            ### 🔗 Resources
            - [GitHub](https://github.com/QwenLM/Qwen3-TTS)
            - [Paper](https://arxiv.org/abs/2601.15621)
            - [Hugging Face](https://huggingface.co/collections/Qwen/qwen3-tts)
            """)

        return interface


def main():
    """Main entry point"""
    app = Qwen3TTSGUI()
    interface = app.create_interface()

    # Launch the interface
    interface.launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )


if __name__ == "__main__":
    main()
