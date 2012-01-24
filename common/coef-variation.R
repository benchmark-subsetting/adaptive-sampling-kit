#!/usr/bin/env Rscript
# This module computes the coefficient of variation upper bound

suppressPackageStartupMessages(require(MBESS, quietly=T))

# Parse the arguments
args <- commandArgs(trailingOnly = T)
if (length(args) != 4) {
    stop("Usage: coef-variation mean sd sample-size alpha")
}

i_mean=as.real(args[1])
i_sd=as.real(args[2])
i_n=as.integer(args[3])
i_alpha=as.real(args[4])

print(ci.cv(mean=i_mean,sd=i_sd,n=i_n,conf.level=i_alpha)$Upper.Limit.CofV)


