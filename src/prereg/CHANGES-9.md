# E5a: the P3 result, a correction to CHANGES-8, and the bix-3 origin rebuild (lane, 30 Sep 2026, 17:10 EDT)

- P3 ran twice (17:04-17:09, heavy slot `e5a-bix3`), byte-identical (`runs/recorded-2026-09-30-p3/`).
  bix-3-q1: 105 to 107 genes, none in the key range; bix-3-q2: 19 of 270 readings in range; bix-3-q3: 727 to 731 with one fit over all Control samples (in range), 846 with pair fits (out of range).
- Correction to CHANGES-8: the lane read cell 29 as per-sample scaling. Reading cells 26-27 shows the notebook's table has samples as rows, so its `.sum()` is per gene: each gene is scaled to total one million over the 90 samples, after genes with a total below 10 are dropped.
  P3 (per-sample counts per million) is therefore the lane's own reading of the words, not the notebook's procedure; it stays marked "added after recorded run 1 and the notebook", outside the rubric.
- `q/bix-3-origin.R` rebuilds the notebook's per-gene scaling, Control-only fit, cell-41 DEG criteria, all-gene denominator and Wilson interval in R DESeq2, as evidence of the keys' origin only; the notebook itself used pydeseq2, so small differences are expected.
  Scaling each gene to the same total is not a standard pseudo-count scaling and is not proposed as a defensible reading.
- Hashes: `SCRIPTS-9.sha256`. Run twice under a heavy slot into `runs/recorded-2026-09-30-origin3/`.
