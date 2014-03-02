from z3 import *
import random
import copy

# Return the first "M" models of formula list of formulas F 
def get_models(F, M):
    result = []
    s = Solver()
    s.add(F)
    # print "This is the solver", s
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

def modelLength(F):
    return len(get_models(F, 30))

def genSudoku():
    # Generates a complete sudoku
    
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
        return r
    else:
        return "failed to solve"
def emptySquareNotUsingRowandCol(board, organizer):
    # Empties a square without using row and column restriction
    vals_tried = []
    i = random.randint(0, 8) # random row
    j = random.randint(0, 8) # random column
    while (str(board[i][j]) == str(0)) or ((i,j) in vals_tried):
        i = random.randint(0, 8) # random row
        j = random.randint(0, 8) # random column
    val_now = board[i][j] # value before the box changes to 0
    board[i][j] =  0 # set cell to 0
    vals_tried.append((i,j)) # Now that this value has been tried, it does not have to be tried again
    F = createSudoku(board) # Make a new sudoku with our new constraints
    numSolutions = modelLength(F)
    ## boardcopy = copy.deepcopy(board)
    organizer = addResult(board, organizer, numSolutions)
    while (not exactly_one_model(F)):
        # After the square is emptied, the resulting sudoku must have a unique solution
        if notEmpty(board) == len(vals_tried):
            # If every value on the board has been emptied and all of them have not worked, no squares can be emptied and we can stop looking
            break
        i = random.randint(0, 8) # random row
        j = random.randint(0, 8) # random column
        while (str(board[i][j]) == str(0)) or ((i,j) in vals_tried):
            i = random.randint(0, 8) # random row
            j = random.randint(0, 8) # random column
        val_now = board[i][j] # value before the box changes to 0
        board[i][j] =  0 # set cell to 0
        vals_tried.append((i,j)) # Now that this value has been tried, it does not have to be tried again
        F = createSudoku(board) # Make a new sudoku with our new constraints
        numSolutions = modelLength(F)
        ## boardcopy = copy.deepcopy(board)
        organizer = addResult(board, organizer, numSolutions)
    return board, vals_tried, organizer

def emptySquareUsingRowandCol(board, organizer):
    # Will empty a square using row and column restriction
    vals_tried = []
    i, j = chooseSquare(board, vals_tried) # Gets a square using row and column restriction
    val_now = board[i][j] # value before the box changes to 0
    board[i][j] =  0 # set cell to 0
    vals_tried.append((i,j)) # Now that this value has been tried, it does not have to be tried again
    F = createSudoku(board) # Make a new sudoku with our new constraints
    numSolutions = modelLength(F)
   ##  boardcopy = copy.deepcopy(board)
    organizer = addResult(board, organizer, numSolutions)
    while (not exactly_one_model(F)):
        # After the square is emptied, the resulting sudoku must have a unique solution
        if notEmpty(board) == len(vals_tried):
            # If every value on the board has been emptied and all of them have not worked, no squares can be emptied and we can stop looking
            break
        i, j = chooseSquare(board, vals_tried)
        val_now = board[i][j] # value before the box changes to 0
        board[i][j] =  0 # set cell to 0
        vals_tried.append((i,j)) # Now that this value has been tried, it does not have to be tried again
        F = createSudoku(board) # Make a new sudoku with our new constraints
        numSolutions = modelLength(F)
        ## boardcopy = copy.deepcopy(board)
        organizer = addResult(board, organizer, numSolutions)
    return board, vals_tried, organizer

def addResult(board, organizer, numSolutions):
    board_added = False
    print "board being added:"
    print_matrix(board)
    for length in organizer.keys():
        if numSolutions == length:
            organizer[length].append((board, numSolutions))
            board_added = True
    if not board_added:
        organizer[1].append((numSolutions, "Num solutions too large!"))
    print "printing the organizer...."
    printOrganizer(organizer)
    return organizer

