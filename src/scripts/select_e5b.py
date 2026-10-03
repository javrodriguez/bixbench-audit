#!/usr/bin/env python3
"""E5b selection: the second batch of ten BixBench v1.5 questions, by a fixed mechanical rule.

Run as: python3 -P src/scripts/select_e5b.py   (inputs in src/inputs, git-ignored; their sha256 is checked first)
Output is ids and metadata only, never question text, keys or distractors.

Rule (frozen in prereg/E5B-PREREG-2026-10-01.md before any E5b script runs):
  1. Question-level exclusion: the question_id is not one of the 50 in phylobio/BixBench-Verified-50
     (BixBench-Verified-50.jsonl at revision c77fc8ea..., read with Javier's accepted terms on 1 Oct 2026).
  2. eval_mode is str_verifier or range_verifier (a fixed key).
  3. Its categories intersect FIELDS (Javier's fields; same set as E5a).
  4. Its capsule zip is at most 50 MB (same as E5a).
  5. Not audited elsewhere: (a) not in an Anqi-Dai capsule (bix-1, 4, 8, 26, 43, 49) and not a Harbor Index task
     (E5a amendment A); (b) its id is not named anywhere in the prior-art threads fetched on 1 Oct 2026
     (PRIOR_ART files below, pinned by hash); (c) not in capsule bix-22, which Future-House/BixBench issue #35
     discusses question by question without ids.
  6. Not one of E5a's ten (addendum 3), and not a question E5a's notes already compared with a computed value
     (bix-36-q4, whose key E5a's rebuild matched; bix-7-q2 and bix-8-q6 are excluded by 5 anyway), so that no
     E5b question has a value already seen against its key.
  Shortlist = every question passing 1-6. Ten = round-robin by source paper (E5a's A' ordering: the `paper` field
  with its scheme removed and lower-cased; papers ordered by their lowest question number, questions within a paper
  by (capsule number, question number)), until ten are taken.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

IN = Path(__file__).resolve().parent.parent / "inputs"
PINS = {
    "BixBench.jsonl": "0d1204dcdae7193a9132ced5a3502008f6b3b163debc1b65b2aa2d86cb132dc9",
    "bixbench_tree.json": "db7a3ecb0b96e6a4df9f44361ec1df3f41ed9f946d992861a5bbbe062b1f2b35",
    "BixBench-Verified-50.jsonl": "940de7d97eb6a9616a446734f4838188879deaf5a6b43acf5cac63623bccb593",
}
PRIOR_ART = sorted(p.name for p in (IN / "priorart").glob("*.json"))
FIELDS = {"RNA-seq", "Differential Expression Analysis", "Transcriptomics", "Epigenomics",
          "Genomic Variant Analysis", "Single-Cell Analysis"}
MODES = {"str_verifier", "range_verifier"}
MAX_BYTES = 50_000_000
ANQI_DAI_CAPSULES = {"bix-1", "bix-4", "bix-8", "bix-26", "bix-43", "bix-49"}
HARBOR_INDEX = {"bix-6-q5", "bix-7-q2", "bix-10-q2", "bix-30-q1", "bix-52-q2"}
ISSUE_35_CAPSULES = {"bix-22"}
E5A_TEN = {"bix-2-q1", "bix-3-q1", "bix-13-q1", "bix-36-q1", "bix-2-q2", "bix-3-q2", "bix-13-q2", "bix-36-q3",
           "bix-7-q1", "bix-3-q3"}
E5A_NOTES_NAMED = {"bix-36-q4", "bix-7-q2", "bix-8-q6"}  # ids named in E5a's VERDICTS, PROPOSED-VERDICTS, README
TOP = 10


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def cats(v) -> set:
    return {c.strip() for c in (v if isinstance(v, list) else str(v).split(","))}


def num(s: str) -> tuple:
    return tuple(int(x) for x in re.findall(r"\d+", s))


def paper_key(p: str) -> str:
    return re.sub(r"^https?://", "", str(p).strip()).lower()


def main() -> int:
    for name, want in PINS.items():
        if sha(IN / name) != want:
            print(f"PIN MISMATCH {name}", file=sys.stderr)
            return 2
    rows = [json.loads(line) for line in (IN / "BixBench.jsonl").open()]
    v50 = {json.loads(line)["question_id"] for line in (IN / "BixBench-Verified-50.jsonl").open() if line.strip()}
    tree = {e["path"]: e["size"] for e in json.loads((IN / "bixbench_tree.json").read_text())}
    named = set()
    prior_hashes = {}
    for name in PRIOR_ART:
        p = IN / "priorart" / name
        prior_hashes[name] = sha(p)
        named |= set(re.findall(r"bix-\d+-q\d+", p.read_text()))
    assert len(rows) == 205 and len(v50) == 50, (len(rows), len(v50))

    tests = {}
    short = []
    for r in rows:
        qid, cap = r["question_id"], r["short_id"]
        size = tree.get(r["data_folder"])
        t = {
            "1_not_v50": qid not in v50,
            "2_fixed_key": r["eval_mode"] in MODES,
            "3_field": bool(cats(r["categories"]) & FIELDS),
            "4_light": size is not None and size <= MAX_BYTES,
            "5a_not_anqi_dai_or_harbor_index": cap not in ANQI_DAI_CAPSULES and qid not in HARBOR_INDEX,
            "5b_not_named_in_prior_art": qid not in named,
            "5c_not_issue_35_capsule": cap not in ISSUE_35_CAPSULES,
            "6_not_e5a": qid not in E5A_TEN and qid not in E5A_NOTES_NAMED,
        }
        tests[qid] = t
        if all(t.values()):
            short.append({"question_id": qid, "short_id": cap, "capsule_uuid": r["capsule_uuid"],
                          "capsule_bytes": size, "eval_mode": r["eval_mode"],
                          "fields": sorted(cats(r["categories"]) & FIELDS), "paper": paper_key(r["paper"])})
    short.sort(key=lambda q: num(q["question_id"]))
    by_paper: dict = {}
    for q in short:
        by_paper.setdefault(q["paper"], []).append(q)
    order = sorted(by_paper, key=lambda p: num(by_paper[p][0]["question_id"]))
    top, i = [], 0
    while len(top) < min(TOP, len(short)):
        for p in order:
            if i < len(by_paper[p]) and len(top) < TOP:
                top.append(by_paper[p][i]["question_id"])
        i += 1
    passing = {k: sum(t[k] for t in tests.values()) for k in next(iter(tests.values()))}
    cum, alive = {}, set(tests)
    for k in passing:
        alive = {q for q in alive if tests[q][k]}
        cum[k] = len(alive)
    out = {
        "rule": "question not in Verified-50 · str/range · field · capsule <= 50 MB · not audited elsewhere · "
                "not E5a · round-robin by source paper, top 10",
        "pins": PINS,
        "prior_art_files": prior_hashes,
        "prior_art_ids_named": sorted(named, key=num),
        "pool_rows": len(rows),
        "remaining_after_each_test_in_order": cum,
        "shortlist": short,
        "papers_in_order": order,
        "top10": top,
    }
    json.dump(out, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
