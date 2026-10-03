# E5b changes 1: pre-run review, second environment and data pins (lane, 1 Oct 2026, 18:53 EDT)

Written before any E5b question script has run and before any E5b key was read.
It amends nothing in `E5B-PREREG-2026-10-01.md` (sha256 `53302713…af82a`), which stays frozen; it records what the pre-registration said would be recorded in an E5B-CHANGES file, and the readings added after a fresh-context review.

## Pre-run review

A fresh-context reviewer (claude-opus-5-5), blind to keys (it printed question text only, opened no notebook and computed no answer), reviewed the scripts: MAJOR 5, MINOR 12, NIT 5.
Changes made before any run:
- MAJOR 1, bix-13-q3: the numeric-strain reading S2 (strain IDs fitted as a linear covariate) is a coding accident, not a field convention; it is now reported with `"defensible": false`.
- MAJOR 2, bix-52-q3: the data hold sites on chromosomes 1A and 4A, which the length table lacks; added K3 (every chromosome in the data, with equal or background expectations; proportional-to-length cannot include them), U4 (sites with every sample beyond the cut-offs), E3 (expected in proportion to all age-related sites per chromosome), and per-chromosome counts of dropped sites.
- MAJOR 3, bix-36-q5: the comparison direction is now a reading (O1 later against earlier, O3 reversed, O2 both); O2's symmetry label cannot depend on the data and is reported with `"defensible": false`.
- MAJOR 4, bix-36-q5: a synonym list per label, fixed now, before the key; a modality label (L4: binned Gaussian kernel density, Scott's bandwidth, maxima above 10% of the highest); `scripts/compare_e5b.py` accepts a text key equal to a label or one of its pre-registered synonyms and says which.
- MAJOR 5, bix-14-q2: percent units (F1p, F2p) and the direction of the difference (D1 control minus probands, D2 the reverse, D3 absolute).
- MINOR 6-7, bix-14-q2: G3 (all parents) and M3 (RefSeq "Effect (Combined)" is "Missense"; the frozen `chip_common.py` is unchanged, the script adds the column to its map at run time).
- MINOR 8-9, bix-3-q4: C3 (the sum of per-comparison counts); A3 (Control mice, paired, `~ Animal + Tissue`) and A4 (all mice, `~ Tissue`), each fitted with all three tissues only.
  Not carried over from E5a's bix-3 readings because q4's words do not name them, and disclosed in the fit script: apeglm fold changes, the lfcThreshold test, baseMean >= 10, a global pseudo-count scale.
- MINOR 10, bix-27-q2: a strict consistency reading (K1-S2) and a co-association consensus (K2); readings R1-R3 disagreeing is evidence for remove.
- MINOR 12, bix-30-q5: linear-scale readings N3 (2^-Ct) and N4 (2^-delta-Ct).
- MINOR 13: gseapy itself is not run; bix-53-q3 computes Enrichr's overlap for the term directly; DESeq2's third shrinkage type (ashr) is not installed and not a reading.
- MINOR 14-17, the runner: the hashes of the three data-side hash lists are frozen in `E5B-DATA.sha256`; the manifest must cover every script a job runs; the conda environment must match `conda-lock.txt` package by package and the E5b Python environment must match `e5b-py-lock.txt`; a reused intermediate folder is refused.
- NIT 18 and 22: `VECLIB_MAXIMUM_THREADS=1` for bix-27; BiocParallel is loaded in the R environment capture.
Not changed: NIT 19 (a multi-gene cell for ENO1 would fail the assert loudly, which is safe), NIT 20 (bix-36's miRNA-only reading stays and the note says it brings in study context), NIT 21 (a non-finite value prints as JSON `NaN`, which the comparator reports as "not finite").

## The second Python environment (pre-registration, Pins)

bix-27-q2 needs scikit-learn and bix-30-q5 needs xlrd, which the conda lockfile lacks.
`envlock/e5b-py-lock.txt` (uv, hashed wheels, Python 3.12.14) pins numpy 2.1.3, pandas 2.2.3, scipy 1.14.1 and openpyxl 3.1.5 as in the conda environment, plus xlrd 2.0.1 and scikit-learn 1.5.2 with their dependencies; its sha256 is in `E5B-SCRIPTS-1.sha256`.
It is an extension of the run environment for those two questions, not a second environment in the rubric's sense.

## Annotation inputs for bix-53-q3 (fetched 1 Oct 2026, 17:50-18:49 EDT)

- `KEGG_2019_Mouse.gmt` from `https://maayanlab.cloud/Enrichr/geneSetLibrary?mode=text&libraryName=KEGG_2019_Mouse`, sha256 `6aabbf753f6d14dd2205f47fc5e461688fa550a9685dffc77d27c28c7fb13df4` (the library gseapy's Enrichr call downloads).
- `Mus_musculus.GRCm38.102.gtf.gz` from `https://ftp.ensembl.org/pub/release-102/gtf/mus_musculus/`, sha256 `8321415404aaf788c7da79774488ff227ac006d09a57ce6c616573a510338f64`.
- `Mus_musculus.GRCm39.116.gtf.gz` from `https://ftp.ensembl.org/pub/release-116/gtf/mus_musculus/`, sha256 `5c29fd9e3157cf40fdbbf76ab25bfe7f79aa61313e0b672664ddb0cb251c02e1`.

## Capsule zips and data trees

All ten zips fetched at the pinned dataset revision (17:46-17:47 EDT); the four E5a capsules (bix-3, bix-7, bix-13, bix-36) match ADDENDUM-2's pins and E5a's data-tree hashes exactly.
Their hashes are in the lane's `inputs.sha256` and `data-trees.sha256`, whose own hashes are frozen in `E5B-DATA.sha256`.
Only `CapsuleData-*` folders were extracted; the reference notebooks stay zipped and unread until after each question's first recorded repetition.
