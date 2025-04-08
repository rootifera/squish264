import argparse

from squish264.converter import convert_video
from squish264.db import init_db, get_files_by_status
from squish264.scanner import scan_folder
from squish264.utils import ffmpeg_installed
from squish264.utils import log


def main():
    if not ffmpeg_installed():
        log("ffmpeg not found. Please install ffmpeg and ensure it's in your PATH.", "ERROR")
        return

    parser = argparse.ArgumentParser(description="Squish264 - Convert h264 videos to h265")
    parser.add_argument("--path", required=True, help="Root folder path to scan")
    parser.add_argument("--mode", default="auto", choices=["auto", "manual"], help="Conversion mode")
    args = parser.parse_args()

    log("Initialising database...")
    init_db()

    log(f"Scanning path: {args.path}")
    scan_folder(args.path)

    log("Ready to convert:")
    files = get_files_by_status("found")
    for original, output in files:
        print(f"{original} → {output}")

    for original, output in files:
        convert_video(original, output)


if __name__ == "__main__":
    main()
