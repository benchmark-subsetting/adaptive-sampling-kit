#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = T)

if (length(args) != 6) {
    stop("Usage: 4D_stencil.R <configuration> <test_set> <predicted> <labelled> <newly_labelled> <output.png>")
}

source(file.path(Sys.getenv("ASKHOME"), "common/configuration.R"))
testset = read.table(args[2])
predicted = read.table(args[3])
labelled = read.table(args[4])
newlylabelled = read.table(args[5])
outputpng = args[6]

suppressPackageStartupMessages(require(graphics, quietly=T))
suppressPackageStartupMessages(require(lattice, quietly=T))
png(file=outputpng, width=1000, height=1200)

colnames(testset)   =  c("N","M","dimX","dimY","cpi")
colnames(predicted) =  c("N","M","dimX","dimY","cpi")
colnames(labelled)   =  c("N","M","dimX","dimY","cpi")

testset=testset[testset$N > 64 & testset$M > 64,]
predicted=predicted[predicted$N > 64 & predicted$M > 64,]

ep = levelplot(cpi ~ N * M | dimX + dimY,
	       data=testset,
               cuts=40,
               at=seq(from=min(testset$cpi),to=max(testset$cpi), length=41),
               col.regions=rev(heat.colors(41)),
               main="exhaustive"
	      )

pp = levelplot(cpi ~ N * M | dimX + dimY,
	       data=predicted,
               cuts=40,
               at=seq(from=min(testset$cpi),to=max(testset$cpi), length=41),
               col.regions=rev(heat.colors(41)),
               main="predicted",
	       panel=function(x, y, subscripts, ...) {
       		     panel.levelplot(x, y, subscripts=subscripts, ...)
		     aPoint = predicted[subscripts[1],]
		     dX = aPoint$dimX
		     dY = aPoint$dimY
		     la = labelled[labelled$dimX == dX & labelled$dimY == dY,]
            	     lpoints(la$N, la$M, pch=1, col=1, cex=1)
		     la = newlylabelled[newlylabelled$dimX == dX & newlylabelled$dimY == dY,]
            	     lpoints(la$N, la$M, pch=1, col=2, cex=1)
               }
	      )

print(ep, split=c(1,1,1,2), more=TRUE)
print(pp, split=c(1,2,1,2), more=FALSE)


# write time series statistics
stats_out = conf("modules.reporter.params.timeseries", "")
if (stats_out != "") {
    card = nrow(labelled)
    res = testset$cpi - predicted$cpi
    mean_err = mean(abs(res))
    max_err = max(abs(res))
    rmse_err = sqrt(mean(res*res))
    sf = file(stats_out, "a")
    writeLines(paste(card, mean_err, max_err, rmse_err),con=sf,sep="\n")
    close(sf)
}
