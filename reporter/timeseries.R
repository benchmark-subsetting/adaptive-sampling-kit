#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = T)

if (length(args) != 6) {
    stop("Usage: timeseries.R <configuration> <test_set> <predicted> <labelled> <newly_labelled> <output.png>")
}

source(file.path(Sys.getenv("ASKHOME"), "common/configuration.R"))
testset = read.table(args[2])
predicted = read.table(args[3])
labelled = read.table(args[4])
newlylabelled = read.table(args[5])
outputpng = args[6]

colnames(testset)   =  c("T","N","M","dimX","dimY","cpi")
colnames(predicted) =  c("T","N","M","dimX","dimY","cpi")
colnames(labelled)   =  c("T","N","M","dimX","dimY","cpi")

# write time series statistics
stats_out = conf("modules.reporter.params.timeseries", "")
if (stats_out != "") {
    card = nrow(labelled)
    res = testset$cpi - predicted$cpi
    mean_err = mean(abs(res))
    max_err = max(abs(res))
    rmse_err = sqrt(mean(res*res))
    per_err = mean(abs(res)/testset$cpi*100)
    max_per_err = max(abs(res)/testset$cpi*100)
    sf = file(stats_out, "a")
    writeLines(paste(card, mean_err, max_err, rmse_err, per_err, max_per_err),con=sf,sep="\n")
    close(sf)
}
