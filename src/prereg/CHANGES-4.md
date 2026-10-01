# E5a changes for the recorded run (lane, 30 Sep 2026, 10:37 EDT)

Written after addendum 3 (Javier's pick, A′) unsealed the pilot, and before any new script below produced a value.
The pilot's compared values are in `runs/pilot-2026-09-30/compare.txt` (local evidence; it quotes keys).

## The recorded run's environment

- A conda environment solved by micromamba 2.0.5 (`tools/micromamba.tar.bz2` sha256 `d8ae81a89dbddf88dcf7e31c68a6f9633b95898ff22adc549b9bca034344512a`) from conda-forge and bioconda with strict channel priority: R 4.4.3, DESeq2 1.46.0, apeglm 1.28.0, jsonlite, Python 3.12, pandas 2.2.3, openpyxl 3.1.5, numpy 2.1.3, scipy 1.14.1, pydantic 2.9.2 (198 packages).
- Its explicit lockfile (`env/conda-lock.txt`, every package URL with its md5) is written after creation and hashed.
- The Mac's own R 4.4.3 and uv Python, which ran the pilot, are the second environment for any "wrong key" proposal (the reference notebooks' recorded versions are read only after the recorded run).
- The Anaconda install on this Mac (conda 4.12) was tried first and abandoned after an 11-minute unfinished solve.

## Shared fit steps (one script per question still computes each question's value)

- `q/bix-13-fit.R` fits every design and model once and writes tables; `q/bix-13-q1.py` and `q/bix-13-q2.py` read them.
  `q/bix-13-q1.py` replaces `q/bix-13-q1.R` (the pilot's version) with the same readings, so on the same data and versions its before-pilot readings must reproduce the pilot's values exactly; that equality is checked and reported.
- `q/bix-3-fit.R` fits the bix-3 models once; `q/bix-3-q1.py`, `q/bix-3-q2.py`, `q/bix-3-q3.py` read them.
  `q/bix-3-q1.py` replaces `q/bix-3-q1.R`, which never produced a value (stopped at the pilot's booking end).
- Reason: machine time; the pilot's single bix-13 script took about 10 minutes a run, and the Mac is booked in slots under 25 minutes.

## Readings added

- bix-3-q1, before any bix-3 value existed: M, whether the dentate-gyrus samples share the fit (M1) or only the two blood tissues are fitted (M2).
- bix-13-q1, **after pilot run 1**, marked "added after pilot run 1" in the output:
  C2, the cut-off read as a natural-log fold change (|ln FC| > 1.5), because "logfold" does not name a base;
  N2, the union of the three strains' DE genes as the denominator, not a defensible reading of the words, recorded only as a candidate origin of the key.
  The pilot showed every before-pilot reading between 48% and 65% against a key of 10.6%; these readings were added knowing that.
- New questions (bix-2-q2, bix-3-q2, bix-3-q3, bix-13-q2, bix-36-q3): readings are in each script's header, written before its first run.

## The comparator (review round 3, MINOR 2)

- `compare2.py` replaces `compare.py` for the recorded run; `compare.py` stays as the pilot ran it.
- A fraction or percent value is compared on its own scale and on the other one (x100 or /100) whenever the key does not fix the scale with a % sign, for range and numeric keys alike; the output says which scale matched.
- It prints a per-question summary of defensible readings accepted and rejected.

## Unchanged

- bix-2-q1, bix-7-q1 and bix-36-q1 run their frozen pilot scripts (SCRIPTS-3.sha256).
