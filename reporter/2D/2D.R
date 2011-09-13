#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = T)

if (length(args) != 6) {
    stop("Usage: 2D.R <configuration> <test_set> <predicted> <labelled> <newly_labelled> <output.png>")
}

source(file.path(Sys.getenv("ASKHOME"), "common/configuration.R"))
testset = read.table(args[2])
predicted = read.table(args[3])
labelled = read.table(args[4])
newlylabelled = read.table(args[5])
outputpng = args[6]

D = data.frame(X=testset$V1,Y=testset$V2,
               E=abs(testset$V3-predicted$V3),
               P=predicted$V3)

suppressPackageStartupMessages(require(graphics, quietly=T))
suppressPackageStartupMessages(require(lattice, quietly=T))
png(file=outputpng, width=1000, height=1200)

ep = levelplot(D$E ~ D$X*D$Y, cuts=31, 
        colorkey=list(col=rev(heat.colors(32))),
        col.regions=rev(heat.colors(32)),
        at=seq(from=0,to=conf("modules.reporter.params.max_error_scale",
                              max(D$E))
          ,length=32),
        xlab="X",
        ylab="Y     (Absolute Error)",
        panel=function(...){
            panel.levelplot(...)
            lpoints(labelled$V1, labelled$V2, pch=1, col=1, cex=1)
            lpoints(newlylabelled$V1, newlylabelled$V2, pch=1, col=2, cex=1)
        }
#        main="Absolute Error"
        )


pp = levelplot(D$P ~ D$X*D$Y, cuts=31, 
        colorkey=list(col=rev(heat.colors(32))),
        col.regions=rev(heat.colors(32)), xlab="X",
        ylab="Y     (Prediction)",
        panel=function(...){
            panel.levelplot(...)
            lpoints(labelled$V1, labelled$V2, pch=1, col=1, cex=1)
            lpoints(newlylabelled$V1, newlylabelled$V2, pch=1, col=2, cex=1)
        }
        )

print(ep, split=c(1,1,1,2), more=TRUE)
print(pp, split=c(1,2,1,2), more=TRUE)


# write time series statistics
stats_out = conf("modules.reporter.params.timeseries", "") 
if (stats_out != "") {
    card = nrow(labelled)
    mean_err = mean(D$E)
    max_err = max(D$E)
    sf = file(stats_out, "a")
    writeLines(paste(card, mean_err, max_err),con=sf,sep="\n")
    close(sf)
}
