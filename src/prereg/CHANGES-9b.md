# E5a: result of the bix-3 origin rebuild (lane, 30 Sep 2026, 17:15 EDT)

- `q/bix-3-origin.R` ran twice (17:14), and both runs stopped with the same error in DESeq2's dispersion-trend fit (`locfit ... newsplit: out of vertex space`), after DESeq2 had already fallen back from its parametric trend to its local one; no value was produced (`runs/recorded-2026-09-30-origin3/`).
- Cause, as far as the lane can tell: scaling every gene to the same total over the 90 samples makes every gene's mean count nearly equal (about 11,000), which leaves DESeq2 no mean-dispersion trend to fit; pydeseq2, which the notebook used, completed its fit and printed the keys' values.
- The lane stops here rather than change DESeq2's settings until a fit succeeds, since that would tune the instrument towards the key.
- Origin evidence for bix-3 is therefore the notebook's own code and printed output (cells 26-29, 33, 41, 56, 61, 66), not a rerun; the notes say so.
