import os

from squish264.db import update_status
from squish264.utils import log, run_command, get_best_encoder, get_recommended_threads, maybe_cleanup_database


def convert_video(input_path, output_path, mode="auto", manual_options=None):
    log(f"Starting conversion: {input_path}", "INFO")
    update_status(input_path, "processing")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if mode == "auto":
        encoder, hwaccel_flags = get_best_encoder()
        preset = "p5" if encoder != "libx265" else "medium"
        quality_flag = "-cq" if encoder != "libx265" else "-crf"
        quality_value = "19" if encoder != "libx265" else "23"
        copy_audio = True
    else:
        encoder = manual_options.get("encoder", "libx265")
        preset = manual_options.get("preset", "medium")
        quality_flag = "-cq" if encoder != "libx265" else "-crf"
        quality_value = str(manual_options.get("quality", 23))
        copy_audio = manual_options.get("copy_audio", True)
        hwaccel_flags = []

    cmd = [
        "ffmpeg",
        "-threads", get_recommended_threads(),
        *hwaccel_flags,
        "-i", input_path,
        "-c:v", encoder,
        "-preset", preset,
        quality_flag, quality_value,
        "-b:v", "0"
    ]

    if copy_audio:
        cmd += ["-c:a", "copy"]
    else:
        cmd += ["-c:a", "aac", "-b:a", "192k"]

    cmd += ["-c:s", "copy", output_path]

    code, _, err = run_command(cmd)
    if code == 0:
        log(f"Finished: {input_path}", "OK")
        update_status(input_path, "done")
    else:
        log(f"Failed to convert {input_path}\n{err}", "ERROR")
        update_status(input_path, "found")

    maybe_cleanup_database()
