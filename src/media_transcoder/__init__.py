"""Media Transcoder: safe local FFmpeg workflows."""

from .core import Job, PRESETS, TranscodeError, discover, probe, transcode

__all__ = ["Job", "PRESETS", "TranscodeError", "discover", "probe", "transcode"]
__version__ = "1.0.0"
__author__ = "Radwan Abdulhadi Ahmed (@rad03i2)"
