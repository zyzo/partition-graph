#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

## Read inputs

data = open(sys.argv[1], 'r')
#data.readline()
n, e = [int(x) for x in data.readline().split()]
g, e = [], []
ge = []
for idx, line in enumerate(data):
    split = line.split()
    g.append([int(x) for x in split])
    e.append(len(split))
    ge.append((idx, len(split)))
data.close()
ge = sorted(ge, key=lambda node: node[1], reverse=True)

## Select starting points
## Pistes d'amélioration possibles : choisir les starting points qui ne sont pas connectés
P = int(sys.argv[2])
start = []
for idx in range(P):
    start.append(ge[idx][0])
print "Starting points: " + str(start)
partitions = [[x] for x in start]

## Cost function
def cost(partitions, g, node):
    res = []
    for p in partitions:
        cnt = 0
        for edge in g[node]:
            if (edge in p): 
                cnt += 1
        res.append(cnt)
    return res
       
## Launch greedy algorithm


for i in range(P,n):
    print ge[i][0]
    costs = cost(partitions, g, ge[i][0])
    partitions[costs.index(max(costs))].append(ge[i][0])
    print [[x+1 for x in l] for l in partitions]
    
    