# E5a: the bix-3 probe split by scale (lane, 30 Sep 2026, 18:15 EDT)

- `q/bix-3-probes.R` (all three scales in one run) ran 17:54-18:15 under a heavy slot and had not finished when the slot neared its 25-minute limit; the lane stopped it by pid and released the slot. It wrote no output (`runs/review1-probes-2026-09-30/bix-3-probes.run1.json` is empty and kept as a record).
- `q/bix-3-probes-v2.R` is the same probe with the scale as an argument (one of 1, 10, 100 per run) and DESeq2's parallel option on both `lfcShrink` calls (the model, readings and outputs are unchanged).
- Each scale runs twice, one or two runs per slot, into `runs/review1-probes-2026-09-30/bix-3-probes-K<scale>.run<N>.json`.
- The bix-13 variant grid ran twice at 17:53-17:54, byte-identical: 192 variants, 0.57% to 52.70%, none rounding to 10.6%.
- Hashes: `SCRIPTS-10b.sha256`.
