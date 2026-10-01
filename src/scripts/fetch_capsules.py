#!/usr/bin/env python3
"""Fetch capsule zips at the pinned BixBench revision and record their sha256 before any unzip.

Usage: fetch_capsules.py <run_dir>   (reads <run_dir>/capsules.txt: "<short_id> <uuid>" per line)
Writes <run_dir>/zips/CapsuleFolder-<uuid>.zip and <run_dir>/inputs.sha256.
"""
import hashlib
import sys
import urllib.request
from pathlib import Path

REV = "f8cc3bdcc6357c88b8c3648306522b9c422dc95a"
BASE = f"https://huggingface.co/datasets/futurehouse/BixBench/resolve/{REV}/"


def main() -> int:
    run = Path(sys.argv[1])
    lines = []
    for row in (run / "capsules.txt").read_text().split("\n"):
        if not row.strip():
            continue
        short, uuid = row.split()
        name = f"CapsuleFolder-{uuid}.zip"
        dest = run / "zips" / name
        if not dest.exists():
            with urllib.request.urlopen(BASE + name) as r, dest.open("wb") as f:
                while chunk := r.read(1 << 20):
                    f.write(chunk)
        digest = hashlib.sha256(dest.read_bytes()).hexdigest()
        lines.append(f"{digest}  zips/{name}  {short}")
        print(lines[-1], dest.stat().st_size)
    (run / "inputs.sha256").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
