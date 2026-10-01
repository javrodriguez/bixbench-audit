# E5a evidence steps after the first recorded runs (lane, 30 Sep 2026, 11:39 EDT)

Recorded runs 1 and 2 of stages chip, bix36 and bix13 finished between 11:18 and 11:38 (log: `runs/recorded-2026-09-30/log.txt`).
As the pre-registration allows once a question's first recorded run exists, the lane then read the reference notebooks for bix-2, bix-7, bix-13 and bix-36 (extracted to `notebooks/`, never into the workspace).

- `q/bix-13-origin.R` is new: not a reading of either question, but a reconstruction of the notebook's own steps (three samples dropped, `~ Replicate + Strain + Media`, padj < 0.05 alone, Venn regions as shares of the union), to test whether it reproduces the keys of bix-13-q1 and bix-13-q2.
  It was written after the lane saw the recorded values and the notebook, and is labelled evidence of the keys' origin only; it never enters the rubric.
- The bix-13 notebook records R 4.4.2 with Bioconductor 3.20, which ships DESeq2 1.46.0, the version in the pinned environment; the lane treats that as meeting the pre-registration's "package versions recorded in the capsule's reference notebook" for bix-13, and says so in the notes.
- No reading of any question was changed or added.
