from z3 import *

N = 16

cells = [[Int("x%d%d" % (i,j)) for i in range(1,N+1)] for j in range(1,N+1)]

valid_cells = [And(cells[i][j] <= N, cells[i][j] >=1) for i in range(N) for j in range(N)]

def getAdjacent1(x,y):
    result = []
    if x-1>=0:
        result.append((x-1,y))
    if x+1<N:
        result.append((x+1,y))
    if y-1>=0:
        result.append((x,y-1))
    if y+1 < N:
        result.append((x,y+1))
    return result

edge_var={}

for i in range(N):
    for j in range(N):
        for (k,l) in getAdjacent1(i,j):
            edge_var[(i,j,k,l)] = Int("e%d%d%d%d" % (i,j,k,l))

edge_val_constraints = [Or(edge_val==0,edge_val==1) for edge_val in edge_var.values()]

def lessThan(i,j,k,l):
    if i < k:
        return True
    elif i> k:
        return False
    else:
        return j < l

for i in range(N):
    for j in range(N):
        for (k,l) in getAdjacent1(i,j):
            if lessThan(i,j,k,l):
                sum_edges = edge_var[(i,j,k,l)] + edge_var[(k,l,i,j)]
                edge_val_constraints.append(sum_edges <= 1)


in_cell = [[Int("in%d%d"%(i,j)) for i in range(N)] for j in range(N)]
in_cell_constraints=[]
for i in range(N):
    for j in range(N):
        in_cell_constraints.append(And(in_cell[i][j]>=0, in_cell[i][j]<=1))
        sum_incoming_edges = Sum([edge_var[(k,l,i,j)] for (k,l) in getAdjacent1(i,j)])
        in_cell_constraints.append(in_cell[i][j]==sum_incoming_edges)
      
same_value_constraint = []

for i in range(N):
    for j in range(N):
        for (k,l) in getAdjacent1(i,j):
            if lessThan(i,j,k,l):
                same_value_constraint.append(Implies(Or(edge_var[(i,j,k,l)]==1, edge_var[(k,l,i,j)]==1), cells[i][j] == cells[k][l]))
  

size_region_constraint=[]
size_cell = [[ Int("size%d%d" % (i,j)) for i in range(N)] for j in range(N)]
size_region_constraint=[And(size_cell[i][j] >=1, size_cell[i][j]<=N) for i in range(N) for j in range(N)]        

for i in range(N):
    for j in range(N):
        size_adjacent = Sum([If(edge_var[(i,j,k,l)]==1, size_cell[k][l],0) for (k,l) in getAdjacent1(i,j)])
        size_region_constraint.append(size_cell[i][j] == (size_adjacent+1))
        size_region_constraint.append(Implies(in_cell[i][j]==0, size_cell[i][j] == cells[i][j]))

init_constraints=[cells[0][0]==3, cells[0][1]==4]
#init_constraints=[And(cells[0][0]==1)]

s = Solver()

s.add(valid_cells)
s.add(edge_val_constraints)
s.add(in_cell_constraints)
s.add(same_value_constraint)
s.add(size_region_constraint)
s.add(init_constraints)


if s.check() == sat:
    m = s.model()
    r = [ [m.evaluate(cells[i][j]) for j in range(N)]
          for i in range(N)]
    print_matrix(r)

 ##    es = []
##     print "size_cells"
##     s = [ [m.evaluate(size_cell[i][j]) for j in range(5)]
##           for i in range(5)]
##     print_matrix(s)
##     print "in_cell"
##     i = [ [m.evaluate(in_cell[i][j]) for j in range(5)]
##           for i in range(5)]
##     print_matrix(i)

##     for i in range(N):
##         for j in range(N):
##             size_adjacent = 0
##             for (k,l) in getAdjacent1(i,j):
##                 if size_adjacent == 0:
##                     size_adjacent = m.evaluate(If(edge_var[(i,j,k,l)]==1,size_cell[k][l],0))
##                 else:
##                     size_adjacent += m.evaluate(If(edge_var[(i,j,k,l)]==1,size_cell[k][l],0))
##             print "size_cell_%d_%d = " %(i,j), m.evaluate(size_cell[i][j]), " size_adjacent = ", size_adjacent


##     for i in range(N):
##         for j in range(N):
##             for (k,l) in getAdjacent1(i,j):
##                 print "e%d%d%d%d = "%(i,j,k,l), m.evaluate(edge_var[(i,j,k,l)])

##     print m
## else:
##     print "not satisfiable"
