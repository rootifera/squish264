import datetime
import os
import shutil
import subprocess

try:
    from colorama import Fore, Style, init as colorama_init

    colorama_init()
except ImportError:
    class Dummy:
        RESET_ALL = ''


    Fore = Style = Dummy()


def log(msg, level="INFO"):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    colour = {
        "INFO": Fore.CYAN,
        "CMD": Fore.YELLOW,
        "WARN": Fore.MAGENTA,
        "ERROR": Fore.RED,
        "OK": Fore.GREEN
    }.get(level.upper(), "")
    print(f"{colour}[{ts}] [{level.upper()}] {msg}{Style.RESET_ALL}")


def run_command(command, dry_run=False):
    log(f"Running command: {' '.join(command)}", "CMD")
    if dry_run:
        return 0, "", ""
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def format_bytes(size):
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


def ffmpeg_installed():
    return shutil.which("ffmpeg") is not None


def is_video_file(filename, extensions):
    ext = os.path.splitext(filename)[1].lower()
    return ext in extensions


def get_available_encoders():
    result = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else ""


def get_best_encoder():
    encoders = get_available_encoders()

    if "hevc_nvenc" in encoders and test_encoder_available("hevc_nvenc"):
        log("NVIDIA NVENC available and functional.", "INFO")
        return "hevc_nvenc", ["-hwaccel", "nvdec"]

    if "hevc_qsv" in encoders and test_encoder_available("hevc_qsv"):
        log("Intel QSV available and functional.", "INFO")
        return "hevc_qsv", ["-hwaccel", "qsv", "-hwaccel_output_format", "qsv"]

    if "hevc_amf" in encoders and test_encoder_available("hevc_amf"):
        log("AMD AMF available and functional.", "INFO")
        return "hevc_amf", ["-hwaccel", "dxva2"]

    log("No hardware encoders available. Falling back to CPU.", "WARN")
    return "libx265", []


def get_recommended_threads():
    cores = os.cpu_count() or 4
    if cores <= 2:
        return "2"
    elif cores <= 4:
        return "4"
    elif cores <= 8:
        return "6"
    else:
        return str(min(cores - 2, 16))


def test_encoder_available(encoder: str) -> bool:
    try:
        result = subprocess.run([
            "ffmpeg", "-hide_banner", "-y",
            "-f", "lavfi", "-i", "nullsrc",
            "-frames:v", "1", "-c:v", encoder,
            "-f", "null", "-"
        ], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False
