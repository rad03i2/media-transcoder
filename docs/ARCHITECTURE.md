# Media Transcoder Architecture

Media Transcoder is deliberately small. The repository separates command-line orchestration from the FFmpeg/FFprobe execution layer so behavior can stay visible and testable.

## Components

### `src/media_transcoder/cli.py`

Responsible for:

- defining the `probe`, `convert`, and `batch` commands;
- parsing paths, presets, output extensions, and safety flags;
- printing probe JSON or conversion status;
- iterating over discovered files during batch work;
- returning non-zero exit codes for command-level failures.

### `src/media_transcoder/core.py`

Responsible for:

- locating FFmpeg and FFprobe through `PATH`;
- defining the current preset argument lists;
- validating source and destination paths;
- generating FFmpeg command arrays;
- probing metadata through FFprobe;
- writing real conversions to a unique temporary sibling file;
- promoting successful output with `Path.replace()`;
- removing temporary output during cleanup;
- discovering supported batch inputs.

## Conversion flow

```text
Job(source, destination, preset)
          │
          ▼
     validate preset
          │
          ▼
   require FFmpeg tools
          │
          ▼
 validate source/output
          │
          ├──────── dry_run=True ───────► return final command
          │
          ▼
create destination parent
          │
          ▼
build unique sibling temp path
          │
          ▼
run FFmpeg using argument array
          │
     ┌────┴────┐
     │         │
 failure     success
     │         │
     │     verify temp exists
     │     and size > 0
     │         │
     │     Path.replace()
     │         │
     └────┬────┘
          ▼
 cleanup temporary path
```

## Probe flow

`probe(path)` validates that the input is a file, locates FFprobe, executes it with JSON output enabled, and parses the returned JSON. Invalid FFprobe output becomes a `TranscodeError`.

## Batch flow

`discover()` uses a conservative extension allow-list. The CLI calculates a path relative to the input directory, applies the requested output extension, and processes each discovered source sequentially. A failed item is reported and counted while later items continue.

## Safety boundary

The project does not inspect or decode media in Python. Media parsing and encoding are delegated to the locally installed FFmpeg/FFprobe binaries.

The Python layer is responsible for path-level safeguards and process invocation:

- no shell command string;
- no `shell=True`;
- no same input/output path;
- no implicit overwrite;
- temporary output before final replacement;
- cleanup after failed conversions.

The security of codec parsing itself is therefore also dependent on the user's FFmpeg build. Keep it updated when processing untrusted media.

## External dependencies

Runtime Python code uses the standard library. FFmpeg and FFprobe are external executable dependencies and are intentionally not bundled by this repository.

## Tests

The current test suite covers:

- preset command generation;
- overwrite refusal;
- same-path refusal;
- preservation of existing output when an overwrite attempt fails;
- cleanup of failed temporary output;
- supported-media discovery;
- CLI dry-run output;
- empty batch handling.

Tool discovery and subprocess behavior are mocked where required so unit tests can exercise the Python control layer without requiring a real conversion fixture.
