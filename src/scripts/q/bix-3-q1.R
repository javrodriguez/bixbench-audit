#!/usr/bin/env Rscript
# bix-3-q1. Readings, fixed before the first run (addenda 1 and 2); unit: count of genes.
#   samples: Control_baseline_blood* and Control_final_blood*; design ~ Tissue; contrast final vs baseline.
#   P, integer pseudo-counts: P1 round(), size factors estimated; P2 round(), size factors fixed at 1.
#   F, independent filtering: F1 DESeq2 default (alpha 0.1); F2 alpha = 0.05; F3 independentFiltering = FALSE.
#   cut-offs: padj < 0.05, |MLE log2FoldChange| > 1, baseMean >= 10.
#   duplicate gene symbols stay separate rows.
# Usage: Rscript bix-3-q1.R <normcount_csv>
suppressPackageStartupMessages({ library(DESeq2); library(jsonlite) })
args <- commandArgs(trailingOnly = TRUE)
x <- read.csv(args[1], check.names = FALSE, stringsAsFactors = FALSE)
cols <- grep("^Control_(baseline|final)_blood[0-9]+$", colnames(x), value = TRUE)
m <- as.matrix(x[, cols]); rownames(m) <- make.unique(as.character(x$GeneID))
cd <- data.frame(row.names = cols, Tissue = factor(ifelse(grepl("baseline", cols), "baseline_blood", "final_blood"),
                                                  levels = c("baseline_blood", "final_blood")))
stopifnot(all(table(cd$Tissue) > 1), !anyNA(m))
out <- list()
for (pk in c("P1", "P2")) {
  ic <- round(m); storage.mode(ic) <- "integer"
  dds <- DESeqDataSetFromMatrix(ic, cd, ~ Tissue)
  if (pk == "P2") sizeFactors(dds) <- rep(1, ncol(dds))
  dds <- DESeq(dds, quiet = TRUE)
  ctr <- c("Tissue", "final_blood", "baseline_blood")
  res <- list(F1 = results(dds, contrast = ctr), F2 = results(dds, contrast = ctr, alpha = 0.05),
              F3 = results(dds, contrast = ctr, independentFiltering = FALSE))
  for (fk in names(res)) {
    r <- res[[fk]]
    keep <- !is.na(r$padj) & r$padj < 0.05 & abs(r$log2FoldChange) > 1 & r$baseMean >= 10
    out[[paste(pk, fk, sep = "-")]] <- list(value = sum(keep), unit = "count", defensible = TRUE)
  }
}
env <- list(R = R.version.string, DESeq2 = as.character(packageVersion("DESeq2")), platform = R.version$platform)
cat(toJSON(list(question_id = "bix-3-q1", readings = out,
                meta = list(samples = as.list(table(cd$Tissue)), genes = nrow(m), env = env)),
           auto_unbox = TRUE, digits = I(17)), "\n")
