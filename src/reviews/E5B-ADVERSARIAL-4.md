# E5b adversarial review, round 4 (fresh context, claude-opus-5-5, 1 Oct 2026, about 21:58-22:14 EDT)

Saved verbatim by the lane from the reviewer's report. **No MAJOR: the review loop stops here.** Its probes p52_zf_r and p3_apeglm are rerun under the lane's hashing (E5B-CHANGES-8).

**Scope.** I checked `notes/E5B-PROPOSED-VERDICTS.md` with Amendments 1-3 against:
- the rules: E5B-PREREG, E5B-CHANGES-1 to -7, PREREG, ADDENDUM-1, ADDENDUM-2 §4, ADDENDUM-4-PROPOSED-v4 and ADDENDUM-4;
- the scripts, including `origin/bix-52-q3-zf-lengths.py` and `run_zf.sh`;
- `compare-r1.txt`, the zf-lengths outputs and the review-1 and review-2 probe outputs;
- both pinned assembly reports, the bix-52 and bix-53 notebooks, and the ten question and key rows (read only).

**Probes.** All are in the lane's `reviews/r4-scratch/` and nothing else was written:
- `p52_contrib.py` → `.out`: per-chromosome contributions with the real lengths, and how the data's positions fit the assembly.
- `p52_zf_r.R` → `.out`: the real-length E1 readings in base R.
- `p3_apeglm.R` → `.out`: the bix-3-q4 apeglm route.

I ran each once, single-threaded. `p3_apeglm` took 4.2 minutes, over the ~3-minute guideline. That was the only overrun.

**There is no MAJOR.** Every proposed verdict, conditional and ruling still stands as amended.

## Amendment 3 (answering review 3) is correct and complete
- **M1, bix-52-q3.** The real lengths come from the pinned bTaeGut1.4.pri report. Its sha256 matches the pin `0e6042…1655`, and the file hashes match `E5B-SCRIPTS-7.sha256`.
  - The output figures (161.03 / 176.10 / 183.85 distinct sites; 594.76 / 632.56 / 652.00 sample rows) match the note, and r1 and r2 are identical.
  - Where the 161.0 comes from: chr32 contributes 67.2 (7 sites against 0.61 expected on 2.09 Mb) and chrZ 38.4. Even with chr32 removed, the statistic stays far above 50, so the wrong-key case no longer leans on any table.
  - The assembly choice holds up better than CHANGES-7 says. On many chromosomes the data's last CpG lies within about 1 kb of the assembly's chromosome end: chr11: 21,108,132 against 21,108,237; chr8: 31,249,895 against 31,251,066; chr1A: 71,567,216 against 71,569,005; chr5: 61,658,910 against 61,663,524.
  - The older bTaeGut1_v1.p cannot be the reference: chr11's last site lies beyond its 21,012,354 bp.
- **MINOR 1-2 and NIT 1-3:** applied as described (the K3 values cited, item 8 now carries the 1(c) question, the bix-27 asymmetry sentence, bix-13's inert filters, the header, and the bix-30 disclosure).
- **Count:** keep 1, reword 2, wrong key 1, conditional 5, undecided 1. This matches the table.

## MAJOR
None.

## MINOR

1. **bix-52-q3, rule (d): the second environment does not yet cover the real-length readings, which (a) now cites.** The 161-652 values come only from the Python script. My `p52_zf_r.R` uses base R `chisq.test` with the same lengths and site definition. It reproduces all six exactly: U2-E1 K1 183.8489, K2 161.0271, K3 176.0992; U3-E1 K1 651.9993, K2 594.7583, K3 632.5616. Fix: copy the probe under the lane's hashing (an E5B-CHANGES-8), run it twice, and cite R as the second environment for the real-length family too.
2. **E5B-CHANGES-7: a factual slip in why v1.p is ruled out.** CHANGES-7 says GCF_003957565.1 "lacks chromosomes 30-37 and W". The pinned v1.p report does have chromosome 30 (`scaffold_343_arrow_ctg1`, 6,068,150 bp). It lacks 31-37 and W. MINOR: the conclusion stands; the same report also has chr11 shorter than the data's last site. Fix: correct it in an E5B-CHANGES-8 and add the end-of-chromosome fit as the positive evidence for bTaeGut1.4.
3. **bix-3-q4: the route Javier ruled fair for bix-3 in E5a (apeglm) can now be reported, not just disclosed as untested.** From `p3_apeglm.R`, after the key: Control mice, one fit `~ Tissue`, P1, unshrunk padj < 0.05 at default alpha, apeglm-shrunk |LFC| > 1, genes DE in all three comparisons: **275**, outside 400-500; with baseMean >= 10 added, **233**; the same run's MLE intersection gives 557 and 469, agreeing with the lane's 522-578 and 442-484. So extending his E5a apeglm ruling would not give a reword. The conditional is unchanged. Fix: rerun the probe under hashing, replace the "Nor was the apeglm route" clause with these figures, and note in item 1 that the apeglm route misses.

## NIT

1. **`run_zf.sh`, `run_review1.sh`, `run_review2.sh`: the logged exit status is always 0.** In `echo "$(date …) … exit=$?"`, the `$(date)` substitution runs first and resets `$?`. `run_probe36.sh` is not affected. No consequence this time: every output is non-empty and r1 equals r2. Fix: capture `rc=$?` right after the command.
2. **bix-52-q3, "Does not claim":** "since the capsule holds no Zebra Finch lengths" now reads as if no Zebra Finch value was computed. Suggest: "which reading is right; on the real lengths every pre-registered per-base-pair reading gives 161-652."
3. **bix-52-q3:** add one line saying that chr32 (67.2) and chrZ (38.4) drive the real-length 161.0, and that the value stays above 100 without chr32.

## Confirmed without findings
- bix-7-q3, reword (minor): 11,896 and 13,047 accepted; 673 and 699 rejected.
- bix-14-q2, conditional: none of the 270 values is in 0.2-0.3, including the percent readings.
- bix-37-q2, reword (minor): R1 is 72,896,133.29, which rounds to the key; R2 (26.1) is rejected.
- bix-53-q3: the notebook's cells 14-16 do swap the labels, as the rule-4 finding says. The two-ruling conditional stands.
- bix-13-q3, bix-27-q2 and bix-30-q5 (keep): the logic as amended stands.
- bix-36-q5, undecided: the pre-registered synonym lists do not map any symmetry label onto "Normal", so undecided stands.
- bix-52-q3, wrong key: (a) holds with the real lengths. (b) cites ADDENDUM-1 §2. (c) is put to Javier, and remove is weighed. The key brackets the Jackdaw value, 49.638.

MAJOR 0, MINOR 3, NIT 3
