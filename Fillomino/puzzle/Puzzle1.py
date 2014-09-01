import random
from genBoard import *
from Model1 import *

class Puzzle:
    
    def __init__(self, nSolutions, nEmpty, N, board = []):
        if board == []:
            self.__fullBoard = filler(N) #create new sudoku board from generator
        else:
            self.__fullBoard = board
        self.__nSolutions = nSolutions #number of solutions board has
        self.__nEmpty = nEmpty #number of squares removed
        self.__emptiedBoard = copyListOfLists(self.__fullBoard)
        self.__valsTried = []
        self.__emptiedSquares = []
        self.__numSquaresRemaining = self.__nEmpty
        self.__continue = True
        self.__currNumSolutions = 1
        self.__N = N
    
    def reset(self):
        self.__valsTried = [] #remove all values from valsTried
    
    def getRandomIJ(self):
        ls = []
        for i in range(self.__N):
            for j in range(self.__N):
                if (((i, j) not in self.__emptiedSquares) and ((i, j) not in self.__valsTried)):
                    ls.append((i, j))
        if (len(self.__emptiedSquares) + len(self.__valsTried) == self.__N**2):
            return -1, -1
        else:
            i, j = random.choice(ls)
            return i, j
    
    def empty(self):
        while(self.__numSquaresRemaining>0 and self.__continue):
            print("Emptied " + str(self.__nEmpty - self.__numSquaresRemaining ) + " squares")
            print(self.__emptiedBoard)
            self.removeSquare()
            self.__numSquaresRemaining -= 1
        print("Emptied " + str(len(self.__emptiedSquares)) + " squares")
        print("This puzzle has " + str(self.__currNumSolutions) + " solution(s)")
    
    def removeSquare(self):
        i, j = self.getRandomIJ()
        print "i = ", i, " j = ", j
        while ((not self.validSquare(i, j))):
            if ((i, j) == (-1, -1)):
                break
            self.__valsTried.append((i, j))
            print("Another value added to valsTried: " + str(len(self.__valsTried)) +
                  " total values in valsTried and " + str(len(self.__emptiedSquares)) + " already empty.")
            i, j = self.getRandomIJ()
        
        if ((i, j) != (-1, -1)):
            self.__emptiedBoard[i][j] = 0
            #self.__currNumSolutions = self.__solutionsAfterEmptying
            self.__emptiedSquares.append((i, j))
        else:
            self.__continue = False
    
    def haveNeighborInSameRegion(self, i, j, tempBoard):
        t1 = i-1>=0 and tempBoard[i][j] == tempBoard[i-1][j]
        t2 = i+1<self.__N and tempBoard[i][j] == tempBoard[i+1][j]
        t3 = j-1>=0 and tempBoard[i][j] == tempBoard[i][j-1]
        t4 = j+1<self.__N and tempBoard[i][j] == tempBoard[i][j+1]
        return t1 or t2 or t3 or t4
    
    def validSquare(self, i, j):
        #val_now = board[i][j] # value before the box changes to 0
        tempBoard = copyListOfLists(self.__emptiedBoard)
        if (not self.haveNeighborInSameRegion(i,j,tempBoard)) : return False
        tempBoard[i][j] =  0 # set cell to 0
        F = createFillominoNew(tempBoard, self.__N, self.__fullBoard)
        return get_models_new(F)
    # print "solving z3 constraints"
    # self.__solutionsAfterEmptying = len(get_models(F, self.__nSolutions + 1, self.__N))
    # print "z3 constraints solved"
    # print("solutions: " + str(self.__solutionsAfterEmptying));
    # return (self.__solutionsAfterEmptying <= self.__nSolutions and self.__solutionsAfterEmptying > 0)
    
    def getPuzzle(self):
        return self.__emptiedBoard
    
    def getOriginalBoard(self):
        return self.__fullBoard
    
    def printPuzzle(self):
        print_matrix(self.__emptiedBoard)
    
    
    def puzzleID(self):
        return self.__currNumSolutions, len(self.__emptiedSquares)

    def optimal(self):
        for i in range(len(self.__fullBoard)):
            for j in range(len(self.__fullBoard[0])):
                if (self.__fullBoard[i][j] != 0):
                    if (self.validSquare(i, j)):
                        return False
        return True

'''

N = 6

p = Puzzle(1, N*N, N)
p.empty()
p.getOriginalBoard()
p.printPuzzle()'''