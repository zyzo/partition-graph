# -*- coding: utf-8 -*-
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
    
def read_url(url):
    data = urllib.urlopen(url)
    graph = parse_graph(data)
    data.close()
    return graph