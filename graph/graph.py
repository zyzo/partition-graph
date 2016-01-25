import urllib as url
import networkx as nx
import matplotlib.pyplot as plt

class Graph(nx.Graph):
    def parse(self, data):
        self.clear()
        data.readline()
        for x, line in enumerate(data):
            self.add_weighted_edges_from([(x+1, int(y), 1) for y in line.split()])
        return self
    
    def load(self, path):
        data = open(path, 'r')
        self.parse(data)
        data.close()
        return self

    def download(self, path):
        data = url.urlopen(path)
        self.parse(data)
        data.close()
        return self

    def sample(self):
        G = nx.karate_club_graph()
        for e in G.edges_iter():
            self.add_edge(e[0], e[1])
            self[e[0]][e[1]]['weight'] = 1
        return self

    def draw(self, label=False):
        layout = nx.spring_layout(self)
        nx.draw_networkx_nodes(self, layout)
        nx.draw_networkx_edges(self, layout)
        if (label):
            nx.draw_networkx_labels(self, layout)
        plt.show()
        
        

    
