#!/usr/bin/env Rscript

if(!("gbm" %in% .packages(all.available=TRUE))) {
  new.repos <- getOption("repos")
  new.repos["CRAN"] <- "http://cran.stat.ucla.edu"
  options(repos = new.repos)
  install.packages("gbm")
}

if(!("rpart" %in% .packages(all.available=TRUE))) {
  new.repos <- getOption("repos")
  new.repos["CRAN"] <- "http://cran.stat.ucla.edu"
  options(repos = new.repos)
  install.packages("rpart")
}

if(!("lattice" %in% .packages(all.available=TRUE))) {
  new.repos <- getOption("repos")
  new.repos["CRAN"] <- "http://cran.stat.ucla.edu"
  options(repos = new.repos)
  install.packages("lattice")
}
