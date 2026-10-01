#!/usr/bin/env python3
"""Compare each reading's value with the question's key under addendum 1, section 1.

Usage: compare.py <jsonl_of_script_outputs> <BixBench.jsonl> <graders.py>
For each reading prints: accepted by the addendum-1 rule (yes/no), and what BixBench's pinned grader says
(an E6 observation only). Output is local lane evidence; it quotes keys, so it is never published as is.
"""
import asyncio
import json
import math
import re
import sys
import types
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

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


def accept(key: str, value, unit: str | None) -> tuple[bool | None, str]:
    """Addendum 1 section 1, with addendum 2's unit rule: the value is compared in the key's unit."""
    if value is None:
        return None, "no value"
    if isinstance(value, float) and not math.isfinite(value):
        return False, "not finite"
    k = key.strip()
    m = re.fullmatch(r"\(\s*([-+0-9.eE]+)\s*,\s*([-+0-9.eE]+)\s*\)", k)
    if m:
        lo, hi = sorted((float(m.group(1)), float(m.group(2))))
        return lo <= float(value) <= hi, f"range [{lo}, {hi}]"
    pct = k.endswith("%")
    num = k.rstrip("%").strip()
    if re.fullmatch(r"[-+]?\d+(\.\d+)?([eE][-+]?\d+)?", num):
        if pct and unit == "fraction":
            ok, how = _numeric(num, float(value) * 100)
            return ok, how + " (fraction x 100 for a percent key)"
        if not pct and unit == "percent":
            ok1, how1 = _numeric(num, float(value))
            ok2, how2 = _numeric(num, float(value) / 100)
            return ok1 or ok2, f"both ways: as percent {how1}; as fraction {how2}"
        return _numeric(num, float(value))
    return str(value).strip().lower() == k.lower(), "text"


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
    for rk, r in sorted(o["readings"].items()):
        if not isinstance(r, dict) or "value" not in r:
            continue
        ok, how = accept(key, r["value"], r.get("unit"))
        print(f"   {rk:22} value={r['value']!s:24} accepted={ok!s:5} ({how})  bixbench_grader={bixbench_grade(key, mode, r['value'])}"
              f"{'' if r.get('defensible', True) else '  [not a defensible reading]'}")
