import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from squish264.converter import convert_video
from squish264.db import init_db, get_files_by_status
from squish264.scanner import scan_folder
from squish264.utils import get_best_encoder


class Squish264GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Squish264 GUI")
        self.folder_path = tk.StringVar()
        self.mode = tk.StringVar(value="auto")
        self.encoder = tk.StringVar(value="libx265")
        self.preset = tk.StringVar(value="medium")
        self.quality = tk.IntVar(value=23)
        self.copy_audio = tk.BooleanVar(value=True)
        self.total_files = 1

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Select folder to convert:").grid(row=0, column=0, sticky="w", padx=(0, 5))
        ttk.Entry(frame, textvariable=self.folder_path, width=50).grid(row=0, column=1, sticky="ew", padx=(0, 5))
        ttk.Button(frame, text="Browse", command=self.browse_folder).grid(row=0, column=2, padx=(0, 5))

        ttk.Label(frame, text="Mode:").grid(row=1, column=0, sticky="w")
        mode_menu = ttk.Combobox(frame, textvariable=self.mode, values=["auto", "manual"], state="readonly")
        mode_menu.grid(row=1, column=1, sticky="w")
        mode_menu.bind("<<ComboboxSelected>>", self.toggle_manual_controls)

        self.manual_frame = ttk.LabelFrame(frame, text="Manual Options")
        self.manual_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(5, 10))

        ttk.Label(self.manual_frame, text="Encoder:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(self.manual_frame, textvariable=self.encoder,
                     values=["libx265", "hevc_nvenc", "hevc_qsv", "hevc_amf"], state="readonly").grid(row=0, column=1,
                                                                                                      sticky="w")

        ttk.Label(self.manual_frame, text="Preset:").grid(row=1, column=0, sticky="w")
        ttk.Combobox(self.manual_frame, textvariable=self.preset,
                     values=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower",
                             "veryslow", "p1", "p2", "p3", "p4", "p5", "p6", "p7"], state="readonly").grid(row=1,
                                                                                                           column=1,
                                                                                                           sticky="w")

        ttk.Label(self.manual_frame, text="Quality (CRF/CQ):").grid(row=2, column=0, sticky="w")
        quality_frame = ttk.Frame(self.manual_frame)
        quality_frame.grid(row=2, column=1, sticky="ew")
        self.quality_label = ttk.Label(quality_frame, text=str(self.quality.get()))
        self.quality_label.pack(side="right")
        quality_slider = ttk.Scale(quality_frame, from_=16, to=28, variable=self.quality, orient=tk.HORIZONTAL,
                                   command=self.update_quality_label)
        quality_slider.pack(side="left", fill="x", expand=True)

        ttk.Checkbutton(self.manual_frame, text="Copy audio", variable=self.copy_audio).grid(row=3, column=0,
                                                                                             columnspan=2, sticky="w")

        ttk.Button(frame, text="Start Squish", command=self.start_conversion).grid(row=3, column=0, pady=10)
        ttk.Button(frame, text="Exit", command=self.root.quit).grid(row=3, column=2, pady=10)

        self.progress = ttk.Progressbar(frame, length=400, mode="determinate")
        self.progress.grid(row=4, column=0, columnspan=3, pady=10)

        self.log_text = tk.Text(frame, wrap="word", height=20, state="disabled")
        self.log_text.grid(row=5, column=0, columnspan=3, sticky="nsew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(5, weight=1)

        self.toggle_manual_controls()

    def update_quality_label(self, val):
        self.quality_label.config(text=str(int(float(val))))

    def toggle_manual_controls(self, event=None):
        state = "normal" if self.mode.get() == "manual" else "disabled"
        for child in self.manual_frame.winfo_children():
            try:
                child.configure(state=state)
            except:
                pass

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def update_progress(self, value):
        self.progress["value"] = value
        self.root.update_idletasks()

    def start_conversion(self):
        folder = self.folder_path.get()
        mode = self.mode.get()

        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        self.log("Starting scan and conversion...")
        threading.Thread(target=self.convert_thread, args=(folder, mode), daemon=True).start()

    def convert_thread(self, path, mode):
        init_db()
        scan_folder(path)
        files = get_files_by_status("found")
        total = len(files)
        self.total_files = total
        self.progress["maximum"] = total

        self.log(f"Found {total} file(s) for conversion.")

        if mode == "auto":
            encoder, _ = get_best_encoder()
            self.log(f"[Auto Mode] Using encoder: {encoder}")
        else:
            self.log(
                f"[Manual Mode] Encoder: {self.encoder.get()}, Preset: {self.preset.get()}, Quality: {self.quality.get()}, Copy Audio: {self.copy_audio.get()}")

        for idx, (original, output) in enumerate(files, start=1):
            self.log(f"Converting: {original}\n → {output}")
            convert_video(original, output, mode=mode,
                          manual_options={
                              "encoder": self.encoder.get(),
                              "preset": self.preset.get(),
                              "quality": self.quality.get(),
                              "copy_audio": self.copy_audio.get()
                          })
            self.update_progress(idx)

        self.log("\nAll files converted!")


if __name__ == "__main__":
    root = tk.Tk()
    app = Squish264GUI(root)
    root.mainloop()
