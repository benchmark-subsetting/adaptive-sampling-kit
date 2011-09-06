import numpy as np
import sys

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
