import glob

import eval
import input
from GreedyPartitioning import GreedyPartitioning

print glob.glob("./graph/*")
data = open("graph_link.txt", 'r')

TEST_PARTITIONS = [2,4,6,8]

for partition in TEST_PARTITIONS:
    print "CAS ", partition, " PARTITIONS"
    for line in glob.glob("./graph/*"):
        print "Graph : ", line
        g = GreedyPartitioning(line, partition)
        g2 = input.read_local(line)
        print "Cut : ", eval.cut(g2[2], g.get_partitions())
        print "Ratio : ", eval.ratio(g2[2], g.get_partitions())

