import random
from Generator16 import *
from Model16 import *

class Puzzle16:

    def __init__(self, nSolutions, nEmpty):
        self.__fullBoard = new() #create new sudoku board from generator
        self.__nSolutions = nSolutions #number of solutions board has
        self.__nEmpty = nEmpty #number of squares removed
        self.__emptiedBoard = copyListOfLists(self.__fullBoard)
        self.__valsTried = []
        self.__emptiedSquares = []
        self.__numSquaresRemaining = self.__nEmpty
        self.__continue = True
        self.__currNumSolutions = 1

    def reset(self):
        self.__valsTried = [] #remove all values from valsTried

    def getRandomIJ(self):
        ls = []
        for i in range(16):
            for j in range(16):
                if (((i, j) not in self.__emptiedSquares) and ((i, j) not in self.__valsTried)):
                    ls.append((i, j))
        if (len(self.__emptiedSquares) + len(self.__valsTried) == 256):
            return -1, -1
        else:
            i, j = random.choice(ls)
            return i, j

    def empty(self):
        while(self.__numSquaresRemaining>0 and self.__continue):
            print("Emptied " + str(self.__nEmpty - self.__numSquaresRemaining ) + " squares")
            self.removeSquare()
            self.__numSquaresRemaining -= 1
        print("Emptied " + str(len(self.__emptiedSquares)) + " squares")
        print("This puzzle has " + str(self.__currNumSolutions) + " solution(s)")

    def removeSquare(self):
        i, j = self.getRandomIJ()
        while ((not self.validSquare(i, j))):
            if ((i, j) == (-1, -1)):
                break
            self.__valsTried.append((i, j))
            print("Another value added to valsTried: " + str(len(self.__valsTried)) +
                  " total values in valsTried and " + str(len(self.__emptiedSquares)) + " already empty.")
            i, j = self.getRandomIJ()

        if ((i, j) != (-1, -1)):
            self.__emptiedBoard[i][j] = 0
            self.__emptiedSquares.append((i, j))
            self.reset()
        else:
            self.__continue = False

    def validSquare(self, i, j):
        #val_now = board[i][j] # value before the box changes to 0
        tempBoard = copyListOfLists(self.__emptiedBoard)
        tempBoard[i][j] =  0 # set cell to 0
        F = createSudoku(tempBoard)
        self.__currNumSolutions = len(get_models(F, self.__nSolutions + 1))
        print "currNumSols = ", self.__currNumSolutions
        print "nSolutions = ", self.__nSolutions
        return (self.__currNumSolutions <= self.__nSolutions and self.__currNumSolutions > 0)

    def getPuzzle(self):
        return self.__emptiedBoard
    
    def getOriginalBoard(self):
        return self.__fullBoard

    def printPuzzle(self):
        print_matrix(self.__emptiedBoard)


    def puzzleID(self):
        return self.__currNumSolutions, len(self.__emptiedSquares)

## ap = Puzzle16(1, 256)
## ap.printPuzzle()
## ap.empty()
## ap.printPuzzle()
