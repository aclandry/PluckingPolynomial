import copy
from sympy.abc import q
import matplotlib.pyplot as plt
from igraph import *


#Vertex Class
class Vertex:
    def __init__(self, graph, order, parent, delay):
        graph.tree.insert(order, self)
        self.graph = graph
        if parent == None:
            self.parent = None
        else:
            self.parent = self.graph.tree[parent]
        self.delay = delay


    @property
    def order(self):
        return self.graph.tree.index(self)


    def r(self):
        return len(self.graph.tree) - self.order - 1


#Tree Class
class Tree:
    def __init__(self):
        self.tree = []


    def add(self, *args):
        if len(args) == 2:
            Vertex(self, args[0], args[1], 1)
        elif len(args) == 3:
            Vertex(self, args[0], args[1], args[2])


    def reduce(self):
        for vertex in self.tree:
            if vertex.delay > 1:
                vertex.delay -= 1


    def split(self):
        ones = self.ones
        split = [[copy.deepcopy(self), leaf.r()] for leaf in ones]

        for c, data in enumerate(split):
            del data[0].tree[ones[c].order]
            data[0].reduce()

        return split


    def draw(self):
        g = Graph()
        g.add_vertices(len(self.tree))
        edges = []

        for count, vertex in enumerate(self.tree):
            if vertex.parent != None:
                edges.append((vertex.parent.order, count))
   

        g.add_edges(edges)
        g.vs["delay"] = [vertex.delay if vertex in self.leaves else None for vertex in self.tree]

        visual_style = {}
        visual_style["vertex_label"] = g.vs["delay"]

        fig, ax = plt.subplots()
        layout = g.layout_reingold_tilford(root=[0])
        plot(g, layout=layout, target=ax, **visual_style)
        plt.show()


    @property
    def leaves(self):
        leaves = []
        nums = [inc for inc, obj in enumerate(self.tree)]
       
        for vertex in self.tree:
            if vertex.parent != None and vertex.parent.order in nums:
                nums.remove(vertex.parent.order)

        for order in nums:
            leaves.append(self.tree[order])

        return leaves


    @property
    def ones(self):
        ones = []
        nums = [inc for inc, obj in enumerate(self.tree)]
       
        for vertex in self.tree:
            if vertex.parent != None and vertex.parent.order in nums:
                nums.remove(vertex.parent.order)

        for order in nums:
            if self.tree[order].delay == 1:
                ones.append(self.tree[order])

        return ones
           
#Plucking Polynomial Function
def Q(t):
    if len(t.tree) < 2:
        return 1

    elif len(t.ones) < 1:
        return 0

    else:
        split = t.split()
        s = 0

        for data in split:
            s += q**data[1] * Q(data[0])

        return s.expand()

