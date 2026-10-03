# BixBench answer-key audit: twenty questions in two batches

An audit of twenty answer keys in [BixBench](https://huggingface.co/datasets/futurehouse/BixBench) v1.5, FutureHouse's benchmark for AI agents doing computational biology, in two batches of ten.
The sections from "What was audited" to "Limits" describe the first batch (E5a); the second batch (E5b), with its own pre-registration, is under "Second batch (E5b)".
Each key was re-derived from the question's own data by deterministic scripts, under a pre-registration frozen by hash before any value was computed and extended, with dated and hashed addenda, as the work went on (Method, step 1), and given one verdict: keep, reword, wrong key, or undecided.
The verdicts are the auditor's, Javier Rodriguez Hernaez's: on 30 Sep 2026 he adopted, in one reply ("defaults"), the rulings recommended by the orchestrating agent and recorded in `src/prereg/ADDENDUM-4.md`; for the second batch he did the same on 1 Oct 2026, recorded in `src/prereg/E5B-ADDENDUM-1.md`.
This repository holds the scripts, the run records and the reviews behind each verdict; a few figures come from reviewers' own probes, and those are marked as such where they are cited.

**How the work was done.** The scripts, the runs and the reviews were carried out, and the proposed verdicts and these texts drafted, by AI coding agents (Claude Code, Anthropic's Claude models) working under the auditor's direction; the auditor adopted the recommended verdicts and rulings, so every verdict, and every ruling on whether a reading is fair, is his.

## What was audited (first batch)

Ten questions from BixBench v1.5 (Hugging Face revision `f8cc3bdc…`), chosen by a fixed rule (`src/prereg/PREREG.md`, amended by `ADDENDUM-1.md` and `ADDENDUM-3.md`; how and when it was fixed is under Method, step 1):
- in the auditor's fields, by BixBench's own categories (RNA-seq, differential expression, transcriptomics, epigenomics, genomic variant analysis, single-cell); the ten that resulted cover bulk RNA-seq and differential expression in mouse, bacteria and human immune cells, and exome variant analysis;
- outside BixBench-Verified-50's data capsules, outside the capsules re-derived by the Anqi-Dai BixBench audit, and not one of the Harbor Index tasks;
- graded by a fixed key (a string or a numeric range), not by a model;
- with data small enough to re-run on a laptop.
The ten are spread over four studies.
They are not a random sample, so the results below say nothing about how often any verdict applies across BixBench.

## Method, in plain words (first batch)

1. **Pre-registration.** Before any value was computed, the candidate selection rules, a verdict rubric, and how a value is compared with a key were written down and frozen by their sha256 hashes (`src/prereg/PREREG.md` and its addenda).
   The selection itself was fixed in two stages: three candidate rules were frozen before any value was computed; a pilot then ran, sealed and unread, on the five questions common to all three (four produced values; one was stopped before it did), plus a positive control, bix-8-q6, whose published counts it reproduced and which was read at once; the auditor then picked one rule (`ADDENDUM-3.md`) before any sealed value was read, and the remaining questions' scripts were frozen before they ran.
   Every later change is a dated addendum or change note with its own hash. No pre-registration text or addendum was edited, and no script was changed after it produced a value; some scripts were edited in place before their first value under new hash manifests (`SCRIPTS`, `-2`, `-4` and `-4b` are superseded and no longer match), as the change notes record. The hashes and file times of the core files are collected in `src/prereg/CORE.sha256` (see `src/prereg/CORE-NOTE.md` and its correction `CORE-NOTE-2.md` for when and from what it was compiled).
   After the auditor's pick, the four pilot values were compared with their keys (10:18 EDT). The scripts of the five questions the pilot had not covered (bix-2-q2, bix-3-q2, bix-3-q3, bix-13-q2, bix-36-q3), and the comparator, were written after that and frozen in hash manifests at 10:36 and 10:58 EDT, so their readings were written knowing those four results (for example, that bix-13-q1's readings all fell well above its key); each was frozen before it produced a value of its own (`src/prereg/CHANGES-4.md`, `CHANGES-5.md`).
   bix-3-q1, stopped in the pilot before it produced a value, also had its recorded script written then: it added the M readings (whether the dentate-gyrus samples share the fit) and the FT readings (DESeq2's thresholded test) to the pilot's six, so 10 of its 16 readings, including its lowest and highest values, date from after the pilot's other values had been read (the pilot-era six give 235 to 247).
   The agent that wrote the pre-registration had read the candidate questions and their keys while designing the selection rule and before writing the readings, as `PREREG.md` discloses; the rule is mechanical, so anyone can check that the ten follow from it, but neither it nor the readings were written blind to the keys.
2. **Readings.** Where a question's words leave a choice open (a statistical test, a normalisation, a model design, a denominator), each standard choice is a separate "reading", written into the script before it ran.
3. **Two pinned runs.** Every question was computed twice in a pinned environment (R 4.4.3, DESeq2 1.46.0, apeglm 1.28.0, Python 3.12, pandas 2.2.3; `src/envlock/conda-lock.txt`), and the two runs were checked to be byte-identical.
   For the four questions also run in an earlier pilot (a second install of the same package versions), the values were identical.
4. **Provenance.** After the recorded run, each reference notebook was read and, where possible, rebuilt from the data, to find where each key's value comes from.
5. **Adversarial review.** Six fresh-context AI reviewers (Claude model instances that had not seen the work), each told to break the proposed verdicts, read the evidence in turn; every finding was answered with a dated amendment, and the loop stopped at the first round with no major finding (`src/reviews/`).
   Readings added after values had been computed are labelled as such. The auditor ruled on the five readings the verdicts turn on (four added after values were seen, and one pre-registered reading whose fairness a review questioned, for bix-7-q1; `src/prereg/ADDENDUM-4.md`); the others are listed as evidence without a ruling, except that readings which contradict a question's words are set aside by the frozen rule in `ADDENDUM-1.md` section 2 (this is how three later in-key routes for bix-13-q1 are set aside).
   Further rounds (reviews 7 onward, named `-PUBLIC`) reviewed these public texts against the same stop rule; their findings are in the same folder, and the fixes are in the commit history.
6. **Verdict.** The labels in force: *keep* (every pre-registered reading run gives a value the key accepts), *reword* (a fair reading, pre-registered or ruled fair, reaches the key but others do not, so the question needs words that fix the open choice), *wrong key* (no fair reading of the words reaches the key, and the reference notebook computes something the words rule out), *undecided* (neither can be shown).
   *Keep* and *reword* are the frozen rubric's definitions; *wrong key* and *undecided* are addendum 4's, adopted with the auditor's ruling after the values were known, and apply to the five questions with no accepted pre-registered reading. Where a reading the auditor ruled fair reaches the key, addendum 4 hands the case back to the frozen rubric, which is how bix-36-q1 is a reword although its key is a different quantity. With his rulings on readings they give the same ten verdicts as the frozen rubric, which, like addendum 4, asks for a second environment before "wrong key", and which has a fifth label, *remove*, given to none.

## Results (first batch)

| Question | Topic | Verdict | In one line |
|---|---|---|---|
| bix-2-q1 | exome CHIP variants, somatic share in BLM-variant carriers | keep | every reading run accepts the key |
| bix-2-q2 | exome CHIP variants, germline-band share in control children | keep | every reading run accepts the key |
| bix-7-q1 | exome CHIP variants, groups differing from control | reword (minor) | the test and the frequency measure are unstated; one fair reading (at two thresholds) gives a different count |
| bix-36-q1 | miRNA expression across immune cell types, ANOVA F | reword | the key matches an ANOVA of fold changes in the reference notebook, while the question names expression levels; one expression reading ruled fair also reaches it |
| bix-36-q3 | miRNA median fold change, CD14 against CD19 | reword | most readings accept the key; one normalisation with an expression filter does not, so the normalisation and filter should be stated |
| bix-13-q1 | bacterial mutants, overlap of DE gene sets as a percentage | **wrong key** | no reading run that keeps the question's stated cut-off and denominator reaches the key; the key matches the notebook's share of the union of the three strains' DE sets |
| bix-13-q2 | bacterial mutants, genes DE in one mutant only | reword | among the readings run, only the notebook's sample exclusion, with its design, reaches the key; the question does not state it |
| bix-3-q1 | mouse blood, DE genes between two time points | undecided | the answer depends on unstated choices; no reading ruled fair reaches the key |
| bix-3-q2 | mouse blood, confidence interval for the share of DE genes | reword | the question asks for an interval, the key is one range, and the DE set and denominator are unstated |
| bix-3-q3 | mouse brain and blood, DE genes specific to one comparison | reword | apeglm-shrunk fold changes with one model over all Control samples reach the key; the question should name the estimator and the model |

**Count: keep 2, reword 6, wrong key 1, undecided 1.**
A **separate finding** concerns the reference notebook behind the bix-3 questions: it scales each gene, rather than each sample, to one million before the differential-expression fit, which makes bix-3-q1's stated baseMean filter remove nothing.
The reason, the evidence files, and what each verdict does **not** claim are in `notes/VERDICTS.md`.

## Limits (first batch)

- Ten questions, chosen by a rule, in one auditor's fields; no rate or generalisation to BixBench follows from them.
- A verdict counts the readings the audit ran; a reading nobody tried could change a "keep" into a "reword", an "undecided" into a "reword", or a "wrong key" into a "reword". The rubric, the readings and the reviews are all here so that anyone can try more.
- "Wrong key" means the key does not answer the question as worded; it does not mean the reference analysis is wrong as an analysis.
- Readings added after values had been computed are labelled; they enter a verdict through the auditor's rulings on four such readings (three rewords and the undecided rest on them; his fifth ruling, for bix-7-q1, is on a pre-registered reading) or, for bix-13-q1, through the frozen rule that sets aside readings contradicting the question's words, and those rulings are judgements, recorded with the reasons given for the recommendations he adopted (`notes/PROPOSED-VERDICTS.md`).
- The pre-registration's freeze is attested by hashes and local file times, not by an external timestamp; the hashes of the selection files and of addendum 3 were recorded at the time in the auditor's private plan and collected into this repository later the same day.
- Two reference notebooks (bix-3, bix-36) used pydeseq2. The bix-36 fold-change analysis was rebuilt in R DESeq2 and matches the key; bix-3's key-producing step could not be rebuilt in R DESeq2, so that provenance rests on the notebook's own code and printed output.
- The reviewers were AI model instances of the same model family as the agents that did the work, not independent human experts.
- The pre-registered readings were written by an agent that had seen the keys; they are listed in full in the scripts so that anyone can judge whether they lean toward them.
- Nothing here evaluates any model or agent.

## Second batch (E5b)

Ten more BixBench v1.5 questions, audited the same way under a new pre-registration.
The verdicts are the auditor's: on 1 Oct 2026 at 23:48 EDT (as relayed by the orchestrating agent, `src/prereg/E5B-ADDENDUM-1.md`) he adopted, in one reply ("defaults"), the nine rulings and ten verdicts recommended by the orchestrating agent on a decision sheet (`notes/E5B-FOR-JAVIER.md`).
His first-batch rulings on readings were not extended to this batch; where a ruling here matches one of them, it is a new ruling of his.
The E5b records were written before he gave his word to publish this batch, so they still say that word was not yet given; he gave it on 2 Oct 2026 at 22:05 EDT ("publish E5b").
The reasons, the evidence files, and what each verdict does **not** claim are in `notes/E5B-VERDICTS.md`.

### What changed from the first batch

1. **Pre-registration.** `src/prereg/E5B-PREREG-2026-10-01.md` was frozen by its sha256, recorded in the auditor's private plan, before any E5b question script was written (1 Oct 2026); it carries over the first batch's rubric with addendum 4 as the auditor adopted it on 30 Sep, and every later change is a dated, hashed file (`E5B-CHANGES-1` to `-8`, `E5B-ADDENDUM-1`).
2. **Selection.** A mechanical rule (`src/scripts/select_e5b.py`, output `src/prereg/E5B-selection-2026-10-01.json`): not one of the 50 BixBench-Verified-50 questions (this time the questions themselves are excluded, not whole capsules); graded by a fixed key; the first batch's fields and size limit; not in the capsules or tasks the first batch set aside, nor in capsule bix-22; not named in eleven public GitHub threads about BixBench keys or graders, listed in the pre-registration; and not one of the first batch's ten or named in its notes.
   21 questions from ten papers remained, and the first question of each paper was taken.
   The selection was computed before the agent read the text or key of any of the ten.
   Four of the ten come from capsules (bix-3, bix-7, bix-13, bix-36) whose data the first batch had already computed on; no first-batch value was compared with a second-batch key.
3. **Readings before the keys.** Each script's readings were written from the question text alone; a fresh-context reviewer, blind to the keys, checked the scripts before any ran, and its five major findings were answered before the first run (`E5B-CHANGES-1`).
   One script stopped at its own check before producing a value, and readings for missing values were added before any value of that question existed and before any E5b output or key was read (`E5B-CHANGES-2`; the stopped attempt is kept as a record).
   The keys were read only after the first recorded repetition of all ten.
4. **Two pinned runs.** The first batch's environment, plus a second Python lockfile (`src/envlock/e5b-py-lock.txt`) for two packages two questions need, scikit-learn and xlrd; every output of the two repetitions is byte-identical (`src/scripts/verify_runs_e5b.py`).
5. **Provenance.** After the first repetition each reference notebook was read and, where possible, the key's origin was rebuilt from the data and run twice; those readings are labelled "added after key".
6. **Adversarial review.** Four rounds of fresh-context AI reviewers (claude-opus-5-5 instances) were told to break every proposed wrong key and undecided and to test every keep and reword; they made 5, 2, 1 and 0 major findings, and each round was answered by a dated amendment; the probes of rounds 1 and 2 and two of round 4's three were rerun twice under the lane's hashing, while round 3's probe, a bound rather than a reading, was not rerun and its major finding was answered by new readings on the real Zebra Finch lengths (`E5B-CHANGES-7`); the loop stopped at round 4, the first with no major finding (`src/reviews/E5B-ADVERSARIAL-1.md` to `-4.md`).

### Results (second batch)

| Question | Topic | Verdict | In one line |
|---|---|---|---|
| bix-3-q4 | mouse tissues, genes DE in all three tissue comparisons | reword | no pre-registered reading reaches the key; adding a baseMean filter, ruled fair, does for two model set-ups, so the question should name the cohort, the fit and the thresholds |
| bix-7-q3 | exome variants, a count of variants | reword (minor) | counting variant rows (one per sample) reaches the key and counting distinct variants does not |
| bix-13-q3 | bacterial mutants, genes with a very small dispersion estimate | reword | with all samples no reading reaches the key; with the notebook's three samples removed, ruled fair, it does, so the question should name them |
| bix-14-q2 | exome variants, missense share in parents against probands | reword | no pre-registered reading reaches the key; the notebook's removal of intronic, intergenic and UTR variants, ruled fair, does, and the value rests on few variants |
| bix-27-q2 | clustering, samples placed alike by two clusterings | reword | the notebook's route with the cluster labels matched, ruled fair, lands in the key for 31 of 34 seeds; the steps and the seed should be stated |
| bix-30-q5 | miRNA qPCR, miRNAs significant under three corrections | keep | all 36 pre-registered readings give the key |
| bix-36-q5 | miRNA fold changes, the shape of their distribution | undecided | no pre-registered label gives the key; the notebook reaches it by a judgement by eye, which was ruled not a fair reading |
| bix-37-q2 | proteomics, one protein's level in one sample group | reword (minor) | the value on its linear scale reaches the key; the pre-registered log2 reading does not, and was kept |
| bix-52-q3 | Zebra Finch CpG sites, a chi-squared test across chromosomes | **wrong key** | no Zebra Finch reading run reaches the key; the key matches the notebook's statistic for the other species in the capsule, the Jackdaw |
| bix-53-q3 | DE genes overlapping a pathway | reword | with all six samples no reading reaches the key; with the notebook's two samples removed, ruled fair, every variant tried does, with the key's ratio format read as the count |

**Count: keep 1, reword 7, wrong key 1, undecided 1.**
**Four separate findings**, reported whatever the rulings:
- **bix-3 (reference notebook).** Cell 29 scales each gene's row, not each sample, the defect the first batch reported for bix-3.
- **bix-27 (reference notebook).** Cell 71 compares raw cluster labels from two separate clusterings; its count is right only when the arbitrary numbering happens to agree.
- **bix-53 (reference notebook).** Cells 15-16 label the two conditions the reverse of cell 14's description and of the question; the count is unaffected.
- **bix-52 (capsule).** The capsule's Zebra Finch chromosome-length file (`ZF_Chromosome_Length.csv`) is byte-identical to its Jackdaw length file; the notebook's cell 14 downloads the Jackdaw file under the Zebra Finch name.

For comparison, the first batch ended keep 2, reword 6, wrong key 1, undecided 1.
The two batches were chosen by different fixed rules, not at random; neither count, nor their sum, says anything about how often any verdict applies across BixBench or BixBench-Verified-50.

### bix-52-q3: what the wrong key is, and is not

- **What it is.** The question names the Zebra Finch.
  The key's range holds, to the key's shown precision, the reference notebook's chi-squared statistic for the Jackdaw (cell 39), not its Zebra Finch statistic (cell 36).
  None of the 32 pre-registered Zebra Finch readings reaches the key, and neither do the readings that need no length table or the per-base-pair readings recomputed, after the key, on the real Zebra Finch chromosome lengths from the NCBI reference assembly bTaeGut1.4.pri, which give 161 to 652 (`src/prereg/E5B-CHANGES-7.md`).
  Base R's `chisq.test`, the notebook's own tool, reproduces all six real-length readings and three of the length-free ones as the second environment, and a planted change to the input moves a reading's value (the mutation witness).
  The auditor ruled it wrong key, holding that the genome a question names is "the variable measured" under addendum 4's rule 1(c) (ruling 8).
- **The alternative was remove.** Because the capsule's Zebra Finch length file is the Jackdaw file, the capsule lacks a file the per-base-pair reading needs; that case for remove was put to the auditor, and he chose wrong key.
- **What it is not.** It does not say which Zebra Finch reading is right, or what a repaired key should be: that needs a Zebra Finch computation with words that fix the reading.
  Beyond the length file, it does not judge the notebook's analysis.
  It rests on four rounds of review by AI model instances, the last with no major finding, not on independent human experts, and a reading nobody tried could still change it.

### Limits (second batch)

- Ten questions, chosen by a rule; no rate or generalisation to BixBench follows from them, and nothing here concerns BixBench-Verified-50's own 50 questions.
- The prior-art test covers only the eleven threads the pre-registration lists; it does not show that no one else has examined these questions.
- Six verdicts rest on the auditor's rulings on readings added after the keys were seen (the rewords of bix-3-q4, bix-13-q3, bix-14-q2, bix-27-q2 and bix-53-q3, and the undecided bix-36-q5), bix-52-q3 rests on his rulings that it is wrong key rather than remove and on how rule 1(c) applies, bix-14-q2 also on his ruling that its variant filter is an open choice, and bix-37-q2 on his choice not to set aside a pre-registered reading; those rulings are judgements, recorded with the reasons given for the recommendations he adopted (`notes/E5B-FOR-JAVIER.md`, `notes/E5B-PROPOSED-VERDICTS.md`).
- The pre-registration's freeze is attested by hashes and local file times, not by an external timestamp.
- The reviewers were AI model instances of the same model family as the agents that did the work.
- Nothing here evaluates any model or agent.

## How to reproduce

**About the public copy.** In the public copy of this repository, file paths on the auditor's machine are masked by `src/scripts/public_export.py` (four recorded rules; every file's sha256 before and after masking is in `EXPORT-MANIFEST.json`), while the frozen originals stay unchanged, so a masked file's hash differs from `src/prereg/`'s manifests and `EXPORT-MANIFEST.json` maps each one back.

These steps rebuild the environment and the data layout the recorded runs read. Steps 3-5 were followed once in a separate folder for the `chip` and `bix36` stages (repetition 1, with the zips already downloaded and the audit's own environment) and reproduced the recorded outputs byte for byte; the `bix13` and `bix3` stages, a second repetition, a fresh download and a newly built environment have not been tried this way.

1. **Environment.** `micromamba create -p env --file src/envlock/conda-lock.txt` (the lockfile is for macOS on Intel, `osx-64`; on other platforms, install the same versions of R, DESeq2, apeglm, jsonlite, Python, pandas, openpyxl, numpy and scipy).
2. **Question file and grader.** Download `BixBench.jsonl` from the dataset at revision `f8cc3bdcc6357c88b8c3648306522b9c422dc95a` into `src/inputs/`, and BixBench's `bixbench/graders.py` at GitHub commit `49311180bdacb324c596f2e07596c126f2004008` into `src/inputs/graders_49311180.py`.
   Check `graders_49311180.py` against the sha256 in `src/prereg/PREREG.md` (`c5786585…`); the runner checks the question file itself.
   Neither is included here: BixBench asks that its data never appear in training corpora.
   The reference notebooks cited in `notes/VERDICTS.md` are the `CapsuleNotebook-*` folders inside each capsule zip (step 4 deliberately leaves them out); notebook cell numbers there are zero-based positions in the `.ipynb` file.
3. **Capsules.** Copy `src/runs/pilot-2026-09-30` to a work folder `W`, create `W/zips`, and run `python3 -P src/scripts/fetch_capsules.py W`, which downloads the eight pinned capsule zips (the recorded runs check all eight, though only five are used by the ten questions).
4. **Data layout.** Run `python3 src/scripts/extract_data.py W`: it checks each zip against the hashes in `src/prereg/ADDENDUM-2.md` section 7, extracts only the `CapsuleData-*` folders into `W/data/<short id>/`, and checks every data tree against `W/data-trees.sha256`.
5. **Runs.** For each stage run two repetitions: `python3 -P src/scripts/run_recorded_v2.py <run_dir> W/data env <stage> 1`, then the same with `2`. Stages are `chip`, `bix36` and `bix13`, plus `bix3`, which takes a sixth argument, `SCRIPTS-7.sha256`. The runner refuses to start if any pinned file differs.
6. **Checks.** `python3 -P src/scripts/verify_runs_v2.py src/runs/pilot-2026-09-30/sealed <run_dir>` checks repetition against repetition and against the pilot. `env/bin/python -P src/scripts/compare2.py <run_dir>/r1/<question>.json src/inputs/BixBench.jsonl src/inputs/graders_49311180.py` compares values with keys; its output quotes keys, so keep it local.
7. **Key-origin rebuilds and review probes.** The key-origin rebuilds (`src/scripts/q/bix-13-origin.R`, `bix-3-origin.R`) and the per-sample counts-per-million runs (`src/scripts/run_p3.sh`) are described in `src/prereg/CHANGES-6.md`, `CHANGES-8.md` and `CHANGES-9b.md`; the probes added during review are in `src/scripts/q/`, with their change notes in `CHANGES-10.md` to `CHANGES-15.md`. Some run drivers name a local Mac-scheduling helper and local paths, which a reader replaces or removes.
8. **Second batch.** `src/scripts/run_e5b.py` runs one stage and one repetition per call (its header names the arguments and the stages `light`, `bix3`, `bix27` and `origin`) and refuses to start unless every pinned file matches; `src/scripts/verify_runs_e5b.py` checks repetition against repetition. The data layout it reads, and the hash lists it checks, are described in `src/prereg/E5B-PREREG-2026-10-01.md` and `E5B-CHANGES-1.md`; this route has not been followed from a fresh copy.

## Contact

The benchmark's authors have not been contacted yet.
A courteous note to them, with the evidence for bix-13-q1 and the bix-3 notebook finding, has been drafted; whether and when to send it is the auditor's decision.
Any correction they make, or any error they find in this audit, will be recorded here.

## Credits and prior work

BixBench is by FutureHouse (Mitchener et al., 2025, arXiv:2503.00096; Apache-2.0).
The selection set aside the data capsules of Phylo's BixBench-Verified-50, the capsules re-derived in the Anqi-Dai BixBench audit, and the Harbor Index tasks.
marin-community/harbor issue #167 reviewed one agent run's outcomes on all 205 questions and reported confirmed defects in other questions; its body and comments name none of these ten (checked 30 Sep 2026).

## License

The write-up and records are licensed under [CC BY 4.0](LICENSE-CC-BY-4.0); the scripts under the [MIT License](LICENSE). The BixBench questions and data are not included and keep their own license.

## Changes after the export

1 Oct 2026: the unsent draft note to the benchmark's authors (`notes/DRAFT-maintainer-issue.md`) was removed from this public copy at the auditor's request, so `EXPORT-MANIFEST.json` lists one file this copy no longer carries; license files were added.
2 Oct 2026: the second batch was added, at the auditor's word, by a new export from the records repository; the license files and this README are now part of the export, and the draft note is again left out of this copy, so `EXPORT-MANIFEST.json` still lists that one file.
