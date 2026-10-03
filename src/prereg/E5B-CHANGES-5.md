# E5b changes 5: rerunning adversarial review 1's probes (lane, 1 Oct 2026, 20:59 EDT)

Adversarial review 1 (`src/reviews/E5B-ADVERSARIAL-1.md`, fresh claude-opus-5-5): MAJOR 5, MINOR 8, NIT 3.
Its six probes are copied unchanged into `src/scripts/q/e5b/review1/` (p3: bix-3 baseMean under the notebook's per-gene scaling; p27: the bix-27 origin procedure over seeds 0-33; p52, p52b, p52c: bix-52 length-free readings, a bound on what any length table could give, and per-chromosome contributions; p53: bix-53 p-value or padj and baseMean edge), hashed in `E5B-SCRIPTS-5.sha256`, and run twice by `run_review1.sh` into `src/runs/e5b-review1-probes-2026-10-01/`.
Every value they give was produced after the keys were read; none enters a rubric count.
The answers to the findings are recorded in `notes/E5B-PROPOSED-VERDICTS.md`, section "Amendment 1".
