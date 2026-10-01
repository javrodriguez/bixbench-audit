# bix-13-q1 critic probes (CHANGES-11): review 2 part B rerun under the lane hashing. EVERY READING HERE WAS ADDED
# AFTER THE KEY WAS KNOWN; none enters the rubric. Part A of the original lives in bix-36-origin.R.
# Part B, bix-13-q1 readings the lane never ran: DESeq2's thresholded test (lfcThreshold, greaterAbs) at 1.5 and
#   log2(1.5), normal-shrunk fold changes, and the notebook's three dropped samples with the question's cut-off.
# Usage: Rscript bix-13-probes2.R <data_root>
suppressPackageStartupMessages({ library(DESeq2); library(jsonlite); library(BiocParallel) })
register(MulticoreParam(4))
args <- commandArgs(trailingOnly = TRUE)
DATA <- args[1]
out <- list()
{
  d <- Sys.glob(file.path(DATA, "bix-13", "CapsuleData-*"))
  meta0 <- read.csv(file.path(d, "experiment_metadata.csv"), stringsAsFactors = FALSE)
  cnt0 <- read.csv(file.path(d, "raw_counts.csv"), row.names = 1, check.names = FALSE)
  designs <- list(D1 = ~ Strain, D3 = ~ Replicate + Strain + Media)
  for (drop in c("all36", "dropped")) for (dk in names(designs)) {
    meta <- if (drop == "dropped") meta0[!meta0$AzentaName %in% c("resub-5", "resub-10", "resub-33"), ] else meta0
    cnt <- as.matrix(cnt0[, meta$AzentaName]); storage.mode(cnt) <- "integer"
    meta$Strain <- relevel(factor(meta$Strain), ref = "1")
    meta$Media <- factor(meta$Media); meta$Replicate <- factor(meta$Replicate)
    dds <- DESeq(DESeqDataSetFromMatrix(cnt, meta, designs[[dk]]), quiet = TRUE, parallel = TRUE)
    sets <- list()
    for (s in c("97", "98", "99")) {
      coef <- paste0("Strain_", s, "_vs_1")
      r <- results(dds, name = coef)
      nrm <- lfcShrink(dds, coef = coef, type = "normal", quiet = TRUE)
      ok <- function(x) !is.na(x) & x
      sets[[s]] <- list(
        post15 = rownames(r)[ok(r$padj < 0.05 & abs(r$log2FoldChange) > 1.5)],
        nrm15 = rownames(r)[ok(r$padj < 0.05 & abs(nrm$log2FoldChange) > 1.5)],
        thr15 = { t <- results(dds, name = coef, lfcThreshold = 1.5, altHypothesis = "greaterAbs"); rownames(t)[ok(t$padj < 0.05)] },
        thrlin = { t <- results(dds, name = coef, lfcThreshold = log2(1.5), altHypothesis = "greaterAbs"); rownames(t)[ok(t$padj < 0.05)] },
        thr15_post = { t <- results(dds, name = coef, lfcThreshold = 1.5, altHypothesis = "greaterAbs"); rownames(t)[ok(t$padj < 0.05 & abs(t$log2FoldChange) > 1.5)] },
        padj = rownames(r)[ok(r$padj < 0.05)])
    }
    for (rule in names(sets[["97"]])) {
      a <- sets[["97"]][[rule]]; b <- sets[["98"]][[rule]]; c <- sets[["99"]][[rule]]
      num <- setdiff(intersect(a, c), b); u <- union(union(a, b), c)
      out[[paste(drop, dk, rule, sep = "-")]] <- list(num = length(num), de97 = length(a), union = length(u),
        pct_de97 = 100 * length(num) / max(1, length(a)), pct_union = 100 * length(num) / max(1, length(u)))
    }
  }
}
out$env <- list(R = R.version.string, DESeq2 = as.character(packageVersion("DESeq2")), apeglm = as.character(packageVersion("apeglm")))
cat(toJSON(out, auto_unbox = TRUE, digits = I(10)), "\n")
