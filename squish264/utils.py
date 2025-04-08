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
