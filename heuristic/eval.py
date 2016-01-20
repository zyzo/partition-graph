from greedy import Greedy
import numpy as np

# Cut of a graph of two partition p1, p2
def cut(g, p1=None, p2=None):
    if p1 == None and p2 == None:
        return sum([sum([cut(g, p1, p2) for p2 in range(p1+1, g.k)]) for p1 in range(g.k)])
    elif p2 == None:
        return sum([cut(g, p1, p2) for p2 in range(g.k) if p1 != p2])
    elif p1 == None:
        return cut(g, p2)
    else:
        return sum([g[e[0]][e[1]]['weight'] for e in g.C[p1][p2]])

# Weight of a partition p
def weight(g, p):
    return sum([g[e[0]][e[1]]['weight'] for e in g.E[p]])

# Cut ratio of a graph
def ratio(g):
    return sum([cut(g, p)/float(weight(g, p)) for p in range(g.k)])
