# E5b changes 2: missing Ct values in bix-30 (lane, 1 Oct 2026, 18:58 EDT)

Recorded run, stage light, repetition 1 (started 18:53:41): eight jobs exited 0; bix-30-q5 stopped at its own assert (`np.isfinite`) before computing any value, because the Ct sheet has 22 blank cells (the error text was read; no output exists).
No E5b key has been read and no E5b output has been opened.

- `q/e5b/bix-30-q5.py` adds reading H for missing Ct values: H1 left out of that miRNA's test and of the sample's global mean; H2 set to Ct 40 (the conventional cycle limit for an undetected target); H3 miRNAs with any missing value left out, the corrections running over the rest.
- `run_e5b.py` takes the manifest name as an eighth argument (default `E5B-SCRIPTS-1.sha256`), as E5a's runner did in CHANGES-7.
- `E5B-SCRIPTS-2.sha256` lists every file again with the two new hashes; it supersedes SCRIPTS-1 for all later runs.
- Rerun rule: the failed attempt's folders are kept unread as a record, renamed `runs/e5b-recorded-2026-10-01-attempt1/` (workspace) and `fits-2026-10-01-attempt1/` (lane); the whole light stage then runs twice, from repetition 1, in fresh folders with the original names.
