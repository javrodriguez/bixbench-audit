# r4 probe (after key): bix-3-q4 A1-M1 (Control mice, ~ Tissue, one fit), P1, apeglm-shrunk LFC for |LFC|>1, unshrunk padj.
suppressPackageStartupMessages({ library(DESeq2); library(apeglm) })
t0 <- Sys.time()
x <- read.csv("/Users/<user>/aegis-builds/e5b-bixbench-lane/runs/fits-2026-10-01/r1/bix-3_normcount.csv", check.names = FALSE)
cols <- setdiff(colnames(x), "GeneID"); m <- as.matrix(x[, cols]); rownames(m) <- make.unique(as.character(x$GeneID))
tissue <- sub("^(Control|good_responder|bad_responder)_(.*?)[0-9]+$", "\\2", cols)
resp <- sub("^(Control|good_responder|bad_responder)_.*$", "\\1", cols)
keep <- resp == "Control"
ic <- round(m[, keep]); storage.mode(ic) <- "integer"
cd <- data.frame(row.names = cols[keep], Tissue = factor(tissue[keep], levels = c("baseline_blood", "final_blood", "dentate_gyrus")))
dds <- DESeq(DESeqDataSetFromMatrix(ic, cd, ~ Tissue), quiet = TRUE)
r <- list(); a <- list()
r$FB_BB <- results(dds, contrast = c("Tissue", "final_blood", "baseline_blood"))
r$DG_BB <- results(dds, contrast = c("Tissue", "dentate_gyrus", "baseline_blood"))
a$FB_BB <- lfcShrink(dds, coef = "Tissue_final_blood_vs_baseline_blood", type = "apeglm", quiet = TRUE)$log2FoldChange
a$DG_BB <- lfcShrink(dds, coef = "Tissue_dentate_gyrus_vs_baseline_blood", type = "apeglm", quiet = TRUE)$log2FoldChange
cat("t after 2 shrinks", format(Sys.time() - t0), "\n")
d2 <- dds; d2$Tissue <- relevel(d2$Tissue, "final_blood"); d2 <- nbinomWaldTest(d2, quiet = TRUE)
r$DG_FB <- results(dds, contrast = c("Tissue", "dentate_gyrus", "final_blood"))
a$DG_FB <- lfcShrink(d2, coef = "Tissue_dentate_gyrus_vs_final_blood", type = "apeglm", quiet = TRUE)$log2FoldChange
for (bm in c(0, 10)) {
  de <- sapply(names(r), function(k) !is.na(r[[k]]$padj) & r[[k]]$padj < 0.05 & abs(a[[k]]) > 1 & r[[k]]$baseMean >= bm)
  deM <- sapply(names(r), function(k) !is.na(r[[k]]$padj) & r[[k]]$padj < 0.05 & abs(r[[k]]$log2FoldChange) > 1 & r[[k]]$baseMean >= bm)
  cat("baseMean>=", bm, " apeglm per-contrast", colSums(de), " intersection", sum(rowSums(de) == 3), " union", sum(rowSums(de) > 0),
      " | MLE intersection", sum(rowSums(deM) == 3), "\n")
}
cat("elapsed", format(Sys.time() - t0), "\n")
