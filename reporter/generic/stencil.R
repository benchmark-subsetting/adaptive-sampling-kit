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
png(file=outputpng, width=10000, height=10000)

colnames(testset)   =  c("T","N","M","dimX","dimY","cpi")
colnames(predicted) =  c("T","N","M","dimX","dimY","cpi")
colnames(labelled)   =  c("T","N","M","dimX","dimY","cpi")

CUTS=10
LAYOUT=c(8,25)

ep = levelplot(cpi ~ N * M | T + dimX + dimY,
	       data=testset[1:12800,],
               cuts=CUTS,
               at=seq(from=min(testset$cpi),to=max(testset$cpi), length=CUTS+1),
               col.regions=rev(heat.colors(CUTS+1)),
               layout=LAYOUT,
               main="exhaustive",
               strip=strip.custom(strip.levels = c(TRUE, TRUE))
	      )

pp = levelplot(cpi ~ N * M | T + dimX + dimY,
	       data=predicted[1:12800,],
               cuts=CUTS,
               at=seq(from=min(testset$cpi),to=max(testset$cpi), length=CUTS+1),
               col.regions=rev(heat.colors(CUTS+1)),
               main="predicted",
               layout=LAYOUT,
               strip=strip.custom(strip.levels = c(TRUE, TRUE)),
	       panel=function(x, y, subscripts, ...) {
       		     panel.levelplot(x, y, subscripts=subscripts, ...)
		     aPoint = predicted[subscripts[1],]
		     dX = aPoint$dimX
		     dY = aPoint$dimY
		     dT = aPoint$T
		     la = labelled[labelled$dimX == dX & labelled$dimY == dY & labelled$T == dT,]
		     ts = testset[testset$dimX == dX & testset$dimY == dY & testset$T == dT,]
		     pe = predicted[predicted$dimX == dX & predicted$dimY == dY & predicted$T == dT,]
		     res = ts$cpi - pe$cpi
		     mean_error = mean(abs(res))
		     per_error = mean(abs(res)/ts$cpi*100) 
		     panel.text(x=1000,y=1000,cex=10,label=paste(round(mean_error,2), "/", round(per_error,2), "%"))
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
    per_err = mean(abs(res)/testset$cpi*100)
    max_per_err = max(abs(res)/testset$cpi*100)
    sf = file(stats_out, "a")
    writeLines(paste(card, mean_err, max_err, rmse_err, per_err, max_per_err),con=sf,sep="\n")
    close(sf)
}
