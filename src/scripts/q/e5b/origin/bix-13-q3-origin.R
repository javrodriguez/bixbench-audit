#!/usr/bin/env Rscript
# bix-13-q3 origin check (E5B-CHANGES-3; written after the key and the reference notebook were read).
# The notebook (cells 18-21) drops samples resub-5, resub-10 and resub-33, builds ~ Replicate + Strain + Media with
# every variable a factor, and calls estimateSizeFactors, estimateDispersions, then DESeq. It never counts the
# dispersions itself, so this script counts DESeq2's gene-wise estimates (dispGeneEst) below 1e-05 in that fit,
# with the same three row filters as the pre-registered script (K1 all rows, K2 total >= 10, K3 non-zero total).
# Readings here are "added after key" (the three-sample exclusion is the one Javier ruled fair for bix-13-q2 in E5a;
# for E5b it needs his own ruling).
# Usage: Rscript bix-13-q3-origin.R <data_root>
suppressPackageStartupMessages({ library(DESeq2) })
args <- commandArgs(trailingOnly = TRUE)
d <- Sys.glob(file.path(args[1], "bix-13", "CapsuleData-*"))
stopifnot(length(d) == 1)
meta <- read.csv(file.path(d, "experiment_metadata.csv"), stringsAsFactors = FALSE)
cnt <- read.csv(file.path(d, "raw_counts.csv"), row.names = 1, check.names = FALSE)
drop <- c("resub-5", "resub-10", "resub-33")
stopifnot(all(drop %in% meta$AzentaName))
meta <- meta[!meta$AzentaName %in% drop, ]
cnt <- as.matrix(cnt[, meta$AzentaName]); storage.mode(cnt) <- "integer"
meta$Strain <- factor(meta$Strain); meta$Media <- factor(meta$Media); meta$Replicate <- factor(meta$Replicate)
lines <- c()
for (kk in c("K1", "K2", "K3")) {
  keep <- switch(kk, K1 = rep(TRUE, nrow(cnt)), K2 = rowSums(cnt) >= 10, K3 = rowSums(cnt) > 0)
  dds <- suppressMessages(DESeqDataSetFromMatrix(cnt[keep, ], meta, ~ Replicate + Strain + Media))
  dds <- estimateSizeFactors(dds)
  dds <- suppressMessages(estimateDispersions(dds))
  dds$Strain <- relevel(dds$Strain, ref = "1")
  dds <- suppressMessages(DESeq(dds, quiet = TRUE))
  g <- mcols(dds)$dispGeneEst
  lines <- c(lines, sprintf('"X33-%s": {"value": %d, "unit": "count", "samples": %d, "genes_in_fit": %d, "added": "after key", "defensible": "Javier to rule"}',
                            kk, sum(!is.na(g) & g < 1e-05), ncol(dds), nrow(dds)))
}
cat(sprintf('{"question_id": "bix-13-q3", "origin": true, "readings": {%s}}\n', paste(lines, collapse = ", ")))
