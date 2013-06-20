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
