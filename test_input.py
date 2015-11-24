
import input

n,e,g = input.read_local("./test.graph")
print "test7: n = ", n, ", e = ", e, ", len(g)= ", len(g)
n,e,g = input.read_url("http://staffweb.cms.gre.ac.uk/~c.walshaw/partition/archive/add20/add20.graph")
print "add20: n = ", n, ", e = ", e, ", len(g)= ", len(g)