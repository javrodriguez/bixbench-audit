# E5a: all ten recorded; bix-13 origin; a post-hoc bix-3 reading (lane, 30 Sep 2026, 16:42 EDT)

## Recorded run complete

- Stage bix3 ran both repetitions in `runs/recorded-2026-09-30-bix3` (16:23-16:39, heavy slot `e5a-bix3` via `mac_slot.py`), byte-identical, fit tables included.
- `verify_runs_v2.py` over both run folders: every one of the ten questions, both fit steps and the bix-3 prep are identical between repetitions, and bix-2-q1, bix-7-q1, bix-36-q1 and bix-13-q1 equal the pilot's values reading for reading: ALL CHECKS PASS.
- `q/bix-13-origin.R` ran twice (16:40, 16:41), byte-identical (`runs/recorded-2026-09-30-origin/`, sha256 `5c57b306…`).
  With the notebook's three samples dropped, the region "DE in JBX97 and JBX99, not JBX98" is 464 of 4,387 genes in the union, 10.577%, which rounds to bix-13-q1's key; the region "DE in JBX98 only" is 166, bix-13-q2's key.

## A reading added after recorded run 1 and after the notebook (P3)

- After bix-3's first recorded run the lane read its reference notebook, as the pre-registration allows.
  Cell 29 turns the normalised table into integer pseudo-counts by scaling each sample to counts per million over all genes and rounding; the lane's pre-registered readings only rounded (P1) or rounded with unit size factors (P2).
- The question bix-3-q1's words ("scale to integer pseudo-counts") are consistent with P3, so the lane missed a reading it should have named.
- `q/bix-3-fit-p3.R` and `q/bix-3-p3.py` compute P3 for bix-3-q1, q2 and q3, every reading marked "added after recorded run 1 and the notebook"; none enters the rubric, and whether P3 is defensible is Javier's ruling.
- bix-3-q3 also gets B10 (baseMean >= 10 added, which its words do not state and the notebook's cell 41 applies), marked not defensible, as origin evidence only.
- The notebook fits with pydeseq2 in Python; the lane fits with R DESeq2 1.46.0, so P3 values need not equal the notebook's printed numbers (846, 766, and the interval 0.0312 to 0.0356).
- Hashes: `SCRIPTS-8.sha256`. Run twice under a heavy slot into `runs/recorded-2026-09-30-p3`.
