# Squish264

**Squish264** is a Python application that recursively converts H.264 video files into H.265 (HEVC) format using `ffmpeg`. It's smart enough to detect available hardware (NVIDIA, Intel QSV, AMD AMF) and falls back to CPU encoding when needed. It also tracks conversion progress in a SQLite database, so it can resume from where it left off if interrupted.

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

- 📁 **Creates output folders per source**  
  Converted videos are stored inside an `h265/` folder next to the original videos.

- 📊 **Tracks progress via SQLite**  
  Keeps track of each file's state (`found`, `processing`, `done`) to prevent redundant conversions and support resuming.

- 📄 **Skips ignored folders**  
  Any folder with an `ignore.txt` or `.ignore` file will be skipped entirely.

---

## 🧱 Requirements

- Python 3.8+
- [`ffmpeg`](https://ffmpeg.org/) installed and available in your system PATH
- `colorama` (optional, for colourful logs)

Install dependencies:

```bash
pip install colorama
```

---

## 🧪 Example usage

```bash
python -m squish264 --path "/home/you/Videos" --mode auto
```

This will:
- Scan all folders under `/home/you/Videos`
- Create `h265/` folders where needed
- Convert each H.264 video to H.265 using the best available encoder
- Resume partially converted directories if re-run

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

## 🗃 File Tracking

The app creates a local SQLite database (`squish264.db`) with a table of all detected video files and their statuses:
- `found` → ready to be converted
- `processing` → in progress (if the app crashed, these are retried)
- `done` → successfully converted

---

## 💻 Thread Management

Squish264 automatically selects a safe number of threads based on your system's core count. You can tweak the logic in `utils.py` if needed.

---

## 🔍 Future Ideas

- Parallel/multi-threaded conversion
- GUI or web interface
- Custom CRF/CQ and preset controls
- File size reduction stats
- Integration with `ffprobe` to skip already-compressed H.265 files

---

## 💬 License

This is an open-source project. Feel free to use, modify, or contribute! ❤️
