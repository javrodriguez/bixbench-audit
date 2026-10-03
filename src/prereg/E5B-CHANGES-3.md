# E5b changes 3: origin checks after the keys and notebooks were read (lane, 1 Oct 2026, 19:31 EDT)

Written after repetition 1 of all ten questions had been recorded (light at 18:58, bix3 at 19:06, bix27 at 19:21) and after the keys were compared (19:25, `runs/e5b-recorded-2026-10-01/compare-r1.txt`, git-ignored because it quotes keys) and the ten reference notebooks were extracted and read (from 19:26).
Nothing here changes a pre-registered script or reading; every reading below is labelled "added after key", and its defensibility, where it could change a verdict, is Javier's to rule.

New scripts in `q/e5b/origin/`, run twice by `run_e5b.py` stage `origin` into `runs/e5b-origin-2026-10-01/`:
- `bix-13-q3-origin.R`: the notebook's three-sample exclusion (resub-5, -10, -33) with its design, counting gene-wise dispersions below 1e-05 (the notebook never prints that count).
- `bix-14-q2-origin.py`: the notebook's route (non-reference calls, intronic, intergenic and UTR rows removed, VAF < 0.3, effect labels, Control Parents minus BSyn Probands), with and without the "exome" row filter.
- `bix-52-q3-origin.py`: the notebook's chi-square function for both species, before and after the filter, plus a mutation witness and a check that the capsule's two length tables are identical.
- `bix-53-q3-origin-fit.R` and `bix-53-q3-origin.py`: the notebook's four-sample fit and filters in R DESeq2 with apeglm (an independent implementation of the notebook's pydeseq2), and the six-sample fit under the same filters.
- `bix-3-q4-probe.py`: the notebook's baseMean >= 10 added to the pre-registered padj and fold-change criterion, on the recorded fit tables.
- `bix-27-q2-origin.py`: the notebook's procedure (178 samples, log10, Ward, unseeded splits, consensus matrices clustered by Ward, raw label equality) under ten global seeds.
`run_e5b.py` gains the `origin` stage and `verify_runs_e5b.py` an optional job list; hashes in `E5B-SCRIPTS-3.sha256`, which supersedes SCRIPTS-2 for the origin runs (the recorded runs ran under SCRIPTS-2, whose files are unchanged except these two).
