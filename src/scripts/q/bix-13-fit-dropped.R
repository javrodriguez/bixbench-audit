#!/usr/bin/env Rscript
# bix-13 fits with the reference notebook's three samples dropped (CHANGES-14): bix-13-fit.R plus one line, rerunning
# adversarial review 5's probe. ADDED AFTER THE KEYS WERE KNOWN; not a rubric reading.
# Otherwise as bix-13-fit.R (CHANGES-4). Writes one CSV per design x model x strain.
#   D, design: D1 ~ Strain; D2 ~ Media + Strain; D3 ~ Replicate + Strain + Media.
#   M, samples in the fit: M1 all 36 samples, one joint model; M2 JBX1 plus the one strain tested.
#   Per strain 97, 98, 99 against JBX1: MLE log2FoldChange, apeglm-shrunk log2 fold change, baseMean,
#   and padj under F1 DESeq2 default (alpha 0.1), F2 alpha 0.05, F3 independentFiltering = FALSE.
# Usage: Rscript bix-13-fit.R <data_root> <out_dir>
suppressPackageStartupMessages({ library(DESeq2) })
args <- commandArgs(trailingOnly = TRUE)
d <- Sys.glob(file.path(args[1], "bix-13", "CapsuleData-*"))
stopifnot(length(d) == 1)
dir.create(args[2], recursive = TRUE, showWarnings = FALSE)
meta <- read.csv(file.path(d, "experiment_metadata.csv"), stringsAsFactors = FALSE)
cnt <- read.csv(file.path(d, "raw_counts.csv"), row.names = 1, check.names = FALSE)
stopifnot(all(meta$AzentaName %in% colnames(cnt)), nrow(meta) == 36)
meta <- meta[!meta$AzentaName %in% c("resub-5", "resub-10", "resub-33"), ]; stopifnot(nrow(meta) == 33)  # CHANGES-14
cnt <- as.matrix(cnt[, meta$AzentaName])
storage.mode(cnt) <- "integer"
meta$Strain <- relevel(factor(meta$Strain), ref = "1")
meta$Media <- factor(meta$Media); meta$Replicate <- factor(meta$Replicate)
designs <- list(D1 = ~ Strain, D2 = ~ Media + Strain, D3 = ~ Replicate + Strain + Media)
fmt <- function(x) ifelse(is.na(x), "NA", formatC(x, digits = 17, format = "g"))
for (dk in names(designs)) {
  joint <- DESeq(DESeqDataSetFromMatrix(cnt, meta, designs[[dk]]), quiet = TRUE)
  for (s in c("97", "98", "99")) {
    keep <- meta$Strain %in% c("1", s)
    pair <- DESeq(DESeqDataSetFromMatrix(cnt[, keep], droplevels(meta[keep, ]), designs[[dk]]), quiet = TRUE)
    for (mk in c("M1", "M2")) {
      dds <- if (mk == "M1") joint else pair
      coef <- paste0("Strain_", s, "_vs_1")
      r1 <- results(dds, name = coef)
      r2 <- results(dds, name = coef, alpha = 0.05)
      r3 <- results(dds, name = coef, independentFiltering = FALSE)
      sh <- lfcShrink(dds, coef = coef, type = "apeglm", quiet = TRUE)
      stopifnot(identical(rownames(r1), rownames(sh)))
      out <- data.frame(gene = rownames(r1), baseMean = fmt(r1$baseMean), lfc_mle = fmt(r1$log2FoldChange),
                        lfc_apeglm = fmt(sh$log2FoldChange), padj_F1 = fmt(r1$padj), padj_F2 = fmt(r2$padj),
                        padj_F3 = fmt(r3$padj))
      write.csv(out, file.path(args[2], sprintf("bix-13_%s_%s_%s.csv", dk, mk, s)), row.names = FALSE, quote = FALSE)
    }
  }
}
cat(R.version.string, "DESeq2", as.character(packageVersion("DESeq2")), "apeglm", as.character(packageVersion("apeglm")),
    R.version$platform, "\n")
