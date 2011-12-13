#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = T)

if (length(args) != 6) {
    stop("Usage: 1D.R <configuration> <test_set> <predicted> <labelled> <newly_labelled> <output.png>")
}

source(file.path(Sys.getenv("ASKHOME"), "common/configuration.R"))
require(rjson, quietly=T)


testset = read.table(args[2])
predicted = read.table(args[3])
labelled = read.table(args[4])
newlylabelled = read.table(args[5])
outputpng = args[6]

D = data.frame(X=testset$V1,
               E=abs(testset$V2-predicted$V2),
               P=predicted$V2)

pdf(file=outputpng)
plot(testset$V1, testset$V2, t="l", col="white", xlab="factor", ylab="response")
hierarchical_dump = file.path(conf("output_directory"), "hierarchical.dump")
if (file.exists(hierarchical_dump)) {
    hierarchical = read.table(hierarchical_dump, header=T)

    for (i in 1:nrow(hierarchical)) {
        p = hierarchical[i,]

        p$vu = p$mean+p$variance
        p$vl = p$mean-p$variance
        p$mu = p$mean+p$ub
        p$ml = p$mean-p$ub

        rect(p$mi,p$ml,p$ma,p$mu, border=NA, col="wheat")
        rect(p$mi,p$vl,p$ma,p$vu, border=NA, col="seashell")
    }
}

lines(testset$V1, testset$V2, t="l")

rug(labelled$V1)
#lines(predicted$V1, predicted$V2, t="l", col="green")
lab = labelled[1:(nrow(labelled)-nrow(newlylabelled)),] 
points(lab$V1, lab$V2)
points(newlylabelled$V1, newlylabelled$V2,col="red", pch=4)
legend("topleft", c("samples", "last iteration samples"), col=c("black", "red"), pch=c(1,4))


# write time series statistics
stats_out = conf("modules.reporter.params.timeseries", "")
if (stats_out != "") {
    card = nrow(labelled)
    res = testset$V2 - predicted$V2
    mean_err = mean(abs(res))
    max_err = max(abs(res))
    rmse_err = sqrt(mean(res*res))
    sf = file(stats_out, "a")
    writeLines(paste(card, mean_err, max_err, rmse_err),con=sf,sep="\n")
    close(sf)
}
