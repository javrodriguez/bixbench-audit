#!/usr/bin/env python3
"""Public export of this repository: a masked copy of the tracked tree, built by a recorded, hashed transformation.

The originals are never modified (several are frozen by hash in src/prereg/). The export is a separate folder.

Usage:
  public_export.py build <repo> <out_dir> [--rev HEAD]   write the masked tree and <out_dir>/EXPORT-MANIFEST.json
  public_export.py check <repo> <out_dir>                re-derive the export from <repo> at the manifest's commit into
                                                          a sibling folder and fail on any byte difference
  public_export.py sweep <out_dir> [--gitleaks-config f]  look for what must not be public; print counts only

Mask rules, applied in this order to every text file (the account name and home folder are read at run time from the
environment, so neither appears in this script or in the manifest):
  R1  the path of the auditor's local Mac-scheduling helper (any path under the home folder ending in mac_slot.py)
      -> <local-scheduler>/mac_slot.py
  R2  the home folder prefix (e.g. /Users/<name> or /home/<name>) -> /Users/<user>
  R3  the session scratch prefix /private/tmp/claude-<uid>/... and /tmp/claude-<uid>/... -> <session-tmp>
  R4  any remaining occurrence of the account name as a whole word -> <user>
A file that is not valid UTF-8 is copied unchanged and listed as binary.
The manifest lists, for every tracked file, its sha256 before and after masking and which rules changed it.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

VERSION = "public_export v1"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def account() -> tuple[str, str]:
    home = str(Path.home())
    name = Path(home).name
    assert name and home.endswith(name), "cannot read the home folder"
    return home, name


def rules() -> list[tuple[str, re.Pattern, str]]:
    home, name = account()
    h = re.escape(home)
    return [
        ("R1", re.compile(h + r"/[^\s'\"`)\]]*?mac_slot\.py"), "<local-scheduler>/mac_slot.py"),
        ("R2", re.compile(h + r"(?=[/\s'\"`)\]:,.]|$)"), "/Users/<user>"),
        ("R3", re.compile(r"(?:/private)?/tmp/claude-\d+(?:/[^\s'\"`)\]]*)?"), "<session-tmp>"),
        ("R4", re.compile(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])"), "<user>"),
    ]


def git(repo: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True).stdout


def build(repo: Path, out: Path, rev: str) -> dict:
    if out.exists():
        sys.exit(f"REFUSED: {out} exists; remove it or choose another folder")
    commit = git(repo, "rev-parse", rev).decode().strip()
    entries = git(repo, "ls-tree", "-r", "-z", commit).split(b"\0")
    rs = rules()
    files = []
    for e in filter(None, entries):
        meta, path = e.split(b"\t", 1)
        mode, kind, obj = meta.split()
        if kind != b"blob":
            continue
        p = path.decode()
        data = git(repo, "cat-file", "blob", obj.decode())
        rec = {"path": p, "sha256_before": sha(data), "rules": [], "binary": False}
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            rec["binary"] = True
            new = data
        else:
            for rid, pat, rep in rs:
                text, n = pat.subn(rep, text)
                if n:
                    rec["rules"].append({"rule": rid, "count": n})
            new = text.encode("utf-8")
        rec["sha256_after"] = sha(new)
        dest = out / p
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(new)
        if mode == b"100755":
            dest.chmod(0o755)
        files.append(rec)
    manifest = {
        "tool": VERSION,
        "tool_sha256": sha(Path(__file__).read_bytes()),
        "source_commit": commit,
        "rules": [{"rule": r, "pattern": d} for r, d in (
            ("R1", "path under the home folder ending in mac_slot.py -> <local-scheduler>/mac_slot.py"),
            ("R2", "home folder prefix -> /Users/<user>"),
            ("R3", "(/private)/tmp/claude-<uid>/... -> <session-tmp>"),
            ("R4", "account name as a whole word -> <user>"))],
        "files": files,
        "masked_files": sum(1 for f in files if f["rules"]),
        "total_files": len(files),
    }
    (out / "EXPORT-MANIFEST.json").write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
    return manifest


def check(repo: Path, out: Path) -> int:
    m = json.loads((out / "EXPORT-MANIFEST.json").read_text())
    redo = out.with_name(out.name + ".recheck")
    if redo.exists():
        shutil.rmtree(redo)
    build(repo, redo, m["source_commit"])
    bad = []
    a = sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())
    b = sorted(p.relative_to(redo).as_posix() for p in redo.rglob("*") if p.is_file())
    if a != b:
        bad.append(f"file lists differ: only in export {sorted(set(a) - set(b))[:5]}, only in re-derivation {sorted(set(b) - set(a))[:5]}")
    for rel in sorted(set(a) & set(b)):
        if (out / rel).read_bytes() != (redo / rel).read_bytes():
            bad.append(f"differs: {rel}")
    for f in m["files"]:
        if f["path"] in a and sha((out / f["path"]).read_bytes()) != f["sha256_after"]:
            bad.append(f"manifest sha256_after mismatch: {f['path']}")
        src = git(repo, "cat-file", "blob", f"{m['source_commit']}:{f['path']}")
        if sha(src) != f["sha256_before"]:
            bad.append(f"manifest sha256_before mismatch: {f['path']}")
    shutil.rmtree(redo)
    print(f"check: {len(a)} files re-derived from {m['source_commit'][:12]}; differences: {len(bad)}")
    for x in bad[:20]:
        print("  " + x)
    return 1 if bad else 0


def sweep(out: Path, config: str | None) -> int:
    home, name = account()
    pats = {
        "home folder paths (/Users/..., /home/...) other than /Users/<user>": re.compile(r"/(?:Users|home)/(?!<user>)[A-Za-z0-9._-]+"),
        "the account name (never printed)": re.compile(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])", re.I),
        "temp paths (/tmp/, /private/tmp, /var/folders)": re.compile(r"(?:/private)?/tmp/|/var/folders/"),
    }
    # Excluded from the text patterns (not from gitleaks), because they name the patterns themselves: this tool's own
    # source, and the manifest's "rules" descriptions. Both are printed as excluded so the exclusion is never silent.
    own = {"src/scripts/public_export.py"}
    print("sweep · excluded from the path and temp patterns: src/scripts/public_export.py and the manifest's rule descriptions (they name the patterns)")
    total = 0
    for label, pat in pats.items():
        hits = []
        for p in sorted(out.rglob("*")):
            excluded = "account" not in label and p.relative_to(out).as_posix() in own
            if p.is_file() and not excluded:
                try:
                    t = p.read_text("utf-8")
                except UnicodeDecodeError:
                    continue
                if p.name == "EXPORT-MANIFEST.json" and "account" not in label:
                    m = json.loads(t)
                    m.pop("rules", None)
                    t = json.dumps(m)
                n = len(pat.findall(t))
                if n:
                    hits.append((p.relative_to(out).as_posix(), n))
        total += sum(n for _, n in hits)
        print(f"sweep · {label}: {sum(n for _, n in hits)} occurrence(s) in {len(hits)} file(s)")
        if "account" not in label:
            for rel, n in hits[:10]:
                print(f"    {rel}: {n}")
    cmd = ["gitleaks", "dir", str(out), "--redact", "--no-banner", "--exit-code", "3"]
    if config:
        cmd += ["--config", config]
    g = subprocess.run(cmd, capture_output=True, text=True)
    leaks = re.search(r"leaks found: (\d+)", g.stdout + g.stderr)
    clean = re.search(r"no leaks found", g.stdout + g.stderr)
    status = "clean" if (g.returncode == 0 and clean) else (f"{leaks.group(1)} finding(s)" if leaks else f"did not run cleanly (exit {g.returncode})")
    print(f"sweep · gitleaks ({'config ' + Path(config).name if config else 'default rules'}): {status}")
    return 1 if (total or g.returncode != 0) else 0


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    mode = sys.argv[1]
    if mode == "build":
        rev = sys.argv[sys.argv.index("--rev") + 1] if "--rev" in sys.argv else "HEAD"
        m = build(Path(sys.argv[2]), Path(sys.argv[3]), rev)
        print(f"build: {m['total_files']} files from {m['source_commit'][:12]}; {m['masked_files']} masked")
        return 0
    if mode == "check":
        return check(Path(sys.argv[2]), Path(sys.argv[3]))
    if mode == "sweep":
        cfg = sys.argv[sys.argv.index("--gitleaks-config") + 1] if "--gitleaks-config" in sys.argv else None
        return sweep(Path(sys.argv[2]), cfg)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
