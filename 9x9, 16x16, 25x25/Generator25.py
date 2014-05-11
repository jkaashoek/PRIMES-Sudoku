import random
import copy
from Model25 import *

def switchCols(board):
    temp = copy.deepcopy(board)
    bandNum = random.randint(0, 4) #random vertical bands
    colOrder = [0, 1, 2, 3, 4]
    random.shuffle(colOrder) #mix the order of the columns in that band
    
    #go through each column in the band to change cell
    for r in range(25):
        for c in range(5*bandNum, 5*bandNum + 5):
            #cell value in column gets assigned according to colOrder
            board[r][c] = temp[r][colOrder[c%5] + 5*bandNum]
    return board

'''Mixes up the rows in a random 3x9 horizontal stack'''
def switchRows(board):
    temp = copy.deepcopy(board)
    stackNum = random.randint(0, 4) #random horizontal stack
    rowOrder = [0, 1, 2, 3, 4]
    random.shuffle(rowOrder) #mix the order of the rows in that stack
    #go through each row in stack
    for r in range(5*stackNum, 5*stackNum + 5):
        #change order of rows according to rowOrder
        board[r] = temp[stackNum*5 + rowOrder[r%5]]
    return board


'''Reflects the board horizontally, over the middle vertical line'''
def horizontalReflect(board):
    temp = copy.deepcopy(board)
    for r in range(25):
        for c in range(25):
            board[r][c] = temp[r][24-c]
    return board

'''Reflects the board vertically, over the middle horizontal line'''
def verticalReflect(board):
    temp = copy.deepcopy(board)
    for i in range(25):
        board[i] = temp[24 - i]
    return board

'''randomly mixes the order of the 3x9 horizontal stacks'''
def switchStacks(board):
    order = [0, 1, 2, 3, 4]
    random.shuffle(order)
    temp = board[:]
    for i in range(25):
        board[i] = temp[5*order[(i//5)] + i%5]
    return board

'''randomly mixes the order of the 9x3 vertical bands'''
def switchBands(board):
    order = [0, 1, 2, 3, 4]
    random.shuffle(order)
    temp = copy.deepcopy(board)
    for i in range(25):
        for j in range(25):
            board[i][j] = temp[i][5*order[(j//5)] + j%5]
    return board

'''randomly switches the placement of the digits'''
def permutateDigits(board):
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    shuffled = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    random.shuffle(shuffled)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y']
    numToLetters = dict()
    for i in range(1, 26):
        numToLetters[i] = letters[i-1]
    lettersToNum = dict()
    for i in range(1, 26):
        lettersToNum[letters[i-1]] = shuffled[i-1]
    for a in range(25):
        for b in range(25):
            # print "DEBUG:", board[a][b], a, b
            board[a][b] = numToLetters[board[a][b]]
    for c in range(25):
        for d in range(25):
            board[c][d] = lettersToNum[board[c][d]]
    return board

'''rotates the board 90 degrees to the left'''
def rotate(board):
    horizontalReflect(board)
    temp = copy.deepcopy(board)
    for i in range(25):
        for j in range(25):
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
        [[4, 21, 7, 18, 13, 3, 6, 15, 9, 20, 24, 12, 16, 25, 2, 22], [5, 9, 19, 1, 12, 14, 18, 8, 24, 23, 11, 22, 17, 15, 10, 21], [3, 16, 22, 8, 23, 17, 1, 4, 7, 25, 19, 13, 6, 18, 14, 10], [2, 15, 24, 11, 10, 13, 21, 16, 5, 19, 3, 8, 20, 23, 7, 18], [20, 25, 6, 14, 17, 12, 22, 10, 11, 2, 1, 21, 4, 5, 9, 16], [14, 18, 8, 6, 16, 20, 17, 7, 23, 13, 15, 11, 3, 4, 21, 1], [25, 22, 15, 2, 7, 24, 3, 21, 18, 10, 8, 6, 23, 1, 19, 14], [10, 17, 13, 9, 3, 22, 19, 11, 14, 5, 7, 24, 18, 16, 12, 6], [19, 24, 21, 4, 11, 25, 2, 12, 15, 1, 20, 9, 22, 14, 5, 13], [1, 5, 23, 12, 20, 8, 4, 9, 16, 6, 10, 17, 25, 2, 13, 7], [7, 4, 16, 15, 6, 9, 24, 2, 20, 22, 17, 5, 12, 8, 18, 19], [23, 13, 2, 19, 21, 4, 5, 18, 10, 11, 22, 14, 24, 3, 25, 9], [9, 3, 10, 17, 14, 23, 25, 6, 8, 15, 13, 7, 1, 20, 16, 24], [18, 20, 12, 24, 25, 21, 14, 1, 13, 16, 23, 10, 11, 19, 4, 17], [11, 8, 1, 22, 5, 19, 12, 3, 17, 7, 6, 2, 21, 9, 15, 23], [17, 1, 18, 10, 8, 15, 9, 5, 12, 14, 2, 20, 13, 11, 6, 3]]]
    board = random.choice(boards)
    shuffle(board)
    return board


## def new():
##     boards = [
## [[4, 9, 7, 1, 8, 2, 5, 3, 6],
## [1, 5, 2, 3, 6, 4, 8, 9, 7],
## [8, 6, 3, 5, 7, 9, 4, 1, 2],
## [7, 3, 4, 6, 9, 1, 2, 5, 8],
## [2, 8, 9, 4, 3, 5, 7, 6, 1],
## [5, 1, 6, 7, 2, 8, 9, 4, 3],
## [3, 2, 5, 9, 1, 7, 6, 8, 4],
## [9, 7, 1, 8, 4, 6, 3, 2, 5],
## [6, 4, 8, 2, 5, 3, 1, 7, 9]],

## [[1, 3, 5, 4, 6, 8, 9, 7, 2],
## [7, 9, 6, 3, 5, 2, 4, 1, 8],
## [2, 4, 8, 9, 1, 7, 5, 6, 3],
## [5, 6, 9, 7, 2, 1, 3, 8, 4],
## [4, 2, 7, 8, 9, 3, 6, 5, 1],
## [3, 8, 1, 6, 4, 5, 2, 9, 7],
## [6, 1, 3, 5, 8, 4, 7, 2, 9],
## [8, 5, 4, 2, 7, 9, 1, 3, 6],
## [9, 7, 2, 1, 3, 6, 8, 4, 5]]
## ]
    
##     board = random.choice(boards)
##     shuffle(board)
##     return board

