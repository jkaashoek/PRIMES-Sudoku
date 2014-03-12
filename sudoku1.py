from z3 import *
import random
import copy

#Generates about 3x10^6 different sudoku boards

import random
import copy
from z3 import *

'''
Mixes up the columns in a random 9x3 vertical band
'''
def switchCols(board):
    temp = copy.deepcopy(board)
    bandNum = random.randint(0, 2) #random vertical bands
    colOrder = [0, 1, 2]
    random.shuffle(colOrder) #mix the order of the columns in that band

    #go through each column in the band to change cell
    for r in range(9):
        for c in range(3*bandNum, 3*bandNum + 3):
            #cell value in column gets assigned according to colOrder
            board[r][c] = temp[r][colOrder[c%3] + 3*bandNum]           
    return board

'''Mixes up the rows in a random 3x9 horizontal stack'''
def switchRows(board):
    temp = copy.deepcopy(board)
    stackNum = random.randint(0, 2) #random horizontal stack
    rowOrder = [0, 1, 2]
    random.shuffle(rowOrder) #mix the order of the rows in that stack

    #go through each row in stack
    for r in range(3*stackNum, 3*stackNum + 3):
        #change order of rows according to rowOrder
        board[r] = temp[stackNum*3 + rowOrder[r%3]]
    return board
    

'''Reflects the board horizontally, over the middle vertical line'''
def horizontalReflect(board):
    temp = copy.deepcopy(board)
    for r in range(9):
        for c in range(9):
            board[r][c] = temp[r][8-c]
    return board

'''Reflects the board vertically, over the middle horizontal line'''
def verticalReflect(board):
    temp = copy.deepcopy(board)
    for i in range(9):
        board[i] = temp[8 - i]
    return board
    
