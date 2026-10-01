# E5a pre-registration, addendum 1 (lane draft)

Written 30 Sep 2026, 09:21 EDT, by the E5a lane agent, after a fresh-context review (claude-opus-5-5) of v0 returned 4 MAJOR findings, and before any re-derivation value was computed.
The only pilot attempt so far (09:18) stopped in the data loader, before any question's value was computed; no value for any question in any candidate ten has been seen.
It amends `PREREG.md` (sha256 `89c412cb…2347b5`), which stays unchanged; where the two differ, this addendum rules.
Javier may amend it again by a later addendum before the recorded run.

## 1. What "the key accepts a value" means (replaces v0's "How a value is compared with the key")

- The key is the row's `ideal` field; the `answer` field is the source hypothesis label and is never used.
- **Range key** `(lo,hi)`: accepted when `min(lo,hi) <= value <= max(lo,hi)`, both ends inclusive; a reversed range is noted.
- **Numeric string key** (for example `2.5`, `10.6%`, `9.92E-35`): the value is rounded to the precision the key shows, half away from zero (Python `decimal.ROUND_HALF_UP`), then compared exactly.
  Fixed notation: the key's number of decimal places.
  Scientific notation: the key's number of significant digits in the mantissa.
  A key with `%` is compared with the value times 100; a key without `%` for a question that asks for a percentage is compared both ways and the note says so.
- **Text key**: accepted when it equals the value after trimming and lower-casing.
- BixBench's own grader output (pinned `graders.py`) is recorded next to each value as an observation for lane E6 only; it never decides a verdict.
  v0's sentence that `range_verifier` "checks lower <= value <= upper" is wrong for values outside the range, where it raises `UnboundLocalError`.

## 2. What a defensible reading is (sharpens v0's "Re-derivation")

- A reading is defensible when it is consistent with the question's literal words under a named convention of the field, and it is written into the script, with its convention, before the script's first run.
- Where the words are silent on a choice (which test, which model design, which quantile definition, which cohort is "control"), every standard choice from a list named in the script is a reading.
- A reading rebuilt from the reference notebook that contradicts the question's words is not defensible; it is evidence of where the key came from.
- The positive control is pre-registered: for bix-8-q6 the script must reproduce 680 records marked "m6A Hyper" and 260 distinct `gene_id` values; "genes" read literally counts distinct genes, so the rows reading is not defensible, and the expected proposal is **wrong key**, pending the second environment and the notebook step.
  If the script does not reproduce 680 and 260, the instrument is wrong and nothing else is trusted until it does.

## 3. Order of operations (answers "the pilot runs before the final pre-registration")

- Each question script is hashed into `prereg/SCRIPTS.sha256` before its first run; the pilot is run 1 of those frozen scripts, and any later change is a new hash with a reason.
- The pilot covers only questions that are in every candidate ten (v0, amendment A and option A′ below): bix-2-q1, bix-3-q1, bix-7-q1, bix-13-q1, bix-36-q1; plus the positive control bix-8-q6.
  Javier's choice among v0, A and A′ therefore cannot change whether these questions are audited, and seeing their values cannot steer his choice of which others join them.
- Questions in only some candidate tens wait until Javier has picked, and their scripts are frozen before they run.

## 4. Named readings for the CHIP capsules (bix-2, bix-7, bix-39)

- Of the 86 per-sample exome tables, 28 are named by a family-table sample ID and 58 by an SRA run accession (`SRR…`), which the family table does not list.
- Readings for who counts: (i) only samples joined to the family table; (ii) the 58 accession-named samples as an external control cohort, alongside the family table's "Unaffected" members, when a question says "control".
- "Non-reference": the genotype is not `Reference` and not blank; "somatic": variant allele frequency below 0.3, as the questions state.

## 5. Keeping the question bank out of anything published

- `inputs/` and every capsule's data stay out of git: fetched by `make fetch` at the pinned revision, checked against their hashes, git-ignored.
- Capsule data stays in the lane folder or a git-ignored `data/` folder; the Brain's search index never reads workspaces, so it never reaches Glitch's memory.
- Before any push, `scripts/check_no_bank.py` fails if a tracked file contains any 60-character window of any question's text, or all three distractors of any question.
- Every published file that quotes a key carries the BixBench canary line verbatim, and the methods page says so.

## 6. Pins added

- `inputs/bixbench_tree.json` sha256 `db7a3ecb0b96e6a4df9f44361ec1df3f41ed9f946d992861a5bbbe062b1f2b35` (capsule sizes, test 4).
- `inputs/verified50_meta.json` sha256 `1b0fded4d0c4c47de6a09b66b499852dc68120bcfd3f0a8ff4ec92949588bcda` (Verified-50 file list, test 1).
- `scripts/select.py` shadows Python's standard `select` module; every script in `scripts/` runs with `python -P`, and the recorded run's command lines are written into its run folder.

## 7. Disclosures and corrections

- 26 capsule files (23 distinct `short_id` values) and 71 questions remain after test 1.
- v0's `remove` example "asks for an interval and keys a range" was written after the author had read bix-3-q2's key; bix-3-q2 is handled by the readings rule, not by that example.
- Under amendment A, five of the ten come from one paper (doi 10.3324/haematol.2024.285239) and three from one Zenodo record (4287588); no Epigenomics question remains.
  BixBench v1.5 has no question naming ChIP-seq, ATAC, Hi-C, HiChIP, CUT&RUN or chromatin (a search of all 205 question texts), so his chromatin work cannot show in a BixBench audit.
- Option A′, for Javier: amendment A's shortlist, taken round-robin by source paper (the `paper` field with the scheme removed and lower-cased) instead of by capsule: bix-2-q1, bix-3-q1, bix-13-q1, bix-36-q1, bix-2-q2, bix-3-q2, bix-13-q2, bix-36-q3, bix-7-q1, bix-3-q3.
- Non-determinism: two runs that differ within one environment flag the question "unstable in environment X"; the claim "not deterministic" needs both environments.
- The freeze is attested by hash and local file times, not by an external timestamp.
