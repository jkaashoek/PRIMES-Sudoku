from z3 import *
import time
    
def get_models(F, M):
    result = []
    s = Solver()
    s.add(F)
    n = 0
    # print "This is the solver", s
    while n < M:
        if s.check() == sat:
            m = s.model()
            result.append(m)
            # Create a new constraint the blocks the current model
            block = []
            for d in m:
                c = d() # convert z3 key into z3 variable
                block.append(c != m[d])
            s.add(Or(block))
            n += 1
        else:
            return result
    return result


def exactly_n_models(F, n):
    return len(get_models(F, n+1)) == n

def fewer_than_n_models(F, n):
    return len(get_models(F, n+1)) <= n

def at_least_one_model(F, n):
    return len(get_models(F, n+1)) > 0

def unique(F):
    return exactly_n_models(F, 1)

def modelLength(F):
    return len(get_models(F, 30))


def createSudoku(board):
    X = [[Int('x%dd%dd' % (i,j)) for i in range(16)] for j in range(16)]
    valid_values = [And ( X[i][j] >= 1, X[i][j] <= 16) for i in range(16) for j in range(16)]
    # Every row should be disntinct
    row_distinct = [Distinct(X[i]) for i in range(16)]
    # Every column should be disntinct
    cols_distinct = [Distinct([X[i][j] for i in range(16)]) for j in range(16)]
    # Every 3 x 3 square should be disntinct
    three_by_three_distinct = [ Distinct([X[4*k + i][4*l + j] for i in range(4) for j in range(4)]) for k in range(4) for l in range(4)]
    # There are values already set in the board, which we need to take into account
    s = Solver()
    s.add(valid_values + row_distinct + cols_distinct + three_by_three_distinct + already_set)
    if s.check() == sat:
        m = s.model()
        r = [ [ m.evaluate(X[i][j]) for j in range(16) ] for i in range(16) ]
    return r
    already_set = []
    for i in range(16):
        for j in range(16):
            if board[i][j] != 0:
                already_set.append(X[i][j] == board[i][j])
    F = valid_values + row_distinct + cols_distinct + three_by_three_distinct + already_set
    return F

# timeInit = time.time()
# board = createSudoku([])
# timeLater = time.time()
# print board
# print "time to run:", timeLater-timeInit

