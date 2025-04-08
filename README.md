# Squish264

**Squish264** is a Python application that recursively converts H.264 video files into H.265 (HEVC) format using `ffmpeg`. It's smart enough to detect available hardware (NVIDIA, Intel QSV, AMD AMF) and falls back to CPU encoding when needed. It also tracks conversion progress in a SQLite database, and cleans it up automatically when conversion is complete.

---

## 🚀 Features

- 🎯 **Recursive folder scanning**  
  Scans all subfolders under a specified path, detects videos, and skips `h265/` subfolders.

- 🧠 **Hardware-aware "auto" mode**  
  Automatically detects and uses the best available encoder:
  - `hevc_nvenc` (NVIDIA)
  - `hevc_qsv` (Intel Quick Sync)
  - `hevc_amf` (AMD)
  - `libx265` (CPU fallback)

- 🛠 **Manual mode with GUI controls or CLI options**  
  Select encoder, preset, CRF/CQ value, and audio settings manually.

- 📁 **Creates output folders per source**  
  Converted videos are stored inside an `h265/` folder next to the original videos.

- 🧠 **Skips ignored folders**  
  Any folder with an `ignore.txt` or `.ignore` file will be skipped entirely.

- 💾 **SQLite tracking & safe resuming**  
  Files are marked as `found`, `processing`, or `done` to prevent reprocessing.

- 🧹 **Auto database cleanup**  
  Once all videos are processed, the `squish264.db` is deleted.

- 🪟 **Optional GUI**  
  A clean Tkinter-based GUI is available for selecting folders and conversion settings.

---

## 🧱 Requirements

- Python 3.8+
- [`ffmpeg`](https://ffmpeg.org/) installed and available in your system PATH
- `tkinter` (usually comes with Python, install separately on Linux if needed)

Install optional dependencies:

```bash
pip install colorama
```

---

## 🧪 CLI Usage

### ✅ Auto Mode

```bash
python -m squish264 --path "/your/video/folder" --mode auto
```

### ✅ Manual Mode

```bash
python -m squish264 \
  --path "/your/video/folder" \
  --mode manual \
  --encoder libx265 \
  --preset slow \
  --quality 22 \
  --copy-audio
```

---

## 🛠 Output Structure

```
/Videos
├── Game1
│   ├── intro.mp4
│   └── h265/
│       └── intro.mp4  ← converted H.265 version
├── Game2
│   ├── .ignore        ← skipped
```

---

## 🖼 GUI Mode

Launch the GUI with:

```bash
python squish264_gui.py
```

Features:
- Folder selection
- Auto/manual mode
- Manual options via dropdowns (no typing needed)
- Progress bar and live logs
- Database auto cleanup when done

---

## 💬 License

This is an open-source project. Feel free to use, modify, or contribute! ❤️