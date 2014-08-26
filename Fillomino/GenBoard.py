import random


def genEmptyBoard():
    board = []
    for k in range(N):
        board.append([])
    for i in range(N):
        for j in range(N):
            board[i].append(0)
    return board

def selectLength(avail_squares):
    poss_lengths = []
    length = 0
    if avail_squares < 9:
        for i in range(avail_squares):
            poss_lengths.append(i+1)
    else:
        for i in range(8):
            poss_lengths.append(i+1)
    length = random.choice(poss_lengths)
    return length

def randomDirection(start, board):
    directions = [(0,1), (0,-1), (1, 0), (-1, 0)]
    direc = random.choice(directions)
    while board[start[0]+direc[0]][start[1]+direc[1]] != 0:
        direc = random.choice(directions)
    return direc

def getAdj(xloc, yloc, do_shuffle):
    adj = []
    adj.append((xloc+1, yloc))
    adj.append((xloc-1, yloc))
    adj.append((xloc, yloc+1))
    adj.append((xloc, yloc-1))
    copy = adj[0:]
    for i in adj:
        if (i[0] < 0 or i[0] > (N-1)) or (i[1] < 0 or i[1] > (N-1)):
            copy.remove(i)
    if do_shuffle:
        copy = shuffle(copy)
    return copy

def shuffle(lists):
    shuffled = []
    length = len(lists)
    for i in range(length):
        choice = random.choice(lists)
        shuffled.append(choice)
        lists.remove(choice)
    return shuffled

def isStuck(start, board):
    adj = getAdj(start[0], start[1], False)
    for i in adj:
        if board[i[0]][i[1]] == 0:
            return False
    return True


def countPossSquares(start, board, counted=[]):
    counted.append(start)
    if isStuck(start, board) and len(counted) == 1:
        return counted
    if isStuck(start, board) or board[start[0]][start[1]] != 0:
        return counted
    else:
        adj = getAdj(start[0], start[1], False)
        for i in adj:
            if i not in counted:
                counted = countPossSquares(i, board, counted)
        return counted

def getPossSquares(start, board, seq_length, total, squares=[]):
    if total == 1:
        return [start]
    if len(squares) >= total:
        return squares
    if seq_length <= 0:
        return squares
    if isStuck(start, board) or board[start[0]][start[1]] != 0:
        return squares
    else:
        squares.append(start)
        adj = getAdj(start[0], start[1], True)
        for i in adj:
            if len(squares) >= total:
                break 
            if i not in squares:
                squares = getPossSquares(i, board, seq_length-1, total, squares)
        return squares

def isFull(board):
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                return False
    return True

def findStart(board):
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                return (i,j)

def showBoard(board):
    for i in range(N):
        for j in range(N):
            print board[i][j],
        print "\n"

def addSquares(board, squares):
    for i in range(N):
        for j in range(N):
            if (i,j) in squares:
                board[i][j] = len(squares)
    return board

def filler():
    board = genEmptyBoard()
    while not isFull(board):
        start = findStart(board)
        squares_available = countPossSquares(start, board, [])
        seq_length = selectLength(len(squares_available))
        add_squares = getPossSquares(start, board, seq_length, seq_length, [])
        board = addSquares(board, add_squares)
    return board

for i in range(5, 20):
    for j in range(10):
        N = i
        print filler()

       
