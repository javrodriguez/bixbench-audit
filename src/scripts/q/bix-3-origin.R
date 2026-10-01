#!/usr/bin/env Rscript
# bix-3 origin reconstruction (CHANGES-9): not a reading of any question; evidence of where the keys come from.
# Written after the recorded run and the P3 run, and after reading the reference notebook's cells 18-41 and 55-67.
# The notebook transposes the table (samples as rows, cell 26), drops genes whose total over the 90 samples is below
# 10 (cell 27), then scales each GENE (its column) to sum 1e6 over the 90 samples and rounds (cell 29: `.sum()` on a
# samples-by-genes frame sums per gene). It fits Control samples only, design ~ Tissue (cell 33, pydeseq2), and keeps
# DEGs with padj < 0.05, |log2FC| > 1 and baseMean >= 10 (cell 41); proportions use n = all 25,402 genes (cell 56);
# Wilson intervals at 95% (cell 61); the dentate-gyrus-specific count excludes genes DE in the other two comparisons.
# This script repeats that in R DESeq2 1.46.0 (not pydeseq2), so its numbers may differ slightly from the notebook's.
# Usage: Rscript bix-3-origin.R <normcount_csv>
suppressPackageStartupMessages({ library(DESeq2); library(BiocParallel); library(jsonlite) })
register(MulticoreParam(workers = 4))
args <- commandArgs(trailingOnly = TRUE)
x <- read.csv(args[1], check.names = FALSE, stringsAsFactors = FALSE)
cols <- setdiff(colnames(x), "GeneID")
m <- as.matrix(x[, cols]); rownames(m) <- make.unique(as.character(x$GeneID))
stopifnot(length(cols) == 90, nrow(m) == 25402)
keep_g <- rowSums(m) >= 10
mg <- m[keep_g, ]
pg <- round(mg / rowSums(mg) * 1e6)
storage.mode(pg) <- "integer"
ctrl <- grepl("^Control_", cols)
tissue <- factor(sub("^Control_(.*?)[0-9]+$", "\\1", cols[ctrl]), levels = c("baseline_blood", "final_blood", "dentate_gyrus"))
dds <- DESeq(DESeqDataSetFromMatrix(pg[, ctrl], data.frame(row.names = cols[ctrl], Tissue = tissue), ~ Tissue),
             quiet = TRUE, parallel = TRUE)
deg <- function(a, b) {
  r <- results(dds, contrast = c("Tissue", a, b))
  rownames(r)[!is.na(r$padj) & r$padj < 0.05 & abs(r$log2FoldChange) > 1 & r$baseMean >= 10]
}
fb_bb <- deg("final_blood", "baseline_blood"); dg_bb <- deg("dentate_gyrus", "baseline_blood")
dg_fb <- deg("dentate_gyrus", "final_blood")
z <- 1.959963984540054
wilson <- function(k, n) { p <- k / n; d <- 1 + z^2 / n; c0 <- (p + z^2 / (2 * n)) / d
  h <- z * sqrt(p * (1 - p) / n + z^2 / (4 * n^2)) / d; c(lo = c0 - h, pt = p, hi = c0 + h) }
specific <- setdiff(setdiff(dg_bb, dg_fb), fb_bb)
out <- list(genes_kept = sum(keep_g), control_samples = sum(ctrl),
            q1_fb_bb_degs = length(fb_bb), q2_wilson_all_genes = as.list(wilson(length(fb_bb), 25402)),
            q3_dg_bb_specific = length(specific),
            n_degs = list(FB_BB = length(fb_bb), DG_BB = length(dg_bb), DG_FB = length(dg_fb)),
            base_mean_range = as.list(range(results(dds, contrast = c("Tissue", "final_blood", "baseline_blood"))$baseMean)))
cat(toJSON(list(evidence = "bix-3 origin reconstruction", results = out,
                env = list(R = R.version.string, DESeq2 = as.character(packageVersion("DESeq2")))),
           auto_unbox = TRUE, digits = I(17)), "\n")
