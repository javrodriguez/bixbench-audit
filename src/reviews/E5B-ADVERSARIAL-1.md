# E5b adversarial review, round 1 (fresh context, claude-opus-5-5, 1 Oct 2026, about 20:36-20:51 EDT)

Brief: break every proposed wrong key, undecided and remove; test every keep, reword and conditional. Saved verbatim by the lane from the reviewer's report; the reviewer's probes are rerun under the lane's hashing (E5B-CHANGES-5).

I reviewed `notes/E5B-PROPOSED-VERDICTS.md` against E5B-PREREG, E5B-CHANGES-1 to -4, PREREG, ADDENDUM-1, -2, -4-PROPOSED-v4 and ADDENDUM-4.
I also checked the recorded, origin and probe36 outputs, `compare-r1.txt`, the ten notebooks and the capsule data.
Every r1/r2 JSON in the three run folders is byte-identical (cmp, no differences).
My probes are in the lane's `reviews/r1-scratch/` (p3.py, p27.py with p27-seed0.json and p27-seeds10-33.json, p52.py, p52b.py, p52c.py, p53.py).
I ran them with the pinned conda python (`-s -P`), and the bix-27 probe with the env2 venv.
Nothing outside that folder was written.

## MAJOR

**M1 · bix-27-q2 (remove): the case for remove rests on an artifact, and the "160-174" stability claim does not hold beyond ten seeds.**
- The note's evidence of randomness is the swing in raw-label equality (27-174).
  Comparing raw labels from two separate Ward clusterings is not a defensible reading, because cluster numbering is arbitrary.
  The pre-registered script itself mandates Hungarian matching.
  So that swing is mostly label permutation, not chance in the answer.
  The note's own matched figures for those ten seeds (`origin-bix-27-q2.json`, `matched_labels` 160-174) are all inside (160,180).
  That contradicts the sentence "no wording short of fixing a seed and a label-matching step makes the target single", as far as the seed goes.
- Probe: `p27.py` is the origin script unchanged except for the seed range.
  Seed 0 reproduces 173/173.
  Seeds 10-33 give matched counts of 150, 152, 158, 164, 169, 169, 171×4, 172×7, 173×5, 174, 175.
  21 of 24 are in the key, so 31 of 34 seeds overall.
- So: with labels matched, the answer stays near 171-173 and falls below 160 in about 9% of seeds.
  Remove is still arguable under "rests on randomness the question does not fix".
  So is reword: name the 178 deduplicated samples, log10(x+1) and matched labels, and either fix a seed or widen the range to about 150-180.
- **Fix:**
  1. Base the note on matched labels and give the 34-seed spread.
  2. Report raw-label equality as a separate finding (rule 4: a defect in the reference analysis).
  3. Drop the claim "160-174 of 178".
  4. Present remove and reword to Javier as two real options (item 7), each with this evidence.
  5. Also: the pre-registered example "168, 187 and 200" is the most seed-sensitive construction; most others move by 9 or less (L1-Q1 194/199/193; L2-Q1 209/213/210). Say so (MINOR).

**M2 · bix-52-q3 (wrong key): the Zebra Finch values that use chromosome length use Jackdaw lengths, and the note does not address the frozen rubric's remove clause.**
- The capsule's ZF length file is the JD file (byte-identical; notebook cell 14).
  Its chromosome numbering visibly does not match the Zebra Finch data: chr4 is listed at 8.0 Mb, chr26 at 46 Mb, chr32 at 0.74 Mb.
  Probe `p52c.py`: in the 458.27 statistic, chr32 alone contributes 220.5 (7 sites against 0.21 expected) and chr4 contributes 123.1.
  So 458.27, and every E1 (proportional-to-length) reading, is a chi-square against another species' karyotype.
  None of them is a value for the Zebra Finch genome.
- Under the frozen rubric, "remove" covers "a required file ... is missing".
  For the length reading, which is the most natural sense of "uniform across the genome", the capsule has no Zebra Finch lengths.
  The note's "Does not claim" line concedes this but never weighs remove against wrong key.
