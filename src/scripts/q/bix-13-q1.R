#!/usr/bin/env Rscript
# bix-13-q1. Readings, fixed before the first run (addenda 1 and 2); unit: percent.
#   D, model design: D1 ~ Strain; D2 ~ Media + Strain; D3 ~ Replicate + Strain + Media.
#   M, samples in the fit: M1 all 36 samples, one joint model; M2 JBX1 plus the one strain being tested.
#   L, fold change: L1 MLE log2FoldChange; L2 apeglm-shrunk log2 fold change.
#   F, independent filtering: F1 DESeq2 default (alpha 0.1); F2 alpha = 0.05; F3 independentFiltering = FALSE.
#   cut-offs: |log2 fold change| > 1.5 and padj < 0.05 (Benjamini-Hochberg).
#   value: 100 x |DE97 and DE99, not DE98| / |DE97|.
# Usage: Rscript bix-13-q1.R <data_root>
suppressPackageStartupMessages({ library(DESeq2); library(jsonlite) })
args <- commandArgs(trailingOnly = TRUE)
d <- Sys.glob(file.path(args[1], "bix-13", "CapsuleData-*"))
stopifnot(length(d) == 1)
meta <- read.csv(file.path(d, "experiment_metadata.csv"), stringsAsFactors = FALSE)
cnt <- read.csv(file.path(d, "raw_counts.csv"), row.names = 1, check.names = FALSE)
stopifnot(all(meta$AzentaName %in% colnames(cnt)), nrow(meta) == 36)
cnt <- as.matrix(cnt[, meta$AzentaName])
storage.mode(cnt) <- "integer"
meta$Strain <- relevel(factor(meta$Strain), ref = "1")
meta$Media <- factor(meta$Media); meta$Replicate <- factor(meta$Replicate)
designs <- list(D1 = ~ Strain, D2 = ~ Media + Strain, D3 = ~ Replicate + Strain + Media)
shrunk <- new.env()
de_set <- function(dds, tag, coef, lk, fk) {
  r <- switch(fk, F1 = results(dds, name = coef), F2 = results(dds, name = coef, alpha = 0.05),
              F3 = results(dds, name = coef, independentFiltering = FALSE))
  lfc <- if (lk == "L1") r$log2FoldChange else {
    key <- paste(tag, coef)
    if (is.null(shrunk[[key]])) shrunk[[key]] <- lfcShrink(dds, coef = coef, type = "apeglm", quiet = TRUE)$log2FoldChange
    shrunk[[key]]
  }
  rownames(r)[!is.na(r$padj) & r$padj < 0.05 & !is.na(lfc) & abs(lfc) > 1.5]
}
out <- list()
for (dk in names(designs)) {
  joint <- DESeq(DESeqDataSetFromMatrix(cnt, meta, designs[[dk]]), quiet = TRUE)
  pair <- list()
  for (s in c("97", "98", "99")) {
    keep <- meta$Strain %in% c("1", s)
    m2 <- droplevels(meta[keep, ])
    pair[[s]] <- DESeq(DESeqDataSetFromMatrix(cnt[, keep], m2, designs[[dk]]), quiet = TRUE)
  }
  for (mk in c("M1", "M2")) for (lk in c("L1", "L2")) for (fk in c("F1", "F2", "F3")) {
    de <- list()
    for (s in c("97", "98", "99")) {
      dds <- if (mk == "M1") joint else pair[[s]]
      tag <- paste(dk, mk, if (mk == "M1") "joint" else s)
      de[[s]] <- de_set(dds, tag, paste0("Strain_", s, "_vs_1"), lk, fk)
    }
    stopifnot(length(de[["97"]]) > 0)
    num <- setdiff(intersect(de[["97"]], de[["99"]]), de[["98"]])
    out[[paste(dk, mk, lk, fk, sep = "-")]] <- list(value = 100 * length(num) / length(de[["97"]]), unit = "percent",
      n_de97 = length(de[["97"]]), n_de98 = length(de[["98"]]), n_de99 = length(de[["99"]]),
      numerator = length(num), defensible = TRUE)
  }
}
env <- list(R = R.version.string, DESeq2 = as.character(packageVersion("DESeq2")),
            apeglm = as.character(packageVersion("apeglm")), platform = R.version$platform)
cat(toJSON(list(question_id = "bix-13-q1", readings = out, meta = list(genes = nrow(cnt), samples = ncol(cnt), env = env)),
           auto_unbox = TRUE, digits = I(17)), "\n")
