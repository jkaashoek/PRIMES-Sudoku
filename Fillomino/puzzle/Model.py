from z3 import *
from genBoard import *

def copy(lists):
    res = []
    for i in range(len(lists)):
        res1 = []
        for j in range(len(lists[i])):
            res1.append(int(lists[i][j].as_long()))
        res.append(res1)
    return res

def get_models(F, M, N):
    result = []
    boards = []
    s = Solver()
    s.add(F)
    # print "This is the solver", s
    n = 0
    while (len(boards) < M):
        if s.check() == sat:
            m = s.model()
            r = [ [ m.evaluate(Int("x%d%d" % (i,j))) for i in range(1, N+1) ]
                 for j in range(1, N+1)]
            x = copy(r)
            #print("Attempt #" + str(n+1) + ": checking with board ")
            #print_matrix(x)
            if x not in boards:
                result.append(m)
                boards.append(x)
                #print ("Appended new board!")
            '''
            else:
                print("Found the board " + str(x) + " in " + str(boards))
                print ("Result: " + str(x in boards))
                b1 = x
                b2 = [[[2, 3, 3, 1], [2, 1, 3, 2], [1, 1, 1, 2], [1, 2, 2, 1]]]
                print (b1 in b2)
       '''
            # Create a new constraint the blocks the current model
            block = []
            for d in m:
                c = d() # convert z3 key into z3 variable
                block.append(c != m[d])
            #print ("Looping")
            s.add(Or(block))
            n += 1
        else:
            print(boards)
            return boards
    print(boards)
    return boards


def exactly_n_models(F, n):
    return len(get_models(F, n+1)) == n

def fewer_than_n_models(F, n):
    return len(get_models(F, n+1)) <= n

def at_least_one_model(F, n):
    return len(get_models(F, n+1)) > 0

def unique(F):
    return exactly_n_models(F, 1)

def modelLength(F):
    return len(get_models(F, 31))


def getAdjacent1(x,y, N):
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

def lessThan(i,j,k,l):
    if i < k:
        return True
    elif i> k:
        return False
    else:
        return j < l

def createFillomino(board, N):
    cells = [[Int("x%d%d" % (i,j)) for i in range(1,N+1)] for j in range(1,N+1)]
    valid_cells = [And(cells[i][j] <= N, cells[i][j] >=1) for i in range(N) for j in range(N)]

    edge_var={}

    for i in range(N):
        for j in range(N):
            for (k,l) in getAdjacent1(i,j, N):
                edge_var[(i,j,k,l)] = Int("e%d%d%d%d" % (i,j,k,l))

    edge_val_constraints = [Or(edge_val==0,edge_val==1) for edge_val in edge_var.values()]

    for i in range(N):
        for j in range(N):
            for (k,l) in getAdjacent1(i,j, N):
                if lessThan(i,j,k,l):
                    sum_edges = edge_var[(i,j,k,l)] + edge_var[(k,l,i,j)]
                    edge_val_constraints.append(sum_edges <= 1)


    in_cell = [[Int("in%d%d"%(i,j)) for i in range(N)] for j in range(N)]
    in_cell_constraints=[]
    for i in range(N):
        for j in range(N):
            in_cell_constraints.append(And(in_cell[i][j]>=0, in_cell[i][j]<=1))
            sum_incoming_edges = Sum([edge_var[(k,l,i,j)] for (k,l) in getAdjacent1(i,j, N)])
            in_cell_constraints.append(in_cell[i][j]==sum_incoming_edges)

    same_value_constraint = []

    for i in range(N):
        for j in range(N):
            for (k,l) in getAdjacent1(i,j, N):
                if lessThan(i,j,k,l):
                    same_value_constraint.append(Implies(Or(edge_var[(i,j,k,l)]==1, edge_var[(k,l,i,j)]==1), cells[i][j] == cells[k][l]))


    size_region_constraint=[]
    size_cell = [[ Int("size%d%d" % (i,j)) for i in range(N)] for j in range(N)]
    size_region_constraint=[And(size_cell[i][j] >=1, size_cell[i][j]<=N) for i in range(N) for j in range(N)]

    for i in range(N):
        for j in range(N):
            size_adjacent = Sum([If(edge_var[(i,j,k,l)]==1, size_cell[k][l],0) for (k,l) in getAdjacent1(i,j, N)])
            size_region_constraint.append(size_cell[i][j] == (size_adjacent+1))
            size_region_constraint.append(Implies(in_cell[i][j]==0, size_cell[i][j] == cells[i][j]))

    #init_constraints=[cells[0][0]==3, cells[0][1]==4]
    #init_constraints=[And(cells[0][0]==1)]

    init_constraints = [ If(board[i][j] == 0,
                      True,
                      cells[i][j] == board[i][j])
                  for i in range(N) for j in range(N) ]

    F = valid_cells + edge_val_constraints + in_cell_constraints + same_value_constraint + size_region_constraint + init_constraints
    return F


'''
board = [[1, 3, 3, 4],
         [3, 1, 3, 4],
         [3, 3, 1, 4],
         [2, 2, 1, 4]]

N = 4
F = createFillomino(board, N)
s = Solver()
s.add(F)

if s.check() == sat:
    m = s.model()
    r = [ [m.evaluate(Int("x%d%d" % (i,j))) for j in range(1, N + 1)]
         for i in range(1, N + 1)]
    print m
    print "satisfiable"
    print_matrix(r)


else:
    print "not satisfiable"



a = get_models(F, 100)
print(len(a))
for i in range(len(a)):
    m = a[i]
    r = [ [ m.evaluate(Int("x%d%d" % (i,j))) for j in range(1, N+1) ]
     for i in range(1, N+1)]
    print_matrix(r)
    s =[ [ m.evaluate(Int("size%d%d" % (i,j))) for j in range(N) ]
        for i in range(N)]
    print_matrix(s)
    print('\n')

board = [[2, 3, 3, 1],
         [2, 1, 3, 2],
         [0, 1, 1, 2],
         [0, 0, 0, 1]]
N = 4
F = createFillomino(board, N)
print (get_models(F, 10, N))
'''