- Is wrong key still forced? Mostly yes, but on different grounds than the note gives:
  - The readings that need no lengths all stay far outside 48-50: E2 713-2,163, E3 192-450, and my extra probes `p52.py`, a 2×k contingency of filtered against unfiltered sites at 263-274, and per-sample mean rows at 61.4.
  - No probe reading lands in 48-50.
  - The key brackets the Jackdaw value 49.638 (cell 39) to three digits.
  - Probe `p52b.py`: if every length may vary from ×0.5 to ×2, the smallest reachable ZF statistic is 119.2. But from ×0.25 to ×4 it is 27.8.
  - So a true ZF length table could in principle reach 48-50. With the table's numbering this far off, "forced" cannot rest on the E1 readings.
- **Fix:**
  1. Rest rule 1(a) explicitly on the length-free readings plus the Jackdaw match.
  2. Relabel 458.27 as "the notebook's construction against the Jackdaw lengths".
  3. Add a paragraph weighing remove (the length file is missing for the length reading) against wrong key, and put that choice to Javier.
  4. Recast the rule-4 "separate finding": using the wrong species' lengths does change the quantity computed, so it is more than a rule-4 defect.

**M3 · bix-36-q5 (undecided): the origin description is wrong, and the ruling put to Javier is mis-framed.**
- The notebook does not pool the six columns.
  Cell 46 concatenates the fits side by side (`axis=1`).
  Cell 48 draws one histogram per column (a 2×3 grid), and cell 49's "normally distributed" judges those six.
- Probe36 output (`origin-bix-36-q5.json`), per column, MLE: five of six are labelled moderately skewed (|skewness| 0.49-0.74; CD14_vs_CD8 is approximately symmetric at -0.49).
  apeglm: three of six are skewed, one highly (CD8_vs_CD4, skewness 2.55, excess kurtosis 28.1).
  All twelve fail normality and are leptokurtic.
  Only the pooled set is approximately symmetric (0.04-0.16).
- So asking Javier whether "approximately symmetric and unimodal" may be called normal asks about a pooled shape the notebook never looked at.
- **Fix:**
  1. Correct the origin text to "six per-column histograms (cells 46-49)".
  2. Report the per-column skewness range next to the pooled figure.
  3. Re-pose ruling 5 so that he rules with that information.
  4. Also add that cell 46 reads `varm["LFC"]`, pydeseq2's natural-log coefficients, not log2. Shape is unchanged (NIT, but it is "the variable" the words fix).

**M4 · bix-3-q4: factual error. "Other cohorts give 145-264 or 812-919" is false.**
`origin-bix-3-q4.json`: A2-M2 (all mice, ~ Response + Tissue, pairwise fits) with baseMean >= 10 gives 438-447, inside (400,500).
**Fix:**
1. List A2-M2 as a second in-key route.
2. The proposed words must also fix the fit, not only the cohort: Control mice in one fit with all three tissues. A1-M2 (Control mice, pairwise fits) gives 145-159.

**M5 · bix-3-q4: baseMean >= 10 does nothing in the notebook's own pipeline, so "departs only in a gene filter" misplaces where the key comes from.**
- In the notebook, cell 29 scales each gene's row to sum to 1e6 over 90 samples.
  So baseMeans sit around 11,000 (cell 36 prints about 10,700-11,400).
- Probe `p3.py` (cells 26, 27 and 29 rebuilt from `bix-3_normcount.csv`; Control samples; median-of-ratios size factors) finds about 18 of 21,251 genes with baseMean < 10.
  On the lane's unscaled path, 9,863 of 25,402 genes have a Control mean below 10.
- So the notebook reaches 429 without the baseMean filter having any effect.
  Its per-comparison counts (846 / 11,663 / 11,746, cell 41) differ from the lane's (524-541 / ~9,930 / ~10,000) for other reasons: the per-gene scaling, pydeseq2, and cell 27's filter.