def chooseSquare(board, vals_tried):
    # Chooses which square to empty
    row_appear = calcRowAppearances(board) # Calculates how many numbers are not empty in each row
    col_appear = calcColAppearances(board) # Calculates how many numbers are not empty in each column
    ijfound = False
    while ijfound==False:
        possible_i = random.randint(0, 8) # random row
        possible_j = random.randint(0, 8) # random column
        prob = random.random()
        if float(row_appear[possible_i])/9 >= prob and float(col_appear[possible_j])/9 >= prob: # The more empty squares, the less likely a square will be chosen from that row or column
            i = possible_i
            j = possible_j
            ijfound = True
    while (str(board[i][j]) == str(0)) or ((i,j) in vals_tried): # The box being emptied must not be 0 and should not have been tried already
        possible_i = random.randint(0, 8) # random row
        possible_j = random.randint(0, 8) # random column
        prob = random.random()
        if float(row_appear[possible_i])/9 >= prob and float(col_appear[possible_j])/9 >= prob: # The more empty squares, the less likely a square will be chosen from that row or column
            i = possible_i
            j = possible_j
    return i, j

def calcRowAppearances(board):
    # Finds how many non empty boxes there are in each row
    appearances = []
    for row in board:
        num_appear = 0
        for box in row:
            if box != 0:
                num_appear += 1
        appearances.append(num_appear)
    return appearances

def calcColAppearances(board):
    # Finds how many non empty boxes there are in each column
    appearances = []
    for i in range(9):
        num_appear = 0
        for j in range(9):
            if board[j][i] != 0:
                num_appear += 1
        appearances.append(num_appear)
    return appearances

def createSudoku(board):
    X = [[Int('x%d%d' % (i,j)) for i in range(9)] for j in range(9)]
    valid_values = [And ( X[i][j] >= 1, X[i][j] <= 9) for i in range(9) for j in range(9)]
    # Every row should be disntinct
    row_distinct = [Distinct(X[i]) for i in range(9)]
    # Every column should be disntinct
    cols_distinct = [Distinct([X[i][j] for i in range(9)]) for j in range(9)]
    # Every 3 x 3 square should be disntinct
    three_by_three_distinct = [ Distinct([X[3*k + i][3*l + j] for i in range(3) for j in range(3)]) for k in range(3) for l in range(3)]
    # There are values already set in the board, which we need to take into account
    already_set = []
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                already_set.append(X[i][j] == board[i][j])
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

def createOrganizer():
    organizer = {}
    for i in range(1, 16):
        organizer[i] = []
    return organizer
def emptySquareNoUnique(board, useRowandCol):
    if useRowandCol:
        i,j = chooseSquare(board, [])
    else:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
    board[i][j] = 0
    return board
    
def emptySquares(numsquares, useRowandCol, unique):
    vals_tried = [] # which box we have tried to change but they failed. A box value fails if we change it to empty and the resulting sudoku is not unique.
    organizer = createOrganizer()
    r = genSudoku()
    if r != "failed to solve":
        while (numsquares >= 0):
            if unique:
                if useRowandCol:
                    board_after, vals_tried, organizer = emptySquareUsingRowandCol(r, organizer)
                if not useRowandCol:
                    board_after, vals_tried, organizer = emptySquareNotUsingRowandCol(r, organizer)
                if notEmpty(board_after) == len(vals_tried):
                    break
                numsquares -= 1
                r = board_after
            else:
                if useRowandCol:
                    board_after = emptySquareNoUnique(r, True)
                if not useRowandCol:
                    board_after = emptySquareNoUnique(r, False)
                numsquares -= 1
                r = board_after
                print_matrix(r)
                print modelLength(createSudoku(r))
        print printOrganizer(organizer)
    else:
        print r

def printOrganizer(organizer):
    for length in range(1,16):
        print "All models that have", length, "solution(s):"
        for board in organizer[length]:
            print "NEW BOARD PRINTING..."
            print_matrix(board)
            
def getInput():
    unique = raw_input("Would you like to restrict the number of solutions? (y or n) ")
    numsquares = raw_input("How many squares would you like to empty? 1-10 = easy, 11-30 = medium, 31-40 = hard. Please do not choose over 40 squares. ")
    useRowandCol = raw_input("Would you like to restrict how the squares are emptied? (y or n) ")
    if useRowandCol == "y" and unique=="y":
        ## for i in range(10):
        emptySquares(int(numsquares), True, True)
        ## print "-----------------------------NEW TRIAL-----------------------------\n"
    if useRowandCol =="y" and unique=="n":
        emptySquares(int(numsquares), True, False)
    if useRowandCol =="n" and unique=="y":
        emptySquares(int(numsquares), False, True)
    if useRowandCol == "n" and unique == "n":
        emptySquares(int(numsquares), False, False)

getInput()





