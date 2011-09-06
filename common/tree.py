import os
import pickle
import tempfile
from colors import colors
from regression import linear

def tree2dot(outfilename, tree, axes, categories):
    """
    Dumps a tree in dotty format.

    outfilename : name of the output dot file
    tree : the tree to dump
    axes : a list of strings containing the label for the axes
    categories : a list of dictionnaries that returns for each
                 categorical axis, the labels of each category.
                 For instance, if dimension 3 contains three
                 classes: 1-> blue, 2-> red, 3 -> green
                 then categories[3] = {1:"blue", 2:"red", 3:"green"}
    """
    f = open(outfilename, "w")
    f.write("graph decisionT {\n"+tree.todot(axes, categories)+"\n}")
    f.close()

def tree2png(outfilename, tree, axes, categories):
    """
    Dumps a tree in png.

    outfilename : name of the output png file
    tree : the tree to dump
    axes : a list of strings containing the label for the axes
    categories : a list of dictionnaries that returns for each
                 categorical axis, the labels of each category.
                 For instance, if dimension 3 contains three
                 classes: 1-> blue, 2-> red, 3 -> green
                 then categories[3] = {1:"blue", 2:"red", 3:"green"}
    """
    dotfile = tempfile.NamedTemporaryFile()
    tree2dot(dotfile.name, tree, axes, categories)
    os.system("dot -Tpng -o {0} {1}".format(outfilename, dotfile.name))
    dotfile.close()


def Lformat(L, pl=6):
    """
    Line format utility function.
    L: a list of tags.
    pl: the number of tags per line

    returns a string representation of the tags with exactly pl tags
    per line.
    """
    lines = []
    for i,v in enumerate(L):
        lines.append(v)
        if i%pl==pl-1:
            lines.append("\\n")
    return ",".join(lines)

def tag_leaves(tree):
    """
    Decorates the leaves of a tree with consecutive numeric tags
    going from 0 to NUMBER_OF_LEAVES-1.

    The tag is added inside each leaf object in parameter tag
    (leaf.tag).

    Returns NUMBER_OF_LEAVES-1.

    As an example consider this three leaved tree:
    >>> T = Node(Node(Leaf([0]),\
                      Leaf([1]),\
                      0,0,[]),\
                 Leaf([2]),\
                 0,0,[])
    >>> tag_leaves(T)
    2
    >>> list(map(lambda l: l.tag, leaf_iterator(T)))
    [0, 1, 2]
    """
    leaves = list(leaf_iterator(tree))
    for i,leaf in enumerate(leaves):
        leaf.tag = i
    return len(leaves)-1

def leaf_iterator(tree):
    """
    Returns a generator that iterates over all leaves of a tree
    in depth first order.

    As an example consider this three leaved tree:
    >>> T = Node(Node(Leaf([0]),\
                      Leaf([1]),\
                      0,0,[]),\
                 Leaf([2]),\
                 0,0,[])
    >>> list(leaf_iterator(T))
    [L([0]), L([1]), L([2])]
    """
    if isinstance(tree, Leaf):
        yield tree
    else:
        for subtree in [tree.left, tree.right]:
            for n in leaf_iterator(subtree):
                yield n

def node_iterator(tree):
    """
    Returns a generator that iterates over all nodes of a tree
    in depth first order.

    """
    if isinstance(tree, Leaf):
        yield tree
    else:
        yield tree
        for subtree in [tree.left, tree.right]:
            for n in node_iterator(subtree):
                yield n


def save_tree(T, output_file):
    f = open(output_file, "w")
    pickle.dump(T, f)
    f.close()

def load_tree(input_file):
    f = open(input_file, "r")
    return pickle.load(f)
    f.close()

class Node():
    """
    Regression tree internal node.
    """
    def __init__(self,left,right,axis,cut,model,categorical=False):
        """
        left, right (Node) : left and right subtrees
        axis (int) : axis over which this node splits the domain
        cut : cut point for this node
              * for ordinal data: a value v, the cut is done for
                (all x < v , all x >= v)
              * for categorical data: a 2-uplet containing the
                two classes. For example to separate odd and even
                categories ([1,3,5], [2,4,6]).
        model : the linear model associated to this subtree
        categorical : is this cut categorical ?
        """
        self.left = left
        self.right = right
        self.axis = axis
        self.model = model
        self.cut = cut
        self.categorical=categorical
        self.data = []

    def fill(self, point):
        """
        point: array of coordinates for a point
        returns the value predicted by the tree for the
        given point.
        """
        self.data.append(point)
        p = point[self.axis]
        if self.categorical:
            is_left = (p in self.cut[0])
        else:
            is_left = p < self.cut

        if is_left:
            return self.left.fill(point)
        else:
            return self.right.fill(point)

    def compute(self, point):
        """
        point: array of coordinates for a point
        returns the value predicted by the tree for the
        given point.
        """
        p = point[self.axis]
        if self.categorical:
            is_left = (p in self.cut[0])
        else:
            is_left = p < self.cut

        if is_left:
            return self.left.compute(point)
        else:
            return self.right.compute(point)

    def whichnode(self, point):
        """
        point: array of coordinates for a point
        returns the leaf responsible for modeling
        the passed point.
        """
        p = point[self.axis]
        if self.categorical:
            is_left = p in self.cut[0]
        else:
            is_left = p < self.cut

        if is_left:
            return self.left.whichnode(point)
        else:
            return self.right.whichnode(point)

    def whichmodel(self, point):
        """
        point: array of coordinates for a point
        returns the tag of the leaf responsible for modeling
        the passed point.
        """
        p = point[self.axis]
        if self.categorical:
            is_left = p in self.cut[0]
        else:
            is_left = p < self.cut

        if is_left:
            return self.left.whichmodel(point)
        else:
            return self.right.whichmodel(point)

    def todot(self, axes=None, categories=None):
        """
        Internal function to output the tree in dot format.
        """
        out = []
        if self.categorical:
            labelsl = Lformat([categories[self.axis][i] for i in self.cut[0]])
            labelsr = Lformat([categories[self.axis][i] for i in self.cut[1]])
            out.append("{0} [label=\"{1}\"];"
                       .format(id(self),axes[self.axis]))
        else:
            labelsr = labelsl = ""
            out.append("{0} [label=\"{1} < {2}\"];"
                       .format(id(self),axes[self.axis],"%.2f"%self.cut))
        out.append(self.left.todot(axes,categories))
        out.append(self.right.todot(axes,categories))
        out.append("{0} -- {1} [label=\"{2}\"];".format(id(self), id(self.left), labelsl))
        out.append("{0} -- {1} [label=\"{2}\"];".format(id(self), id(self.right), labelsr))
        return "\n".join(out)

class Leaf(Node):
    """
    Regression tree leaf node.
    """
    def __init__(self, model, error=None):
        """
        model : the linear model associated to this leaf
        """
        self.model = model
        self.error = error
        self.data = []

    def compute(self, point):
        regression_d = len(self.model)-1
        if regression_d == 0:
            return self.model[0]
        else:
            p = point[-regression_d:]
            return linear(self.model, *p)

    def fill(self, point):
        self.data.append(point)
        
    def whichmodel(self, point=None):
        return self.tag

    def whichnode(self, point=None):
        return self

    def __repr__(self):
        return "L({0})".format(repr(self.model))

    def todot(self, axes=None, categories=None):
        model = "*%s*|"%self.tag+"|".join(["%.4f"%v for v in self.model])
        return (
            "{0} [label=\"{{{1}}}\", shape=\"record\",color=\"{2}\"];"
                .format(id(self),model,colors[self.tag%len(colors)]))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
