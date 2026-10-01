# E5a pre-registration, v0 (lane draft, frozen before any re-derivation)

Written 30 Sep 2026, 09:11 EDT, by the E5a lane agent for glitch-14, on Javier's "go E5a".
This file is frozen by its sha256, recorded in `plans/e5a-bixbench-audit.md` before any capsule is opened.
It is a lane draft: Javier may amend it before the recorded run, and any amendment is a dated addendum with its own hash, never an edit to this file.

## Disclosure

The author of this file read the question text and answer keys of the candidate questions while designing the selection rule.
The rule below is mechanical so that anyone can check that the ten follow from it, but it was not designed blind.

## Pinned inputs

- BixBench v1.5: Hugging Face `futurehouse/BixBench` at revision `f8cc3bdcc6357c88b8c3648306522b9c422dc95a`, `BixBench.jsonl` sha256 `0d1204dcdae7193a9132ced5a3502008f6b3b163debc1b65b2aa2d86cb132dc9` (205 rows, all `version` 1.5).
- BixBench-Verified-50: `phylobio/BixBench-Verified-50` at revision `c77fc8ea4611b546947b8a4710ed36ab72ee233c`, used only for its public file list (33 capsule zips); its question file is behind a gate and is not read.
- BixBench code: GitHub `Future-House/BixBench` at `49311180bdacb324c596f2e07596c126f2004008`, `bixbench/graders.py` sha256 `c5786585fb302594942984636b0809c3fdf92941661ef87ed78d110551ac4733`.
- Each capsule zip is downloaded at the pinned dataset revision and its sha256 recorded in `runs/<run-id>/inputs.sha256` before it is unzipped.

## Selection rule (`scripts/select.py`)

1. The question's capsule is not one of the 33 capsules shipped with Verified-50 (capsule-level exclusion, stricter than question-level).
2. `eval_mode` is `str_verifier` or `range_verifier`.
3. Its categories include at least one of: RNA-seq, Differential Expression Analysis, Transcriptomics, Epigenomics, Genomic Variant Analysis, Single-Cell Analysis.
4. Its capsule zip is at most 50 MB.

Shortlist: every question passing 1-4 (27 at the pinned revision).
Top ten: round-robin over capsules ordered by the number in `short_id`, within a capsule by question number.
At the pinned revision the ten are: bix-1-q1, bix-2-q1, bix-3-q1, bix-7-q1, bix-8-q1, bix-9-q4, bix-13-q1, bix-36-q1, bix-39-q2, bix-1-q2.

## Re-derivation

- One script per question, `scripts/q/<question_id>.(py|R)`, reading only the capsule's data folder, never its reference notebook's outputs.
- Every script prints one line of JSON: the question id, each reading it computes (see below), the value for each, and the environment it ran in.
- A reading is one defensible interpretation of an under-specified question (for example intersection versus union, log base, the denominator of a percentage, the quantile definition, the annotation version).
  Every reading the lane can name is written into the script before it runs, with a one-line reason; readings added after a first run are marked "added after run N".
- Random steps take a fixed seed, and each script is run twice; the two outputs must be byte-identical, or the question is flagged non-deterministic.
- The environment is recorded: the language and package versions (`sessionInfo()` or `pip freeze`), the OS and CPU architecture.
- The reference notebook is read only after the script's first recorded run, to name the step where a disagreement arises.

## How a value is compared with the key

BixBench's own graders at the pinned commit decide a match: `str_verifier` lower-cases both strings and deletes every character that is not a letter or digit before an exact comparison; `range_verifier` checks `lower <= value <= upper`.
The lane also records the plain numeric comparison, because the string grader treats 1.33, 13.3 and 133 as the same answer.

## Verdict rubric

Each verdict is proposed by the lane and decided by Javier.

- **keep**: every defensible reading gives a value the key accepts, in the pinned environment.
- **reword**: at least one defensible reading gives a value the key accepts, and at least one other defensible reading, or an unstated tool version, parameter or annotation release, gives a value it rejects.
  The note proposes the missing words.
- **wrong key**: no defensible reading gives a value the key accepts, the same holds in a second environment (the package versions recorded in the capsule's reference notebook, or a second independent implementation), and the note names the step in the reference notebook where the key's value arises.
- **remove**: the capsule's data cannot answer the question (a required file, column or sample is missing), or the question has no single target (for example it asks for an interval and keys a range), or the answer rests on randomness the question does not fix.

When evidence is short of a rule above, the proposal is "undecided", with what would settle it.

## What is published (on Javier's word only)

A table of question id, eval mode, key accepted (yes, no, depends on reading), proposed verdict, Javier's verdict, and a link to the per-question note.
Per-question notes cite questions by id and describe the issue in the lane's own words, because the rows carry a canary asking that they never appear in training corpora and aegis-0018 rules that the audit never republishes the question bank.
A note may quote the one key value a verdict turns on; it never reproduces question text in full, distractors, or a set of keys.
