#!/usr/bin/env Rscript
# Copyright (c) 2011-2012, Universite de Versailles St-Quentin-en-Yvelines
#
# This file is part of ASK.  ASK is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

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


