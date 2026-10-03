#!/usr/bin/env Rscript
# bix-13-q3 (E5b). Readings named from the question's words before any run and before the key was read; unit: count.
#   The design is fixed by the words: ~ Replicate + Strain + Media, all 36 samples, DESeq2.
#   "Dispersion estimate prior to shrinkage": DESeq2's gene-wise estimate (mcols(dds)$dispGeneEst), i.e. before
#     the fit to the trend and the shrinkage towards it; genes whose estimate is NA (all-zero rows) are not counted.
#   S, how Strain enters the model: S1 a factor (strain is a label); S2 numeric, as read from the CSV (DESeq2 then
#     fits the strain IDs as a linear covariate). S2 is a coding accident, not a field convention (E5B-CHANGES-1,
#     pre-run review MAJOR 1): it is reported as "defensible": false, evidence of a key's origin only.
#   K, rows kept before fitting: K1 every row; K2 rows with a total count of at least 10 (the DESeq2 vignette's
#     pre-filter); K3 rows with a non-zero total.
#   value: the number of genes with dispGeneEst < 1e-05 (strictly below).
# Usage: Rscript bix-13-q3.R <data_root>
suppressPackageStartupMessages({ library(DESeq2) })
args <- commandArgs(trailingOnly = TRUE)
d <- Sys.glob(file.path(args[1], "bix-13", "CapsuleData-*"))
stopifnot(length(d) == 1)
meta <- read.csv(file.path(d, "experiment_metadata.csv"), stringsAsFactors = FALSE)
cnt <- read.csv(file.path(d, "raw_counts.csv"), row.names = 1, check.names = FALSE)
stopifnot(all(meta$AzentaName %in% colnames(cnt)), nrow(meta) == 36)
cnt <- as.matrix(cnt[, meta$AzentaName])
storage.mode(cnt) <- "integer"
meta$Media <- factor(meta$Media); meta$Replicate <- factor(meta$Replicate)
fmt <- function(x) formatC(x, digits = 17, format = "g")
lines <- c()
for (sk in c("S1", "S2")) {
  m <- meta
  m$Strain <- if (sk == "S1") factor(m$Strain) else as.numeric(m$Strain)
  for (kk in c("K1", "K2", "K3")) {
    keep <- switch(kk, K1 = rep(TRUE, nrow(cnt)), K2 = rowSums(cnt) >= 10, K3 = rowSums(cnt) > 0)
    dds <- suppressMessages(DESeqDataSetFromMatrix(cnt[keep, ], m, ~ Replicate + Strain + Media))
    dds <- DESeq(dds, quiet = TRUE)
    g <- mcols(dds)$dispGeneEst
    n_below <- sum(!is.na(g) & g < 1e-05)
    lines <- c(lines, sprintf('"%s-%s": {"value": %d, "unit": "count", "genes_in_fit": %d, "genes_with_estimate": %d, "min_dispGeneEst": %s, "defensible": %s}',
                              sk, kk, n_below, nrow(dds), sum(!is.na(g)), fmt(min(g, na.rm = TRUE)), if (sk == "S1") "true" else "false"))
  }
}
cat(sprintf('{"question_id": "bix-13-q3", "readings": {%s}, "meta": {"R": "%s", "DESeq2": "%s"}}\n',
            paste(lines, collapse = ", "), R.version.string, as.character(packageVersion("DESeq2"))))
