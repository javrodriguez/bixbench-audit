d <- Sys.glob("/Users/<user>/aegis-builds/e5b-bixbench-lane/runs/data-2026-10-01/data/bix-52/CapsuleData-*")[1]
rp <- readLines("/Users/<user>/aegis-builds/e5b-bixbench-lane/inputs/zf/GCF_003957565.2_bTaeGut1.4.pri_assembly_report.txt")
rp <- rp[!startsWith(rp, "#")]
f <- strsplit(rp, "\t")
ln <- c()
for (x in f) if (length(x) > 8 && x[2] == "assembled-molecule" && !(x[1] %in% c("MT","bTaeGut1_MT"))) ln[sub("mat_","",sub("SUPER_","",x[1]))] <- as.numeric(x[9])
cpg <- read.csv(file.path(d, "ZF_AgeRelated_CpG_noMT_Final.csv"), colClasses = c(Chromosome = "character"))
cpg$Chromosome <- trimws(cpg$Chromosome)
cpg$site <- paste0(cpg$Chromosome, ":", cpg$StartPosition)
cpg$x <- cpg$MethylationPercentage > 90 | cpg$MethylationPercentage < 10
anyx <- tapply(cpg$x, cpg$site, any); chr <- tapply(cpg$Chromosome, cpg$site, function(v) v[1])
U <- list(U2 = table(chr[anyx]), U3 = table(cpg$Chromosome[cpg$x]))
for (u in names(U)) {
  ob <- U[[u]]
  ks <- list(K1 = names(ln), K2 = names(ln)[names(ln) %in% names(ob)], K3 = sort(unique(cpg$Chromosome)))
  for (k in names(ks)) { o <- as.numeric(ob[ks[[k]]]); o[is.na(o)] <- 0
    r <- suppressWarnings(chisq.test(o, p = ln[ks[[k]]] / sum(ln[ks[[k]]])))
    cat(u, "E1", k, sprintf("%.4f", r$statistic), r$parameter, sum(o), "\n") }
}
