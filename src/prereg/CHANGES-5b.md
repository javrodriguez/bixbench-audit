# E5a changes after the confirming review (lane, 30 Sep 2026, 10:58 EDT)

The confirming review of CHANGES-5 (claude-opus-5-5, fresh context) returned MAJOR 0, MINOR 4, NIT 4; the review loop stops here.
Before any recorded-run script produced a value:

- `q/bix36_common.py`: Z1 is the table exactly as given (unclipped, as in the pilot); negatives are set to 0 for Z2 and Z3 only, and counted for all genes and for miRNA rows apart.
- `verify_runs.py`: requires every expected output (ten questions, two fit steps, the bix-3 prep, both fit folders) in both repetitions, and compares fit folders both ways.
- `q/bix-3-q2.py`: drops E1 and E2 against N4, whose numerators are not subsets of N4's genes.
- `run_recorded.py` is pinned in `SCRIPTS-5b.sha256` together with `SCRIPTS-5.sha256`; the lane checks SCRIPTS-5b before every stage.
- Rerun rule: if a stage fails, both repetitions of every stage are rerun into a fresh run folder, so run 1 and run 2 always share one folder; failed folders are kept and listed.
- Noted, not changed: among the ten, only bix-2-q2 is in the percent-words set, and its values are already in percent, so the other-scale path cannot fire for the ten; `graders.py` is checked by the hash in PREREG v0 when the pilot probe ran, not by `compare2.py`; bix-3-q2 has no FT reading; fit and prep outputs are logs, excluded from what `compare2.py` reads.
