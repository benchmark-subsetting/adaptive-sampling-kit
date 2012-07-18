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

def linear(reg,*args):
    """
    reg: a numpy vector that contains the coefficients of a n-dim affine equation.
         (the constant intercept is last).
    args: the n coordinates of a point.

    returns the value of the affine equation for the passed point.

    For example to compute f(x) = 2.x + 1 when x = 2,
   we can call:
    >>> import numpy as np
    >>> linear(np.array([ 2.,  1.]), 2)
    5.0
    """
    f = reg[-1]
    assert(len(reg)-1 == len(args))
    for p,v in zip(reg, args):
        f+=p*v
    return f

if __name__ == "__main__":
    import doctest
    doctest.testmod()
