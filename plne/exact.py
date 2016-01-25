from gurobipy import Var, Model, GRB, LinExpr, quicksum
from graph.partition import Partition

def half(num):
    return int(num/2.0 + 0.5)

def sort(ij):
    i, j = ij
    if i > j:
        return j, i
    else:
        return i, j

class Bind:
    def __init__(self, model, n, prefix='x', link='.'):
        self.bind = [[model.addVar(vtype=GRB.BINARY,
                               name=prefix+str(i+1)+link+str(j+1))
                      for j in range(i+1, n)]
                     for i in range(n-1)]

    def __getitem__(self, ij):
        i, j = sort(ij)
        return self.bind[i][j-i-1]
        

class Exact(Partition):
    # K :: Number of partition
    # R :: Tolerance between the biggest and smallest partition
    def partition(self, k=None, size=None, balance=None, name='partition'):
        n = self.number_of_nodes()

        # Create a new model
        self.model = Model(name)
        
        # Create variables
        # Xi  :: Node i is representative of a partition
        # Xij :: Edge between i and j is cut 
        #   0 => i & j are in the same partition
        #   1 => i & j are in different partition
        xi = [self.model.addVar(vtype=GRB.BINARY, name='x'+str(i+1))
              for i in range(n)] 
        xij = Bind(self.model, n)
        
        # Reinforcement of model
        # Zij = Xi x Xij
        zij = [[self.model.addVar(vtype=GRB.BINARY,
                                  name='x'+str(i+1)+' x x'+str(i+1)+'.'+str(j+1))
                for i in range(j)]
               for j in range(1, n)]
 
        # Integrate new variables
        self.model.update()
    
        # Number of nodes in the partition of node i 
        if balance != None or size != None:
            wi = [quicksum([xij[i, j] for j in range(n) if j != i])
                  for i in range(n)]

        # Set objective
        # Minimize the weighted sum of Xij
        obj = LinExpr()
        for i, j in self.edges_iter():
            obj.addTerms(self[i][j]['weight'], xij[i-1, j-1])
        self.model.setObjective(obj, GRB.MINIMIZE)

        # Add partition number
        # There must be exactly K partitions
        if k != None:
            self.model.addConstr(quicksum(xi[i] for i in range(n)) == k)
        else:
            self.model.addConstr(quicksum(xi[i] for i in range(n)) >= 2)

        # Absolute limitation the size of a partition
        if size != None:
            for i in range(n):
                self.model.addConstr((n - wi[i]) <= size)

        # Relative limit of the size of a partition 
        if balance != None:
            for i in range(n):
                self.model.addConstr((n - wi[i]) * k <= n * balance)


        # Linerarisation of multiplication Xi x Xij
        for j in range(n-1):
            for i in range(j+1):
                self.model.addConstr(zij[j][i] <= xi[i])
                self.model.addConstr(zij[j][i] <= 1 - xij[i, j+1])
                self.model.addConstr(zij[j][i] >= xi[i] - xij[i, j+1])

        # Add triangle inequality
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    # xij <= xik + xjk
                    self.model.addConstr(xij[i, j] <= xij[i, k] + xij[j, k])
                    self.model.addConstr(xij[i, k] <= xij[i, j] + xij[j, k])
                    self.model.addConstr(xij[j, k] <= xij[i, j] + xij[i, k])

        # A node is either a representative,
        # either in a partition with a smaller node
        for j in range(n):
            obj = LinExpr()
            obj.addTerms(1, xi[j])
            for i in range(j):
                obj.addTerms(1, zij[j-1][i])
            self.model.addConstr(obj == 1)

        # Resolve 
        self.model.optimize()
        
        # Compute resultat
        self.k = 0
        for i, v in enumerate(xi):
            if v.x == 1:
                self.node[i+1]['partition'] = self.k
                for j in range(i+1, n):
                    if xij[i, j].x == 0:
                        self.node[j+1]['partition'] = self.k
                self.k += 1
        self.compute() 
        

    def max(self, i, sup):
        size = len(i)
        if size == 1:
            return i[0]
        elif size == 2:
            i1, i2 = i
            m = self.model.addVar(vtype=GRB.INTEGER)
            w = self.model.addVar(vtype=GRB.BINARY)
            self.model.update()
            self.model.addConstr(m >= i1)
            self.model.addConstr(m >= i2)
            self.model.addConstr(i1 >= i2 - sup * w)
            self.model.addConstr(m <= i1 + sup * w)
            self.model.addConstr(i2 >= i1 - sup * (1 - w))
            self.model.addConstr(m <= i2 + sup * (1 - w))
            return m
        else:
            return self.max([self.max(i[0:half(size)], sup),
                             self.max(i[half(size):size], sup)], sup)

    def min(self, i, sup):
        size = len(i)
        if size == 1:
            return i[0]
        elif size == 2:
            i1, i2 = i
            m = self.model.addVar(vtype=GRB.INTEGER)
            w = self.model.addVar(vtype=GRB.BINARY)
            self.model.update()
            self.model.addConstr(m <= i1)
            self.model.addConstr(m <= i2)
            self.model.addConstr(i1 <= i2 + sup * w)
            self.model.addConstr(m >= i1 - sup * w)
            self.model.addConstr(i2 <= i1 + sup * (1 - w))
            self.model.addConstr(m >= i2 - sup * (1 - w))
            return m
        else:
            return self.min([self.min(i[0:half(size)], sup),
                             self.min(i[half(size):size], sup)], sup)
