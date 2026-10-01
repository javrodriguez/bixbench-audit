# E5a script changes after review round 3 (lane, 30 Sep 2026, 09:43 EDT)

Review round 3 (claude-opus-5-5, fresh context) returned MAJOR 0, MINOR 5, NIT 5, and the review loop stopped there.
Before any script produced a value, the lane changed five scripts for the reasons below; their new hashes are in `SCRIPTS-3.sha256`, which supersedes `SCRIPTS-2.sha256`.
Addenda 1 and 2 are unchanged; the wording corrections at the end are recorded here and carried into addendum 3's preamble.

- `q/bix-3-q1.R`, `q/bix-13-q1.R` (MINOR 1): DESeq2's independent filtering is a choice the questions do not fix, so it becomes a reading: F1 the default (alpha 0.1), F2 alpha 0.05, F3 filtering off.
  `bix-13-q1.R` also caches each apeglm shrinkage so it is computed once per model and coefficient.
- `run_pilot.py` (MINOR 3, MINOR 5, NIT 3, NIT 4): the run refuses to start unless every zip matches its pinned hash; it writes a hash of each extracted `CapsuleData` tree and the full Python and R environments into the run folder; it reports the positive control as pass or fail with its two public numbers only; it makes every sealed output read-only.
- `q/bix-8-q6.py` (MINOR 4): carries the BixBench canary line for its question, because it quotes that question's key.
- `q/bix-3-prep.py` (NIT 5): keeps only the gene column and per-sample count columns; the sheet's own differential-expression result columns are dropped unread.

Deferred, with reason:
- MINOR 2 (`compare.py` unit handling for range keys, and a fraction value against a key without `%` on a percentage question): none of the five pilot keys reaches those branches; the rule and the code are fixed, reviewed and hashed before any other question's script is frozen.

Wording corrections (NIT 1, NIT 2):
- Addendum 2's "before any question script had run" should read "before any script produced a value": the 09:18 attempt ran and stopped in the loader.
- Addendum 2's control reading C2 is role-matched (Affected patients against Unaffected children, Carrier parents against Unaffected parents), not age-matched: the Age column is not used.
- The seal rests on the lane not reading plain files; the outputs are made read-only, and the methods page says the seal is procedural.
