import networkx as nx
import matplotlib.pyplot as plt
from graph import Graph

def division(a, b):
    try:
        return a / float(b)
    except ZeroDivisionError:
        if a > 0:
            return float('+inf')
        else:
            return float('-inf')

class Partition(Graph):
    
    def compute(self):
        self.P = [set() for p in range(self.k)]
        self.S = [0 for p in range(self.k)] 
        self.E = [set() for x in range(self.k)]
        self.C = set()
        for n in self.nodes_iter():
            p = self.node[n]['partition']
            self.P[p].add(n)
            self.S[p] += 1
        for e in self.edges_iter():
            p0 = self.node[e[0]]['partition']
            p1 = self.node[e[1]]['partition']
            self[e[0]][e[1]]['edge'] = e
            if p0 == p1:
                self.E[p0].add(e)
            else:
                self.C.add(e)
        self.K = [self.cut(p) for p in range(self.k)]
        self.W = {p: self.weight(p) for p in range(self.k)}

    # Cut of a graph of two partition p1, p2
    def cut(self, p1=None, p2=None):
        if p1 == None and p2 == None:
            return sum([sum([self.cut(p1, p2) for p2 in range(p1+1, self.k)]) for p1 in range(self.k)])
        elif p2 == None:
            return sum([self.cut(p1, p2) for p2 in range(self.k) if p1 != p2])
        elif p1 == None:
            return self.cut(g, p2)
        else:
            return sum([self[e[0]][e[1]]['weight'] for e in self.C if (self.node[e[0]]['partition'] == p1 and self.node[e[1]]['partition'] == p2) or (self.node[e[1]]['partition'] == p1 and self.node[e[0]]['partition'] == p2)])

    # Weight of a partition p
    def weight(self, p):
        return sum([self[e[0]][e[1]]['weight'] for e in self.E[p]])

    # Balance of a graph
    def balance(self):
        return max(self.W.values()) * self.k / float(sum(self.W.values()))

    # Cut ratio of a graph
    def ratio(self):
        return sum([division(self.K[p], self.W[p]) for p in range(self.k)])

    def draw(self, label=False):
        layout = nx.spring_layout(self)
        if label:
            nx.draw_networkx_labels(self, layout)
        colors = ['r', 'b', 'y', 'g', 'c', 'm', 'k', '#eeffcc']
        for p in range(self.k):
            nx.draw_networkx_nodes(self, layout,
                                   nodelist=self.P[p], 
                                   node_color=colors[p],
                                   alpha=0.8)
            nx.draw_networkx_edges(self, layout,
                                   edgelist=self.E[p],
                                   edge_color=colors[p],
                                   width=3, alpha=0.8)
        nx.draw_networkx_edges(self, layout, edgelist=self.C)
        plt.show()
