# -*- coding: utf-8 -*-
import sys
import math
import random
from gurobipy import *

import urllib

def parse_graph(data):
    n, e = [int(x) for x in data.readline().split()]
    g = []
    for idx, line in enumerate(data):
        split = line.split()
        g.append([[int(x),1] for x in split])
    return [n, e, g]

def read_local(filepath):
    data = open(filepath, 'r')
    graph = parse_graph(data)
    data.close()
    return graph


n, e, g = read_local("../heuristic/test.graph")
print g

m = Model()

# Create n random points

random.seed(1)
partition = []
for i in range(n):
    partition.append((random.randint(0,100),random.randint(0,100)))

representative = []
for i in range(n):
    representative.append(0)

K = 3
m = Model()

# Create variables

def is_edge(g, i, j):
    for a in g[i]:
        if a[0] == j: return a[1]
    return 0

vars = {}
for i in range(n):
    for j in range(i+1):
        poids = is_edge(g,i,j)
        vars[i,j] = m.addVar(obj=poids, vtype=GRB.BINARY,
                             name='cut'+str(i)+'_'+str(j))
        vars[j,i] = vars[i,j]
for i in range(n):
    representative[i] = m.addVar(obj=0.0, vtype=GRB.BINARY, name='representative'+str(i))
m.update()

# Add triangle inequality constraints
for i in range(n):
    for j in range(i+1):
        for k in range(j+1):
            m.addConstr(vars[i,j] + vars[i,k] >= vars[j,k])
            m.addConstr(vars[i,j] + vars[j,k] >= vars[i,k])
            m.addConstr(vars[i,k] + vars[j,k] >= vars[i,j])
m.update()

# Add partition representative constraint (node with smallest index is representative)
# If not representative, there is a node with smaller index in partition
for i in range(n):
    m.addConstr(representative[i] + quicksum(vars[i,j] for j in range(i)) >= 1)
m.update()
# If is representative, there is no node with smaller index in partition
for i in range(n):
    m.addConstr(representative[i] + quicksum(vars[i,j] for j in range(i)) <= 1)
m.update()
# Add unique representative constraint
# If representative, there is no node with smaller index in partition which is also a representative
for i in range(n):
    for j in range(i):
        m.addConstr(representative[i] + vars[i,j] + representative[j] <= 2)
m.update()
# Add partition number constraint
m.addConstr(quicksum(representative[i] for i in range(n)) == K)
m.update()

m._vars = vars
m.ModelSense = 1
m.optimize()
if m.Status == GRB.OPTIMAL:
    solution = m.ObjVal
else:
    print "toto"