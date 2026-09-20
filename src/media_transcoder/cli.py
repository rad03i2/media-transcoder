from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path

from .core import Job, PRESETS, TranscodeError, discover, probe, transcode


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="media-transcoder", description="Local, safe FFmpeg media transcoder")
    sub = p.add_subparsers(dest="command", required=True)

    info = sub.add_parser("probe", help="Inspect media streams and format as JSON")
    info.add_argument("input", type=Path)

    one = sub.add_parser("convert", help="Convert one media file")
    one.add_argument("input", type=Path)
    one.add_argument("output", type=Path)
    one.add_argument("--preset", choices=PRESETS, default="web")
    one.add_argument("--overwrite", action="store_true")
    one.add_argument("--dry-run", action="store_true")

    batch = sub.add_parser("batch", help="Convert supported files in a directory")
    batch.add_argument("input_dir", type=Path)
    batch.add_argument("output_dir", type=Path)
    batch.add_argument("--preset", choices=PRESETS, default="web")
    batch.add_argument("--ext", default=".mp4", help="Output extension, e.g. .mp4 or .mp3")
    batch.add_argument("--recursive", action="store_true")
    batch.add_argument("--overwrite", action="store_true")
    batch.add_argument("--dry-run", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "probe":
            print(json.dumps(probe(args.input), indent=2, ensure_ascii=False))
            return 0
        if args.command == "convert":
            cmd = transcode(Job(args.input, args.output, args.preset), overwrite=args.overwrite, dry_run=args.dry_run)
            print("Command:" if args.dry_run else "Done:", shlex.join(cmd))
            return 0

        ext = args.ext if args.ext.startswith(".") else "." + args.ext
        sources = discover(args.input_dir, args.recursive)
        if not sources:
            print("No supported media files found.")
            return 0
        failed = 0
        for source in sources:
            relative = source.relative_to(args.input_dir)
            destination = (args.output_dir / relative).with_suffix(ext)
            try:
                cmd = transcode(Job(source, destination, args.preset), overwrite=args.overwrite, dry_run=args.dry_run)
                print(("PLAN" if args.dry_run else "OK"), source, "->", destination)
                if args.dry_run:
                    print(" ", shlex.join(cmd))
            except TranscodeError as exc:
                failed += 1
                print("FAIL", source, "-", exc, file=sys.stderr)
        return 1 if failed else 0
    except TranscodeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
