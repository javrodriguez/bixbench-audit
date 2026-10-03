# E5b adversarial review, round 2 (fresh context, claude-opus-5-5, 1 Oct 2026, about 21:14-21:31 EDT)

Saved verbatim by the lane from the reviewer's report; its probes are rerun under the lane's hashing (E5B-CHANGES-6).

**Scope.** I checked `notes/E5B-PROPOSED-VERDICTS.md` (with Amendment 1) against these sources:
- the rules: E5B-PREREG, E5B-CHANGES-1 to -5, PREREG, ADDENDUM-1 and -2, ADDENDUM-4-PROPOSED-v4, ADDENDUM-4 and CHANGES-5;
- the recorded, origin, probe36 and review-1 outputs, plus `compare-r1.txt`;
- the notebooks and the capsule data.

**Probes.** All are in the lane's `reviews/r2-scratch/`, and nothing else was written:
- `q27_l3seeds.py`, with outputs `q27_l3seeds.out`, `q27_l3_*.out` and `q27_l3_summary.txt`;
- `p52_r.R` with `p52_r.out`;
- `p52_witness.R` with `p52_witness.out`.

**Figures I re-derived and found correct:**
- bix-3-q4: A1-M1 442-484, A2-M2 438-447, A1-M2 145-159, A3 246-264, A2-M1 and A4 812-919, and p3's 18 of 21,251 genes.
- bix-27-q2: the 34-seed spread (matched 31/34 in key; raw labels 27-70 for 13 seeds, 169-175 for the rest).
- bix-36-q5: the per-column skewness and kurtosis figures (MLE |skew| 0.517-0.743 plus -0.493; apeglm CD8_vs_CD4 2.55 and 28.1; pooled 0.04-0.16 and 7.6-10.8).
- bix-52-q3: chr4 = 8,011,800, chr32 = 736,907, the ZF and JD length files identical under `cmp`, and the E2 range 713-2,163 and E3 range 192-450.
- bix-14-q2: 2/6 against 2/19; one row moves the difference by 0.048-0.133.
- bix-53-q3: 22 with four samples and 20 with six, under p or padj.
- bix-30-q5: Benjamini-Hochberg 32 at H1-N1-T1.

## MAJOR

**M1 · bix-27-q2: "reword under the frozen rubric" rests on a single seed. The pre-registration itself named exactly this as evidence for remove.**
- The one accepted pre-registered reading, L3-Q1-R1-K1-S1 (168), is the same construction the note calls "the most seed-sensitive" (168 / 187 / 200). The note never says that the accepted reading and the seed-sensitive one are the same.
- The frozen script header (`bix-27-q2.py`, written before any run) says: "The answer rests on seeds the words do not fix; readings R1-R3 disagreeing is evidence for 'remove'."
  - For this construction R1-R3 disagree on acceptance itself: one in the key, two out.
- **Probe `q27_l3seeds.py`.** It is the pre-registered code, unchanged, run over more `default_rng` seeds.
  - It reproduces seed 0 = 168.
  - The other seeds: 1 → 209, 2 → 208, 3 → 201, 5 → 195, 6 → 206, 8 → 193, 9 → 193, 11 → 203, 12 → 183, 42 → 187, 2024 → 200.
  - So the pre-registered acceptance holds for **1 seed of 12**.
- The matched-label route that lands in the key 31 times in 34 is the notebook's procedure: 178 de-duplicated samples, log10, Ward, co-association consensus, plus label matching.
  - That route was added after the key, so under E5B-PREREG ("any E5b reading added after a key is seen waits for Javier's own ruling") it cannot carry an unconditional reword.
- **On whether the accepted reading is defensible.** It is defensible only because it was pre-registered. Two things weaken it:
  - It clusters 222 columns, which include 44 columns from 21 individuals whose metadata conflict. Even sex differs (cells 23-24), which is why the notebook drops them.
  - It uses complete linkage on unlogged values reaching 4.9e6.
  - The rubric still counts it, but its acceptance is a seed event, not a property of the reading.
- **Fix:**
  1. Make bix-27-q2 conditional: **reword if Javier rules the notebook's matched-label route fair; otherwise remove.** In the "otherwise" branch, the only pre-registered acceptance is a seed-0 event, which the frozen header names as remove evidence.
  2. In Readings, say plainly that the 168 is that most seed-sensitive construction, and add the 12-seed result.
  3. Re-pose ruling 7 accordingly.

**M2 · bix-36-q5: the conditional "no → remove" runs backwards. The remove clause does not decide the question now, and Javier's "no" would not make it decide either.**
- The lane's reason for remove ("a shape question with an exact text key and no stated test has no single target") does not depend on Javier's ruling. If it held, it would hold now, in both branches.
  - If he rules the by-eye "normal" fair, a fair reading reaches the key and the frozen rubric gives reword, whatever remove's clause says.
