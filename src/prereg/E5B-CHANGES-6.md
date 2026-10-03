# E5b changes 6: rerunning adversarial review 2's probes (lane, 1 Oct 2026, 21:35 EDT)

Adversarial review 2 (`src/reviews/E5B-ADVERSARIAL-2.md`, fresh claude-opus-5-5): MAJOR 2, MINOR 5, NIT 3.
Its three probes are copied unchanged into `src/scripts/q/e5b/review2/` (q27_l3seeds: bix-27-q2's one accepted pre-registered construction over twelve seeds; p52_r: bix-52-q3's length-free readings in base R; p52_witness: a mutation witness on those readings), hashed in `E5B-SCRIPTS-6.sha256`, and run twice, single-threaded, by `run_review2.sh` into `src/runs/e5b-review2-probes-2026-10-01/`.
All values are produced after the keys were read; none enters a rubric count.
The answers are in `notes/E5B-PROPOSED-VERDICTS.md`, "Amendment 2".
