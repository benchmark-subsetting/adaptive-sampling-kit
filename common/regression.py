import numpy as np

def linear(reg,*args):
    """
    reg: a numpy vector that contains the coefficients of a n-dim affine equation.
         (the constant intercept is last).
    args: the n coordinates of a point.

    returns the value of the affine equation for the passed point.

    For example to compute f(x) = 2.x + 1 when x = 2,
    we can call:
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
