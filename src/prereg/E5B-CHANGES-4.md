# E5b changes 4: the bix-36-q5 origin probe (lane, 1 Oct 2026, 20:29 EDT)

Written after the keys and the reference notebooks were read and the origin stage (CHANGES-3) was recorded twice, byte-identical.
The pre-registered bix-36-q5 readings used simple per-gene log ratios; the notebook (cells 46-49) instead pooled the six comparison columns of three pydeseq2 fits and judged their histograms "normally distributed" by eye.
`q/e5b/origin/bix-36-q5-origin-fit.R` rebuilds those columns in R DESeq2 (as E5a's `bix-36-origin.R` part A; negative batch-corrected values set to 0 before rounding, which E5a's rebuild did not need to state), MLE and apeglm, natural log; `bix-36-q5-origin.py` applies the pre-registered label conventions to the pooled values and to each column.
`run_probe36.sh` runs both twice and compares; every reading is "added after key".
Hashes: `E5B-SCRIPTS-4.sha256` (these three files and this note).
