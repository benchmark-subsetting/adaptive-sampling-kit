def residues(d,T):
    x = d[:,:-1]

    y = map(lambda x: T.compute(x), x)
    err = []
    for a,b in zip(d[:,-1],y):
        err.append((a-b))
    return err
