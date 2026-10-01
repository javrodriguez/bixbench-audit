#!/usr/bin/env python3
"""Compare each reading's value with its key (addendum 1 section 1, addendum 2 section 4, CHANGES-5).

Usage: compare2.py <jsonl_of_script_outputs> <BixBench.jsonl> <graders.py>
Scale rule: a value is compared on its own scale. Only for a question whose words ask for a percentage while its
key carries no % sign (bix-2-q2 among the ten) is the value also compared on the other scale; such a match is
reported as "other-scale" and can support a units reword, never a keep.
Rubric summary: pre-registered defensible readings only. Readings added after the pilot and readings marked not
defensible are listed on separate lines and never enter the rubric summary.
Output quotes keys: local lane evidence, never published as is.
"""
import asyncio
import json
import math
import re
import sys
import types
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

PERCENT_WORDS_NO_PERCENT_KEY = {"bix-2-q2"}

outputs = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
keys = {}
for line in Path(sys.argv[2]).read_text().splitlines():
    r = json.loads(line)
    keys[r["question_id"]] = (r["ideal"], r["eval_mode"])

for name in ("aviary", "aviary.core", "lmi", "bixbench", "bixbench.prompts", "bixbench.utils"):
    sys.modules[name] = types.ModuleType(name)
sys.modules["aviary.core"].Message = object
sys.modules["lmi"].LiteLLMModel = object
sys.modules["bixbench.prompts"].OPEN_ENDED_GRADING_PROMPT = ""
sys.modules["bixbench.prompts"].OPEN_ENDED_RANGE_GRADING_PROMPT = ""
sys.modules["bixbench.utils"].AnswerMode = object
g = types.ModuleType("bixbench.graders")
g.__package__ = "bixbench"
src = Path(sys.argv[3])
exec(compile(src.read_text(), str(src), "exec"), g.__dict__)
grader = g.GradingFunction()


def _numeric(num: str, value: float) -> tuple[bool, str]:
    kd = Decimal(num)
    if "e" in num.lower():
        mant = num.lower().split("e")[0].lstrip("+-")
        sig = len(mant.replace(".", "").lstrip("0")) or 1
        q = Decimal(1).scaleb(kd.adjusted() - sig + 1)
    else:
        dp = len(num.split(".")[1]) if "." in num else 0
        q = Decimal(1).scaleb(-dp)
    try:
        rounded = Decimal(repr(float(value))).quantize(q, rounding=ROUND_HALF_UP)
    except InvalidOperation:
        return False, f"{value} cannot be rounded to {q}"
    return rounded == kd, f"rounded {rounded} vs {kd}"


def accept(qid: str, key: str, value, unit: str | None) -> tuple[str, str]:
    """Returns (verdict, how); verdict is 'own' (accepted), 'other-scale', 'no', or 'none'."""
    if value is None:
        return "none", "no value"
    k = key.strip()
    if not isinstance(value, (int, float)):
        return ("own" if str(value).strip().lower() == k.lower() else "no"), "text"
    v = float(value)
    if not math.isfinite(v):
        return "no", "not finite"
    alt = None
    if qid in PERCENT_WORDS_NO_PERCENT_KEY:
        alt = {"fraction": v * 100, "percent": v / 100}.get(unit)
    m = re.fullmatch(r"\(\s*([-+0-9.eE]+)\s*,\s*([-+0-9.eE]+)\s*\)", k)
    if m:
        lo, hi = sorted((float(m.group(1)), float(m.group(2))))
        if lo <= v <= hi:
            return "own", f"range [{lo}, {hi}]"
        if alt is not None and lo <= alt <= hi:
            return "other-scale", f"range [{lo}, {hi}] on the other scale ({alt})"
        return "no", f"range [{lo}, {hi}]"
    pct = k.endswith("%")
    num = k.rstrip("%").strip()
    if re.fullmatch(r"[-+]?\d+(\.\d+)?([eE][-+]?\d+)?", num):
        if pct:
            ok, how = _numeric(num, v * 100 if unit == "fraction" else v)
            return ("own" if ok else "no"), how
        ok, how = _numeric(num, v)
        if ok:
            return "own", how
        if alt is not None:
            ok2, how2 = _numeric(num, alt)
            if ok2:
                return "other-scale", how2 + " (other scale)"
        return "no", how
    return ("own" if str(value).strip().lower() == k.lower() else "no"), "text"


def bixbench_grade(key: str, mode: str, value) -> str:
    try:
        if mode == "range_verifier":
            return str(grader._grade_range_verifier(target=key, predicted=str(value)).correct)
        return str(asyncio.run(grader._grade_str_verifier(target=key, predicted=str(value))).correct)
    except Exception as e:  # noqa: BLE001 - recording the grader's behaviour
        return f"raises {type(e).__name__}"


for o in outputs:
    qid = o["question_id"]
    key, mode = keys[qid]
    print(f"== {qid} ({mode})  key={key}")
    tally = {"pre": {}, "after": {}, "nondef": {}}
    for rk, r in sorted(o["readings"].items()):
        if not isinstance(r, dict) or "value" not in r:
            continue
        verdict, how = accept(qid, key, r["value"], r.get("unit"))
        group = "nondef" if r.get("defensible", True) is False else (
            "pre" if r.get("added", "before pilot") == "before pilot" else "after")
        tally[group][verdict] = tally[group].get(verdict, 0) + 1
        label = {"pre": "", "after": f"  [added {r.get('added')}]", "nondef": "  [not a defensible reading]"}[group]
        print(f"   {rk:28} value={r['value']!s:24} {verdict:11} ({how})  "
              f"bixbench_grader={bixbench_grade(key, mode, r['value'])}{label}")
    for group, title in (("pre", "RUBRIC (pre-registered defensible readings)"),
                         ("after", "after-pilot readings (candidates; defensibility is Javier's ruling)"),
                         ("nondef", "non-defensible readings (evidence of the key's origin only)")):
        if tally[group]:
            t = tally[group]
            print(f"   {title}: accepted {t.get('own', 0)}, other-scale only {t.get('other-scale', 0)}, "
                  f"rejected {t.get('no', 0)}, no value {t.get('none', 0)}")
