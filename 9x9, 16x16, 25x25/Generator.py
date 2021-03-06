import random
import copy

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

def copyListOfLists(lists):
    res = []
    for i in range(len(lists)):
        res1 = []
        for j in range(len(lists[i])):
            res1.append(lists[i][j])
        res.append(res1)
    return res

def new():
    boards = [
[[4, 9, 7, 1, 8, 2, 5, 3, 6],
[1, 5, 2, 3, 6, 4, 8, 9, 7],
[8, 6, 3, 5, 7, 9, 4, 1, 2],
[7, 3, 4, 6, 9, 1, 2, 5, 8],
[2, 8, 9, 4, 3, 5, 7, 6, 1],
[5, 1, 6, 7, 2, 8, 9, 4, 3],
[3, 2, 5, 9, 1, 7, 6, 8, 4],
[9, 7, 1, 8, 4, 6, 3, 2, 5],
[6, 4, 8, 2, 5, 3, 1, 7, 9]]

## [[1, 3, 5, 4, 6, 8, 9, 7, 2],
## [7, 9, 6, 3, 5, 2, 4, 1, 8],
## [2, 4, 8, 9, 1, 7, 5, 6, 3],
## [5, 6, 9, 7, 2, 1, 3, 8, 4],
## [4, 2, 7, 8, 9, 3, 6, 5, 1],
## [3, 8, 1, 6, 4, 5, 2, 9, 7],
## [6, 1, 3, 5, 8, 4, 7, 2, 9],
## [8, 5, 4, 2, 7, 9, 1, 3, 6],
## [9, 7, 2, 1, 3, 6, 8, 4, 5]]
]
    
    board = random.choice(boards)
    shuffle(board)
    return board

