#!/usr/bin/env python3
"""Probe BixBench's own str and range graders at the pinned commit (49311180).

Loads inputs/graders_49311180.py with its model-client imports stubbed (they are
only used by the LLM verifier), then calls the two deterministic graders on
chosen pairs. Nothing here touches a model or the network.
"""
import asyncio
import hashlib
import sys
import types
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "inputs" / "graders_49311180.py"
print("graders sha256", hashlib.sha256(SRC.read_bytes()).hexdigest())

for name in ("aviary", "aviary.core", "lmi", "bixbench", "bixbench.prompts", "bixbench.utils"):
    sys.modules[name] = types.ModuleType(name)
sys.modules["aviary.core"].Message = object
sys.modules["lmi"].LiteLLMModel = object
sys.modules["bixbench.prompts"].OPEN_ENDED_GRADING_PROMPT = ""
sys.modules["bixbench.prompts"].OPEN_ENDED_RANGE_GRADING_PROMPT = ""
sys.modules["bixbench.utils"].AnswerMode = object

mod = types.ModuleType("bixbench.graders")
mod.__package__ = "bixbench"
exec(compile(SRC.read_text(), str(SRC), "exec"), mod.__dict__)
g = mod.GradingFunction()

STR_CASES = [
    ("1.33", "1.33"),   # the key itself
    ("1.33", "13.3"),   # decimal point moved
    ("1.33", "133"),
    ("0.0002", "2e-4"), # same number, other notation
    ("1.9E-05", "1.9e5"),  # sign of the exponent dropped
    ("10.6%", "106"),
    ("0", "-0"),
]
for target, pred in STR_CASES:
    r = asyncio.run(g._grade_str_verifier(target=target, predicted=pred))
    print(f"str   target={target!r:10} predicted={pred!r:9} correct={r.correct}")

for target, pred in [("(0.76,0.78)", "0.77"), ("(0.76,0.78)", "0.9")]:
    try:
        r = g._grade_range_verifier(target=target, predicted=pred)
        print(f"range target={target!r} predicted={pred!r} correct={r.correct}")
    except Exception as e:  # noqa: BLE001 - we are recording what happens
        print(f"range target={target!r} predicted={pred!r} RAISES {type(e).__name__}: {e}")
