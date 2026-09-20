from pathlib import Path
from unittest.mock import patch

import pytest

from media_transcoder.core import Job, TranscodeError, build_command, discover


@patch("media_transcoder.core.require_tools", return_value=("ffmpeg", "ffprobe"))
def test_build_command_uses_preset(_, tmp_path: Path):
    source = tmp_path / "in.mov"
    source.write_bytes(b"x")
    cmd = build_command(Job(source, tmp_path / "out.mp4", "web"))
    assert cmd[0] == "ffmpeg"
    assert "libx264" in cmd
    assert "-n" in cmd


@patch("media_transcoder.core.require_tools", return_value=("ffmpeg", "ffprobe"))
def test_refuses_overwrite(_, tmp_path: Path):
    source, output = tmp_path / "in.mkv", tmp_path / "out.mp4"
    source.write_bytes(b"x")
    output.write_bytes(b"existing")
    with pytest.raises(TranscodeError, match="Output exists"):
        build_command(Job(source, output))


@patch("media_transcoder.core.require_tools", return_value=("ffmpeg", "ffprobe"))
def test_refuses_same_path(_, tmp_path: Path):
    source = tmp_path / "same.mp4"
    source.write_bytes(b"x")
    with pytest.raises(TranscodeError, match="different"):
        build_command(Job(source, source))


def test_discover_supported_media(tmp_path: Path):
    (tmp_path / "a.mp4").write_bytes(b"x")
    (tmp_path / "b.txt").write_text("no")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "c.flac").write_bytes(b"x")
    assert [p.name for p in discover(tmp_path)] == ["a.mp4"]
    assert {p.name for p in discover(tmp_path, True)} == {"a.mp4", "c.flac"}