'''randomly mixes the order of the 3x9 horizontal stacks'''
def switchStacks(board):
    order = [0, 1, 2]
    random.shuffle(order)
    temp = board[:]
    for i in range(9):
        board[i] = temp[3*order[(i//3)] + i%3]
    return board

'''randomly mixes the order of the 9x3 vertical bands'''
def switchBands(board):
    order = [0, 1, 2]
    random.shuffle(order)
    temp = copy.deepcopy(board)
    for i in range(9):
        for j in range(9):
            board[i][j] = temp[i][3*order[(j//3)] + j%3]
    return board
    
'''randomly switches the placement of the digits'''
def permutateDigits(board):
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    shuffled = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(shuffled)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    numToLetters = dict()
    for i in range(1, 10):
        numToLetters[i] = letters[i-1]
    lettersToNum = dict()
    for i in range(1, 10):
        lettersToNum[letters[i-1]] = shuffled[i-1]
    for a in range(9):
        for b in range(9):
            # print "DEBUG:", board[a][b], a, b
            board[a][b] = numToLetters[board[a][b]]
    for c in range(9):
        for d in range(9):
            board[c][d] = lettersToNum[board[c][d]]
    return board

'''rotates the board 90 degrees to the left'''
def rotate(board):
    horizontalReflect(board)
    temp = copy.deepcopy(board)
    for i in range(9):
        for j in range(9):
            board[i][j] = temp[j][i]
    return board

    
'''complete shuffle of the board with symmetry changes'''
def shuffle(board):
    for i in range(1000):
        a = random.randint(0, 7)
        if (a == 0):
            horizontalReflect(board)
        elif (a == 1):
            verticalReflect(board)
        elif (a == 2):
            switchStacks(board)
        elif (a == 3):
            switchBands(board)
        elif (a == 4):
            permutateDigits(board)
        elif (a == 5):
            switchRows(board)
        elif (a==6):
            switchCols(board)
        elif (a==7):
            rotate(board)
    return board
        

def generate(board):
    shuffle(board)
    return board

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
def restrict_solutions(F):
    return len(get_models(F, 3)) != 3

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
        res = []
        for i in range(9):
            res1 = []
            for j in range(9):
                res1.append(m.evaluate(X[i][j]))
            res.append(res1)
    
        return res
    else:
        return "failed to solve"

def copyListOfLists(lists):
    res = []
    for i in range(len(lists)):
        res1 = []
        for j in range(len(lists[i])):
            res1.append(lists[i][j])
        res.append(res1)
    return res

def emptySquareNotUsingRowandCol(board, organizer, useOrganizer):
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
    if useOrganizer:
        numSolutions = modelLength(F)
        boardcopy = copyListOfLists(board)
        organizer = addResult(boardcopy, organizer, numSolutions)
    else:
        organizer = addResult([], organizer, 1)
    while (not restrict_solutions(F)):
        board[i][j] = val_now
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
        if useOrganizer:
            numSolutions = modelLength(F)
            boardcopy = copyListOfLists(board)
            organizer = addResult(boardcopy, organizer, numSolutions)
        else:
            organizer = addResult([], organizer, 1)
    return board, vals_tried, organizer

def emptySquareUsingRowandCol(board, organizer, useOrganizer):
    # Will empty a square using row and column restriction
    vals_tried = []
    i, j = chooseSquare(board, vals_tried) # Gets a square using row and column restriction
    val_now = board[i][j] # value before the box changes to 0
    board[i][j] =  0 # set cell to 0
    vals_tried.append((i,j)) # Now that this value has been tried, it does not have to be tried again
    F = createSudoku(board) # Make a new sudoku with our new constraints
    if useOrganizer:
        numSolutions = modelLength(F)
        boardcopy = copyListOfLists(board)
        organizer = addResult(boardcopy, organizer, numSolutions)
    else:
        organizer = addResult([], organizer, 1)
    while (not restrict_solutions(F)):
        # After the square is emptied, the resulting sudoku must have a unique solution
        if notEmpty(board) == len(vals_tried):
            # If every value on the board has been emptied and all of them have not worked, no squares can be emptied and we can stop looking
            break
        i, j = chooseSquare(board, vals_tried)
        val_now = board[i][j] # value before the box changes to 0
        board[i][j] =  0 # set cell to 0
        vals_tried.append((i,j)) # Now that this value has been tried, it does not have to be tried again
        F = createSudoku(board) # Make a new sudoku with our new constraints
        if useOrganizer:
            numSolutions = modelLength(F)
            boardcopy = copyListOfLists(board)
            organizer = addResult(boardcopy, organizer, numSolutions)
        else:
            organizer = addResult([], organizer, 1)
    return board, vals_tried, organizer

def addResult(board, organizer, numSolutions):
    board_added = False
    for length in organizer.keys():
        if numSolutions == length:
            organizer[length].append((board, numSolutions))
            board_added = True
    if not board_added:
        organizer[1].append((numSolutions, "Num solutions too large!"))
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
    for i in range(1, 50):
        organizer[i] = []
    return organizer

def emptySquareNoUnique(board, useRowandCol, organizer, useOrganizer):
    if useRowandCol:
        i,j = chooseSquare(board, [])
    else:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
    board[i][j] = 0
    if useOrganizer:
        F = createSudoku(board)
        numSolutions = len(get_models(F, 50))
        addResult(board, organizer, numSolutions)
    else:
        addResult([], organizer, 1)
    return board, organizer
    
def emptySquares(numsquares, useRowandCol, unique, useOrganizer, r):
    vals_tried = [] # which box we have tried to change but they failed. A box value fails if we change it to empty and the resulting sudoku is not unique.
    organizer = createOrganizer()
    if r != "failed to solve":
        while (numsquares >= 0):
            if unique:
                if useRowandCol:
                    board_after, vals_tried, organizer = emptySquareUsingRowandCol(r, organizer, useOrganizer)
                if not useRowandCol:
                    board_after, vals_tried, organizer = emptySquareNotUsingRowandCol(r, organizer, useOrganizer)
                if notEmpty(board_after) == len(vals_tried):
                    break
                numsquares -= 1
                r = board_after
            else:
                if useRowandCol:
                    board_after, organizer = emptySquareNoUnique(r, True, organizer, useOrganizer)
                if not useRowandCol:
                    board_after, organizer = emptySquareNoUnique(r, False, organizer, useOrganizer)
                numsquares -= 1
                r = board_after
        return organizer, r
    else:
        print r

def printOrganizer(organizer):
    for length in range(1,50):
        print "All models that have", length, "solution(s):"
        for board in organizer[length]:
            print "NEW BOARD PRINTING..."
            print_matrix(board)
            
def getInput():
    board = [[1, 3, 5, 4, 6, 8, 9, 7, 2],
    [7, 9, 6, 3, 5, 2, 4, 1, 8],
    [2, 4, 8, 9, 1, 7, 5, 6, 3],
    [5, 6, 9, 7, 2, 1, 3, 8, 4],
    [4, 2, 7, 8, 9, 3, 6, 5, 1],
    [3, 8, 1, 6, 4, 5, 2, 9, 7],
    [6, 1, 3, 5, 8, 4, 7, 2, 9],
    [8, 5, 4, 2, 7, 9, 1, 3, 6],
    [9, 7, 2, 1, 3, 6, 8, 4, 5]]
    r = generate(board)
    board_copy = copyListOfLists(r)
    unique = raw_input("Would you like to restrict the number of solutions? (y or n) ")
    numsquares = raw_input("How many squares would you like to empty? 1-10 = easy, 11-30 = medium, 31-40 = hard. Please do not choose over 40 squares. ")
    useRowandCol = raw_input("Would you like to restrict how the squares are emptied? (y or n) ")
    useOrganizer = raw_input("Would you like to use the organizer? (y or n) ")
    if useOrganizer == "y":
        useOrganizer = True
    else:
        useOrganizer = False
    if useRowandCol == "y":
        useRowandCol = True
    else:
        useRowandCol = False
    if unique == "y":
        unique = True
    else:
        unique = False
    organizer, r = emptySquares(int(numsquares), useRowandCol, unique, useOrganizer, r)
    print "INITIAL BOARD FOUND:"
    print_matrix(r)
    solutions = []
    solutions.append(r)
    for i in range(100):
        nboard = copyListOfLists(board_copy)
        board = createMoreSudoku(nboard, r)
        solutions.append(board)
    for sudoku in solutions:
        print "BOARD FOUND AFTER SHUFFLE:"
        print_matrix(sudoku)
        
def createMoreSudoku(starting_board, emptied_board):
    empty_squares = rememberEmptySquares(emptied_board)
    starting_board = shuffle(starting_board)
    board = putBack(empty_squares, starting_board)
    return board
def putBack(empty_squares, board):
    for pair in empty_squares:
        board[pair[0]][pair[1]] = 0
    return board
def rememberEmptySquares(board):
    empty_squares = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                empty_squares.append((i,j))
    return empty_squares

getInput()
