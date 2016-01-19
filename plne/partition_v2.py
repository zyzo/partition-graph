from gurobipy import *
from imput import read_local
import sys

try:
    # Create a new model
    m = Model("m")

    # K :: Number of partition
    # R :: Tolerance between the biggest and smallest partition
    #K = int(sys.argv[2])
    R = int(sys.argv[2])

    # Import the graph data
    # n :: Number of nodes
    # e :: Number of edges /!\useless
    # g :: Representation of graph [node,  ...]
    #                        node  [edge,  ...]
    #                        edge  [dest, cost]
    n, e, g = read_local(sys.argv[1])  
    c = [[0 for j in range(i+1, n)] for i in range(n-1)]
    for i, v in enumerate(g):
        for e in v:
            if (i < e[0]-1):
                c[i][e[0]-i-2] = e[1]

    # Create variables
    # Xi  :: Node i is representative of a partition
    # Xij :: Edge between i and j is cut 
    #   0 => i & j are in the same partition
    #   1 => i & j are in different partition
    # /!\ Xij are not a matrice! It is triangular. Be careful to the indices.
    xi = [m.addVar(vtype=GRB.BINARY, name="x"+str(i+1)) for i in range(n)] 
    xij = [[m.addVar(vtype=GRB.BINARY, name="x"+str(i+1)+","+str(j+1)) for j in range(i+1, n)] for i in range(n-1)]

    # Reinforcement of model
    # Zij = Xi x Xij
    zij = [[m.addVar(vtype=GRB.BINARY, name="x"+str(i+1)+"x"+str(i+1)+","+str(j+1)) for i in range(j)] for j in range(1, n)]

    # Max & Min variables
    sma = [m.addVar(vtype=GRB.INTEGER, name="max"+str(i+1)) for i in range(n-1)]
    wma = [m.addVar(vtype=GRB.BINARY, name=">w"+str(i+1)) for i in range(n-1)]
    smi = [m.addVar(vtype=GRB.INTEGER, name="min"+str(i+1)) for i in range(n-1)]
    wmi = [m.addVar(vtype=GRB.BINARY, name="<w"+str(i+1)) for i in range(n-1)]

    # Integrate new variables
    m.update()

    # Set objective
    # Minimize the weighted sum of Xij
    obj = LinExpr()
    for i in range(n-1):
        for j in range(n-i-1):
            # Only if there are an edge between i & j
            # Maybe test is useless but I prefer to get minimum sized expression
            if c[i][j] != 0:
                obj.addTerms(c[i][j], xij[i][j])
    m.setObjective(obj, GRB.MINIMIZE)

    # Linerarisation of multiplication XiXij
    for j in range(n-1):
        for i in range(j+1):
            m.addConstr(zij[j][i] <= xi[i])
            m.addConstr(zij[j][i] <= 1 - xij[i][j-i])
            m.addConstr(zij[j][i] >= xi[i] - xij[i][j-i])

    # Add triangle inequality
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                # xij <= xik + xjk
                # Ok guy, I understand now why you talked about indices...
                # TODO Maybe hide this under a class layer?
                m.addConstr(xij[i][j-i-1] <= xij[i][k-i-1] + xij[j][k-j-1])
                m.addConstr(xij[i][k-i-1] <= xij[i][j-i-1] + xij[j][k-j-1])
                m.addConstr(xij[j][k-j-1] <= xij[i][j-i-1] + xij[i][k-i-1])

    # Add partition number
    # There must be exactly K partitions
    #m.addConstr(quicksum(xi[i] for i in range(n)) == K)

    # A node is either a representative,
    # either in a partition with a smaller node
    for j in range(n):
        exp = LinExpr()
        exp.addTerms(1, xi[j])
        for i in range(j):
            exp.addTerms(1, zij[j-1][i])
        m.addConstr(exp == 1)

    ## Add balance constraint
    ## Zealot method
    ## Nothing shall pass
    m.addConstr(quicksum(xi[i] for i in range(n)) >= 2)
    sav = int(n/2.0 + 0.5) + R
    bal = []
    for i in range(n):
        bal.append(LinExpr())
        for j in range(n):
            if i < j:
                bal[i].addTerms(1, xij[i][j-i-1])
            elif i > j:
                bal[i].addTerms(1, xij[j][i-j-1])

    m.addConstr(sma[0] >= bal[0])
    m.addConstr(sma[0] >= bal[1])
    m.addConstr(sma[0] <= bal[0] + sav*wma[0])
    m.addConstr(sma[0] <= bal[1] + sav*(1-wma[0]))
    m.addConstr(smi[0] <= bal[0])
    m.addConstr(smi[0] <= bal[1])
    m.addConstr(smi[0] >= bal[0] - sav*wmi[0])
    m.addConstr(smi[0] >= bal[1] - sav*(1-wmi[0]))
    for i in range(n-2):
        m.addConstr(sma[i+1] >= bal[i+2]);
        m.addConstr(sma[i+1] >= sma[i]);
        m.addConstr(sma[i+1] <= bal[i+2] + sav*wma[i+1])
        m.addConstr(sma[i+1] <= sma[i] + sav*(1-wma[i+1]))
        m.addConstr(smi[i+1] <= bal[i+2])
        m.addConstr(smi[i+1] <= smi[i])
        m.addConstr(smi[i+1] >= bal[i+2] - sav*wmi[i+1])
        m.addConstr(smi[i+1] >= smi[i] - sav*(1-wmi[i+1]))
    m.addConstr(sma[-1] <= smi[-1] + R) 

    # A less expensive methode
    # for each node
    #    calculate the weigth of its partition
    #    this weigth must not deviate more than R/2 of the estimated average
    # /!\ this constraint is stronger than (biggest - smallest) < R
    # /!\ and may not completed
    #for i in range(n):
    #    bal = LinExpr()
    #    for j in range(n):
    #        if i < j:
    #            bal.addTerms(-1, xij[i][j-i-1])
    #        elif i > j:
    #            bal.addTerms(-1, xij[j][i-j-1])
    #    m.addConstr(n+bal <= n/K + R/2)
    #    m.addConstr(n+bal >= n/K - R/2)

    # Resolve 
    m.optimize()

    # Print result
    for i, x in enumerate(xi):
        if x.x == 1:
            p = [x.VarName]
            for j in range(i+1, n):
                if xij[i][j-i-1].x == 0:
                    p.append(xi[j].VarName)
            print(p)

    #print('Tol: %g' % R)
    print('Obj: %g' % m.objVal)
    
except GurobiError as e:
    print(e)