- The lane's in-key route, baseMean >= 10 on unscaled fits, is a different mechanism that happens to land in the range.
  The conditional verdict (reword if Javier rules the filter fair) still follows from rule 1(b) and rule 3.
  But the "Origin" and "Rule" text invites Javier to read baseMean as the cause of the key.
- **Fix:**
  1. State that the filter does nothing on the notebook's scaled data, with the probe figure.
  2. Say the in-key route is the lane's own, not the notebook's.
  3. Name the per-gene scaling as the notebook's main departure, a rule-4 finding that rule 4 excludes from the 1(c) test.

## MINOR

1. **bix-14-q2, "Also noted": wrong arithmetic.** Adding or removing one row in the parents' group (2/6) moves the difference by 0.048 to 0.133 (2/7, 3/7, 1/5, 2/5). Only reclassifying one row moves it by 1/6 ≈ 0.17. Fix the sentence.
2. **bix-14-q2: rule 2 or rule 1(c).** Rule 2's list has "a gene filter" but no variant-class filter. The words fix the population examined (variants with VAF < 0.3), which is the denominator of "missense variant frequency". A reader could call the exonic-only restriction a departure from a stated denominator (1(c)); then the "not fair" branch would be wrong key, not undecided. Add one sentence on why it is treated as a gene-filter analogue, and flag that the classification is Javier's.
3. **bix-52-q3: 1(c)'s list is "variable measured, groups compared, stated denominator or threshold", and species is none of these literally.** Say which one it falls under (the data set measured, the CpG sites of the named genome) or flag it as an extension for Javier.
4. **bix-53-q3: the conditional needs a second ruling.** Under the text accept rule, the key "22/64" is reached only by a reading that reports Enrichr's overlap string. The question asks for "the number", and the value 22 is not accepted. So reword under rule 2 needs both the exclusion and that format reading ruled fair. The "For Javier" list asks only about the exclusion; add the format.
5. **bix-53-q3, proposed words: padj does not need naming.** Probe `p53.py` on the origin fit tables, four samples: raw p < 0.05 and baseMean > 10 (the words' own thresholds) give 22 (1,952 genes); padj and >= 10 also give 22 (1,927). At six samples every variant gives 20. The exclusion is the only thing that matters.
6. **bix-3-q4: tie the proposed words to the fit** (see M4).
7. **bix-37-q2: the log2 reading is weak.** The sheet has one row per protein and a linear "Normal" column of 1e6-3e9. The pre-registered reason for log2 ("often reported on a log2 scale") does not fit this file. Tell Javier the column is linear. The lane could lean toward keep, while still following the frozen rubric's count.
8. **bix-27-q2: the selective seed example** (see M1, point 5).

## NIT

1. bix-27-q2: the origin cell list omits cell 44 (the log10 transform), which the origin script's docstring cites; the note lists 70, which the script does not.
2. bix-30-q5 (keep holds): the keep rests on reading "all three" as an intersection. Disclose that Benjamini-Hochberg alone gives up to 32 and Bonferroni up to 1 in some readings (e.g. H1-N1-T1: BH 32; H1-N2-T1: BH 4, Bonferroni 1). A reader then sees that Benjamini-Yekutieli is what binds.
3. bix-36-q5: the natural-log note (in M3).

## Confirmed without findings

- bix-7-q3: cell 15 gives 11,896; the reword stands.
- bix-13-q3: cells 18-21; 7 under every row filter on 33 samples; the reword-or-undecided conditional stands.
- bix-52-q3: all four notebook statistics are reproduced (14,722.2 / 458.27 / 4,397.4 / 49.638), and the mutation witness moves 458.27 to 439.12.
- bix-53-q3: the cell references and the four-sample count of 22 are right.
- bix-14-q2: the origin values are right (0.228 against -0.014).
- bix-30-q5: the keep stands.

MAJOR 5, MINOR 8, NIT 3
