# r2 probe: bix-52-q3 length-free readings (E2 equal per chromosome, E3 prop. to all age-related sites) in base R chisq.test
d <- Sys.glob(file.path(commandArgs(TRUE)[1], "bix-52", "CapsuleData-*"))
z <- read.csv(file.path(d, "ZF_AgeRelated_CpG_noMT_Final.csv"), colClasses=c(Chromosome="character"))
z$Chromosome <- trimws(z$Chromosome)
f <- z[z$MethylationPercentage > 90 | z$MethylationPercentage < 10, ]
ds <- tapply(f$Pos, f$Chromosome, function(p) length(unique(p)))   # distinct filtered sites (U2) per chrom (K3)
bg <- tapply(z$Pos, z$Chromosome, function(p) length(unique(p)))
cat("U2-E2-K3", unname(suppressWarnings(chisq.test(ds)$statistic)), "\n")
cat("U2-E3-K3", unname(suppressWarnings(chisq.test(ds, p=bg[names(ds)]/sum(bg[names(ds)]))$statistic)), " (only chroms with sites)\n")
o <- setNames(rep(0, length(bg)), names(bg)); o[names(ds)] <- ds
cat("U2-E3-K3 all data chroms", unname(suppressWarnings(chisq.test(o, p=bg/sum(bg))$statistic)), "\n")
rows <- table(f$Chromosome); o3 <- setNames(rep(0,length(bg)),names(bg)); o3[names(rows)] <- rows
bgr <- table(z$Chromosome)[names(bg)]
cat("U3-E2-K3", unname(suppressWarnings(chisq.test(o3)$statistic)), " U3-E3-K3", unname(suppressWarnings(chisq.test(o3, p=bgr/sum(bgr))$statistic)), "\n")
