#!/usr/bin/env python3
"""
Piper TTS Voice Trainer GUI
A comprehensive graphical interface for training custom Piper TTS voices

Features:
- Dataset management (import audio, create transcripts)
- Audio recording and validation
- Preprocessing configuration
- Training launcher and monitoring
- Model export to ONNX
"""

import os
import sys
import json
import wave
import threading
import subprocess
from pathlib import Path
from typing import Optional, List, Dict
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime

try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️  sounddevice/soundfile not installed. Recording features disabled.")


class PiperTrainerGUI:
    """Main GUI application for Piper TTS voice training"""

    def __init__(self, root):
        self.root = root
        self.root.title("Piper TTS Voice Trainer")
        self.root.geometry("900x700")

        # Project state
        self.project_dir = None
        self.dataset_dir = None
        self.audio_files = []
        self.metadata = {}
        self.is_recording = False
        self.training_process = None

        # Audio recording state
        self.sample_rate = 22050
        self.recording_data = []

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""

        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=self.new_project)
        file_menu.add_command(label="Open Project", command=self.open_project)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title = tk.Label(
            main_frame,
            text="🎙️ Piper TTS Voice Trainer",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(0, 10))

        # Project info frame
        info_frame = ttk.LabelFrame(main_frame, text="Project Information", padding=10)
        info_frame.pack(fill="x", pady=(0, 10))

        self.project_label = tk.Label(
            info_frame,
            text="No project loaded. Create or open a project to begin.",
            fg="orange"
        )
        self.project_label.pack()

        # Tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)

        # Create tabs
        self.create_dataset_tab()
        self.create_recording_tab()
        self.create_preprocessing_tab()
        self.create_training_tab()
        self.create_export_tab()

        # Status bar
        self.status_var = tk.StringVar(value="Ready. Create or open a project to begin.")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(side="bottom", fill="x")

    def create_dataset_tab(self):
        """Create dataset management tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📁 Dataset")

        # Instructions
        instructions = ttk.LabelFrame(tab, text="Dataset Requirements", padding=10)
        instructions.pack(fill="x", padx=10, pady=10)

        tk.Label(
            instructions,
            text="For good quality training, you need:\n"
                 "• Minimum: 30 minutes of clean audio\n"
                 "• Recommended: 1-3 hours\n"
                 "• Ideal: 5-10 hours\n"
                 "• Format: WAV, mono, 22050 Hz\n"
                 "• Quality: Clear speech, no background noise",
            justify="left"
        ).pack()

        # Import section
        import_frame = ttk.LabelFrame(tab, text="Import Audio Files", padding=10)
        import_frame.pack(fill="x", padx=10, pady=10)

        btn_frame = ttk.Frame(import_frame)
        btn_frame.pack(fill="x")

        ttk.Button(
            btn_frame,
            text="Import Audio Files",
            command=self.import_audio_files
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Import Folder",
            command=self.import_audio_folder
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Validate Audio",
            command=self.validate_audio_files
        ).pack(side="left", padx=5)

        # Dataset list
        list_frame = ttk.LabelFrame(tab, text="Dataset Files", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable listbox
        scroll_frame = ttk.Frame(list_frame)
        scroll_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side="right", fill="y")

        self.dataset_listbox = tk.Listbox(
            scroll_frame,
            yscrollcommand=scrollbar.set,
            font=("Courier", 9)
        )
        self.dataset_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.dataset_listbox.yview)

        self.dataset_listbox.bind("<Double-Button-1>", self.edit_transcript)

        # Info label
        self.dataset_info_var = tk.StringVar(value="No files loaded")
        tk.Label(list_frame, textvariable=self.dataset_info_var).pack(pady=5)

    def create_recording_tab(self):
        """Create audio recording tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🎤 Record")

        if not AUDIO_AVAILABLE:
            tk.Label(
                tab,
                text="⚠️ Recording not available\n\n"
                     "Install: pip install sounddevice soundfile",
                fg="red",
                font=("Arial", 12)
            ).pack(expand=True)
            return

        # Recording controls
        control_frame = ttk.LabelFrame(tab, text="Recording Controls", padding=20)
        control_frame.pack(fill="x", padx=10, pady=10)

        # Sentence to record
        tk.Label(control_frame, text="Sentence to record:").pack()
        self.sentence_var = tk.StringVar()
        sentence_entry = ttk.Entry(
            control_frame,
            textvariable=self.sentence_var,
            font=("Arial", 11),
            width=50
        )
        sentence_entry.pack(pady=5)

        # Load sentences button
        ttk.Button(
            control_frame,
            text="Load Sentence List",
            command=self.load_sentences
        ).pack(pady=5)

        # Record button
        self.record_btn = ttk.Button(
            control_frame,
            text="🔴 Start Recording",
            command=self.toggle_recording
        )
        self.record_btn.pack(pady=10)

        # Recording status
        self.recording_status_var = tk.StringVar(value="Ready to record")
        tk.Label(
            control_frame,
            textvariable=self.recording_status_var,
            font=("Arial", 10, "bold")
        ).pack()

        # Playback controls
        playback_frame = ttk.LabelFrame(tab, text="Playback", padding=10)
        playback_frame.pack(fill="x", padx=10, pady=10)

        btn_row = ttk.Frame(playback_frame)
        btn_row.pack()

        ttk.Button(btn_row, text="▶️ Play", command=self.play_recording).pack(side="left", padx=5)
        ttk.Button(btn_row, text="💾 Save", command=self.save_recording).pack(side="left", padx=5)
        ttk.Button(btn_row, text="🗑️ Discard", command=self.discard_recording).pack(side="left", padx=5)

        # Recording list
        list_frame = ttk.LabelFrame(tab, text="Recorded Files", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.recording_listbox = tk.Listbox(list_frame, height=8)
        self.recording_listbox.pack(fill="both", expand=True)

        self.recording_count_var = tk.StringVar(value="0 recordings")
        tk.Label(list_frame, textvariable=self.recording_count_var).pack()

    def create_preprocessing_tab(self):
        """Create preprocessing configuration tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Preprocess")

        # Settings
        settings_frame = ttk.LabelFrame(tab, text="Preprocessing Settings", padding=20)
        settings_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Language
        ttk.Label(settings_frame, text="Language:").grid(row=0, column=0, sticky="w", pady=5)
        self.preprocess_lang_var = tk.StringVar(value="en-us")
        lang_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.preprocess_lang_var,
            values=["en-us", "en-gb", "es-es", "fr-fr", "de-de", "it-it", "zh-cn", "ja", "ko"],
            width=15
        )
        lang_combo.grid(row=0, column=1, sticky="w", pady=5)

        # Sample rate
        ttk.Label(settings_frame, text="Sample Rate:").grid(row=1, column=0, sticky="w", pady=5)
        self.sample_rate_var = tk.StringVar(value="22050")
        ttk.Entry(settings_frame, textvariable=self.sample_rate_var, width=15).grid(row=1, column=1, sticky="w", pady=5)

        # Max wav value
        ttk.Label(settings_frame, text="Max WAV Value:").grid(row=2, column=0, sticky="w", pady=5)
        self.max_wav_var = tk.StringVar(value="32768")
        ttk.Entry(settings_frame, textvariable=self.max_wav_var, width=15).grid(row=2, column=1, sticky="w", pady=5)

        # Single speaker
        self.single_speaker_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            settings_frame,
            text="Single Speaker (recommended for custom voices)",
            variable=self.single_speaker_var
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=10)

        # Run button
        ttk.Button(
            settings_frame,
            text="▶️ Run Preprocessing",
            command=self.run_preprocessing
        ).grid(row=4, column=0, columnspan=2, pady=10)

        # Output log
        log_frame = ttk.LabelFrame(tab, text="Preprocessing Log", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.preprocess_log = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            wrap=tk.WORD,
            font=("Courier", 9)
        )
        self.preprocess_log.pack(fill="both", expand=True)

    def create_training_tab(self):
        """Create training configuration and monitoring tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🏋️ Train")

        # Training settings
        settings_frame = ttk.LabelFrame(tab, text="Training Settings", padding=20)
        settings_frame.pack(fill="x", padx=10, pady=10)

        # Epochs
        ttk.Label(settings_frame, text="Epochs:").grid(row=0, column=0, sticky="w", pady=5)
        self.epochs_var = tk.StringVar(value="1000")
        ttk.Entry(settings_frame, textvariable=self.epochs_var, width=15).grid(row=0, column=1, sticky="w", pady=5)

        # Batch size
        ttk.Label(settings_frame, text="Batch Size:").grid(row=1, column=0, sticky="w", pady=5)
        self.batch_size_var = tk.StringVar(value="32")
        ttk.Entry(settings_frame, textvariable=self.batch_size_var, width=15).grid(row=1, column=1, sticky="w", pady=5)

        # Learning rate
        ttk.Label(settings_frame, text="Learning Rate:").grid(row=2, column=0, sticky="w", pady=5)
        self.lr_var = tk.StringVar(value="0.0001")
        ttk.Entry(settings_frame, textvariable=self.lr_var, width=15).grid(row=2, column=1, sticky="w", pady=5)

        # Checkpoint epochs
        ttk.Label(settings_frame, text="Checkpoint Every:").grid(row=3, column=0, sticky="w", pady=5)
        self.checkpoint_var = tk.StringVar(value="100")
        ttk.Entry(settings_frame, textvariable=self.checkpoint_var, width=15).grid(row=3, column=1, sticky="w", pady=5)

        # Validation split
        ttk.Label(settings_frame, text="Validation Split:").grid(row=4, column=0, sticky="w", pady=5)
        self.val_split_var = tk.StringVar(value="0.05")
        ttk.Entry(settings_frame, textvariable=self.val_split_var, width=15).grid(row=4, column=1, sticky="w", pady=5)

        # Control buttons
        btn_frame = ttk.Frame(settings_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        self.train_btn = ttk.Button(
            btn_frame,
            text="▶️ Start Training",
            command=self.start_training
        )
        self.train_btn.pack(side="left", padx=5)

        self.stop_train_btn = ttk.Button(
            btn_frame,
            text="⏹️ Stop Training",
            command=self.stop_training,
            state="disabled"
        )
        self.stop_train_btn.pack(side="left", padx=5)

        # Training log
        log_frame = ttk.LabelFrame(tab, text="Training Log", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.training_log = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            wrap=tk.WORD,
            font=("Courier", 9)
        )
        self.training_log.pack(fill="both", expand=True)

        # Training status
        self.training_status_var = tk.StringVar(value="Not started")
        tk.Label(
            log_frame,
            textvariable=self.training_status_var,
            font=("Arial", 10, "bold")
        ).pack(pady=5)

    def create_export_tab(self):
        """Create model export tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📦 Export")

        # Export settings
        export_frame = ttk.LabelFrame(tab, text="Export to ONNX", padding=20)
        export_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Instructions
        tk.Label(
            export_frame,
            text="Export your trained model to ONNX format for use in applications.\n"
                 "Select a checkpoint file and output location.",
            justify="left"
        ).pack(pady=10)

        # Checkpoint selection
        ckpt_frame = ttk.Frame(export_frame)
        ckpt_frame.pack(fill="x", pady=10)

        ttk.Label(ckpt_frame, text="Checkpoint:").pack(side="left", padx=5)
        self.checkpoint_path_var = tk.StringVar()
        ttk.Entry(ckpt_frame, textvariable=self.checkpoint_path_var, width=40).pack(side="left", padx=5)
        ttk.Button(ckpt_frame, text="Browse...", command=self.browse_checkpoint).pack(side="left")

        # Output location
        output_frame = ttk.Frame(export_frame)
        output_frame.pack(fill="x", pady=10)

        ttk.Label(output_frame, text="Output:").pack(side="left", padx=5)
        self.output_path_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_path_var, width=40).pack(side="left", padx=5)
        ttk.Button(output_frame, text="Browse...", command=self.browse_output).pack(side="left")

        # Export button
        ttk.Button(
            export_frame,
            text="📦 Export to ONNX",
            command=self.export_model
        ).pack(pady=20)

        # Export log
        log_frame = ttk.LabelFrame(tab, text="Export Log", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.export_log = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            wrap=tk.WORD,
            font=("Courier", 9)
        )
        self.export_log.pack(fill="both", expand=True)

    # Project management methods

    def new_project(self):
        """Create a new training project"""
        project_name = tk.simpledialog.askstring(
            "New Project",
            "Enter project name:"
        )
        if not project_name:
            return

        project_dir = filedialog.askdirectory(title="Select project location")
        if not project_dir:
            return

        self.project_dir = Path(project_dir) / project_name
        self.project_dir.mkdir(parents=True, exist_ok=True)

        # Create project structure
        self.dataset_dir = self.project_dir / "dataset"
        self.dataset_dir.mkdir(exist_ok=True)
        (self.dataset_dir / "wavs").mkdir(exist_ok=True)

        # Create config
        config = {
            "project_name": project_name,
            "created": datetime.now().isoformat(),
            "language": "en-us",
            "sample_rate": 22050
        }

        with open(self.project_dir / "project.json", "w") as f:
            json.dump(config, f, indent=2)

        # Create metadata.csv
        metadata_file = self.dataset_dir / "metadata.csv"
        metadata_file.touch()

        self.project_label.config(
            text=f"Project: {project_name} | Location: {self.project_dir}",
            fg="green"
        )
        self.status_var.set(f"Created new project: {project_name}")

    def open_project(self):
        """Open an existing project"""
        project_dir = filedialog.askdirectory(title="Select project directory")
        if not project_dir:
            return

        self.project_dir = Path(project_dir)
        config_file = self.project_dir / "project.json"

        if not config_file.exists():
            messagebox.showerror("Error", "Not a valid Piper training project")
            return

        with open(config_file) as f:
            config = json.load(f)

        self.dataset_dir = self.project_dir / "dataset"

        self.project_label.config(
            text=f"Project: {config['project_name']} | Location: {self.project_dir}",
            fg="green"
        )
        self.status_var.set(f"Opened project: {config['project_name']}")

        # Load metadata
        self.load_metadata()

    def load_metadata(self):
        """Load metadata from metadata.csv"""
        if not self.dataset_dir:
            return

        metadata_file = self.dataset_dir / "metadata.csv"
        if not metadata_file.exists():
            return

        self.metadata = {}
        with open(metadata_file) as f:
            for line in f:
                if "|" in line:
                    parts = line.strip().split("|", 1)
                    if len(parts) == 2:
                        self.metadata[parts[0]] = parts[1]

        self.refresh_dataset_list()

    def save_metadata(self):
        """Save metadata to metadata.csv"""
        if not self.dataset_dir:
            return

        metadata_file = self.dataset_dir / "metadata.csv"
        with open(metadata_file, "w") as f:
            for audio_id, text in sorted(self.metadata.items()):
                f.write(f"{audio_id}|{text}\n")

    # Dataset management methods

    def import_audio_files(self):
        """Import individual audio files"""
        if not self.project_dir:
            messagebox.showwarning("Warning", "Please create or open a project first")
            return

        files = filedialog.askopenfilenames(
            title="Select audio files",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )

        if not files:
            return

        wavs_dir = self.dataset_dir / "wavs"
        count = len(self.metadata)

        for filepath in files:
            # Copy to dataset
            audio_id = f"audio_{count:04d}"
            dest = wavs_dir / f"{audio_id}.wav"

            try:
                import shutil
                shutil.copy(filepath, dest)
                self.metadata[audio_id] = ""  # Empty transcript for now
                count += 1
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import {filepath}: {e}")

        self.save_metadata()
        self.refresh_dataset_list()
        self.status_var.set(f"Imported {len(files)} audio files")

    def import_audio_folder(self):
        """Import all audio files from a folder"""
        if not self.project_dir:
            messagebox.showwarning("Warning", "Please create or open a project first")
            return

        folder = filedialog.askdirectory(title="Select folder with audio files")
        if not folder:
            return

        import shutil
        wavs_dir = self.dataset_dir / "wavs"
        count = len(self.metadata)
        imported = 0

        for filepath in Path(folder).glob("*.wav"):
            audio_id = f"audio_{count:04d}"
            dest = wavs_dir / f"{audio_id}.wav"

            try:
                shutil.copy(filepath, dest)
                self.metadata[audio_id] = ""
                count += 1
                imported += 1
            except Exception as e:
                print(f"Failed to import {filepath}: {e}")

        self.save_metadata()
        self.refresh_dataset_list()
        self.status_var.set(f"Imported {imported} audio files from folder")

    def validate_audio_files(self):
        """Validate audio files in dataset"""
        if not self.dataset_dir:
            messagebox.showwarning("Warning", "Please open a project first")
            return

        wavs_dir = self.dataset_dir / "wavs"
        issues = []

        for audio_id in self.metadata.keys():
            filepath = wavs_dir / f"{audio_id}.wav"

            if not filepath.exists():
                issues.append(f"❌ {audio_id}: File not found")
                continue

            try:
                with wave.open(str(filepath), "rb") as wf:
                    sr = wf.getframerate()
                    channels = wf.getnchannels()
                    duration = wf.getnframes() / sr

                    if sr != 22050:
                        issues.append(f"⚠️  {audio_id}: Sample rate {sr} (should be 22050)")
                    if channels != 1:
                        issues.append(f"⚠️  {audio_id}: Not mono ({channels} channels)")
                    if duration < 2 or duration > 15:
                        issues.append(f"⚠️  {audio_id}: Duration {duration:.1f}s (recommended: 2-15s)")

            except Exception as e:
                issues.append(f"❌ {audio_id}: Error reading file - {e}")

        if issues:
            result = "\n".join(issues[:50])  # Show first 50 issues
            if len(issues) > 50:
                result += f"\n\n... and {len(issues) - 50} more issues"
            messagebox.showwarning("Validation Issues", result)
        else:
            messagebox.showinfo("Validation", "✅ All audio files are valid!")

    def refresh_dataset_list(self):
        """Refresh the dataset listbox"""
        self.dataset_listbox.delete(0, tk.END)

        for audio_id, text in sorted(self.metadata.items()):
            transcript = text if text else "[No transcript]"
            display = f"{audio_id:12s} | {transcript[:60]}"
            self.dataset_listbox.insert(tk.END, display)

        total_duration = 0
        wavs_dir = self.dataset_dir / "wavs"
        for audio_id in self.metadata.keys():
            filepath = wavs_dir / f"{audio_id}.wav"
            if filepath.exists():
                try:
                    with wave.open(str(filepath), "rb") as wf:
                        duration = wf.getnframes() / wf.getframerate()
                        total_duration += duration
                except:
                    pass

        count = len(self.metadata)
        minutes = int(total_duration // 60)
        seconds = int(total_duration % 60)

        self.dataset_info_var.set(
            f"{count} files | Total duration: {minutes}m {seconds}s"
        )

    def edit_transcript(self, event):
        """Edit transcript for selected audio file"""
        selection = self.dataset_listbox.curselection()
        if not selection:
            return

        idx = selection[0]
        audio_id = list(sorted(self.metadata.keys()))[idx]
        current_text = self.metadata[audio_id]

        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Transcript - {audio_id}")
        dialog.geometry("500x200")

        ttk.Label(dialog, text=f"Audio: {audio_id}").pack(pady=5)

        text_widget = scrolledtext.ScrolledText(dialog, height=5, wrap=tk.WORD)
        text_widget.pack(fill="both", expand=True, padx=10, pady=5)
        text_widget.insert("1.0", current_text)

        def save():
            new_text = text_widget.get("1.0", tk.END).strip()
            self.metadata[audio_id] = new_text
            self.save_metadata()
            self.refresh_dataset_list()
            dialog.destroy()

        ttk.Button(dialog, text="Save", command=save).pack(pady=5)

    # Recording methods

    def toggle_recording(self):
        """Start or stop recording"""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        """Start recording audio"""
        if not self.sentence_var.get().strip():
            messagebox.showwarning("Warning", "Please enter a sentence to record")
            return

        self.is_recording = True
        self.recording_data = []
        self.record_btn.config(text="⏹️ Stop Recording")
        self.recording_status_var.set("🔴 Recording...")

        # Start recording in thread
        def record():
            with sd.InputStream(samplerate=self.sample_rate, channels=1, callback=self.audio_callback):
                while self.is_recording:
                    sd.sleep(100)

        threading.Thread(target=record, daemon=True).start()

    def audio_callback(self, indata, frames, time, status):
        """Callback for audio recording"""
        if self.is_recording:
            self.recording_data.append(indata.copy())

    def stop_recording(self):
        """Stop recording audio"""
        self.is_recording = False
        self.record_btn.config(text="🔴 Start Recording")
        self.recording_status_var.set("Recording complete! Review and save.")

    def play_recording(self):
        """Play back the current recording"""
        if not self.recording_data:
            messagebox.showwarning("Warning", "No recording to play")
            return

        audio = np.concatenate(self.recording_data, axis=0)
        sd.play(audio, self.sample_rate)
        self.recording_status_var.set("Playing...")

    def save_recording(self):
        """Save the current recording to dataset"""
        if not self.recording_data:
            messagebox.showwarning("Warning", "No recording to save")
            return

        if not self.project_dir:
            messagebox.showwarning("Warning", "Please create or open a project first")
            return

        sentence = self.sentence_var.get().strip()
        if not sentence:
            messagebox.showwarning("Warning", "Please enter the transcript")
            return

        # Save audio
        audio = np.concatenate(self.recording_data, axis=0)
        count = len(self.metadata)
        audio_id = f"audio_{count:04d}"

        wavs_dir = self.dataset_dir / "wavs"
        filepath = wavs_dir / f"{audio_id}.wav"

        sf.write(filepath, audio, self.sample_rate)

        # Save transcript
        self.metadata[audio_id] = sentence
        self.save_metadata()
        self.refresh_dataset_list()

        # Update recording list
        self.recording_listbox.insert(tk.END, f"{audio_id}: {sentence[:40]}")
        self.recording_count_var.set(f"{len(self.metadata)} recordings")

        # Clear
        self.recording_data = []
        self.sentence_var.set("")
        self.recording_status_var.set("Saved! Ready for next recording.")
        self.status_var.set(f"Saved recording: {audio_id}")

    def discard_recording(self):
        """Discard the current recording"""
        self.recording_data = []
        self.recording_status_var.set("Recording discarded. Ready to record.")

    def load_sentences(self):
        """Load sentences from a text file for recording"""
        filepath = filedialog.askopenfilename(
            title="Select sentence list",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if not filepath:
            return

        # Show sentences in a dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Sentence List")
        dialog.geometry("600x400")

        listbox = tk.Listbox(dialog, font=("Arial", 10))
        listbox.pack(fill="both", expand=True, padx=10, pady=10)

        with open(filepath) as f:
            for line in f:
                sentence = line.strip()
                if sentence:
                    listbox.insert(tk.END, sentence)

        def use_sentence():
            selection = listbox.curselection()
            if selection:
                self.sentence_var.set(listbox.get(selection[0]))
                dialog.destroy()

        ttk.Button(dialog, text="Use Selected Sentence", command=use_sentence).pack(pady=5)

    # Training methods

    def run_preprocessing(self):
        """Run preprocessing on the dataset"""
        if not self.project_dir:
            messagebox.showwarning("Warning", "Please create or open a project first")
            return

        self.preprocess_log.delete("1.0", tk.END)
        self.preprocess_log.insert(tk.END, "Starting preprocessing...\n")

        # Build command
        cmd = [
            sys.executable, "-m", "piper_train.preprocess",
            "--language", self.preprocess_lang_var.get(),
            "--input-dir", str(self.dataset_dir / "wavs"),
            "--output-dir", str(self.project_dir / "preprocessed"),
            "--sample-rate", self.sample_rate_var.get(),
            "--max-wav-value", self.max_wav_var.get()
        ]

        if self.single_speaker_var.get():
            cmd.append("--single-speaker")

        # Run in thread
        def run():
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )

                for line in process.stdout:
                    self.preprocess_log.insert(tk.END, line)
                    self.preprocess_log.see(tk.END)
                    self.root.update()

                process.wait()
                self.preprocess_log.insert(tk.END, "\n✅ Preprocessing complete!\n")
                self.status_var.set("Preprocessing complete")

            except Exception as e:
                self.preprocess_log.insert(tk.END, f"\n❌ Error: {e}\n")
                self.status_var.set("Preprocessing failed")

        threading.Thread(target=run, daemon=True).start()

    def start_training(self):
        """Start model training"""
        if not self.project_dir:
            messagebox.showwarning("Warning", "Please create or open a project first")
            return

        preprocessed_dir = self.project_dir / "preprocessed"
        if not preprocessed_dir.exists():
            messagebox.showwarning(
                "Warning",
                "Please run preprocessing first!"
            )
            return

        self.training_log.delete("1.0", tk.END)
        self.training_log.insert(tk.END, "Starting training...\n")
        self.training_status_var.set("Training...")

        # Build command
        cmd = [
            sys.executable, "-m", "piper_train",
            "--dataset-dir", str(preprocessed_dir),
            "--epochs", self.epochs_var.get(),
            "--batch-size", self.batch_size_var.get(),
            "--learning-rate", self.lr_var.get(),
            "--checkpoint-epochs", self.checkpoint_var.get(),
            "--validation-split", self.val_split_var.get()
        ]

        # Run in thread
        def run():
            try:
                self.training_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )

                self.train_btn.config(state="disabled")
                self.stop_train_btn.config(state="normal")

                for line in self.training_process.stdout:
                    self.training_log.insert(tk.END, line)
                    self.training_log.see(tk.END)
                    self.root.update()

                self.training_process.wait()

                if self.training_process.returncode == 0:
                    self.training_log.insert(tk.END, "\n✅ Training complete!\n")
                    self.training_status_var.set("Training complete!")
                    self.status_var.set("Training complete")
                else:
                    self.training_log.insert(tk.END, "\n⚠️  Training stopped\n")
                    self.training_status_var.set("Training stopped")
                    self.status_var.set("Training stopped")

            except Exception as e:
                self.training_log.insert(tk.END, f"\n❌ Error: {e}\n")
                self.training_status_var.set("Training failed")
                self.status_var.set("Training failed")

            finally:
                self.train_btn.config(state="normal")
                self.stop_train_btn.config(state="disabled")
                self.training_process = None

        threading.Thread(target=run, daemon=True).start()

    def stop_training(self):
        """Stop the training process"""
        if self.training_process:
            self.training_process.terminate()
            self.training_log.insert(tk.END, "\n⏹️ Training stopped by user\n")
            self.training_status_var.set("Stopped")

    def browse_checkpoint(self):
        """Browse for checkpoint file"""
        filepath = filedialog.askopenfilename(
            title="Select checkpoint file",
            filetypes=[("Checkpoint files", "*.ckpt *.pt"), ("All files", "*.*")]
        )
        if filepath:
            self.checkpoint_path_var.set(filepath)

    def browse_output(self):
        """Browse for output location"""
        filepath = filedialog.asksaveasfilename(
            title="Save ONNX model as",
            defaultextension=".onnx",
            filetypes=[("ONNX files", "*.onnx"), ("All files", "*.*")]
        )
        if filepath:
            self.output_path_var.set(filepath)

    def export_model(self):
        """Export trained model to ONNX"""
        checkpoint = self.checkpoint_path_var.get()
        output = self.output_path_var.get()

        if not checkpoint or not output:
            messagebox.showwarning("Warning", "Please select checkpoint and output location")
            return

        self.export_log.delete("1.0", tk.END)
        self.export_log.insert(tk.END, "Exporting to ONNX...\n")

        # Build command
        cmd = [
            sys.executable, "-m", "piper_train.export_onnx",
            "--checkpoint", checkpoint,
            "--output", output,
            "--output-json", f"{output}.json"
        ]

        # Run in thread
        def run():
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )

                for line in process.stdout:
                    self.export_log.insert(tk.END, line)
                    self.export_log.see(tk.END)
                    self.root.update()

                process.wait()

                if process.returncode == 0:
                    self.export_log.insert(tk.END, f"\n✅ Model exported successfully!\n")
                    self.export_log.insert(tk.END, f"Location: {output}\n")
                    self.status_var.set("Model exported successfully")
                    messagebox.showinfo(
                        "Success",
                        f"Model exported to:\n{output}\n\nYou can now use this model in your applications!"
                    )
                else:
                    self.export_log.insert(tk.END, "\n❌ Export failed\n")
                    self.status_var.set("Export failed")

            except Exception as e:
                self.export_log.insert(tk.END, f"\n❌ Error: {e}\n")
                self.status_var.set("Export failed")

        threading.Thread(target=run, daemon=True).start()

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            "Piper TTS Voice Trainer\n\n"
            "A graphical interface for training custom Piper TTS voices.\n\n"
            "Features:\n"
            "• Dataset management\n"
            "• Audio recording\n"
            "• Training configuration\n"
            "• Model export\n\n"
            "Built for QWEN3TTSANO project"
        )


def main():
    """Main entry point"""
    root = tk.Tk()
    app = PiperTrainerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
