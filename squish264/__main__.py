import argparse

from squish264.db import init_db, get_files_by_status
from squish264.scanner import scan_folder
from squish264.utils import log


def main():
    parser = argparse.ArgumentParser(description="Squish264 - Convert h264 videos to h265")
    parser.add_argument("--path", required=True, help="Root folder path to scan")
    parser.add_argument("--mode", default="auto", choices=["auto", "manual"], help="Conversion mode")
    args = parser.parse_args()

    log("Initialising database...")
    init_db()

    log(f"Scanning path: {args.path}")
    scan_folder(args.path)

    log("Ready to convert:")
    for original, output in get_files_by_status("found"):
        print(f"{original} → {output}")


if __name__ == "__main__":
    main()
