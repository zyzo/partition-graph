#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

## Read inputs

data = open(sys.argv[1], 'r')
#data.readline()
n, e = [int(x) for x in data.readline().split()]
g, sum_edges = [[]], [[]]
ge = []
visited = [[]]
for idx, line in enumerate(data):
    split = line.split()
    g.append([[int(x),1] for x in split]) # 
    sum_edges.append(len(split))          # TODO : change ça pour adapter les graphes avec poids # 1 
    ge.append((idx, len(split)))	
    visited.append(False)
data.close()
ge = sorted(ge, key=lambda node: node[1], reverse=True)

## Cost function : calculer distance "directe"
def cost(partition, g, node):
    cnt = 0
    for edge in g[node]:
        if (edge[0] in partition): 
            cnt += edge[1]
    return cnt/float(sum_edges[node])
def weight(v1, v2):
    return [x[1] for x in g[v1] if x[0] == v2][0]
## Select starting points
## Pistes d'amélioration possibles : choisir les starting points qui ne sont pas connectés
P = int(sys.argv[2])
start = []
for idx in range(P):
    start.append(ge[idx][0]+1)
    visited[ge[idx][0]+1] = True
for id in start :
    visited[id] = True
print "Starting points: " + str(start)
partitions = [[x] for x in start]
neighbours = []
for pid, partition in enumerate(partitions):
    for edge in g[partition[0]]:
        if (not visited[edge[0]]):
            neighbours.append([pid, edge[0], cost(partition, g, edge[0])])
neighbours = sorted(neighbours, key=lambda node: node[2])
def update_neighbours(neighbours, pid, inserted):
    neighbours = [x for x in neighbours if x[1] != inserted]
    n_inserted = [x[0] for x in g[inserted]]
    for n in neighbours:
        # mettre à jour les voisins de inserted
        if (n[1] in n_inserted and n[0] == pid):
             n[2] += weight(inserted, n[1])/float(sum_edges[n[1]])
             n_inserted.remove(n[1])
    for ni in n_inserted:
        if (not visited[ni]):
            neighbours.append([pid, ni, cost(partitions[pid], g, ni)])
    return neighbours
## Launch greedy algorithm
print neighbours
while neighbours:
##for i in range(2):
    next_node = neighbours.pop()
    visited[next_node[1]] = True
    partitions[next_node[0]].append(next_node[1])
    neighbours = update_neighbours(neighbours, next_node[0], next_node[1])
    print "ajouté ", next_node[1], "dans partition ", partitions[next_node[0]]
print partitions