# E5a pre-registration, addendum 2 (lane draft)

Written 30 Sep 2026, 09:33 EDT, by the E5a lane agent, after fresh-context review round 2 (claude-opus-5-5) returned 4 MAJOR findings, and before any question script had run.
It amends `PREREG.md` and `ADDENDUM-1.md` (sha256 `d265a0e0…c0ab7ee4`), which stay unchanged; where they differ, this addendum rules.
Javier's pick of v0, A or A′ becomes addendum 3.

## 1. Correction to addendum 1, section 4 (a false statement about the data)

Addendum 1 said the family table does not list the 58 accession-named samples; that was wrong, and so were the counts.
- The CHIP folder holds 86 per-sample tables: 29 named by a numeric family ID and 57 by an SRA run accession.
- The family table lists all 57 accessions, every one "Unaffected": 19 control trios (19 children, 19 fathers, 19 mothers); three IDs carry stray whitespace, which the first loader missed.
- One family member (ID 533) has no per-sample table.
- The loader now asserts that every per-sample table joins exactly one family-table row after whitespace is stripped.
- Addendum 1's control reading C2 ("the accession-named samples as an external cohort") was the same set as C1 and is withdrawn.
  The new C2 is age-matched: Affected children against Unaffected children, and Carrier parents against Unaffected parents.
- Deliberately unread in these capsules: `CHIP VAF mean proportions.xlsx` (a derived table) and the CHIP gene list.

## 2. The pilot runs sealed (replaces addendum 1, section 3's claim that pilot values "cannot steer" the pick)

That claim was wrong: sibling questions share their capsule's data, so a value on bix-13-q1 or bix-3-q1 hints at how many findings each option holds.
- Until addendum 3 (Javier's pick) is hashed, `scripts/run_pilot.py` runs each frozen script twice and writes the outputs to `runs/<run>/sealed/`, printing only the exit status, the sha256 of each run, and whether the two runs match.
- Nobody reads or compares a sealed value before addendum 3's hash is recorded in the plan.
- The one exception is the positive control bix-8-q6, whose expected values (680 and 260) are already public; its output is read at once, because it tests the instrument.
- A sealed script that fails may have its error text read (the text carries code, not values), and a fixed script gets a new hash with a reason.

## 3. Readings added before the first run

- bix-7-q1: the multiple-testing choice is a reading (K0 none at p < 0.05; K1 Bonferroni over the two groups at p < 0.025), and a reading whose p-values are not all finite reports no value.
- bix-13-q1: the samples in the fit are a reading (M1 one joint model on all 36 samples; M2 JBX1 plus the one strain tested).

## 4. The unit rule (sharpens addendum 1, section 1)

- Each reading declares its unit (fraction, percent, count, F); the value is compared in the key's unit.
- A fraction against a key with `%` is multiplied by 100; a percent against a numeric key without `%` is compared both as given and divided by 100, and the note says which matched.
- A value that is not finite, or cannot be rounded to the key's precision, is not accepted.

## 5. Keeping the question bank out of what is published

- Script headers carry the question id and the named readings only, never a paraphrase of the question.
- `scripts/check_no_bank.py` lower-cases every tracked file and every question text and removes everything that is not a letter or digit before it looks for any shared 60-character window, so punctuation changes cannot slip past it.

## 6. Instrument hygiene

- The positive-control script exits with status 3 unless it reproduces 680 records and 260 distinct genes, and no other value is trusted until it passes.
- Only `CapsuleData-*` folders are extracted; the reference notebooks the pilot had unzipped were deleted unopened at about 09:30 EDT and are re-extracted only after a question's first recorded run.
- R outputs are written with 17 significant digits (`digits = I(17)`).
- Every frozen file (the pre-registration, the addenda, the hash lists and every script) is made read-only.

## 7. Capsule zips pinned (sha256, at dataset revision `f8cc3bdc…`)

- bix-13 `6b29bb5d03693e4098452042ae0169a98926d45ce6ca26b0a45682c8feb7039f`
- bix-2 `7f9234d46d92985574164c53b3c62d39fa53dd06f8c10b1dbfb13652dc353be1`
- bix-3 `41706da9f999eb4d02544c02e960f3fe8da0d0e3e0c18cfc95047e59924607d6`
- bix-36 `2f254fd09c1e05bc0eb876dd7395e39f2af07b9cd92f643ce0c80288e8c24f6c`
- bix-39 `be410226ac353bf8afada3e1226f163d374a5d3ffb5ce33560ee312363ba16a2`
- bix-7 `9852ea865a9b394cf0c14469074493f49f8ae79e610fd89ed55b39e4d185e7b4`
- bix-8 `6d0bcc4502eb25118564315573a132931d2b8a662e71b21d9b374bd59a884cf8`
- bix-9 `afcdc39731ec0895aea70e77c06f8750f1629e263b0211be595a7e2d485f8747`
