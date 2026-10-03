#!/usr/bin/env Rscript
# bix-53-q3 origin fit (E5B-CHANGES-3; written after the key and the reference notebook were read).
# The notebook (cells 26-53) keeps genes with a count above 10 in at least one sample, drops samples KL3 and WL3,
# fits pydeseq2 with design ~ condition, shrinks the fold changes, and keeps padj < 0.05, |shrunk LFC| > 1 and
# baseMean >= 10. This rebuild uses R DESeq2 with apeglm (an independent implementation of the same model):
#   X4 the notebook's four samples; X6 all six samples, same gene filter (to separate the exclusion's effect).
# Writes <out_dir>/bix-53-origin-<X>.csv with gene, baseMean, lfc_apeglm, pvalue, padj.
# Usage: Rscript bix-53-q3-origin-fit.R <data_root> <out_dir>
suppressPackageStartupMessages({ library(DESeq2); library(apeglm) })
args <- commandArgs(trailingOnly = TRUE)
d <- Sys.glob(file.path(args[1], "bix-53", "CapsuleData-*"))
stopifnot(length(d) == 1)
dir.create(args[2], recursive = TRUE, showWarnings = FALSE)
cnt <- as.matrix(read.csv(file.path(d, "count.csv"), row.names = 1, check.names = FALSE))
storage.mode(cnt) <- "integer"
cnt <- cnt[rowSums(cnt > 10) > 0, ]
fmt <- function(v) ifelse(is.na(v), "NA", formatC(v, digits = 17, format = "g"))
for (xk in c("X4", "X6")) {
  s <- if (xk == "X4") c("KL1", "KL2", "WL1", "WL2") else colnames(cnt)
  cd <- data.frame(row.names = s, condition = factor(substr(s, 1, 2), levels = c("WL", "KL")))
  dds <- DESeq(DESeqDataSetFromMatrix(cnt[, s], cd, ~ condition), quiet = TRUE)
  r <- results(dds, name = "condition_KL_vs_WL")
  a <- lfcShrink(dds, coef = "condition_KL_vs_WL", type = "apeglm", quiet = TRUE)
  out <- data.frame(gene = rownames(r), baseMean = fmt(r$baseMean), lfc_apeglm = fmt(a$log2FoldChange),
                    pvalue = fmt(r$pvalue), padj = fmt(r$padj))
  write.csv(out, file.path(args[2], sprintf("bix-53-origin-%s.csv", xk)), row.names = FALSE, quote = FALSE)
}
cat(R.version.string, "DESeq2", as.character(packageVersion("DESeq2")), "\n")
