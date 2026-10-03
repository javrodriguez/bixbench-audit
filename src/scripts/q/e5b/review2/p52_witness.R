# r2 probe: mutation witness on length-free bix-52 readings (U2-E3-K3, U2-E2 over chromosomes with sites): plant 20 filtered sites on chr 1
d <- Sys.glob(file.path(commandArgs(TRUE)[1], "bix-52", "CapsuleData-*"))
z <- read.csv(file.path(d, "ZF_AgeRelated_CpG_noMT_Final.csv"), colClasses=c(Chromosome="character"))
z$Chromosome <- trimws(z$Chromosome); z <- z[, c("Pos","Chromosome","MethylationPercentage")]
run <- function(z, tag) {
  f <- z[z$MethylationPercentage > 90 | z$MethylationPercentage < 10, ]
  bg <- tapply(z$Pos, z$Chromosome, function(p) length(unique(p)))
  o <- setNames(rep(0, length(bg)), names(bg)); ds <- tapply(f$Pos, f$Chromosome, function(p) length(unique(p))); o[names(ds)] <- ds
  cat(tag, "U2-E3-K3", unname(suppressWarnings(chisq.test(o, p=bg/sum(bg))$statistic)),
      " U2-E2 (chroms with sites)", unname(suppressWarnings(chisq.test(ds)$statistic)), "\n")
}
run(z, "base   ")
run(rbind(z, data.frame(Pos=paste0("1_planted", 1:20), Chromosome="1", MethylationPercentage=99)), "planted")
