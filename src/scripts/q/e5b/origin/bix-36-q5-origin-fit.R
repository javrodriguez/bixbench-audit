#!/usr/bin/env Rscript
# bix-36-q5 origin fit (E5B-CHANGES-4; written after the key and the reference notebook were read).
# The notebook (cells 27-29, 46-49) fits pydeseq2 three times (~ celltype; reference CD4, CD8, CD14) on genes whose
# name contains "MI" with total >= 10 over the non-PBMC samples, collects the six comparison columns of varm["LFC"]
# (natural log), plots their histograms and calls them "normally distributed" (cell 49). This rebuild, as E5a's
# bix-36-origin.R part A, writes those six columns, MLE and apeglm, on the natural-log scale, one row per gene.
# Usage: Rscript bix-36-q5-origin-fit.R <data_root> <out_csv>
suppressPackageStartupMessages({ library(DESeq2); library(BiocParallel) })
register(MulticoreParam(4))
args <- commandArgs(trailingOnly = TRUE)
d <- Sys.glob(file.path(args[1], "bix-36", "CapsuleData-*"))
stopifnot(length(d) == 1)
sa <- read.csv(file.path(d, "Sample_annotated_Zenodo.csv"), stringsAsFactors = FALSE)
sa <- sa[sa$celltype != "PBMC", ]
full <- as.matrix(read.csv(file.path(d, "BatchCorrectedReadCounts_Zenodo.csv"), row.names = 1, check.names = FALSE))
full <- full[, sa$sample]
nb <- full[grepl("MI", rownames(full), fixed = TRUE), ]
nb <- nb[rowSums(nb) >= 10, ]
cnt <- round(nb); cnt[cnt < 0] <- 0L; storage.mode(cnt) <- "integer"
cols <- c("celltype_CD8_vs_CD4", "celltype_CD14_vs_CD4", "celltype_CD19_vs_CD4",
          "celltype_CD14_vs_CD8", "celltype_CD19_vs_CD8", "celltype_CD19_vs_CD14")
mle <- list(); ape <- list()
for (ref in c("CD4", "CD8", "CD14")) {
  cd <- data.frame(celltype = relevel(factor(sa$celltype), ref = ref), row.names = sa$sample)
  dds <- DESeq(DESeqDataSetFromMatrix(cnt, cd, ~ celltype), quiet = TRUE, parallel = TRUE)
  for (nm in intersect(resultsNames(dds)[-1], cols)) {
    if (!is.null(mle[[nm]])) next
    mle[[nm]] <- coef(dds)[, nm] * log(2)
    ape[[nm]] <- lfcShrink(dds, coef = nm, type = "apeglm", quiet = TRUE, parallel = TRUE)$log2FoldChange * log(2)
  }
}
stopifnot(all(cols %in% names(mle)))
fmt <- function(v) ifelse(is.na(v), "NA", formatC(v, digits = 17, format = "g"))
out <- data.frame(gene = rownames(cnt))
for (c in cols) { out[[paste0("mle_", c)]] <- fmt(mle[[c]]); out[[paste0("ape_", c)]] <- fmt(ape[[c]]) }
write.csv(out, args[2], row.names = FALSE, quote = FALSE)
cat(nrow(cnt), "genes", R.version.string, "DESeq2", as.character(packageVersion("DESeq2")), "\n")
