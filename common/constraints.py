from tree import *
from copy import deepcopy

class OrdinalAxis:
    def __init__(self,minv=-2**32,maxv=2**32):
        self.minv = minv
        self.maxv = maxv

    def add_left(self, cut):
        self.maxv = min(cut, self.maxv)
    def add_right(self, cut):
        self.minv = max(cut, self.minv)
    def get_range(self):
        return {"min":self.minv, "max":self.maxv}

class CategoricalAxis:
    def __init__(self, tags):
        self.belongs_to = set(range(len(tags)))
        self.tags = tags
    def add_left(self, cut):
        self.add(cut[0])
    def add_right(self, cut):
        self.add(cut[1])
    def add(self, ok):
        self.belongs_to = self.belongs_to.intersection(ok)
    def get_range(self):
        out = []
        for i in self.belongs_to:
            out.append(self.tags[i])
        return out

class Constraints:
    def __init__(self, factors):
        self.factors = factors
        self.axes = []
        self.constraints = []

        for i,f in enumerate(factors):
            self.axes.append(f["name"])
            if f["type"] != "categorial":
                self.constraints.append(
                OrdinalAxis(minv=f["range"]["min"],
                            maxv=f["range"]["max"])
                )
            else:
                self.constraints.append(
                    CategoricalAxis(f["values"])
                    )

    def add_left(self, axis, cut):
        self.constraints[axis].add_left(cut)
    def add_right(self, axis, cut):
        self.constraints[axis].add_right(cut)
    def get_range(self):
        return dict([(a,c.get_range())
                     for a,c in zip(self.axes, self.constraints)])

def decorate_leaves(tree, C):
    if isinstance(tree, Leaf):
        tree.constraint = C
        yield tree
    else:
        #left
        CL = deepcopy(C)
        CL.add_left(tree.axis, tree.cut)
        for n in decorate_leaves(tree.left,CL):
            yield n
        #right
        CR = deepcopy(C)
        CR.add_right(tree.axis, tree.cut)
        for n in decorate_leaves(tree.right,CR):
            yield n


def get_tagged_models(factors, T):
    C = Constraints(factors)
    leaves = decorate_leaves(T, C)
    return [{"model":list(l.model),
            "error": l.error,
            "constraint": l.constraint.get_range(),
            "leaf": l
            } for l in leaves]
