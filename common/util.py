# Copyright 2011,2012 Exascale Computing Research
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

def aggregate_same_measures(data):
    aggregated = []
    measures = []
    prev = None
    for i in range(data.shape[0]):
        if prev == list(data[i,:-1]):
            measures.append(data[i,-1])
            continue
        else:
            if prev:
                aggregated.append(prev+[np.mean(measures)])
            prev = list(data[i,:-1])
            measures = [data[i,-1]]
    if prev:
        aggregated.append(prev+[np.mean(measures)])
    return np.array(aggregated)

def get_cov_ub(mean, sd, card, alpha):
    coef_path = os.path.join(os.environ["ASKHOME"],"./common/coef-variation.R")
    print mean, sd, card, alpha
    p = subprocess.Popen(map(str,[coef_path, mean, sd, card, alpha]), 
            stdout=subprocess.PIPE)
    out, err = p.communicate()
    print float(out.split()[1])
    return float(out.split()[1])


