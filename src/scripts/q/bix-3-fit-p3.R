#!/usr/bin/env Rscript
# bix-3 fits under pseudo-count reading P3 (CHANGES-8), ADDED AFTER RECORDED RUN 1 AND AFTER READING THE REFERENCE
# NOTEBOOK: "scale to integer pseudo-counts" read as scaling each sample to counts per million over all genes of the
# table, then rounding (the notebook's cell 29 does this). Same models, contrasts and outputs as bix-3-fit-v2.R:
# A1-M1 (Control, all three tissues, ~ Tissue), A1-M2 (Control, the two tissues compared), A2-M1 (all mice,
# ~ Response + Tissue; final vs baseline blood only). Tables are written with tag P3.
# Usage: Rscript bix-3-fit-p3.R <normcount_csv> <out_dir>
suppressPackageStartupMessages({ library(DESeq2); library(BiocParallel) })
register(MulticoreParam(workers = 4))
args <- commandArgs(trailingOnly = TRUE)
dir.create(args[2], recursive = TRUE, showWarnings = FALSE)
x <- read.csv(args[1], check.names = FALSE, stringsAsFactors = FALSE)
cols <- setdiff(colnames(x), "GeneID")
m <- as.matrix(x[, cols]); rownames(m) <- make.unique(as.character(x$GeneID))
stopifnot(!anyNA(m), length(cols) == 90, all(colSums(m) > 0))
p3 <- round(sweep(m, 2, colSums(m), "/") * 1e6)
storage.mode(p3) <- "integer"
tissue <- sub("^(Control|good_responder|bad_responder)_(.*?)[0-9]+$", "\\2", cols)
resp <- sub("^(Control|good_responder|bad_responder)_.*$", "\\1", cols)
cd_all <- data.frame(row.names = cols, Tissue = factor(tissue, levels = c("baseline_blood", "final_blood", "dentate_gyrus")),
                     Response = factor(resp, levels = c("Control", "good_responder", "bad_responder")))
stopifnot(!anyNA(cd_all$Tissue), all(table(cd_all$Tissue, cd_all$Response) == 10))
contrasts <- list(FB_BB = c("final_blood", "baseline_blood"), DG_BB = c("dentate_gyrus", "baseline_blood"),
                  DG_FB = c("dentate_gyrus", "final_blood"))
fmt <- function(v) ifelse(is.na(v), "NA", formatC(v, digits = 17, format = "g"))
fit <- function(keep, design) {
  DESeq(DESeqDataSetFromMatrix(p3[, keep], droplevels(cd_all[keep, , drop = FALSE]), design), quiet = TRUE, parallel = TRUE)
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
ctrl <- cd_all$Response == "Control"
dds <- fit(ctrl, ~ Tissue)
for (ck in names(contrasts)) write_res(dds, ck, "A1_M1_P3")
for (ck in names(contrasts)) write_res(fit(ctrl & cd_all$Tissue %in% contrasts[[ck]], ~ Tissue), ck, "A1_M2_P3")
write_res(fit(rep(TRUE, length(cols)), ~ Response + Tissue), "FB_BB", "A2_M1_P3")
cat(R.version.string, "DESeq2", as.character(packageVersion("DESeq2")), R.version$platform, "\n")
