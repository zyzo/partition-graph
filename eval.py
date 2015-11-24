# -*- coding: utf-8 -*-
import input

# Le coût de coupe de 2 sous-ensembles s1, s2 
def single_cut(g, s1, s2):
    sum = 0
    for node in s1:
        for n, cost in g[node-1]:
            if n in s2:
                sum += cost
    return sum
# Le coût de coupe d'une partition p
def cut(g, p):
    sum = 0
    for i1, s1 in enumerate(p):
        for i2 in range(i1+1,len(p)):
            sum += single_cut(g,s1,p[i2])
    return sum