import numpy as np
from scipy import optimize

def constant_reg(data):
    """
    Computes a constant fit of the np.array data.
    ret : np.vector with the single constant fit..
    res : residues (difference between the fit and the curve for each point
          of the curve).
    """
    reg = np.array([np.mean(data[:,-1])])
    res = (data[:,-1] - reg)

    return reg, res

def multivariate_reg(data):
    """
    Computes a linear regression of the np.array data.
    The last column of data is assummed to be the dependent variable (measure).
    The other columns are the dimensions over which the regression is computed.

    Returns the couple (ret, res)

    ret : np.vector with the regression factors for each dimensions
          followed by the constant intercept.
    res : residues (difference between the fit and the curve for each point
          of the curve).

    As an example consider the following small example:
            x (1,3)
           /
    (0,1) /
         x

    >>> multivariate_reg(np.array([[0,1], [1,3]]))
    (array([ 2.,  1.]), array([ 0.,  0.]))

    The linear regression is the line: 2x + 1
    and the residues vector is null since the fitting is perfect.
    """

    d = data.shape[1]
    def f(*args):
        params = args[0][:-1]
        const = args[0][-1]
        var = args[1:d]
        assert(len(var)==d-1)
        fitness = args[d]

        f=const-fitness
        for p,v in zip(params,var):
          f+=p*v
        return f

    args = tuple([data[:,i]
                  for i in range(d)])

    ret, err = optimize.leastsq(
        f,
        np.zeros(d),
        args=args)

    res = f(ret,*args)
    return ret,res


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
