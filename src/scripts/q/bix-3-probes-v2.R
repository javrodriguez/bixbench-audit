#!/usr/bin/env Rscript
# bix-3 probes (CHANGES-10), rerunning adversarial review 1's probes under the lane's own hashing.
# EVERY READING HERE WAS ADDED AFTER THE KEYS WERE KNOWN (after the recorded run, the notebook and review 1);
# none enters the rubric.
#   K, global pseudo-count scale before rounding: K1 x1, K10 x10, K100 x100 (NormCount carries two decimals,
#      so x100 is lossless). R stores DESeq2 counts as 32-bit integers: at x100 any gene whose largest value
#      exceeds .Machine$integer.max is DROPPED, and the dropped genes are listed in the output (no numeric path
#      exists in DESeq2's count matrix).
#   M: M1 one fit over all 30 Control samples (~ Tissue); M2 a fit over only the two tissues compared.
#   L, the fold change used for |LFC| > 1: MLE; apeglm (lfcShrink type "apeglm"; DG_FB via relevel to
#      final_blood and nbinomWaldTest); normal (lfcShrink type "normal"). padj is always the unshrunk Wald padj,
#      DESeq2 defaults (independent filtering at alpha 0.1).
#   q1 = final vs baseline blood, padj < 0.05, |LFC| > 1, baseMean >= 10.
#   q3 = DE for dentate gyrus vs baseline blood and DE in neither dentate gyrus vs final blood nor final vs
#        baseline blood (padj < 0.05, |LFC| > 1).
# Usage: Rscript bix-3-probes-v2.R <normcount_csv> <scale 1|10|100>   (v2, CHANGES-10b: one scale per run, parallel shrinkage)
suppressPackageStartupMessages({ library(DESeq2); library(BiocParallel); library(jsonlite) })
register(MulticoreParam(workers = 4))
args <- commandArgs(trailingOnly = TRUE)
x <- read.csv(args[1], check.names = FALSE, stringsAsFactors = FALSE)
cols <- setdiff(colnames(x), "GeneID")
m <- as.matrix(x[, cols]); rownames(m) <- make.unique(as.character(x$GeneID))
stopifnot(length(cols) == 90, nrow(m) == 25402, !anyNA(m))
ctrl <- grepl("^Control_", cols)
mc <- m[, ctrl]
tis <- factor(sub("^Control_(.*?)[0-9]+$", "\\1", colnames(mc)), levels = c("baseline_blood", "final_blood", "dentate_gyrus"))
stopifnot(all(table(tis) == 10))
pairs <- list(FB_BB = c("final_blood", "baseline_blood"), DG_BB = c("dentate_gyrus", "baseline_blood"),
              DG_FB = c("dentate_gyrus", "final_blood"))
lfc_tables <- function(dds, pr) {
  # returns list(padj, baseMean, mle, apeglm, normal) for contrast pr = c(num, den)
  r <- results(dds, contrast = c("Tissue", pr))
  nrm <- lfcShrink(dds, contrast = c("Tissue", pr), type = "normal", quiet = TRUE, parallel = TRUE)$log2FoldChange
  d2 <- dds
  if (levels(d2$Tissue)[1] != pr[2]) { d2$Tissue <- relevel(d2$Tissue, ref = pr[2]); d2 <- nbinomWaldTest(d2, quiet = TRUE) }
  ape <- lfcShrink(d2, coef = paste0("Tissue_", pr[1], "_vs_", pr[2]), type = "apeglm", quiet = TRUE, parallel = TRUE)$log2FoldChange
  list(padj = r$padj, baseMean = r$baseMean, MLE = r$log2FoldChange, apeglm = ape, normal = nrm, genes = rownames(r))
}
out <- list(); dropped <- list()
for (k in as.numeric(args[2])) {
  stopifnot(k %in% c(1, 10, 100))
  s <- mc * k
  over <- apply(s, 1, max) > .Machine$integer.max
  dropped[[paste0("K", k)]] <- rownames(s)[over]
  s <- round(s[!over, ]); storage.mode(s) <- "integer"
  fits <- list(M1 = DESeq(DESeqDataSetFromMatrix(s, data.frame(row.names = colnames(s), Tissue = tis), ~ Tissue),
                          quiet = TRUE, parallel = TRUE))
  tabs <- list(M1 = lapply(pairs, function(pr) lfc_tables(fits$M1, pr)), M2 = list())
  for (pk in names(pairs)) {
    keep <- tis %in% pairs[[pk]]
    d <- DESeq(DESeqDataSetFromMatrix(s[, keep], data.frame(row.names = colnames(s)[keep], Tissue = droplevels(tis[keep])),
                                      ~ Tissue), quiet = TRUE, parallel = TRUE)
    tabs$M2[[pk]] <- lfc_tables(d, pairs[[pk]])
  }
  for (mk in c("M1", "M2")) for (lk in c("MLE", "apeglm", "normal")) {
    de <- function(t, base) t$genes[!is.na(t$padj) & t$padj < 0.05 & !is.na(t[[lk]]) & abs(t[[lk]]) > 1 &
                                    (is.null(base) | t$baseMean >= 10)]
    q1 <- length(de(tabs[[mk]]$FB_BB, TRUE))
    q3 <- length(setdiff(setdiff(de(tabs[[mk]]$DG_BB, NULL), de(tabs[[mk]]$DG_FB, NULL)), de(tabs[[mk]]$FB_BB, NULL)))
    out[[sprintf("K%d-%s-%s", k, mk, lk)]] <- list(q1 = q1, q3 = q3, genes = nrow(s),
                                                  added = "after the keys were known (review 1 probes)")
  }
}
cat(toJSON(list(probe = "bix-3 global scale x estimator", readings = out, dropped_at_scale = dropped,
                env = list(R = R.version.string, DESeq2 = as.character(packageVersion("DESeq2")),
                           apeglm = as.character(packageVersion("apeglm")))), auto_unbox = TRUE, digits = I(17)), "\n")
