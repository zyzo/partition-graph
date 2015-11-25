# -*- coding: utf-8 -*-
import numpy
# Cut of two subsets s1, s2
def single_cut(g, s1, s2):
    res = 0
    for node in s1:
        for n, cost in g[node-1]:
            if n in s2:
                res += cost
    return res
# Cut of a partition p
def cut(g, p):
    res = 0
    for i1, s1 in enumerate(p):
        for i2 in range(i1 + 1,len(p)):
            res += single_cut(g,s1,p[i2])
    return res

def weight(g, s):
    res = 0
    for node in s:
        for n, cost in g[node - 1]:
            if n in s:
                res += cost
    return res / 2

# # Cut ratio of a partition p
# def ratio(g, p):
#     # Initialize array of size len(p)*len(p)
#     sum_ratios = 0
#     for s1 in p:
#         complement_s1 = [[x for x in s] for s in p if s != s1]
#         sum_ratios += cut(s1, complement_s1)/(node_weight(g, s1)+1)
#     return  sum_ratios