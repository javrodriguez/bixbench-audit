# E5a pre-registration, addendum 4 · PROPOSED, version 2, not in force

Drafted 30 Sep 2026, 20:07 EDT, by the E5a lane after adversarial review 3 (`reviews/ADVERSARIAL-3.md`, MAJOR 2 and MINORs 8-13).
It replaces `ADDENDUM-4-PROPOSED.md` (version 1, kept byte-identical as the record of the first draft) as the text put to Javier.
**This rule is Javier's to accept, amend or reject. It is not in force. When he rules, his words go verbatim into a new file `ADDENDUM-4.md` with its own hash; this file stays unchanged.**
Until then the frozen rubric (v0 with addenda 1-3) stands, and every proposal that depends on this rule says so.

## The gap it closes

The frozen rubric's "wrong key" needs "no defensible reading gives a value the key accepts", counted over the lane's pre-registered grid, and CHANGES-5 leaves the defensibility of readings added after the pilot to Javier.
Two questions sat in the same position: 0 accepted pre-registered readings, and at least one reading added after the key that lands in it (bix-36-q1: an RPKM reading, F = 0.7724; bix-3-q1: a x10 pseudo-count scale, 748).
Without a rule, labelling one "wrong key" and the other "undecided" is inconsistent.

## Proposed rule

1. **Wrong key**: no pre-registered defensible reading is accepted, **and** the reference notebook, rebuilt from the capsule data, **departs from something the question's words fix**: the groups compared, the variable measured, or a denominator or threshold the words state.
   This adds to the pre-registration's wrong-key conditions (a second environment, and the note naming the notebook step); it does not replace them.
   In-range values from readings added after the key are listed in the note as disclosed coincidences, never hidden and never counted as support for the key.
2. **Reword**: the key is the quantity the question asks, computed under a choice the words leave open, and at least one route Javier rules standard reaches it; the note names the choice and the proposed words.
   Choices the words leave open include the unit of observation, the normalisation and pseudo-count scale, the fold-change estimator, a sample exclusion, a gene filter and the model design; departing from one of these is rule 2, never rule 1.
3. **Undecided**: neither 1 nor 2 can be shown (for example, the only in-key route is one Javier does not rule standard); the note says what would settle it.
4. A defect in the reference analysis that does not change which quantity is computed (for example bix-3's per-gene scaling) is reported as a **separate finding** and does not by itself make a key wrong.

## Scope

The rule touches only the five questions with no accepted pre-registered reading.
The other five (bix-2-q1, bix-2-q2, bix-7-q1, bix-36-q3, bix-3-q2) each have at least one accepted pre-registered reading; the frozen rubric decides them and this rule does not touch them.

## What it would decide

- bix-36-q1: wrong key (rule 1: the notebook compares six fold-change comparisons, where the words fix four cell types, and measures fold changes, where the words fix expression levels); second environment met by the base-R rebuild.
- bix-13-q1: wrong key (rule 1: the notebook divides by the union, where the words fix JBX97's DE set, and applies no cut-off, where the words state one); second environment met through the notebook's recorded package version (DESeq2 1.46.0, R 4.4.3 against the notebook's 4.4.2), as the pre-registration allows.
- bix-13-q2: reword (rule 2: an unstated sample exclusion).
- bix-3-q1: reword if Javier rules a x10 global pseudo-count scale a standard route (rule 2); otherwise undecided (rule 3); the per-gene scaling is a separate finding (rule 4).
- bix-3-q3: reword if Javier rules apeglm-shrunk fold changes or a global pseudo-count scale a standard route (rule 2); otherwise undecided (rule 3).
