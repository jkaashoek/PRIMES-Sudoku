from z3 import *
import random

# Return the first "M" models of formula list of formulas F 
def get_models(F, M):
    result = []
    s = Solver()
    s.add(F)
    print "This is the solver", s
    while True:
        if s.check() == sat:
            m = s.model()
            result.append(m)
            # Create a new constraint the blocks the current model
            block = []
            for d in m:
                c = d() # convert z3 key into z3 variable
                block.append(c != m[d])
            s.add(Or(block))
        else:
            return result

# Return True if F has exactly one model.
def exactly_one_model(F):
    return len(get_models(F, 2)) == 1



# create 81 variables: one for each sudoku square, x11, x12, ... x19, .... x99

X = [[Int('x%d%d' % (i,j)) for i in range(9)] for j in range(9)]

valid_values = [And ( X[i][j] >= 1, X[i][j] <= 9) for i in range(9) for j in range(9)]

# Every row should be disntinct
row_distinct = [Distinct(X[i]) for i in range(9)]

# Every column should be disntinct
cols_distinct = [Distinct([X[i][j] for i in range(9)]) for j in range(9)]

# Every 3 x 3 square should be disntinct
three_by_three_distinct = [ Distinct([X[3*k + i][3*l + j] for i in range(3) for j in range(3)]) for k in range(3) for l in range(3)]

s = Solver()
s.add(valid_values + row_distinct + cols_distinct + three_by_three_distinct)

if s.check() == sat:
    m = s.model()
    r = [ [ m.evaluate(X[i][j]) for j in range(9) ] 
          for i in range(9) ]
##    print_matrix(r)
else:
    print "failed to solve"


def emptySquare(board, vals_tried):
    i = random.randint(0, 8) # random row
    j = random.randint(0, 8) # random column
    if (board[i][j] != 0) and (board[i][j] not in vals_tried):
        val_now = board[i][j]
        board[i][j] =  0 # set cell to 0
        print_matrix(board)
        F = createSudoku(board)
        if (not exactly_one_model(F)):
            # We know the resulting sudoku is not unique
            board[i][j] = val_now
            vals_tried.append(board[i][j])
    return board, vals_tried

def createSudoku(board):
    X = [[Int('x%d%d' % (i,j)) for i in range(9)] for j in range(9)]
    valid_values = [And ( X[i][j] >= 1, X[i][j] <= 9) for i in range(9) for j in range(9)]
    # Every row should be disntinct
    row_distinct = [Distinct(X[i]) for i in range(9)]
    # Every column should be disntinct
    cols_distinct = [Distinct([X[i][j] for i in range(9)]) for j in range(9)]
    # Every 3 x 3 square should be disntinct
    three_by_three_distinct = [ Distinct([X[3*k + i][3*l + j] for i in range(3) for j in range(3)]) for k in range(3) for l in range(3)]
    already_set = []
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                already_set.append(X[i][j] == board[i][j])
    print "values set", already_set
    F = valid_values + row_distinct + cols_distinct + three_by_three_distinct + already_set
    return F

def notEmpty(board):
    # Finds the number of sudoku squares that are empty
    num_empty = 0
    for i in range(9):
        for j in range(9):
            if (board[i][j] != 0):
                num_empty += 1
    return num_empty
    
num_rand = 5 # number of unfilled cells in sudoku puzzle
vals_tried = [] # which box we have tried to change but they failed. A box value fails if we change it to empty and the resulting sudoku is not unique.
while (num_rand > 0):
    print "num loop:", num_rand
    print "In while loop"
    print_matrix(r)
    board_before = r
    print "before:", board_before
    board_after, vals_tried = emptySquare(r, vals_tried)
    print "before:", board_before
    print "after: ", board_after
    print "r:", r
    if board_after != board_before:
        vals_tried = []
        num_rand -= 1
    print notEmpty(r)
    if notEmpty(r) == len(vals_tried):
        break
    r = board_after
    
        #print_matrix(r)

print "here", print_matrix(r)

## instance_c = [ If(r[i][j] == 0, 
##                   True, 
##                   X[i][j] == r[i][j]) 
##                for i in range(9) for j in range(9) ]

## F = valid_values + row_distinct + cols_distinct + three_by_three_distinct + instance_c

## a = get_models(F, 10) # get first ten solutions for the sudoku puzzle

## for i in range(len(a)): #print all solutions
##     m = a[i]
##     p = [ [ m.evaluate(X[i][j]) for j in range(9) ] 
##           for i in range(9) ]
##     print_matrix(p)
    

## print exactly_one_model(F)
