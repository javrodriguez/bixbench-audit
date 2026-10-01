# E5a pre-registration, addendum 4 · PROPOSED, version 4, not in force

Drafted 30 Sep 2026, 20:31 EDT, by the E5a lane after adversarial review 5 (`reviews/ADVERSARIAL-5.md`, MAJOR 1, MINOR 3 and notes 6a-6b).
It replaces version 3 as the text put to Javier; versions 1-3 are kept byte-identical as the record of earlier drafts.
**This rule is Javier's to accept, amend or reject. It is not in force. When he rules, his words go verbatim into a new file `ADDENDUM-4.md` with its own hash; this file stays unchanged.**
Until then the frozen rubric (v0 with addenda 1-3) stands, and every proposal that depends on this rule says so.

## The gap it closes

The frozen rubric's "wrong key" needs "no defensible reading gives a value the key accepts", counted over the lane's pre-registered grid, and CHANGES-5 leaves the defensibility of readings added after the pilot to Javier, reading by reading.
Two questions sat in the same position: 0 accepted pre-registered readings, and at least one reading added after the key that lands in it (bix-36-q1: an RPKM reading, F = 0.7724, and eleven rank-transform values; bix-3-q1: a x10 pseudo-count scale, 748).
Without a rule, labelling one "wrong key" and the other "undecided" is inconsistent.

## One ruling, not two

For a reading added after the key, "a route Javier rules standard" and "a reading he rules defensible" (addendum 1 section 2) are **the same ruling**.
So the rule never asks him for a second, separate judgement, and wherever he rules a later in-key reading defensible, the frozen rubric's own outcome follows unchanged.

## Proposed rule

1. **Wrong key**: all of the following hold.
   (a) No pre-registered defensible reading is accepted.
   (b) No reading added after the key that Javier rules defensible lands in the key; if one does, the frozen rubric decides (it gives reword: one defensible reading accepted, others rejected), so this rule never turns a key the frozen rubric would not call wrong into a wrong key.
   (c) The reference notebook, rebuilt from the capsule data, departs from something the question's words fix: the variable measured, the groups compared, or a denominator or threshold the words state.
   (d) The pre-registration's own wrong-key conditions hold (a second environment, and the note naming the notebook step).
   In-range readings added after the key that Javier rules **not** defensible are listed in the note as disclosed coincidences, never hidden.
2. **Reword**: the key is the quantity the question asks, computed under a choice the words leave open, and it is reached by at least one reading Javier rules defensible; the note names the choice and the proposed words.
   Choices the words leave open include the unit of observation, the normalisation and pseudo-count scale (and transforms such as ranks or logs), the fold-change estimator, a sample exclusion, a gene filter and the model design; a departure **only** in one of these choices is rule 2, never rule 1.
3. **Undecided**: neither 1 nor 2 can be shown (for example, the only in-key route is a reading Javier does not rule defensible, and the notebook departs only in open choices); the note says what would settle it.
4. A defect in the reference analysis that does not change which quantity is computed (for example bix-3's per-gene scaling) is reported as a **separate finding** and does not by itself make a key wrong.

## Scope

The rule touches only the five questions with no accepted pre-registered reading.
The other five (bix-2-q1, bix-2-q2, bix-7-q1, bix-36-q3, bix-3-q2) each have at least one accepted pre-registered reading; the frozen rubric decides them and this rule does not touch them.

## What it would decide (every line conditional on Javier's rulings named in it)

- bix-36-q1: **wrong key if Javier rules neither the RPKM reading (F = 0.7724) nor the rank-transform readings (eleven values) defensible**; the departure (1c) is first the variable measured (fold changes, where the words name expression levels, the variable the sibling question bix-36-q4 distinguishes), and second the groups compared (contestable, since the benchmark's `result` text calls the six comparisons "groups"); second environment met by the base-R rebuild.
  If he rules any of those readings defensible: **reword** under the frozen rubric, and the note discloses that the key's own computation is a different quantity.
- bix-13-q1: wrong key (1c: the words fix JBX97's DE set **with** its 1.5 cut-off as the denominator; the notebook divides by the union of padj-only sets).
  Two in-key readings were found after the key, and each drops one of the two things the words fix about that set: one divides by the union (10.617%), the other divides by JBX97's padj-only set without its cut-off (10.569%, with the notebook's three samples dropped).
  Both contradict the words, so addendum 1 section 2 makes them not defensible; no reading that keeps JBX97's set as the words define it (FDR and the cut-off) lands in the key, in any run.
  Second environment met through the notebook's recorded package version (DESeq2 1.46.0, R 4.4.3 against the notebook's 4.4.2), as the pre-registration allows.
- bix-13-q2: reword if Javier rules the notebook's three-sample exclusion (with its design) defensible; otherwise undecided.
- bix-3-q1: reword if Javier rules a x10 global pseudo-count scale defensible; otherwise undecided; the per-gene scaling is a separate finding (rule 4).
- bix-3-q3: reword if Javier rules apeglm-shrunk fold changes or a global pseudo-count scale defensible; otherwise undecided.
