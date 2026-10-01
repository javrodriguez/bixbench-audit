#!/usr/bin/env python3
"""E5a selection: a fixed, mechanical rule picks the BixBench v1.5 questions to audit.

Inputs are pinned files in ../inputs (their sha256 is checked first).
Output is ids and metadata only, never question text, answers or distractors,
so the output can be published without republishing the question bank.

Rule (frozen in prereg/PREREG.md before any re-derivation):
  1. The question's capsule is not one of the capsules shipped in
     phylobio/BixBench-Verified-50 at the pinned revision (capsule-level exclusion,
     stricter than question-level, and readable without the dataset's gate).
  2. eval_mode is str_verifier or range_verifier (a fixed key, not a model judge).
  3. categories intersect FIELDS (Javier's fields).
  4. the capsule zip is at most MAX_BYTES (light on this Mac).
  Shortlist = every question passing 1-4.
  Top ten = round-robin over capsules (capsules ordered by the number in short_id),
  within a capsule by the question number, until ten are taken.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent / "inputs"
PINS = {
    "BixBench.jsonl": "0d1204dcdae7193a9132ced5a3502008f6b3b163debc1b65b2aa2d86cb132dc9",
}
FIELDS = {
    "RNA-seq",
    "Differential Expression Analysis",
    "Transcriptomics",
    "Epigenomics",
    "Genomic Variant Analysis",
    "Single-Cell Analysis",
}
MODES = {"str_verifier", "range_verifier"}
MAX_BYTES = 50_000_000
TOP = 10


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def cats(v) -> set:
    if isinstance(v, list):
        return {c.strip() for c in v}
    return {c.strip() for c in str(v).split(",")}


def num(s: str) -> tuple:
    return tuple(int(x) for x in re.findall(r"\d+", s))


def main() -> int:
    for name, want in PINS.items():
        got = sha(HERE / name)
        if got != want:
            print(f"PIN MISMATCH {name}: {got}", file=sys.stderr)
            return 2
    rows = [json.loads(line) for line in (HERE / "BixBench.jsonl").open()]
    tree = {e["path"]: e["size"] for e in json.loads((HERE / "bixbench_tree.json").read_text())}
    v50 = json.loads((HERE / "verified50_meta.json").read_text())
    v50_caps = {
        re.search(r"CapsuleFolder-(.*)\.zip", s["rfilename"]).group(1)
        for s in v50["siblings"]
        if s["rfilename"].startswith("CapsuleFolder-")
    }
    assert len(v50_caps) == 33, len(v50_caps)
    assert len(rows) == 205, len(rows)

    short = []
    for r in rows:
        size = tree.get(r["data_folder"])
        ok = (
            r["capsule_uuid"] not in v50_caps
            and r["eval_mode"] in MODES
            and cats(r["categories"]) & FIELDS
            and size is not None
            and size <= MAX_BYTES
        )
        if ok:
            short.append(
                {
                    "question_id": r["question_id"],
                    "short_id": r["short_id"],
                    "capsule_uuid": r["capsule_uuid"],
                    "capsule_bytes": size,
                    "eval_mode": r["eval_mode"],
                    "fields": sorted(cats(r["categories"]) & FIELDS),
                    "version": r["version"],
                }
            )
    short.sort(key=lambda q: num(q["question_id"]))

    by_cap: dict = {}
    for q in short:
        by_cap.setdefault(q["short_id"], []).append(q)
    order = sorted(by_cap, key=num)
    top, i = [], 0
    while len(top) < min(TOP, len(short)):
        for c in order:
            if i < len(by_cap[c]) and len(top) < TOP:
                top.append(by_cap[c][i]["question_id"])
        i += 1

    out = {
        "rule": "capsule not in Verified-50 · str/range verifier · field match · capsule <= 50 MB · round-robin top 10",
        "pool_rows": len(rows),
        "v50_capsules": len(v50_caps),
        "shortlist": short,
        "top10": top,
    }
    json.dump(out, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
