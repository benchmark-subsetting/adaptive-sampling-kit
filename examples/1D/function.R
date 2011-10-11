#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = T)
if (length(args) != 3) {
    stop("Usage: source <configuration.conf> <requested_file> <output_file>")
}

# Read the requested points
requested = read.table(args[2])

# Define the function we are studying
# (in a real experiment here we would call some measurement process)
#f <- function(x) { return (x**5*sin(x*10)) }
#f <- function(x) { return (x**3*sin(x*20)) }
f <- function(x) { return (x**5*abs(sin(x*2*pi*3))) }


# Compute f over all the requested points
requested$response = f(requested$V1)

# Write results
write.table(requested, args[3], sep=" ", quote=F, col.names=F, row.names=F)
