# E5b adversarial review, round 3 (fresh context, claude-opus-5-5, 1 Oct 2026, about 21:44-21:53 EDT)

Saved verbatim by the lane from the reviewer's report. Its probe (`p52_lenbound2.py`, a bound, not a reading) was not rerun; the lane answered its MAJOR instead by computing the readings with real lengths (E5B-CHANGES-7).

**Scope.** I checked `notes/E5B-PROPOSED-VERDICTS.md`, including Amendments 1 and 2, against these sources:
- the rules: E5B-PREREG, E5B-CHANGES-1 to -6, PREREG, ADDENDUM-1, ADDENDUM-2 §4, CHANGES-5, ADDENDUM-4-PROPOSED-v4 and ADDENDUM-4;
- the outputs: `compare-r1.txt`, the recorded, origin and review-2 outputs;
- the notebooks for bix-13, bix-27, bix-30 and bix-52, and the bix-37 workbook;
- the question and key rows (read only).

**Probes.** I wrote only two, both in the lane's `reviews/r3-scratch/`:
- `p52_lenbound.py` is a first attempt; its optimiser stalled, so ignore it.
- `p52_lenbound2.py`, with output `p52_lenbound2.out`, is the exact convex bound. It ran in the pinned conda python (`-s -P`), single-threaded, in under 10 seconds.

Nothing else was written.

**Amendments 1 and 2.** Every fix promised for round 2's M1, M2, MINOR 1-5 and NIT 1-3 is present and correctly applied:
- bix-27-q2 is conditional, with the 12-seed result and "16 of 18".
- bix-36-q5 reads "no → undecided stands".
- bix-52-q3 names R as the second environment, adds the length-free witness and cites ADDENDUM-1 §2.
- bix-14-q2 reads "wrong key suspected".
- bix-53-q3 has the swapped-label finding.
- bix-37-q2 states reword as the proposal.

The proposed count (keep 1, reword 2, wrong key 1, conditional 5, undecided 1) matches the table.

## MAJOR

**M1 · bix-52-q3 (wrong key): "no Zebra Finch reading, with or without lengths, reproduces [the key]" is not supported. The capsule's own data cannot keep the per-base-pair reading out of 48-50. That sentence is the stated reason for choosing wrong key over remove.**

Where: the "Remove, weighed" paragraph, and rule (a), which still says "No pre-registered reading accepted".

Evidence:
- The note itself says the length file is the Jackdaw table (E1 values are "not a Zebra Finch statistic"). The "Does not claim" line says the true Zebra Finch value is unknown. Round 1's p52b shows a table within ×0.25-×4 reaches 27.9. All three contradict "with … lengths".
- Probe `p52_lenbound2.py` needs no outside data:
  - Each chromosome must be at least as long as its last observed CpG position. Those positions sum to 972.2 Mb, and chr4's last site is at 69.8 Mb, against the table's 8.0 Mb.
  - The genome total is capped at G.
  - The exact minimum of the per-base-pair chi-square on the 291 filtered distinct sites is:

| Genome cap G | Chromosomes holding filtered sites | Every chromosome in the data |
|---|---|---|
| 1,000 Mb | 55.8 | 76.4 |
| 1,060 Mb | 36.6 | 47.0 |
| 1,200 Mb | 20.8 | 27.3 |

  - At the length lower bounds the value is 157-166. The set of allowed length tables is connected, so every value between that and the minimum is reachable.
  - So at roughly the Zebra Finch genome size (about 1.06 Gb; the size comes from my training knowledge, not checked), a length table consistent with the data can put the per-base-pair statistic inside 48-50.
- I expect the real value is far above 50. That belief rests on outside knowledge I could not check offline: chrZ holds 51 filtered sites on about 73 Mb, which contributes about 40 by itself, and chr32 is a microchromosome holding 7 sites. It is not evidence.
- Rule check:
  - The frozen v0 wrong key needs "no defensible reading gives a value the key accepts".
  - The note calls the per-base-pair reading "the most natural sense". Its value is uncomputable from the capsule and not excluded from the key.
  - The eight E1 readings are still counted among the "32 rejected", although the note now says they are not Zebra Finch statistics.
  - Without them, wrong key rests on E2 (equal count per chromosome) and E3 (proportional to all age-related sites, which tests homogeneity with the unfiltered sites rather than uniformity across the genome). Both are pre-registered, but they are the strained readings.
  - The case for wrong key is in truth provenance: the narrow key brackets the Jackdaw value 49.638. The rubric asks for more than provenance.

