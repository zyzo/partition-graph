import random as rd
import networkx as nx
import matplotlib.pyplot as plt
from graph.partition import Partition, division

class Neighborhood:
    def __init__(self, graph, start, select='weight'):
        self.graph = graph
        self.heap = []
        self.sum = 0
        self.part = []
        for p, k in enumerate(start):
            self.part.append(1)
            self.sum += 1
            for n in graph.neighbors(k):
                if graph.node[n]['partition'] == None:
                    c = self.cost(n, p)
                    self.heap.append({'partition':p, 'node':n, 'cost':c, 'weight':c})
        self.heap = sorted(self.heap, key=lambda label: label[select])

    def cost(self, node, partition):
        weight = 0
        for n in self.graph.neighbors(node):
            if self.graph.node[n]['partition'] == partition:
                weight += self.graph[node][n]['weight']
        return weight / float(self.graph.node[node]['degree'])

    def update(self, partition, node, select='weight'):
        neighbors = self.graph.neighbors(node)
        inc = sum([self.graph[node][n]['weight'] for n in neighbors if self.graph.node[n]['partition'] == partition])
        self.part[partition] += inc;
        self.sum += inc;
            
        self.heap = [label for label in self.heap if label['node'] != node]

        for label in self.heap:
            n = label['node']
            if n in neighbors and label['partition'] == partition:
                label['cost'] += self.graph[node][n]['weight'] / float(self.graph.node[n]['degree'])
                neighbors.remove(n)
            label['weight'] = label['cost'] * self.sum / self.part[label['partition']]
        for n in neighbors:
            if self.graph.node[n]['partition'] == None:
                c = self.cost(n, partition)
                self.heap.append({'partition':partition, 'node':n, 'cost':c, 'weight':c * self.sum / self.part[partition]})
        self.heap = sorted(self.heap, key=lambda label: label[select])
            
    def empty(self):
        return len(self.heap) == 0

    def pop(self):
        return self.heap.pop()

class Greedy(Partition):
    def select(self, k=2, rand=False):
        if rand:
            nodes = []
            while len(nodes) != k:
                n = rd.randint(1, self.number_of_nodes())
                if not n in nodes:
                    nodes.append(n)
        else:
            w = int(self.number_of_nodes()/(k + 1))
            edges = nx.dfs_edges(self, 1)
            nodes = [1]
            for n in range(1, k):
                for e in range(w):
                    edge = edges.next()
                nodes.append(edge[1])
        return nodes
            
    def partition(self, k=2, select='weight', rand=False):
        self.k = k
        for n in self.nodes_iter():
            self.node[n]['degree'] = self.degree(n) 
            self.node[n]['partition'] = None
        start = self.select(k, rand)
        for p, n in enumerate(start):
            self.node[n]['partition'] = p
        neighbors =  Neighborhood(self, start, select)
        while not neighbors.empty():
            label = neighbors.pop()
            n = label['node']
            p = label['partition']
            self.node[n]['partition'] = p
            neighbors.update(p, n, select)
        self.compute()
        




            
