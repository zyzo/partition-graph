import networkx as nx
import matplotlib.pyplot as plt
import input
import sys
from GreedyPartitioning import GreedyPartitioning
def draw_graph(graph):

    nodes = [x for x in range(1,graph[0]+1)]
    G=nx.Graph()
    G.add_nodes_from(nodes)
    for id,edges in enumerate(graph[2]):
        for edge in edges:
            G.add_edge(id+1, edge[0])
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.show()

def draw_partitioned_graph(graph, partitions,
                           draw_label=True,
                           font_size=10,
                           node_size=100):
    nodes = [x for x in range(1,graph[0]+1)]
    G=nx.Graph()
    G.add_nodes_from(nodes)
    for id,edges in enumerate(graph[2]):
        for edge in edges:
            G.add_edge(id+1, edge[0])
    pos = nx.spring_layout(G)
    nx.draw_networkx_edges(G, pos)
    if draw_label:
        nx.draw_networkx_labels(G, pos, font_size)
    colors = ['r','b','y','g','c','m','k','#eeffcc']
    for idx, p in enumerate(partitions):
        nx.draw_networkx_nodes(G,
                               pos,
                               nodelist=p,
                               node_color=colors[idx],
                               node_size=int(node_size),
                               alpha=0.8)
    plt.show()
# draw example
g = input.read_local(sys.argv[1])
# draw_graph(g)
gp = GreedyPartitioning(sys.argv[1], sys.argv[2])
draw_partitioned_graph(g, gp.get_partitions(), draw_label=False, node_size=sys.argv[3])
