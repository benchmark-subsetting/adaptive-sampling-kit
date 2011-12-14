#!/usr/bin/env Rscript

packages = c("gbm", "rpart", "lattice", "RJSONIO", "lhs", "tgp", "fields")

new.repos <- getOption("repos")
new.repos["CRAN"] <- "http://cran.stat.ucla.edu"
options(repos = new.repos)

for (p in packages) {
  if(!(p %in% .packages(all.available=TRUE))) {
    install.packages(p)
  }
}
