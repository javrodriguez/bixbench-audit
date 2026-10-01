#!/usr/bin/env Rscript
# bix-13 origin reconstruction (CHANGES-6): not a reading of either question; evidence of where the keys come from.
# Written after the recorded run and after reading the reference notebook (cells 18-24), before this script ran.
# The notebook drops samples resub-5, resub-10 and resub-33 as outliers (cell 18), fits ~ Replicate + Strain + Media
# on the rest (cells 20-21), calls a gene significant at padj < 0.05 with no fold-change cut-off (cell 23), and draws
# a ggvenn diagram of the three significant sets (cell 24); ggvenn labels each region with its count and its share of
# the union of the three sets.
# Output: every Venn region's count and its percentage of the union, with and without the three samples dropped.
# Usage: Rscript bix-13-origin.R <data_root>
suppressPackageStartupMessages({ library(DESeq2); library(jsonlite) })
args <- commandArgs(trailingOnly = TRUE)
d <- Sys.glob(file.path(args[1], "bix-13", "CapsuleData-*"))
stopifnot(length(d) == 1)
meta0 <- read.csv(file.path(d, "experiment_metadata.csv"), stringsAsFactors = FALSE)
cnt0 <- read.csv(file.path(d, "raw_counts.csv"), row.names = 1, check.names = FALSE)
out <- list()
for (drop in c("dropped", "all36")) {
  meta <- if (drop == "dropped") meta0[!meta0$AzentaName %in% c("resub-5", "resub-10", "resub-33"), ] else meta0
  cnt <- as.matrix(cnt0[, meta$AzentaName]); storage.mode(cnt) <- "integer"
  meta$Strain <- relevel(factor(meta$Strain), ref = "1")
  meta$Media <- factor(meta$Media); meta$Replicate <- factor(meta$Replicate)
  dds <- DESeq(DESeqDataSetFromMatrix(cnt, meta, ~ Replicate + Strain + Media), quiet = TRUE)
  s <- lapply(c(`97` = "97", `98` = "98", `99` = "99"), function(k) {
    r <- results(dds, contrast = c("Strain", k, "1")); rownames(r)[!is.na(r$padj) & r$padj < 0.05] })
  u <- union(union(s[["97"]], s[["98"]]), s[["99"]])
  region <- function(a, b, c) length(Filter(function(g) (g %in% s[["97"]]) == a && (g %in% s[["98"]]) == b &&
                                              (g %in% s[["99"]]) == c, u))
  regs <- list(only97 = region(TRUE, FALSE, FALSE), only98 = region(FALSE, TRUE, FALSE), only99 = region(FALSE, FALSE, TRUE),
               r97_98 = region(TRUE, TRUE, FALSE), r97_99 = region(TRUE, FALSE, TRUE), r98_99 = region(FALSE, TRUE, TRUE),
               all3 = region(TRUE, TRUE, TRUE))
  out[[drop]] <- list(samples = ncol(cnt), union = length(u), n_sig = lapply(s, length), regions = regs,
                      pct_of_union = lapply(regs, function(n) 100 * n / length(u)))
}
cat(toJSON(list(evidence = "bix-13 origin reconstruction", results = out,
                env = list(R = R.version.string, DESeq2 = as.character(packageVersion("DESeq2")))),
           auto_unbox = TRUE, digits = I(17)), "\n")
