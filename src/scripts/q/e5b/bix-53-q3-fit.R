#!/usr/bin/env Rscript
# bix-53-q3 (E5b) DESeq2 fit. Readings named from the question's words before any run and before the key was read.
# Data: count.csv (Ensembl mouse gene IDs; samples KL1-3, the knock-down, and WL1-3).
# Design ~ condition, KL against WL (WL the reference); one fit, all six samples.
# Writes: gene, baseMean, MLE log2FoldChange, apeglm-shrunk and normal-shrunk log2 fold changes, pvalue, padj (default).
# Usage: Rscript bix-53-q3-fit.R <data_root> <out_csv>
suppressPackageStartupMessages({ library(DESeq2); library(apeglm) })
args <- commandArgs(trailingOnly = TRUE)
d <- Sys.glob(file.path(args[1], "bix-53", "CapsuleData-*"))
stopifnot(length(d) == 1)
cnt <- read.csv(file.path(d, "count.csv"), row.names = 1, check.names = FALSE)
stopifnot(identical(colnames(cnt), c("KL1", "KL2", "KL3", "WL1", "WL2", "WL3")), !anyNA(cnt))
cnt <- as.matrix(cnt); storage.mode(cnt) <- "integer"
cd <- data.frame(row.names = colnames(cnt), condition = factor(substr(colnames(cnt), 1, 2), levels = c("WL", "KL")))
dds <- DESeq(DESeqDataSetFromMatrix(cnt, cd, ~ condition), quiet = TRUE)
r <- results(dds, name = "condition_KL_vs_WL")
a <- lfcShrink(dds, coef = "condition_KL_vs_WL", type = "apeglm", quiet = TRUE)
n <- lfcShrink(dds, coef = "condition_KL_vs_WL", type = "normal", quiet = TRUE)
stopifnot(identical(rownames(r), rownames(a)), identical(rownames(r), rownames(n)))
fmt <- function(v) ifelse(is.na(v), "NA", formatC(v, digits = 17, format = "g"))
out <- data.frame(gene = rownames(r), baseMean = fmt(r$baseMean), lfc_mle = fmt(r$log2FoldChange),
                  lfc_apeglm = fmt(a$log2FoldChange), lfc_normal = fmt(n$log2FoldChange), pvalue = fmt(r$pvalue),
                  padj = fmt(r$padj))
write.csv(out, args[2], row.names = FALSE, quote = FALSE)
cat(R.version.string, "DESeq2", as.character(packageVersion("DESeq2")), "apeglm", as.character(packageVersion("apeglm")), "\n")
