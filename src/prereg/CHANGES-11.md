# E5a: rerunning adversarial review 2's probes (lane, 30 Sep 2026, 19:51 EDT)

Adversarial review 2 (claude-opus-5-5 for glitch-14, 19:20-19:40, `reviews/ADVERSARIAL-2.md`) found MAJOR 3, MINOR 8, NOTE 13; no verdict flipped.
**Every reading here was added after the keys were known**; none is a rubric reading, and the frozen pre-registration is unchanged.

- `q/bix-36-origin.R` (self-contained, reads only the bix-36 capsule): (A) the R DESeq2 rebuild of the notebook's six-column ANOVA, MLE and apeglm-shrunk; (C) the base-R rebuild of the 12 pre-registered readings with Fisher and Welch F, the pre-registration's independent implementation; (R) review 2's in-window RPKM reading.
- `q/bix-13-probes2.R` (derived from review 2's `probe2.R` part B, reading the capsule path from its argument): DESeq2's thresholded test at 1.5 and log2(1.5), normal-shrunk fold changes, and the notebook's three dropped samples with the question's cut-off, each with JBX97's DE set and the union as the denominator.
- Both run twice under a heavy slot (`mac_slot.py`, owner e5a-bix3) into `runs/review2-probes-2026-09-30/`; hashes in `SCRIPTS-11.sha256`.
- `ADDENDUM-4-PROPOSED.md` drafts the rule review 2 asks for (wrong key when the notebook computes a different quantity; reword when it computes the asked quantity under an unstated choice); it is Javier's ruling and not in force.