- If he rules "no", he is in effect adopting test-based normality. Then the normality facet has a single target, "not normal":
  - the pre-registered L2 readings give "not normal" in 54 of 54;
  - all 12 rebuilt notebook columns fail normality.
  - That argues *against* "no single target". The key is then rejected by every reading, but 1(c) still fails (a visual judgement departs from no variable, group or stated threshold), so the outcome is **undecided under rule 3**, not remove.
- **Does the frozen remove clause already decide it?** No.
  - Its only example (an interval keyed as a range) was written after bix-3-q2's key was read (ADDENDUM-1 §7).
  - The four label facets (symmetry, normality, tails, modality) are distinct conventions that each give one consistent answer. That is not an absence of a target.
- So the current "undecided" is right.
- **Fix:** change the "what would settle it" sentence and ruling 5 to "no → undecided stands (rule 3); yes → reword". If the lane wants remove, it must argue "no single target" now, as a property of the question, and put that to Javier separately.

## MINOR

1. **bix-52-q3, (d): the second environment does not cover the readings (a) now rests on.**
   - The origin script is Python and reproduces only the length-weighted construction (458.27 / 49.638). The pre-registered readings are Python too.
   - Probe `p52_r.R` (base R `chisq.test`, the notebook's tool) reproduces: U2-E3-K3 = 204.1224 (recorded 204.122); U3-E2-K3 = 1687.659 (recorded 1687.659); U3-E3-K3 = 449.0167 (recorded 449.017).
   - The mutation witness also moves the length-weighted value, which the note now says is not a Zebra Finch statistic. Probe `p52_witness.R` (20 sites planted on chr1) moves U2-E3-K3 from 204.12 to 216.53, and U2-E2 (chromosomes with sites) from 727.83 to 802.83.
   - **Fix:** cite R as the second environment for the length-free readings, and add the length-free witness (rerun both under the lane's hashing).
   - Wrong key is otherwise reached as rule 1 is written: (a) 0 of 32; (b) the only in-key route is the Jackdaw data; (c) the key arises at cell 39, on the other species' data.
   - Reading the named genome as "the variable measured" is sound: a count measured on Jackdaw samples is a different variable from the one the words name. It is correctly flagged as Javier's call.
2. **bix-52-q3, (b).** The lane itself rules the Jackdaw route not defensible. Cite ADDENDUM-1 §2 ("a reading … that contradicts the question's words is not defensible"), as the bix-13-q1 precedent did, so it is clear the lane is not ruling in Javier's place.
3. **bix-14-q2 overreaches.** "Then the 'not fair' branch would be wrong key" skips (d). bix-14 has no second environment and no mutation witness. **Fix:** "wrong key suspected, pending a second environment and a witness".
4. **bix-53-q3 misses a separate finding (rule 4).**
   - Cells 15-16 label KL1-3 "WT" and WL1-3 "KD", the reverse of cell 14's own description and of the question's "KD condition (KL)".
   - Cell 49's "WT vs KD" contrast is therefore knockout against wild type under swapped names.
   - The overlap count is unaffected, because the filter is |lfc| > 1 on all genes. Report it as a rule-4 defect.
5. **bix-37-q2: the lean toward keep would strike a pre-registered reading after the key was seen.**
   - The frozen rubric reads pre-registered readings as given, and post-key rulings exist only for readings added later. Here the lane leans toward discarding a pre-registered reading that rejects the key, while in bix-27 it keeps a weak pre-registered reading that accepts it.
   - **Fix:** state the frozen outcome (reword) as the proposal, and present the keep lean as a request to set aside a pre-registered reading, naming the precedent it would set.
   - The substance of the lean is right: one sheet, one row per protein, and the Normal column is linear.

## NIT

1. **bix-36-q5.** "D'Agostino-Pearson p printed as 0" is not true of every reading: the largest pre-registered p is 4.7e-129. Say "p ≤ 5e-129".
2. **bix-3-q4.** Javier's E5a ruling that apeglm fold changes are fair was worded "bix-3". The apeglm route was not computed for q4. Add it to "Does not claim" so he knows that a route he already ruled fair is untested here.
3. **bix-27-q2.** "Most constructions move by 9 or less" holds, but two of the 18 move more: L2-Q2-K1-S2 by 18 and L3-Q2-K1-S2 by 10. Say "16 of 18".

## Confirmed without findings

- **bix-7-q3, reword:** cell 15 gives 11,896.
- **bix-30-q5, keep:** all 36 readings give 0; the intersection reading is disclosed.
- **bix-13-q3:** the conditional is right (7 for every row filter on 33 samples, 4 for 36).
- **bix-3-q4:** the conditional is right under rules 2 and 3. The per-gene scaling is rule 4 by addendum 4's own example, and the cohort is open.
- **bix-53-q3:** the conditional with its two rulings is right.
- **bix-14-q2:** the figures (0.228 against -0.014) are right.
- **bix-52-q3:** wrong key over remove is sound, because the length-free readings E2 and E3 are pre-registered, need no lengths, and all miss the key.
- **Proposed count** (keep 1, reword 3, wrong key 1, conditional 4, undecided 1) is consistent with the table. After M1, reword drops to 2 and the conditionals rise to 5.

MAJOR 2, MINOR 5, NIT 3
