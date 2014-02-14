from z3 import *
import random

# Return the first "M" models of formula list of formulas F 
def get_models(F, M):
    result = []
    s = Solver()
    s.add(F)
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

# every row should be disntinct
row_distinct = [Distinct(X[i]) for i in range(9)]

cols_distinct = [Distinct([X[i][j] for i in range(9)]) for j in range(9)]

three_by_three_distinct = [ Distinct([X[3*k + i][3*l + j] for i in range(3) for j in range(3)]) for k in range(3) for l in range(3)]

val = [X[0][0] == 1, X[0][1]==2]

s = Solver()
s.add(valid_values + row_distinct + cols_distinct + three_by_three_distinct)


if s.check() == sat:
    m = s.model()
    r = [ [ m.evaluate(X[i][j]) for j in range(9) ] 
          for i in range(9) ]
    print_matrix(r)
else:
    print "failed to solve"


num_rand = 40 # number of unfilled cells in sudoku puzzle
while (num_rand > 0): 
    i = random.randint(0, 8) #random row
    j = random.randint(0, 8) #random column
    if (r[i][j] != 0):
        r[i][j] = 0 #set cell to 0
        num_rand -= 1
        #print_matrix(r)

print_matrix(r)

instance_c = [ If(r[i][j] == 0, 
                  True, 
                  X[i][j] == r[i][j]) 
               for i in range(9) for j in range(9) ]

F = valid_values + row_distinct + cols_distinct + three_by_three_distinct + instance_c

a = get_models(F, 10) # get first ten solutions for the sudoku puzzle

for i in range(len(a)): #print all solutions
    m = a[i]
    p = [ [ m.evaluate(X[i][j]) for j in range(9) ] 
          for i in range(9) ]
    print_matrix(p)
    

print exactly_one_model(F)
