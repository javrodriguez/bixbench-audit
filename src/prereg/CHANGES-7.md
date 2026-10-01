# E5a bix-3 rerun rule and parallel fit (lane, 30 Sep 2026, 12:12 EDT)

Stage bix3, repetition 1, started 11:48 in folder `runs/recorded-2026-09-30`; its prep step finished (121 s) and its single-threaded fit was still running at 12:09, when the lane stopped it by pid to keep the booking under 25 minutes.
The Mac was swapping heavily at the time (glitch-14: swap 13.7 of 14.3 GB, load over 200), which likely slowed it.
The fit had written 6 partial tables to `r1/fits-bix3/`; nobody has read them, and they stay in place, unread.
No bix-3 question script has run, so no bix-3 value exists.

- Rerun rule, narrowed from CHANGES-5b: only the failed stage is rerun, both repetitions, into a fresh folder `runs/recorded-2026-09-30-bix3`; the stages already recorded twice (chip, bix36, bix13) keep their folder, where run 1 and run 2 already share one folder.
- `q/bix-3-fit-v2.R` is `q/bix-3-fit.R` with DESeq2's own parallel mode (`BiocParallel::MulticoreParam(workers = 4)`, `DESeq(..., parallel = TRUE)`); the model, contrasts, cut-offs and outputs are unchanged.
- `run_recorded_v2.py` takes the manifest name as a sixth argument and, under `SCRIPTS-7.sha256`, runs `bix-3-fit-v2.R`; otherwise it is `run_recorded.py`.
- `verify_runs_v2.py` checks across several run folders (the last folder listed that holds an output is used, and its r1 and r2 must both be there).
- `SCRIPTS-7.sha256` lists every script the bix3 stage and the checks use; `SCRIPTS-7b.sha256` pins the v2 runner with it.
- The bix-3 stage runs again only after glitch-14 says Javier's deploys are done.
