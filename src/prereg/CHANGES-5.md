# E5a changes after the recorded-run code review (lane, 30 Sep 2026, 10:46 EDT)

A fresh-context review (claude-opus-5-5) of the CHANGES-4 code returned MAJOR 4, MINOR 6, NIT 4.
No recorded-run script had produced a value; the only values seen are the pilot's (bix-2-q1, bix-7-q1, bix-13-q1, bix-36-q1, and the control).
New hashes: `SCRIPTS-5.sha256`, which supersedes SCRIPTS-4 and SCRIPTS-4b for the recorded run.

## MAJOR fixes

1. The comparator's other-scale rule was wider than addenda 1 and 2 allow.
   `compare2.py` now compares a value on its own scale only, except for a question whose words ask for a percentage while its key has no % sign (bix-2-q1 and bix-3-q2 say "proportion" and are not in that set; bix-2-q2 is).
   An other-scale match is reported as "other-scale", tallied apart, and can support a units reword, never a keep.
2. Readings added after the pilot could flip a verdict through the rubric summary.
   `compare2.py` now summarises three groups apart: pre-registered defensible readings (the only group the rubric reads), readings added after the pilot (candidates whose defensibility is Javier's ruling), and non-defensible readings (evidence of the key's origin only).
   This covers bix-13-q1's C2 (natural-log cut-off, not a named convention in DESeq2, edgeR or limma) and bix-36-q1's new normalisations.
3. bix-3-q2 now adds E3 (bix-3-q1's own criterion, including baseMean >= 10), N4 (genes with baseMean >= 10) and the A1-M2 fit, before any bix-3 value existed.
4. bix-36-q3 now crosses its readings with three normalisations (as given, counts per million, median-of-ratios size factors; `bix36_common.py`), before its first run.
   bix-36-q1 gets the same normalisations in `bix-36-q1-v2.py`, marked "added after pilot run 1"; its as-given readings are the pilot's, unchanged.

## MINOR and NIT fixes

- The runner checks every script against SCRIPTS-5, the question file and the lockfile against their pins, refuses to overwrite an earlier attempt's outputs, records R `sessionInfo()` with `.libPaths()` and the Python package list and `sys.path` per repetition, and runs R with `--vanilla` and Python with `-s`.
- `verify_runs.py` checks run 1 against run 2 byte for byte (outputs and fit tables), and checks the recorded values against the pilot's for bix-2-q1, bix-7-q1, bix-36-q1 and bix-13-q1.
- bix-3-q1 and bix-3-q3 add FT, DESeq2's test against |log2 fold change| > 1 (`lfcThreshold = 1`), before any bix-3 value existed.
  For bix-13-q1 that reading was not examined; any note on it says so.
- Negative batch-corrected values in bix-36 are set to 0 and counted, never dropped silently.
- Fit tables are read with `float_precision="round_trip"`.
- `compare2.py` handles a text value before any number conversion.

## Correction to CHANGES-4

The Mac's Homebrew R has the same DESeq2 1.46.0 and apeglm 1.28.0 as the conda environment, so it is not a second environment in the pre-registration's sense (the reference notebook's recorded versions, or an independent implementation).
The pilot-versus-recorded comparison checks the pipeline and the install only.
"Wrong key" still needs the notebook's versions or an independent implementation; until then such a proposal stays "undecided (wrong key suspected)".
