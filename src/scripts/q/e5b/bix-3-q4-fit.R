#!/usr/bin/env Rscript
# bix-3-q4 (E5b) DESeq2 fits. Readings named from the question's words before any run and before the key was read.
# Input: the NormCount CSV written by E5a's frozen bix-3-prep.py (90 samples: three response groups x three tissues x 10).
#   Contrasts (fixed by the words): FB_BB final vs baseline blood; DG_BB dentate gyrus vs baseline blood;
#     DG_FB dentate gyrus vs final blood.
#   A, cohort and design (the words name neither): A1 Control mice only, ~ Tissue; A2 all mice, ~ Response + Tissue;
#     A3 Control mice only, paired, ~ Animal + Tissue (each sample number appears once per tissue within a response
#     group, read as one animal); A4 all mice, ~ Tissue (E5B-CHANGES-1, pre-run review MINOR 9: A3 and A4 added).
#   M, samples in the fit: M1 all three tissues in one fit; M2 only the two tissues compared, one fit per contrast
#     (A1 and A2 only; A3 and A4 are fitted as M1 only, to bound machine time; disclosed).
#   Not carried over from E5a's bix-3 readings, because q4's words do not name them: apeglm-shrunk fold changes,
#     DESeq2's lfcThreshold test, the baseMean >= 10 criterion (bix-3-q1's words), and any global pseudo-count scale
#     (Javier ruled the x10 scale not fair for bix-3).
#   P, integer input (DESeq2 needs counts; the sheet holds normalised values): P1 round(), size factors estimated;
#     P2 round(), size factors fixed at 1.
#   Per contrast: baseMean, MLE log2FoldChange, padj under F1 default (alpha 0.1), F2 alpha 0.05,
#     F3 independentFiltering = FALSE.
# Usage: Rscript bix-3-q4-fit.R <normcount_csv> <out_dir>
suppressPackageStartupMessages({ library(DESeq2); library(BiocParallel) })
register(MulticoreParam(workers = 4))
args <- commandArgs(trailingOnly = TRUE)
dir.create(args[2], recursive = TRUE, showWarnings = FALSE)
x <- read.csv(args[1], check.names = FALSE, stringsAsFactors = FALSE)
cols <- setdiff(colnames(x), "GeneID")
m <- as.matrix(x[, cols]); rownames(m) <- make.unique(as.character(x$GeneID))
stopifnot(!anyNA(m), length(cols) == 90)
tissue <- sub("^(Control|good_responder|bad_responder)_(.*?)[0-9]+$", "\\2", cols)
resp <- sub("^(Control|good_responder|bad_responder)_.*$", "\\1", cols)
animal <- paste(resp, sub("^[^0-9]*([0-9]+)$", "\\1", cols), sep = "_")
cd_all <- data.frame(row.names = cols, Tissue = factor(tissue, levels = c("baseline_blood", "final_blood", "dentate_gyrus")),
                     Response = factor(resp, levels = c("Control", "good_responder", "bad_responder")),
                     Animal = factor(animal))
stopifnot(all(table(cd_all$Animal, cd_all$Tissue) == 1))
stopifnot(!anyNA(cd_all$Tissue), all(table(cd_all$Tissue, cd_all$Response) == 10))
contrasts <- list(FB_BB = c("final_blood", "baseline_blood"), DG_BB = c("dentate_gyrus", "baseline_blood"),
                  DG_FB = c("dentate_gyrus", "final_blood"))
fmt <- function(v) ifelse(is.na(v), "NA", formatC(v, digits = 17, format = "g"))
fit <- function(keep, design, pk) {
  ic <- round(m[, keep]); storage.mode(ic) <- "integer"
  dds <- DESeqDataSetFromMatrix(ic, droplevels(cd_all[keep, , drop = FALSE]), design)
  if (pk == "P2") sizeFactors(dds) <- rep(1, ncol(dds))
  DESeq(dds, quiet = TRUE, parallel = TRUE)
}
write_res <- function(dds, ck, tag) {
  ctr <- c("Tissue", contrasts[[ck]])
  r1 <- results(dds, contrast = ctr); r2 <- results(dds, contrast = ctr, alpha = 0.05)
  r3 <- results(dds, contrast = ctr, independentFiltering = FALSE)
  out <- data.frame(gene = rownames(r1), baseMean = fmt(r1$baseMean), lfc_mle = fmt(r1$log2FoldChange),
                    padj_F1 = fmt(r1$padj), padj_F2 = fmt(r2$padj), padj_F3 = fmt(r3$padj))
  write.csv(out, file.path(args[2], sprintf("bix-3q4_%s_%s.csv", tag, ck)), row.names = FALSE, quote = FALSE)
}
designs <- list(A1 = ~ Tissue, A2 = ~ Response + Tissue, A3 = ~ Animal + Tissue, A4 = ~ Tissue)
for (pk in c("P1", "P2")) {
  for (ak in c("A1", "A2", "A3", "A4")) {
    cohort <- if (ak %in% c("A1", "A3")) cd_all$Response == "Control" else rep(TRUE, length(cols))
    dds <- fit(cohort, designs[[ak]], pk)
    for (ck in names(contrasts)) write_res(dds, ck, paste(ak, "M1", pk, sep = "_"))
    if (ak %in% c("A3", "A4")) next
    for (ck in names(contrasts)) {
      keep <- cohort & cd_all$Tissue %in% contrasts[[ck]]
      write_res(fit(keep, designs[[ak]], pk), ck, paste(ak, "M2", pk, sep = "_"))
    }
  }
}
cat(R.version.string, "DESeq2", as.character(packageVersion("DESeq2")), R.version$platform, "\n")
