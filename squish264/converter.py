# squish264/converter.py

import os

from squish264.db import update_status
from squish264.utils import log, run_command, get_best_encoder, get_recommended_threads


def convert_video(input_path, output_path, mode="auto"):
    log(f"Starting conversion: {input_path}", "INFO")
    update_status(input_path, "processing")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if mode == "auto":
        encoder, hwaccel_flags = get_best_encoder()
    else:
        encoder = "libx265"
        hwaccel_flags = []

    if encoder == "libx265":
        cmd = [
            "ffmpeg",
            "-threads", get_recommended_threads(),
            "-i", input_path,
            "-c:v", encoder,
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "copy",
            "-c:s", "copy",
            output_path
        ]
    else:
        cmd = [
            "ffmpeg",
            "-threads", get_recommended_threads(),
            *hwaccel_flags,
            "-i", input_path,
            "-c:v", encoder,
            "-preset", "p5",
            "-cq", "19",
            "-b:v", "0",
            "-c:a", "copy",
            "-c:s", "copy",
            output_path
        ]

    code, _, err = run_command(cmd)
    if code == 0:
        log(f"Finished: {input_path}", "OK")
        update_status(input_path, "done")
    else:
        log(f"Failed to convert {input_path}\n{err}", "ERROR")
        update_status(input_path, "found")
