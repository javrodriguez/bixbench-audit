# E5a runner fix (lane, 30 Sep 2026, 10:43 EDT)

After the pinned environment was created (10:40) and before any recorded-run script produced a value:
the pinned R segfaulted loading DESeq2, because it searched the user library `~/Library/R/x86_64/4.4/library` (packages built for the Mac's Homebrew R) ahead of its own.
`run_recorded.py` now runs every job with R_LIBS_USER pointed at a missing folder, R_LIBS empty, the user R profile and environment files set to /dev/null, Python user site-packages off, LC_ALL=C and TZ fixed.
With that, R loads DESeq2 1.46.0 and apeglm 1.28.0 from the environment's own library only.
Lockfile: `envlock/conda-lock.txt`, 202 lines, sha256 `ef64e570a912d533554dff4f6db8cbbae21bf31245268bf93fd294afa270e46f`; platform x86_64-apple-darwin13.4.0.
The runner's new hash is in `SCRIPTS-4b.sha256`; every other script is as in `SCRIPTS-4.sha256`.
