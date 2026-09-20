from __future__ import annotations

import json
import shutil
import subprocess
import uuid
from dataclasses import dataclass
from pathlib import Path


class TranscodeError(RuntimeError):
    """Raised when FFmpeg/FFprobe cannot complete a requested operation."""


PRESETS: dict[str, list[str]] = {
    "web": ["-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart"],
    "small": ["-c:v", "libx265", "-crf", "28", "-preset", "medium", "-c:a", "aac", "-b:a", "96k"],
    "audio-mp3": ["-vn", "-c:a", "libmp3lame", "-q:a", "2"],
    "audio-opus": ["-vn", "-c:a", "libopus", "-b:a", "128k"],
    "copy": ["-c", "copy"],
}

SUPPORTED_INPUTS = {".mp4", ".mkv", ".mov", ".avi", ".webm", ".m4v", ".mp3", ".wav", ".flac", ".m4a", ".ogg", ".opus"}


@dataclass(frozen=True)
class Job:
    source: Path
    destination: Path
    preset: str = "web"


def require_tools() -> tuple[str, str]:
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise TranscodeError("FFmpeg and FFprobe must be installed and available on PATH.")
    return ffmpeg, ffprobe


def probe(path: Path) -> dict:
    if not path.is_file():
        raise TranscodeError(f"Input file does not exist: {path}")
    _, ffprobe = require_tools()
    proc = subprocess.run(
        [ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
        capture_output=True, text=True, check=False,
    )
    if proc.returncode:
        raise TranscodeError(proc.stderr.strip() or "FFprobe failed")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise TranscodeError("FFprobe returned invalid JSON") from exc


def _validate(job: Job, overwrite: bool) -> str:
    ffmpeg, _ = require_tools()
    if job.preset not in PRESETS:
        raise TranscodeError(f"Unknown preset: {job.preset}. Choose from: {', '.join(PRESETS)}")
    if not job.source.is_file():
        raise TranscodeError(f"Input file does not exist: {job.source}")
    if job.source.resolve() == job.destination.resolve():
        raise TranscodeError("Input and output paths must be different.")
    if job.destination.exists() and not overwrite:
        raise TranscodeError(f"Output exists: {job.destination}. Use --overwrite to replace it.")
    return ffmpeg


def build_command(job: Job, *, overwrite: bool = False, output: Path | None = None) -> list[str]:
    ffmpeg = _validate(job, overwrite)
    target = output or job.destination
    return [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(job.source), *PRESETS[job.preset], str(target)]


def transcode(job: Job, *, overwrite: bool = False, dry_run: bool = False) -> list[str]:
    # Dry-run shows the conceptual final command; real execution writes to a sibling
    # temporary file and atomically replaces the destination only after success.
    if dry_run:
        return build_command(job, overwrite=overwrite)
    _validate(job, overwrite)
    job.destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = job.destination.with_name(
        f".{job.destination.stem}.{uuid.uuid4().hex}.tmp{job.destination.suffix}"
    )
    command = build_command(job, overwrite=overwrite, output=temporary)
    try:
        proc = subprocess.run(command, capture_output=True, text=True, check=False)
        if proc.returncode:
            raise TranscodeError(proc.stderr.strip() or "FFmpeg failed")
        if not temporary.is_file() or temporary.stat().st_size == 0:
            raise TranscodeError("FFmpeg completed without producing a valid output file.")
        temporary.replace(job.destination)
        return command
    finally:
        temporary.unlink(missing_ok=True)


def discover(folder: Path, recursive: bool = False) -> list[Path]:
    if not folder.is_dir():
        raise TranscodeError(f"Folder does not exist: {folder}")
    iterator = folder.rglob("*") if recursive else folder.glob("*")
    return sorted(p for p in iterator if p.is_file() and p.suffix.lower() in SUPPORTED_INPUTS)
