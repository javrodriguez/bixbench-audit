# E5a: rerunning adversarial review 1's probes (lane, 30 Sep 2026, 17:53 EDT)

Adversarial review 1 (claude-opus-5-5 for glitch-14, `reviews/ADVERSARIAL-1.md`, 17:17-17:51) found that the lane's pre-registered grid missed standard routes for bix-3 and that one published sentence was false.
On glitch-14's ruling, the lane reruns the review's probes twice under its own hashing, as dated additions outside the rubric.
**Every reading added here was added after the keys were known**, after the recorded run, the reference notebooks and review 1; none is a rubric reading, and the frozen pre-registration is unchanged.

- `q/bix-3-probes.R`: a global pseudo-count scale before rounding (x1, x10, x100), one fit over all Control samples or a fit per pair, and three fold-change estimators (MLE, apeglm, normal) for bix-3-q1 and bix-3-q3.
  At x100 some genes exceed R's 32-bit integer limit, which DESeq2's count matrix cannot hold; those genes are dropped and listed in the output (there is no numeric path in DESeq2's counts).
- `q/bix-13-variants.py`: the review's bix-13-q1 variant grid (the cut-off as a linear 1.5-fold change; the cut-off on JBX97 only; on JBX97 and JBX99 only; no cut-off), each against JBX97's DE set and the union, read from the recorded fit tables.
- Both run twice under a heavy slot (`mac_slot.py`, owner e5a-bix3) into `runs/review1-probes-2026-09-30/`; hashes in `SCRIPTS-10.sha256`.
