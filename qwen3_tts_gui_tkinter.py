#!/usr/bin/env python3
"""
Qwen3-TTS Tkinter GUI Application
A traditional desktop GUI for Qwen3-TTS models using Tkinter
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import torch
import soundfile as sf
import os
import traceback
from typing import Optional
import warnings
warnings.filterwarnings("ignore")


class Qwen3TTSTkinterGUI:
    """Tkinter-based GUI for Qwen3-TTS"""

    def __init__(self, root):
        self.root = root
        self.root.title("Qwen3-TTS Desktop GUI")
        self.root.geometry("900x700")

        self.model = None
        self.model_type = None
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        # Speakers
        self.speakers = [
            "Vivian", "Serena", "Uncle_Fu", "Dylan", "Eric",
            "Ryan", "Aiden", "Ono_Anna", "Sohee"
        ]

        self.languages = [
            "Auto", "Chinese", "English", "Japanese", "Korean",
            "German", "French", "Russian", "Portuguese", "Spanish", "Italian"
        ]

        self.create_widgets()

    def create_widgets(self):
        """Create all GUI widgets"""

        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Model Loading Tab
        model_tab = ttk.Frame(notebook)
        notebook.add(model_tab, text="Model")
        self.create_model_tab(model_tab)

        # Custom Voice Tab
        cv_tab = ttk.Frame(notebook)
        notebook.add(cv_tab, text="Custom Voice")
        self.create_custom_voice_tab(cv_tab)

        # Voice Design Tab
        vd_tab = ttk.Frame(notebook)
        notebook.add(vd_tab, text="Voice Design")
        self.create_voice_design_tab(vd_tab)

        # Voice Clone Tab
        vc_tab = ttk.Frame(notebook)
        notebook.add(vc_tab, text="Voice Clone")
        self.create_voice_clone_tab(vc_tab)

        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text=f"Ready | Device: {self.device}",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_model_tab(self, parent):
        """Create model loading tab"""
        frame = ttk.Frame(parent, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title = ttk.Label(frame, text="Model Selection and Loading", font=("Arial", 14, "bold"))
        title.pack(pady=10)

        # Model selection
        ttk.Label(frame, text="Select Model:").pack(anchor=tk.W, pady=5)
        self.model_var = tk.StringVar(value="Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice")
        models = [
            "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
            "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
            "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
            "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
            "Qwen/Qwen3-TTS-12Hz-0.6B-Base",
        ]
        model_combo = ttk.Combobox(frame, textvariable=self.model_var, values=models, width=50)
        model_combo.pack(fill=tk.X, pady=5)

        # Load button
        load_btn = ttk.Button(frame, text="Load Model", command=self.load_model_threaded)
        load_btn.pack(pady=10)

        # Progress
        self.progress = ttk.Progressbar(frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)

        # Status text
        ttk.Label(frame, text="Model Status:").pack(anchor=tk.W, pady=5)
        self.model_status = scrolledtext.ScrolledText(frame, height=10, width=70)
        self.model_status.pack(fill=tk.BOTH, expand=True, pady=5)
        self.model_status.insert(tk.END, "No model loaded. Please select and load a model.\n")
        self.model_status.config(state=tk.DISABLED)

        # Info
        info = ttk.Label(
            frame,
            text="First-time loading will download the model from Hugging Face.\nThis may take several minutes depending on your internet connection.",
            font=("Arial", 9, "italic"),
            foreground="gray"
        )
        info.pack(pady=10)

    def create_custom_voice_tab(self, parent):
        """Create custom voice tab"""
        frame = ttk.Frame(parent, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Text input
        ttk.Label(frame, text="Text to Synthesize:").pack(anchor=tk.W)
        self.cv_text = scrolledtext.ScrolledText(frame, height=5, width=70)
        self.cv_text.pack(fill=tk.BOTH, pady=5)

        # Language
        lang_frame = ttk.Frame(frame)
        lang_frame.pack(fill=tk.X, pady=5)
        ttk.Label(lang_frame, text="Language:").pack(side=tk.LEFT)
        self.cv_lang_var = tk.StringVar(value="Auto")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.cv_lang_var, values=self.languages, width=15)
        lang_combo.pack(side=tk.LEFT, padx=5)

        # Speaker
        speaker_frame = ttk.Frame(frame)
        speaker_frame.pack(fill=tk.X, pady=5)
        ttk.Label(speaker_frame, text="Speaker:").pack(side=tk.LEFT)
        self.cv_speaker_var = tk.StringVar(value="Vivian")
        speaker_combo = ttk.Combobox(speaker_frame, textvariable=self.cv_speaker_var, values=self.speakers, width=15)
        speaker_combo.pack(side=tk.LEFT, padx=5)

        # Instruction
        ttk.Label(frame, text="Style Instruction (Optional):").pack(anchor=tk.W, pady=5)
        self.cv_instruct = ttk.Entry(frame, width=70)
        self.cv_instruct.pack(fill=tk.X, pady=5)

        # Generate button
        gen_btn = ttk.Button(frame, text="Generate Speech", command=self.generate_custom_voice_threaded)
        gen_btn.pack(pady=10)

        # Output
        ttk.Label(frame, text="Output File:").pack(anchor=tk.W)
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=5)
        self.cv_output_var = tk.StringVar(value="output_custom_voice.wav")
        ttk.Entry(output_frame, textvariable=self.cv_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse", command=lambda: self.browse_save_file(self.cv_output_var)).pack(side=tk.LEFT, padx=5)

        # Status
        ttk.Label(frame, text="Status:").pack(anchor=tk.W, pady=5)
        self.cv_status = scrolledtext.ScrolledText(frame, height=5, width=70)
        self.cv_status.pack(fill=tk.BOTH, expand=True)
        self.cv_status.config(state=tk.DISABLED)

    def create_voice_design_tab(self, parent):
        """Create voice design tab"""
        frame = ttk.Frame(parent, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Text input
        ttk.Label(frame, text="Text to Synthesize:").pack(anchor=tk.W)
        self.vd_text = scrolledtext.ScrolledText(frame, height=5, width=70)
        self.vd_text.pack(fill=tk.BOTH, pady=5)

        # Language
        lang_frame = ttk.Frame(frame)
        lang_frame.pack(fill=tk.X, pady=5)
        ttk.Label(lang_frame, text="Language:").pack(side=tk.LEFT)
        self.vd_lang_var = tk.StringVar(value="Auto")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.vd_lang_var, values=self.languages, width=15)
        lang_combo.pack(side=tk.LEFT, padx=5)

        # Voice design instruction
        ttk.Label(frame, text="Voice Design Instructions:").pack(anchor=tk.W, pady=5)
        self.vd_instruct = scrolledtext.ScrolledText(frame, height=4, width=70)
        self.vd_instruct.pack(fill=tk.BOTH, pady=5)

        # Generate button
        gen_btn = ttk.Button(frame, text="Generate Speech", command=self.generate_voice_design_threaded)
        gen_btn.pack(pady=10)

        # Output
        ttk.Label(frame, text="Output File:").pack(anchor=tk.W)
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=5)
        self.vd_output_var = tk.StringVar(value="output_voice_design.wav")
        ttk.Entry(output_frame, textvariable=self.vd_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse", command=lambda: self.browse_save_file(self.vd_output_var)).pack(side=tk.LEFT, padx=5)

        # Status
        ttk.Label(frame, text="Status:").pack(anchor=tk.W, pady=5)
        self.vd_status = scrolledtext.ScrolledText(frame, height=5, width=70)
        self.vd_status.pack(fill=tk.BOTH, expand=True)
        self.vd_status.config(state=tk.DISABLED)

    def create_voice_clone_tab(self, parent):
        """Create voice clone tab"""
        frame = ttk.Frame(parent, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Text input
        ttk.Label(frame, text="Text to Synthesize:").pack(anchor=tk.W)
        self.vc_text = scrolledtext.ScrolledText(frame, height=4, width=70)
        self.vc_text.pack(fill=tk.BOTH, pady=5)

        # Language
        lang_frame = ttk.Frame(frame)
        lang_frame.pack(fill=tk.X, pady=5)
        ttk.Label(lang_frame, text="Language:").pack(side=tk.LEFT)
        self.vc_lang_var = tk.StringVar(value="Auto")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.vc_lang_var, values=self.languages, width=15)
        lang_combo.pack(side=tk.LEFT, padx=5)

        # Reference audio
        ttk.Label(frame, text="Reference Audio:").pack(anchor=tk.W, pady=5)
        ref_frame = ttk.Frame(frame)
        ref_frame.pack(fill=tk.X, pady=5)
        self.vc_ref_audio_var = tk.StringVar()
        ttk.Entry(ref_frame, textvariable=self.vc_ref_audio_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(ref_frame, text="Browse", command=lambda: self.browse_open_file(self.vc_ref_audio_var)).pack(side=tk.LEFT, padx=5)

        # Reference text
        ttk.Label(frame, text="Reference Audio Transcript:").pack(anchor=tk.W, pady=5)
        self.vc_ref_text = scrolledtext.ScrolledText(frame, height=3, width=70)
        self.vc_ref_text.pack(fill=tk.BOTH, pady=5)

        # X-vector only
        self.vc_x_vector_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text="X-Vector Only Mode (faster, lower quality)", variable=self.vc_x_vector_var).pack(anchor=tk.W, pady=5)

        # Generate button
        gen_btn = ttk.Button(frame, text="Generate Speech", command=self.generate_voice_clone_threaded)
        gen_btn.pack(pady=10)

        # Output
        ttk.Label(frame, text="Output File:").pack(anchor=tk.W)
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=5)
        self.vc_output_var = tk.StringVar(value="output_voice_clone.wav")
        ttk.Entry(output_frame, textvariable=self.vc_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse", command=lambda: self.browse_save_file(self.vc_output_var)).pack(side=tk.LEFT, padx=5)

        # Status
        ttk.Label(frame, text="Status:").pack(anchor=tk.W, pady=5)
        self.vc_status = scrolledtext.ScrolledText(frame, height=4, width=70)
        self.vc_status.pack(fill=tk.BOTH, expand=True)
        self.vc_status.config(state=tk.DISABLED)

    def browse_save_file(self, var):
        """Browse for save file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if filename:
            var.set(filename)

    def browse_open_file(self, var):
        """Browse for open file"""
        filename = filedialog.askopenfilename(
            filetypes=[("Audio files", "*.wav *.mp3 *.flac"), ("All files", "*.*")]
        )
        if filename:
            var.set(filename)

    def update_status(self, widget, message):
        """Update status text widget"""
        widget.config(state=tk.NORMAL)
        widget.delete(1.0, tk.END)
        widget.insert(tk.END, message)
        widget.config(state=tk.DISABLED)

    def load_model_threaded(self):
        """Load model in a separate thread"""
        thread = threading.Thread(target=self.load_model)
        thread.daemon = True
        thread.start()

    def load_model(self):
        """Load the TTS model"""
        try:
            self.progress.start()
            self.update_status(self.model_status, "Loading model...\n")

            from qwen_tts import Qwen3TTSModel

            model_name = self.model_var.get()

            # Determine model type
            if "CustomVoice" in model_name:
                self.model_type = "custom_voice"
            elif "VoiceDesign" in model_name:
                self.model_type = "voice_design"
            elif "Base" in model_name:
                self.model_type = "voice_clone"

            # Load model
            self.model = Qwen3TTSModel.from_pretrained(
                model_name,
                device_map=self.device,
                dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
                attn_implementation="flash_attention_2" if torch.cuda.is_available() else "eager",
            )

            msg = f"✅ Model loaded successfully!\n\nModel: {model_name}\nType: {self.model_type}\nDevice: {self.device}"
            self.update_status(self.model_status, msg)
            self.status_bar.config(text=f"Model loaded: {self.model_type} | Device: {self.device}")

        except Exception as e:
            msg = f"❌ Error loading model:\n{str(e)}\n\n{traceback.format_exc()}"
            self.update_status(self.model_status, msg)
            messagebox.showerror("Error", f"Failed to load model: {str(e)}")

        finally:
            self.progress.stop()

    def generate_custom_voice_threaded(self):
        """Generate custom voice in thread"""
        thread = threading.Thread(target=self.generate_custom_voice)
        thread.daemon = True
        thread.start()

    def generate_custom_voice(self):
        """Generate speech with custom voice"""
        try:
            if self.model is None:
                messagebox.showerror("Error", "Please load a model first")
                return

            text = self.cv_text.get(1.0, tk.END).strip()
            if not text:
                messagebox.showerror("Error", "Please enter text to synthesize")
                return

            self.update_status(self.cv_status, "Generating speech...\n")

            language = None if self.cv_lang_var.get() == "Auto" else self.cv_lang_var.get()
            speaker = self.cv_speaker_var.get()
            instruct = self.cv_instruct.get().strip() or None

            wavs, sr = self.model.generate_custom_voice(
                text=text,
                language=language,
                speaker=speaker,
                instruct=instruct,
            )

            output_file = self.cv_output_var.get()
            sf.write(output_file, wavs[0], sr)

            msg = f"✅ Speech generated successfully!\n\nOutput: {output_file}\nSample rate: {sr} Hz\nDuration: {len(wavs[0])/sr:.2f}s"
            self.update_status(self.cv_status, msg)
            messagebox.showinfo("Success", f"Audio saved to:\n{output_file}")

        except Exception as e:
            msg = f"❌ Error:\n{str(e)}\n\n{traceback.format_exc()}"
            self.update_status(self.cv_status, msg)
            messagebox.showerror("Error", str(e))

    def generate_voice_design_threaded(self):
        """Generate voice design in thread"""
        thread = threading.Thread(target=self.generate_voice_design)
        thread.daemon = True
        thread.start()

    def generate_voice_design(self):
        """Generate speech with voice design"""
        try:
            if self.model is None:
                messagebox.showerror("Error", "Please load a model first")
                return

            text = self.vd_text.get(1.0, tk.END).strip()
            instruct = self.vd_instruct.get(1.0, tk.END).strip()

            if not text:
                messagebox.showerror("Error", "Please enter text to synthesize")
                return
            if not instruct:
                messagebox.showerror("Error", "Please provide voice design instructions")
                return

            self.update_status(self.vd_status, "Generating speech...\n")

            language = None if self.vd_lang_var.get() == "Auto" else self.vd_lang_var.get()

            wavs, sr = self.model.generate_voice_design(
                text=text,
                language=language,
                instruct=instruct,
            )

            output_file = self.vd_output_var.get()
            sf.write(output_file, wavs[0], sr)

            msg = f"✅ Speech generated successfully!\n\nOutput: {output_file}\nSample rate: {sr} Hz\nDuration: {len(wavs[0])/sr:.2f}s"
            self.update_status(self.vd_status, msg)
            messagebox.showinfo("Success", f"Audio saved to:\n{output_file}")

        except Exception as e:
            msg = f"❌ Error:\n{str(e)}\n\n{traceback.format_exc()}"
            self.update_status(self.vd_status, msg)
            messagebox.showerror("Error", str(e))

    def generate_voice_clone_threaded(self):
        """Generate voice clone in thread"""
        thread = threading.Thread(target=self.generate_voice_clone)
        thread.daemon = True
        thread.start()

    def generate_voice_clone(self):
        """Generate speech with voice clone"""
        try:
            if self.model is None:
                messagebox.showerror("Error", "Please load a model first")
                return

            text = self.vc_text.get(1.0, tk.END).strip()
            ref_audio = self.vc_ref_audio_var.get().strip()
            ref_text = self.vc_ref_text.get(1.0, tk.END).strip()
            x_vector = self.vc_x_vector_var.get()

            if not text:
                messagebox.showerror("Error", "Please enter text to synthesize")
                return
            if not ref_audio:
                messagebox.showerror("Error", "Please provide reference audio")
                return
            if not x_vector and not ref_text:
                messagebox.showerror("Error", "Please provide reference text or enable X-Vector mode")
                return

            self.update_status(self.vc_status, "Generating speech...\n")

            language = None if self.vc_lang_var.get() == "Auto" else self.vc_lang_var.get()

            wavs, sr = self.model.generate_voice_clone(
                text=text,
                language=language,
                ref_audio=ref_audio,
                ref_text=ref_text if not x_vector else None,
                x_vector_only_mode=x_vector,
            )

            output_file = self.vc_output_var.get()
            sf.write(output_file, wavs[0], sr)

            msg = f"✅ Speech generated successfully!\n\nOutput: {output_file}\nSample rate: {sr} Hz\nDuration: {len(wavs[0])/sr:.2f}s"
            self.update_status(self.vc_status, msg)
            messagebox.showinfo("Success", f"Audio saved to:\n{output_file}")

        except Exception as e:
            msg = f"❌ Error:\n{str(e)}\n\n{traceback.format_exc()}"
            self.update_status(self.vc_status, msg)
            messagebox.showerror("Error", str(e))


def main():
    """Main entry point"""
    root = tk.Tk()
    app = Qwen3TTSTkinterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
