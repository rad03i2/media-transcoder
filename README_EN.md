# Media Transcoder — English Guide

Media Transcoder is a Python command-line toolkit for local video and audio transcoding through FFmpeg and FFprobe. It focuses on repeatable presets, path validation, dry-run visibility, batch workflows, and safer output handling without uploading media to a remote service.

## What it does

- Converts one video or audio file with a named preset.
- Probes media streams and format metadata through FFprobe JSON.
- Batch-converts supported media from a directory.
- Preserves relative directory structure during batch conversion.
- Supports recursive discovery when requested.
- Prints the exact FFmpeg command in `--dry-run` mode.
- Protects existing output unless `--overwrite` is explicit.
- Rejects identical input and output paths.
- Uses a sibling temporary output during real conversions.
- Removes that temporary output if conversion fails.

## Requirements

- Python 3.10+
- FFmpeg
- FFprobe
- `ffmpeg` and `ffprobe` must be available on `PATH`

```bash
ffmpeg -version
ffprobe -version
```

## Installation

```bash
git clone https://github.com/rad03i2/media-transcoder.git
cd media-transcoder
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -e .
```

The installed command is:

```text
media-transcoder
```

## Commands

### Probe

```bash
media-transcoder probe movie.mkv
```

Outputs FFprobe format and stream metadata as JSON.

### Convert

```bash
media-transcoder convert movie.mkv movie.mp4 --preset web
```

Preview first:

```bash
media-transcoder convert movie.mkv movie.mp4 --preset web --dry-run
```

Replace an existing destination intentionally:

```bash
media-transcoder convert movie.mkv movie.mp4 --preset web --overwrite
```

### Batch

```bash
media-transcoder batch ./incoming ./converted --preset web --ext .mp4 --recursive
```

The batch command returns a non-zero exit code when one or more discovered conversions fail.

## Presets

| Name | FFmpeg intent |
|---|---|
| `web` | H.264 + AAC, CRF 23, medium encode preset, `+faststart` |
| `small` | H.265 + AAC, CRF 28, medium encode preset |
| `audio-mp3` | MP3 audio via `libmp3lame` |
| `audio-opus` | Opus audio via `libopus`, 128 kb/s |
| `copy` | Stream copy / remux |

## Batch input allow-list

```text
.mp4 .mkv .mov .avi .webm .m4v
.mp3 .wav .flac .m4a .ogg .opus
```

This allow-list applies to discovery. FFmpeg may accept additional formats when an individual file is passed to `convert`.

## Safety and privacy

Media Transcoder itself performs no uploads, telemetry, authentication, or API calls. It invokes local FFmpeg/FFprobe processes and passes arguments without `shell=True`.

During a real transcode, output is first written to a uniquely named sibling temporary file. The destination is replaced only after FFmpeg returns success and the temporary result exists with a non-zero size. The temporary file is removed in the cleanup path.

For hostile or untrusted media, keep FFmpeg current. See [SECURITY.md](SECURITY.md).

## Testing

```bash
python -m pip install -e . pytest
pytest -q
```

CI tests Python 3.10, 3.12, and 3.13 on Ubuntu, Windows, and macOS.

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the component and execution flow.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Changes should stay portable, testable, and explicit about user-visible FFmpeg behavior.

## License

MIT — see [LICENSE](LICENSE).

## Author

**Radwan Abd alhady Ahmed**  
GitHub: [@rad03i2](https://github.com/rad03i2)
