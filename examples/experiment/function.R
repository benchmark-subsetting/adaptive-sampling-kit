#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = T)
if (length(args) != 3) {
    stop("Usage: source <configuration.conf> <requested_file> <output_file>")
}

# Read the requested points
requested = read.table(args[2])

# Define the function we are studying
# (in a real experiment here we would call some measurement process)
myf <- function (x1,x2) {
  x1 = x1/100
  x2 = x2/100
  return (x1 * exp(-x1*x1 - x2*x2))
}

# Compute f over all the requested points
requested$response = myf(requested$V1, requested$V2)

print(summary(requested))
# Write results
write.table(requested, args[3], sep=" ", quote=F, col.names=F, row.names=F)
