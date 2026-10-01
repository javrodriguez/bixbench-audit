#!/usr/bin/env python3
"""Rebuild the data layout the recorded runs read, from fetched capsule zips (README, "How to reproduce").

Usage: extract_data.py <work_dir>
<work_dir> is a copy of src/runs/pilot-2026-09-30 (it holds capsules.txt, inputs.sha256 and data-trees.sha256)
into which src/scripts/fetch_capsules.py has downloaded the eight pinned zips under <work_dir>/zips/.
For each capsule it extracts only the CapsuleData-* folder into <work_dir>/data/<short_id>/ (reference notebooks are
left out, as in the audit), then checks every zip against the hashes pinned in src/prereg/ADDENDUM-2.md section 7 and every data
tree against data-trees.sha256, with the same tree hash the runner uses. Exits non-zero on any mismatch.
"""
import hashlib
import sys
import zipfile
from pathlib import Path

work = Path(sys.argv[1])


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# The zips are checked against the hashes pinned in src/prereg/ADDENDUM-2.md section 7, not against inputs.sha256,
# which fetch_capsules.py rewrites from whatever it downloaded.
PINNED = {
    "bix-13": "6b29bb5d03693e4098452042ae0169a98926d45ce6ca26b0a45682c8feb7039f",
    "bix-2": "7f9234d46d92985574164c53b3c62d39fa53dd06f8c10b1dbfb13652dc353be1",
    "bix-3": "41706da9f999eb4d02544c02e960f3fe8da0d0e3e0c18cfc95047e59924607d6",
    "bix-36": "2f254fd09c1e05bc0eb876dd7395e39f2af07b9cd92f643ce0c80288e8c24f6c",
    "bix-39": "be410226ac353bf8afada3e1226f163d374a5d3ffb5ce33560ee312363ba16a2",
    "bix-7": "9852ea865a9b394cf0c14469074493f49f8ae79e610fd89ed55b39e4d185e7b4",
    "bix-8": "6d0bcc4502eb25118564315573a132931d2b8a662e71b21d9b374bd59a884cf8",
    "bix-9": "afcdc39731ec0895aea70e77c06f8750f1629e263b0211be595a7e2d485f8747",
}
bad = 0
for line in (work / "capsules.txt").read_text().splitlines():
    if not line.strip():
        continue
    short, uuid = line.split()
    got = sha((work / "zips" / f"CapsuleFolder-{uuid}.zip").read_bytes())
    bad += got != PINNED[short]
    print(f"zip {short}: {'ok' if got == PINNED[short] else 'MISMATCH ' + got}")
for line in (work / "capsules.txt").read_text().splitlines():
    if not line.strip():
        continue
    short, uuid = line.split()
    z = zipfile.ZipFile(work / "zips" / f"CapsuleFolder-{uuid}.zip")
    dest = work / "data" / short
    for member in z.namelist():
        if member.startswith("CapsuleData-") and not member.endswith("/"):
            z.extract(member, dest)
for line in (work / "data-trees.sha256").read_text().splitlines():
    digest, short, _ = line.split()
    root = work / "data" / short
    files = sorted(p for p in root.rglob("*") if p.is_file())
    listing = "".join(f"{sha(p.read_bytes())}  {p.relative_to(root)}\n" for p in files)
    got = sha(listing.encode())
    bad += got != digest
    print(f"data tree {short}: {'ok' if got == digest else 'MISMATCH'} ({len(files)} files)")
print("layout matches the recorded run" if not bad else f"{bad} mismatch(es)")
sys.exit(1 if bad else 0)
