import numpy as np

import math

def compute_squared_error(d, T):
    x = d[:,:-1]

    y = map(lambda x: T.compute(x), x)
    err = 0
    for a,b in zip(d[:,-1],y):
        err+=(a-b)**2
    return math.sqrt(err/len(x))


def compute_max_error(d, T):
    x = d[:,:-1]

    y = map(lambda x: T.compute(x), x)
    err = 0
    for a,b in zip(d[:,-1],y):
        err=max(abs(a-b), err)
    return err
 
def compute_mean_error(d, T):
    x = d[:,:-1]

    y = map(lambda x: T.compute(x), x)
    err = 0
    for a,b in zip(d[:,-1],y):
        err+=abs(a-b)
    return err/float(len(x))
 

def compute_per_error(d, T):
    x = d[:,:-1]

    y = map(lambda x: T.compute(x), x)
    err = 0
    for a,b in zip(d[:,-1],y):
        err+=abs(a-b)/a
    return err/float(len(x))*100.0 

def compute_nerr_error(d, T, threshold):
    x = d[:,:-1]

    y = map(lambda x: T.compute(x), x)
    nerr = 0
    for a,b,xx in zip(d[:,-1],y, x):
        if abs(a-b)/a > threshold:
            nerr +=1

    return nerr 
