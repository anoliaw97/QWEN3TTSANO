#!/usr/bin/env python3
"""
Standalone TTS Application using Piper
Perfect for creating installable apps with custom voices
"""

import os
import wave
import json
from pathlib import Path
from typing import Optional
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading

try:
    from piper import PiperVoice
    PIPER_AVAILABLE = True
except ImportError:
    PIPER_AVAILABLE = False
    print("⚠️  Piper not installed. Install with: pip install piper-tts")


class PiperTTSApp:
    """Simple TTS application using Piper voice models"""

    def __init__(self, root):
        self.root = root
        self.root.title("Piper TTS - Custom Voice App")
        self.root.geometry("600x500")

        self.voice = None
        self.model_path = None

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""

        # Title
        title = tk.Label(
            self.root,
            text="🎙️ Piper TTS App",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        # Model loading frame
        model_frame = ttk.LabelFrame(self.root, text="Voice Model", padding=10)
        model_frame.pack(fill="x", padx=10, pady=5)

        self.model_label = tk.Label(
            model_frame,
            text="No model loaded",
            fg="red"
        )
        self.model_label.pack(side="left", padx=5)

        load_btn = ttk.Button(
            model_frame,
            text="Load Voice Model",
            command=self.load_model
        )
        load_btn.pack(side="right", padx=5)

        # Text input frame
        input_frame = ttk.LabelFrame(self.root, text="Text to Speak", padding=10)
        input_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.text_input = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            height=10,
            font=("Arial", 11)
        )
        self.text_input.pack(fill="both", expand=True)

        # Example text button
        example_btn = ttk.Button(
            input_frame,
            text="Load Example Text",
            command=self.load_example
        )
        example_btn.pack(pady=5)

        # Generate button
        self.generate_btn = ttk.Button(
            self.root,
            text="🎵 Generate Speech",
            command=self.generate_speech,
            state="disabled"
        )
        self.generate_btn.pack(pady=10)

        # Status bar
        self.status_var = tk.StringVar(value="Ready. Load a voice model to begin.")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(side="bottom", fill="x")

        # Info
        info = tk.Label(
            self.root,
            text="Tip: Place your custom .onnx voice model in the same folder",
            font=("Arial", 9),
            fg="gray"
        )
        info.pack(side="bottom", pady=5)

    def load_model(self):
        """Load a Piper ONNX voice model"""
        if not PIPER_AVAILABLE:
            messagebox.showerror(
                "Error",
                "Piper is not installed!\n\n"
                "Install with: pip install piper-tts"
            )
            return

        filename = filedialog.askopenfilename(
            title="Select Piper Voice Model",
            filetypes=[
                ("ONNX Models", "*.onnx"),
                ("All Files", "*.*")
            ]
        )

        if not filename:
            return

        try:
            self.status_var.set("Loading voice model...")
            self.root.update()

            # Load the voice
            self.voice = PiperVoice.load(filename)
            self.model_path = filename

            model_name = Path(filename).stem
            self.model_label.config(
                text=f"✓ {model_name}",
                fg="green"
            )
            self.generate_btn.config(state="normal")
            self.status_var.set(f"Voice model loaded: {model_name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model:\n{str(e)}")
            self.status_var.set("Error loading model")

    def load_example(self):
        """Load example text"""
        example = (
            "Hello! This is a demonstration of Piper text-to-speech. "
            "Piper is a fast, local neural text to speech system that "
            "sounds great and is optimized for embedded devices. "
            "You can create custom voices and bundle them with your application!"
        )
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert("1.0", example)

    def generate_speech(self):
        """Generate speech from text"""
        text = self.text_input.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning("Warning", "Please enter text to synthesize")
            return

        if not self.voice:
            messagebox.showwarning("Warning", "Please load a voice model first")
            return

        # Run in thread to avoid freezing UI
        thread = threading.Thread(target=self._generate_thread, args=(text,))
        thread.start()

    def _generate_thread(self, text):
        """Generate speech in background thread"""
        try:
            self.status_var.set("Generating speech...")
            self.generate_btn.config(state="disabled")

            # Ask where to save
            output_file = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV Audio", "*.wav"), ("All Files", "*.*")]
            )

            if not output_file:
                self.status_var.set("Cancelled")
                self.generate_btn.config(state="normal")
                return

            # Generate audio
            with wave.open(output_file, "wb") as wav_file:
                self.voice.synthesize(text, wav_file)

            self.status_var.set(f"✓ Speech saved to: {output_file}")
            messagebox.showinfo(
                "Success",
                f"Speech generated successfully!\n\nSaved to:\n{output_file}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate speech:\n{str(e)}")
            self.status_var.set("Error generating speech")

        finally:
            self.generate_btn.config(state="normal")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = PiperTTSApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
