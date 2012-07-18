# Copyright (c) 2011-2012, Université de Versailles St-Quentin-en-Yvelines
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

import numpy as np
import sys
import os
import subprocess

def fatal(msg, exitcode = 1):
    """
    Reports fatal error and die with exitcode.
    """
    sys.stderr.write(str(msg) + "\n")
    sys.exit(exitcode)

def find_closest(points, p):
    return min(zip(abs(points-p),points))[1]

def multiselect(x, set):
    """
    Returns a boolean np.array that contains True for the elements
    in x that are in set.
    """
    if len(set) == 0:
        return np.array([False]*x.size)
    l = x == set[0]
    for v in set[1:]:
        l = l | (x == v)
    return l

def get_cov_ub(mean, sd, card, confidence):
    """
    Returns the confidence interval upper-bound of the coefficient of variance.

    mean: empirical mean of the distribution
    sd: empirical standard deviation of the distribution
    card: number of samples in the distribution
    confidence: 0.9 means the upper-bound is correct 90% of the time
    """
    coef_path = os.path.join(os.environ["ASKHOME"],"./common/coef-variation.R")
    p = subprocess.Popen(map(str,[coef_path, mean, sd, card, confidence]), 
            stdout=subprocess.PIPE)
    out, err = p.communicate()
    print float(out.split()[1])
    return float(out.split()[1])


