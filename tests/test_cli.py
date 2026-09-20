from pathlib import Path
from unittest.mock import patch

from media_transcoder.cli import main


@patch("media_transcoder.core.require_tools", return_value=("ffmpeg", "ffprobe"))
def test_convert_dry_run(_, tmp_path: Path, capsys):
    source = tmp_path / "clip.mov"
    source.write_bytes(b"x")
    code = main(["convert", str(source), str(tmp_path / "clip.mp4"), "--dry-run"])
    assert code == 0
    assert "ffmpeg" in capsys.readouterr().out


def test_batch_empty_directory(tmp_path: Path, capsys):
    code = main(["batch", str(tmp_path), str(tmp_path / "out")])
    assert code == 0
    assert "No supported" in capsys.readouterr().out
