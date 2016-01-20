import networkx as nx
import matplotlib.pyplot as plt
from graph import Graph

class Neighborhood:
    def __init__(self, graph, start):
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
        self.heap = sorted(self.heap, key=lambda label: label['weight'])

    def cost(self, node, partition):
        weight = 0
        for n in self.graph.neighbors(node):
            if self.graph.node[n]['partition'] == partition:
                weight += self.graph[node][n]['weight']
        return weight / float(self.graph.node[node]['degree'])

    def update(self, partition, node):
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
        self.heap = sorted(self.heap, key=lambda label: label['weight'])
            
    def empty(self):
        return len(self.heap) == 0

    def pop(self):
        return self.heap.pop()

class Greedy(Graph):
    def select(self, k=2):
        w = int(self.number_of_nodes()/(k + 1))
        edges = nx.dfs_edges(self, 1)
        nodes = [1]
        for n in range(1, k):
            for e in range(w):
                edge = edges.next()
            nodes.append(edge[1])
        return nodes
            
    def partition(self, k=2):
        self.k = k
        self.P = []
        for n in self.nodes_iter():
            self.node[n]['degree'] = self.degree(n) 
            self.node[n]['partition'] = None
        start = self.select(k)
        for p, n in enumerate(start):
            self.P.append([n])
            self.node[n]['partition'] = p
        neighbors =  Neighborhood(self, start)
        while not neighbors.empty():
            label = neighbors.pop()
            n = label['node']
            p = label['partition']
            self.node[n]['partition'] = p
            self.P[p].append(n)
            neighbors.update(p, n)

    def labelize(self):
        self.E = [[] for x in range(self.k + 1)]
        self.C = [[[] for y in range(self.k)] for x in range(self.k)]
        for x in range(self.k):
            for y in range(x, self.k):
                self.C[x][y] = self.C[y][x]
        for e in self.edges_iter():
            p0 = self.node[e[0]]['partition']
            p1 = self.node[e[1]]['partition']
            if p0 == p1:
                self.E[p0].append(e)
            else:
                self.C[p0][p1].append(e)
                self.E[-1].append(e)
        

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
        nx.draw_networkx_edges(self, layout, edgelist=self.E[-1])
        plt.show()
            
