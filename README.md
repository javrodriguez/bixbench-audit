# BixBench answer-key audit: ten questions

An audit of ten answer keys in [BixBench](https://huggingface.co/datasets/futurehouse/BixBench) v1.5, FutureHouse's benchmark for AI agents doing computational biology.
Each key was re-derived from the question's own data by deterministic scripts, under a pre-registration frozen by hash before any value was computed and extended, with dated and hashed addenda, as the work went on (Method, step 1), and given one verdict: keep, reword, wrong key, or undecided.
The verdicts are the auditor's, Javier Rodriguez Hernaez's: on 30 Sep 2026 he adopted, in one reply ("defaults"), the rulings recommended by the orchestrating agent and recorded in `src/prereg/ADDENDUM-4.md`.
This repository holds the scripts, the run records and the reviews behind each verdict; a few figures come from reviewers' own probes, and those are marked as such where they are cited.

**How the work was done.** The scripts, the runs and the reviews were carried out, and the proposed verdicts and these texts drafted, by AI coding agents (Claude Code, Anthropic's Claude models) working under the auditor's direction; the auditor adopted the recommended verdicts and rulings, so every verdict, and every ruling on whether a reading is fair, is his.

## What was audited

Ten questions from BixBench v1.5 (Hugging Face revision `f8cc3bdc…`), chosen by a fixed rule (`src/prereg/PREREG.md`, amended by `ADDENDUM-1.md` and `ADDENDUM-3.md`; how and when it was fixed is under Method, step 1):
- in the auditor's fields, by BixBench's own categories (RNA-seq, differential expression, transcriptomics, epigenomics, genomic variant analysis, single-cell); the ten that resulted cover bulk RNA-seq and differential expression in mouse, bacteria and human immune cells, and exome variant analysis;
- outside BixBench-Verified-50's data capsules, outside the capsules re-derived by the Anqi-Dai BixBench audit, and not one of the Harbor Index tasks;
- graded by a fixed key (a string or a numeric range), not by a model;
- with data small enough to re-run on a laptop.
The ten are spread over four studies.
They are not a random sample, so the results below say nothing about how often any verdict applies across BixBench.

## Method, in plain words

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

## Results

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

## Limits

- Ten questions, chosen by a rule, in one auditor's fields; no rate or generalisation to BixBench follows from them.
- A verdict counts the readings the audit ran; a reading nobody tried could change a "keep" into a "reword", an "undecided" into a "reword", or a "wrong key" into a "reword". The rubric, the readings and the reviews are all here so that anyone can try more.
- "Wrong key" means the key does not answer the question as worded; it does not mean the reference analysis is wrong as an analysis.
- Readings added after values had been computed are labelled; they enter a verdict through the auditor's rulings on four such readings (three rewords and the undecided rest on them; his fifth ruling, for bix-7-q1, is on a pre-registered reading) or, for bix-13-q1, through the frozen rule that sets aside readings contradicting the question's words, and those rulings are judgements, recorded with the reasons given for the recommendations he adopted (`notes/PROPOSED-VERDICTS.md`).
- The pre-registration's freeze is attested by hashes and local file times, not by an external timestamp; the hashes of the selection files and of addendum 3 were recorded at the time in the auditor's private plan and collected into this repository later the same day.
- Two reference notebooks (bix-3, bix-36) used pydeseq2. The bix-36 fold-change analysis was rebuilt in R DESeq2 and matches the key; bix-3's key-producing step could not be rebuilt in R DESeq2, so that provenance rests on the notebook's own code and printed output.
- The reviewers were AI model instances of the same model family as the agents that did the work, not independent human experts.
- The pre-registered readings were written by an agent that had seen the keys; they are listed in full in the scripts so that anyone can judge whether they lean toward them.
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

## Contact

The benchmark's authors have not been contacted yet.
A courteous note to them, with the evidence for bix-13-q1 and the bix-3 notebook finding, has been drafted; whether and when to send it is the auditor's decision.
Any correction they make, or any error they find in this audit, will be recorded here.

## Credits and prior work

BixBench is by FutureHouse (Mitchener et al., 2025, arXiv:2503.00096; Apache-2.0).
The selection set aside the data capsules of Phylo's BixBench-Verified-50, the capsules re-derived in the Anqi-Dai BixBench audit, and the Harbor Index tasks.
marin-community/harbor issue #167 reviewed one agent run's outcomes on all 205 questions and reported confirmed defects in other questions; its body and comments name none of these ten (checked 30 Sep 2026).
