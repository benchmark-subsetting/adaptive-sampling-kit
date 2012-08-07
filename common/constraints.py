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

from copy import deepcopy

from common.tree import Leaf


class OrdinalAxis:
    """
    OrdinalAxis class, tracks range constraints on an ordinal factor
    It is used during a CART tree traversal to accumulate each split node
    constraints. When the traversal is done, and a leaf is reached,
    the get_range method returns the precise range associated with the
    reached leaf.
    """
    def __init__(self, minv=-2 ** 32, maxv=2 ** 32):
        """
        Initialize an OrdinalAxis class.

        minv: minimal value of the axis
        maxv: maximal value of the axis
        """
        self.minv = minv
        self.maxv = maxv

    def add_left(self, cut):
        """
        Add a constraint when following a CART splitting node to the left.
        """
        self.maxv = min(cut, self.maxv)

    def add_right(self, cut):
        """
        Add a constraint when following a CART splitting node to the right.
        """
        self.minv = max(cut, self.minv)

    def get_range(self):
        """
        Retrieve the range that satisfies all the left and right constraints
        added.
        """
        return {"min": self.minv, "max": self.maxv}


class CategoricalAxis:
    """
    OrdinalAxis class, tracks range constraints on an categorical factor
    It is used during a CART tree traversal to accumulate each split node
    constraints. When the traversal is done, and a leaf is reached,
    the get_range method returns the precise range associated with the
    reached leaf.
    """
    def __init__(self, tags):
        """
        Initialize an CategoricalAxis class.

        tags: possible values of the categorical axis
        """

        self.belongs_to = set(range(len(tags)))
        self.tags = tags

    def add_left(self, cut):
        """
        Add a constraint when following a CART splitting node to the left.
        """
        self.add(cut[0])

    def add_right(self, cut):
        """
        Add a constraint when following a CART splitting node to the right.
        """
        self.add(cut[1])

    def add(self, ok):
        """
        Register the ''ok'' constraints, generic function used by add_left
        and add_right.
        """
        self.belongs_to = self.belongs_to.intersection(ok)

    def get_range(self):
        """
        Retrieve the range that satisfies all the left and right constraints
        added.
        """
        out = []
        for i in self.belongs_to:
            out.append(self.tags[i])
        return out


class Constraints:
    """
    Abstract Constraints class.
    It is used during a CART tree traversal to accumulate each split node
    constraints. When the traversal is done, and a leaf is reached
    the get_range method returns the precise range associated with the
    reached leaf.
    """

    def __init__(self, factors):
        """
        Initialize a Constraints class.

        factors: factors tree.py representation
        """
        self.factors = factors
        self.axes = []
        self.constraints = []

        for f in factors:
            self.axes.append(f["name"])
            if f["type"] != "categorical":
                self.constraints.append(
                OrdinalAxis(minv=f["range"]["min"],
                            maxv=f["range"]["max"]))
            else:
                self.constraints.append(
                    CategoricalAxis(f["values"]))

    def add_left(self, axis, cut):
        self.constraints[axis].add_left(cut)

    def add_right(self, axis, cut):
        self.constraints[axis].add_right(cut)

    def get_range(self):
        return dict([(a, c.get_range())
                     for a, c in zip(self.axes, self.constraints)])


def decorate_leaves(tree, C):
    """
    Use a Constraint class to accumulate the splitting constraints
    during a full tree traversal. Decorate all the leaves with the
    associated ranges.

    C: a constraint class
    tree: a tree
    """
    if isinstance(tree, Leaf):
        tree.constraint = C
        yield tree
    else:
        #left
        CL = deepcopy(C)
        CL.add_left(tree.axis, tree.cut)
        for n in decorate_leaves(tree.left, CL):
            yield n
        #right
        CR = deepcopy(C)
        CR.add_right(tree.axis, tree.cut)
        for n in decorate_leaves(tree.right, CR):
            yield n


def get_tagged_models(factors, T):
    """
    Returns an array containing each leaf in the tree 'T',
    its associated model,
    its associated range constraint,
    and a pointer to the leaf itself.

    factors: factors tree.py representation
    T: a tree
    """
    C = Constraints(factors)
    leaves = decorate_leaves(T, C)
    return [{"model":list(l.model),
            "error": l.error,
            "constraint": l.constraint.get_range(),
            "leaf": l}
            for l in leaves]
