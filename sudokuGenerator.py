from z3 import *
import random

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


X = [[Int('x%d%d' % (i,j)) for i in range(9)] for j in range(9)]
board = [[0 for i in range(9)] for j in range(9)]

indices = [str(i) + str(j) for i in range(9) for j in range(9)]

#place random values
n = 0
while True:
    index = random.randint(0, len(indices) - 1)
    row_num = int(indices[index][0])
    col_num = int(indices[index][1])
    digit = random.randint(1, 9)
    print('Row: ' + row_num)
    print('Col: ' + col_num)
    print('Digit: ' + digit)

    row_check = (digit not in [board[row_num][c] for c in range(9)])
    col_check = (digit not in [board[r][col_num] for r in range(9)])
    three_check = (digit not in [board[r][c] for r in range(3*(i//3), 3*(row_num//3)+3)
                                         for c in range(3*(j//3), 3*(col_num//3) + 3)])
    if (row_check and col_check and three_check):                   
        temp = [[board[r][c] for r in range(9)] for c in range(9)]
        temp[row_num][col_num] = digit

        #valid_values = [And ( X[i][j] >= 1, X[i][j] <= 9) for i in range(9) for j in range(9)]
        valid_values = [And ( X[i][j] >= 1, X[i][j] <= 9) for i in range(9) for j in range(9)]
        row_distinct = [Distinct(X[i]) for i in range(9)]
        cols_distinct = [Distinct([X[i][j] for i in range(9)]) for j in range(9)]
        three_by_three_distinct = [ Distinct([X[3*k + i][3*l + j] for i in range(3) for j in range(3)]) for k in range(3) for l in range(3)]
        instance_c = [ If(temp[i][j] == 0, 
                          True, 
                          X[i][j] == temp[i][j]) 
                       for i in range(9) for j in range(9) ]
        F = row_distinct + cols_distinct + three_by_three_distinct + instance_c + valid_values
        s = Solver()
        s.add(F)
        if (n > 10):
            if (s.check() == sat):
                board[row_num][col_num] = digit #set cell to a
                indices.remove(indices[index])
                print('\n' + 'Iteration '+ str(n) + '\n')
                print_matrix(board)
                n += 1
                #if (exactly_one_model(F)):
                    #break
        else:
            board[row_num][col_num] = digit
            indices.remove(indices[index])
            print('\n' + 'Iteration ' + str(n) + '\n')
            print_matrix(board)
            n += 1

  

print_matrix(board)
