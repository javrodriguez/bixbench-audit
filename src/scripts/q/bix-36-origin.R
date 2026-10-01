#!/usr/bin/env Rscript
# bix-36-q1 origin rebuild and critic's readings (CHANGES-11), rerunning adversarial review 2's probes (parts A, C and
# its in-window RPKM reading) under the lane's own hashing. EVERY READING HERE WAS ADDED AFTER THE KEY WAS KNOWN;
# none enters the rubric. Self-contained: reads only the bix-36 capsule data.
#   A  origin: the notebook's gene set (pandas `contains("MIR*")` is a regex, "MI" then any number of "R", so any
#      name containing "MI"; then total >= 10 over the 565 non-PBMC samples), ~ celltype, three fits with CD4, CD8 and
#      CD14 as reference (cells 27-29); the six comparison columns of cell 47 on the natural-log scale (pydeseq2's
#      varm["LFC"]), MLE and apeglm-shrunk; one-way ANOVA F with equal variances (scipy f_oneway, cell 50).
#   C  base-R rebuild of the lane's 12 pre-registered readings (no pandas or scipy): Fisher F and Welch F.
#   R  the RPKM reading review 2 found in the key window: miRNA-biotype genes with total >= 10 over the kept samples,
#      RPKM (gene length from GeneMetaInfo, library size = each sample's total over all genes), log2(x + 0.5),
#      each gene's mean per cell type as the observation, Fisher F.
# Usage: Rscript bix-36-origin.R <data_root>
suppressPackageStartupMessages({ library(DESeq2); library(jsonlite); library(BiocParallel) })
register(MulticoreParam(4))
args <- commandArgs(trailingOnly = TRUE)
d <- Sys.glob(file.path(args[1], "bix-36", "CapsuleData-*"))
stopifnot(length(d) == 1)
gm <- read.csv(file.path(d, "GeneMetaInfo_Zenodo.csv"), stringsAsFactors = FALSE)
sa <- read.csv(file.path(d, "Sample_annotated_Zenodo.csv"), stringsAsFactors = FALSE)
sa <- sa[sa$celltype != "PBMC", ]
full <- as.matrix(read.csv(file.path(d, "BatchCorrectedReadCounts_Zenodo.csv"), row.names = 1, check.names = FALSE))
full <- full[, sa$sample]
stopifnot(ncol(full) == 565, all(is.finite(full)))
out <- list()

# A: origin
nb <- full[grepl("MI", rownames(full), fixed = TRUE), ]
nb <- nb[rowSums(nb) >= 10, ]
cnt <- round(nb); storage.mode(cnt) <- "integer"
lfc <- list(); ape <- list()
for (ref in c("CD4", "CD8", "CD14")) {
  cd <- data.frame(celltype = relevel(factor(sa$celltype), ref = ref), row.names = sa$sample)
  dds <- DESeq(DESeqDataSetFromMatrix(cnt, cd, ~ celltype), quiet = TRUE, parallel = TRUE)
  for (nm in resultsNames(dds)[-1]) {
    lfc[[nm]] <- coef(dds)[, nm] * log(2)
    ape[[nm]] <- lfcShrink(dds, coef = nm, type = "apeglm", quiet = TRUE, parallel = TRUE)$log2FoldChange * log(2)
  }
}
cols <- c("celltype_CD8_vs_CD4", "celltype_CD14_vs_CD4", "celltype_CD19_vs_CD4",
          "celltype_CD14_vs_CD8", "celltype_CD19_vs_CD8", "celltype_CD19_vs_CD14")
anova6 <- function(L) {
  y <- unlist(lapply(cols, function(c) L[[c]])); g <- factor(rep(cols, each = length(L[[cols[1]]])))
  ok <- is.finite(y); a <- oneway.test(y[ok] ~ g[ok], var.equal = TRUE)
  list(F = unname(a$statistic), p = a$p.value, non_finite = sum(!ok))
}
out$A <- list(genes = nrow(cnt), rows_starting_MIR = sum(startsWith(rownames(cnt), "MIR")),
              example_non_MIR = head(rownames(cnt)[!startsWith(rownames(cnt), "MIR")], 5),
              mle = anova6(lfc), apeglm = anova6(ape))

# C: base-R rebuild of the 12 pre-registered readings
x <- full[rownames(full) %in% gm$Geneid[gm$gene_biotype == "miRNA"], ]
ty <- c("CD4", "CD8", "CD14", "CD19")
C <- list()
for (ek in c("E1", "E2")) for (tk in c("T1", "T2")) {
  xe <- if (ek == "E1") x else x[rowSums(x) > 0, ]
  xt <- if (tk == "T1") xe else log2(xe + 1)
  obs <- list(S1 = lapply(ty, function(t) colMeans(xt[, sa$celltype == t, drop = FALSE])),
              S2 = lapply(ty, function(t) as.vector(xt[, sa$celltype == t, drop = FALSE])),
              S3 = lapply(ty, function(t) rowMeans(xt[, sa$celltype == t, drop = FALSE])))
  for (sk in names(obs)) {
    y <- unlist(obs[[sk]]); g <- factor(rep(ty, sapply(obs[[sk]], length)))
    C[[paste(sk, tk, ek, sep = "-")]] <- list(fisher = unname(oneway.test(y ~ g, var.equal = TRUE)$statistic),
                                             welch = unname(oneway.test(y ~ g)$statistic))
  }
}
out$C <- C

# R: the in-window RPKM reading
len <- setNames(gm$Length, gm$Geneid)
xr <- x[rowSums(x) >= 10, ]
lib <- colSums(full)
rpkm <- sweep(xr / (len[rownames(xr)] / 1e3), 2, lib / 1e6, "/")
lt <- log2(rpkm + 0.5)
grp <- lapply(ty, function(t) rowMeans(lt[, sa$celltype == t, drop = FALSE]))
yr <- unlist(grp); gr <- factor(rep(ty, sapply(grp, length)))
out$R <- list(genes = nrow(xr), fisher = unname(oneway.test(yr ~ gr, var.equal = TRUE)$statistic))
out$env <- list(R = R.version.string, DESeq2 = as.character(packageVersion("DESeq2")), apeglm = as.character(packageVersion("apeglm")))
cat(toJSON(out, auto_unbox = TRUE, digits = I(17)), "\n")
