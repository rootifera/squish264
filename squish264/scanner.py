# squish264/scanner.py

import os

from squish264.config import VIDEO_EXTENSIONS, OUTPUT_FOLDER_NAME
from squish264.db import add_file
from squish264.utils import is_video_file, log


def should_ignore(dirpath):
    ignore_markers = ["ignore.txt", ".ignore"]
    for marker in ignore_markers:
        if os.path.exists(os.path.join(dirpath, marker)):
            log(f"Skipping folder (ignore marker found): {dirpath}", "WARN")
            return True
    return False


def scan_folder(root_path):
    scanned_files = 0
    for dirpath, dirnames, filenames in os.walk(root_path):
        if OUTPUT_FOLDER_NAME in dirpath.split(os.sep):
            continue

        if should_ignore(dirpath):
            continue

        video_files = [f for f in filenames if is_video_file(f, VIDEO_EXTENSIONS)]
        if not video_files:
            continue

        h265_dir = os.path.join(dirpath, OUTPUT_FOLDER_NAME)
        os.makedirs(h265_dir, exist_ok=True)

        for filename in video_files:
            full_path = os.path.join(dirpath, filename)
            output_path = os.path.join(h265_dir, filename)
            last_modified = os.path.getmtime(full_path)
            add_file(full_path, output_path, last_modified)
            scanned_files += 1
            log(f"Found video: {full_path}", "INFO")

    log(f"Scan complete. {scanned_files} video(s) found.", "OK")
