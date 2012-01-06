#!/usr/bin/env Rscript

packages = c("gbm", "rpart", "lattice", "RJSONIO", "lhs", "tgp", "fields", "fOptions")

new.repos <- getOption("repos")
new.repos["CRAN"] <- "http://cran.stat.ucla.edu"
options(repos = new.repos)

for (p in packages) {
  # if the package is not installed or old, install/upgrade it
  if ((!(p %in% installed.packages())) | (p %in% old.packages())) {
    install.packages(p)
  }
}
