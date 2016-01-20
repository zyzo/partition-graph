import glob

import eval
import input
from GreedyPartitioning import GreedyPartitioning

print glob.glob("../graph/*")
data = open("graph_link.txt", 'r')

TEST_PARTITIONS = [2,3,4,5]

def print_array(array):
    toPrint = ""
    for i in array:
        print str(i)
for partition in TEST_PARTITIONS:
    cut =[]
    ratio = []
    # print "CAS ", partition, " PARTITIONS"
    for line in glob.glob("../graph/*"):
        g = GreedyPartitioning(line, partition)
        g2 = input.read_local(line)
        cut.append(eval.cut(g2[2], g.get_partitions()))
        ratio.append(eval.ratio(g2[2], g.get_partitions()))
    print_array(cut)
    print_array(ratio)