Fix (either one):
1. **Fetch and pin the real lengths, then compute E1.** Get the chromosome lengths of the Zebra Finch assembly that matches the data's naming (1A, 4A, 29-37, W, Z). Pin them in a dated E5B-CHANGES file, as CHANGES-1 did for bix-53's GTFs. Compute U2/U3-E1 over chromosomes holding sites and over every data chromosome, and run it twice.
   - If the values miss 48-50, wrong key rests on every reading family and the sentence can stay with that evidence.
   - If they land in it, the proposal must change.
2. **Or, without that,** delete "with or without lengths"; state that the per-base-pair reading cannot be computed from the capsule, and that bounds anchored on the data do not exclude the key (cite this probe); drop the eight E1 values from rule (a)'s count; re-pose item 8 so that remove ("a required file is missing", for the most natural reading) is at least co-equal. Wrong key then rests on provenance plus the E2 and E3 readings, and Javier should be told exactly that.

## MINOR

1. **bix-52-q3: "the readings that need no lengths" still depend on the Jackdaw table.** K1 and K2 take their chromosome set from that table: K1 adds its chromosomes with no Zebra Finch sites, and K2 drops 1A and 4A, which hold 26 sites. Only K3 is free of the table: U2-E2-K3 887.0, U2-E3-K3 204.1, U3-E2-K3 1,687.7, U3-E3-K3 449.0, all far from 48-50. Fix: cite the K3 values as the length-free and table-free support, and say that K1 and K2 use the Jackdaw chromosome list.
2. **bix-52-q3: a ruling is missing from "For Javier".** The rule (c) line says reading the named genome as "the variable measured" under rule 1(c) is "Javier's call". Item 8 asks only wrong key or remove. Fix: add that 1(c) question to item 8, as item 9 does for bix-14.
3. **bix-27-q2: say why the randomness ground for remove does not decide the "yes" branch.** "Rests on randomness the words do not fix" is a property of the question; round 2 used exactly that argument on bix-36. It also bites in the "yes" branch, where 3 of 34 seeds fall below 160. The asymmetry can be defended: in the "no" branch the only acceptance is a 1-in-12 seed event, while in "yes" the range absorbs 91% of seeds and the proposed words fix a seed. Fix: add one sentence saying so, so the conditional does not read as remove being decided by Javier's ruling.

## NIT

1. **bix-13-q3: the three row filters do nothing.** Every fit has `genes_in_fit` 5,828 under K1, K2 and K3, both with 36 samples and with 33. So "every row filter gives 4" and "7 under every row filter" are one reading reported three times. Say the filters are inert.
2. **Header: stale.** It still says "E5B-CHANGES-1 to -4" and lists only the recorded, origin and probe36 evidence. Add CHANGES-5 and -6 and the review-1 and review-2 probe folders.
3. **bix-30-q5 (the keep holds): an extra disclosure.** The notebook (cell 16) itself prints 0 under each of BH, BY and Bonferroni (49 unadjusted), whereas the lane's readings give BH up to 32. The difference comes from the two excluded samples, the test (the notebook calls R's default `t.test`, Welch) and the log2(Ct) scale, not from the key. Worth a clause in "Also noted"; it does not change the keep.

## Confirmed without findings

- bix-7-q3, reword (minor): 11,896 and 13,047 accepted, 673 and 699 rejected; cell 15 matches.
- bix-13-q3, conditional: cells 18-21 confirm the exclusion of resub-5, -10 and -33 and the design. The notebook never prints the count; 4 with 36 samples, 7 with 33.
- bix-14-q2, conditional: 2/6 − 2/19 = 0.228; the classification of the filter is correctly left to Javier.
- bix-3-q4, conditional: the nearest unfiltered readings are 522-578 (A1-M1, E2, intersection); A2-M2 on E2 without baseMean gives 779-803; the route through A1-M1 or A2-M2 with baseMean is as stated.
- bix-27-q2: the notebook's cells 55-64 match the described route (unseeded `randint`, consensus matrices fed to Ward, 50 bootstraps); the 54-reading grid adds up (3 × 2 × 3 × 3).
- bix-36-q5, undecided: the logic stands as amended.
- bix-37-q2, reword (minor): one sheet, one ENO1 row, Normal = 72,896,133.29.
- bix-53-q3, conditional with two rulings: stands.
- bix-52-q3: cells 14, 36 and 39 confirm the Jackdaw file saved under the Zebra Finch name, ZF 458.27 (df 29) and JD 49.638 (df 19); 1A plus 4A hold 26 of the 291 filtered sites; the witness output (204.12 → 216.53; 727.83 → 802.83) matches the review-2 probe outputs.

MAJOR 1, MINOR 3, NIT 3
