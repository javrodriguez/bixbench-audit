#!/usr/bin/env python3
"""Pre-push check: no tracked file may carry the BixBench question bank (addendum 1 section 5, addendum 2 section 5).

Fails if any git-tracked file shares a 60-character window with any question's text, or contains all three
distractors of any question, after both sides are lower-cased and stripped of everything but letters and digits.
Also lists tracked files that quote a question id and a key value without the BixBench canary line.
Usage: check_no_bank.py <repo_root> <BixBench.jsonl>
"""
import json
import re
import subprocess
import sys
from pathlib import Path

W = 60
root, bank = Path(sys.argv[1]), Path(sys.argv[2])


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


rows = [json.loads(line) for line in bank.read_text().splitlines() if line.strip()]
windows = {}
for r in rows:
    q = norm(r["question"])
    for i in range(0, max(1, len(q) - W + 1)):
        windows.setdefault(q[i:i + W], r["question_id"])
tracked = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, text=True, check=True).stdout
bad = 0
for rel in filter(None, tracked.split("\0")):
    p = root / rel
    try:
        text = p.read_text(errors="ignore")
    except (IsADirectoryError, FileNotFoundError):
        continue
    t = norm(text)
    hits = {windows[t[i:i + W]] for i in range(0, max(0, len(t) - W + 1)) if t[i:i + W] in windows}
    # Distractor sets count only when all three are text (a letter and 8+ normalised characters): numeric
    # distractors such as "1" or "0.3" normalise to a digit or two and occur in any hash or number.
    dis = [r["question_id"] for r in rows if len(r["distractors"]) == 3
           and all(re.search(r"[a-z]", norm(d)) and len(norm(d)) >= 8 and norm(d) in t for d in r["distractors"])]
    if hits or dis:
        bad += 1
        print(f"FAIL {rel}: question text {sorted(hits)[:5]} distractor sets {dis[:5]}")
    elif rel.startswith("notes/") and re.search(r"bix-\d+-q\d+", text) and "BENCHMARK DATA SHOULD NEVER APPEAR" not in text:
        print(f"WARN {rel}: a note names a question without the canary line")
print("no question bank in tracked files" if not bad else f"{bad} file(s) carry question-bank text")
sys.exit(1 if bad else 0)
