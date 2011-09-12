import numpy as np
import math
import os
import tempfile
from util import fatal
from tree import *

def compute_leaf_error(data, T, params):
    for d in data:
        T.fill(d[:-1])

    for N in node_iterator(T):
        if "leaferror" in params:
            le = params["leaferror"](np.array(N.data), [], params, [])
            N.error = le

def parse_cart_tree(lines, categories):
    nodes = {}
    for l in lines[5:]:
        # read a node
        sp = l.split()
        number = int(sp[0][:-1])

        if sp[1] == "root":
            node = {"prediction": float(sp[4])}
        else:
            if ">" in sp[1] or "<" in sp[1]:
                if ">" in sp[1]:
                    axis = sp[1].split(">=")
                    direction = 1
                else:
                    axis = sp[1].split("<")[0], sp[2]
                    direction = 0
                    sp.pop(2)

                node = {"axis": int(axis[0][1:])-1,
                        "cut": float(axis[1]),
                        "prediction": float(sp[4]),
                        "direction": direction}
            else:
                axis = sp[1].split("=")
                node = {"axis": int(axis[0][1:])-1,
                        "choices": map(int, axis[1].split(",")),
                        "prediction": float(sp[4])}
        nodes[number] = node


    def get_tree(n):
        #is it a leaf
        if 2*n not in nodes: return Leaf(model=[nodes[n]["prediction"]])

        #get left child
        left = get_tree(2*n)
        right = get_tree(2*n+1)

        if "choices" in nodes[2*n]:
            lc = nodes[2*n]["choices"]
            rc = nodes[2*n+1]["choices"]
            axis = nodes[2*n]["axis"]

            chosen = set(lc + rc)
            allp =  set(list(range(len(categories[axis]))))
            missing = allp-chosen
            rc += list(missing)

            return Node(left, right,
                        axis= axis,
                        cut=(lc,
                             rc),
                        model=[nodes[n]["prediction"]],
                        categorical=True
                        )
        else:
            if nodes[2*n]["direction"] == 0:
                return Node(left, right,
                            axis=nodes[2*n]["axis"],
                            cut=nodes[2*n]["cut"],
                            model=[nodes[n]["prediction"]],
                            categorical=False
                            )
            else:
                return Node(right, left,
                            axis=nodes[2*n]["axis"],
                            cut=nodes[2*n]["cut"],
                            model=[nodes[n]["prediction"]],
                            categorical=False
                            )
    return get_tree(1)


def build_tree(conf, cp, input_file):
    temp_dir = tempfile.mkdtemp()
    ti = os.path.join(temp_dir, "rcart.R")
    to = os.path.join(temp_dir, "out")
    categories = []
    rfile = open(ti, "w")

    rfile.write('library(rpart)\n')
    rfile.write('data = read.table("{0}")\n'.
            format(input_file))

    for i,f in enumerate(conf["factors"]):
        if f["type"] == "categorical":
            rfile.write('data$V{0} = as.factor(data$V{1})\n'
                        .format(i+1,i+1))
            categories.append(f["values"])
        else:
            categories.append(f["range"])


    rfile.write("rtree = rpart(data$V{0} ~ . , data=data, "
                "control=rpart.control(cp={1}))\n".format(i+2,cp))

    rfile.write("print(rtree)\n")
    rfile.close()

    print "Building CART model ..."
    os.system("R --slave --no-save < {0} > {1}".format(ti, to))

    tf = open(to, "r")
    print "Parsing CART tree"
    T = parse_cart_tree(tf.readlines(), categories)
    tf.close()
    return T
