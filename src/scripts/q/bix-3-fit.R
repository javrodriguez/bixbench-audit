#!/usr/bin/env Rscript
# Shared DESeq2 fits for bix-3-q1, bix-3-q2 and bix-3-q3 (CHANGES-4). Writes one CSV per cohort x model x
# pseudo-count x contrast.
#   Contrasts: FB_BB final vs baseline blood; DG_BB dentate gyrus vs baseline blood; DG_FB dentate gyrus vs final blood.
#   A, cohort: A1 Control mice only, design ~ Tissue; A2 all mice, design ~ Response + Tissue (bix-3-q2's words
#     name no cohort; A2 is fitted for M1 only).
#   M, samples in the fit: M1 every sample of the cohort (all three tissues); M2 only the two tissues compared.
#   P, integer pseudo-counts: P1 round(), size factors estimated; P2 round(), size factors fixed at 1.
#   Per contrast: baseMean, MLE log2FoldChange, and padj under F1 default (alpha 0.1), F2 alpha 0.05,
#     F3 independentFiltering = FALSE, FT a test against |log2 fold change| > 1 (lfcThreshold = 1, greaterAbs).
# Usage: Rscript bix-3-fit.R <normcount_csv> <out_dir>
suppressPackageStartupMessages({ library(DESeq2) })
args <- commandArgs(trailingOnly = TRUE)
dir.create(args[2], recursive = TRUE, showWarnings = FALSE)
x <- read.csv(args[1], check.names = FALSE, stringsAsFactors = FALSE)
cols <- setdiff(colnames(x), "GeneID")
m <- as.matrix(x[, cols]); rownames(m) <- make.unique(as.character(x$GeneID))
stopifnot(!anyNA(m), length(cols) == 90)
tissue <- sub("^(Control|good_responder|bad_responder)_(.*?)[0-9]+$", "\\2", cols)
resp <- sub("^(Control|good_responder|bad_responder)_.*$", "\\1", cols)
cd_all <- data.frame(row.names = cols, Tissue = factor(tissue, levels = c("baseline_blood", "final_blood", "dentate_gyrus")),
                     Response = factor(resp, levels = c("Control", "good_responder", "bad_responder")))
stopifnot(!anyNA(cd_all$Tissue), all(table(cd_all$Tissue, cd_all$Response) == 10))
contrasts <- list(FB_BB = c("final_blood", "baseline_blood"), DG_BB = c("dentate_gyrus", "baseline_blood"),
                  DG_FB = c("dentate_gyrus", "final_blood"))
fmt <- function(v) ifelse(is.na(v), "NA", formatC(v, digits = 17, format = "g"))
fit <- function(keep, design, pk) {
  ic <- round(m[, keep]); storage.mode(ic) <- "integer"
  dds <- DESeqDataSetFromMatrix(ic, droplevels(cd_all[keep, , drop = FALSE]), design)
  if (pk == "P2") sizeFactors(dds) <- rep(1, ncol(dds))
  DESeq(dds, quiet = TRUE)
}
write_res <- function(dds, ck, tag) {
  ctr <- c("Tissue", contrasts[[ck]])
  r1 <- results(dds, contrast = ctr); r2 <- results(dds, contrast = ctr, alpha = 0.05)
  r3 <- results(dds, contrast = ctr, independentFiltering = FALSE)
  r4 <- results(dds, contrast = ctr, lfcThreshold = 1, altHypothesis = "greaterAbs")
  out <- data.frame(gene = rownames(r1), baseMean = fmt(r1$baseMean), lfc_mle = fmt(r1$log2FoldChange),
                    padj_F1 = fmt(r1$padj), padj_F2 = fmt(r2$padj), padj_F3 = fmt(r3$padj), padj_FT = fmt(r4$padj))
  write.csv(out, file.path(args[2], sprintf("bix-3_%s_%s.csv", tag, ck)), row.names = FALSE, quote = FALSE)
}
for (pk in c("P1", "P2")) {
  ctrl <- cd_all$Response == "Control"
  dds <- fit(ctrl, ~ Tissue, pk)
  for (ck in names(contrasts)) write_res(dds, ck, paste("A1", "M1", pk, sep = "_"))
  for (ck in names(contrasts)) {
    keep <- ctrl & cd_all$Tissue %in% contrasts[[ck]]
    write_res(fit(keep, ~ Tissue, pk), ck, paste("A1", "M2", pk, sep = "_"))
  }
  dds <- fit(rep(TRUE, length(cols)), ~ Response + Tissue, pk)
  write_res(dds, "FB_BB", paste("A2", "M1", pk, sep = "_"))
}
cat(R.version.string, "DESeq2", as.character(packageVersion("DESeq2")), R.version$platform, "\n")
