import json
from Puzzle1 import*
from Model1 import *
from z3 import *
from sklearn import svm
import random

def num_cells(puzzle):
    return len(puzzle)*len(puzzle[0])

def num_empty(puzzle):
    empty = 0
    for row in puzzle:
        for item in row:
            if (item == 0):
                empty+=1
    return empty

def optimal(board):
    p = Puzzle(1, num_empty(board) + 1, len(board), board)
    optimal = p.optimal()
    if optimal: return 1
    return 0

def num_regions(puzzle):
    N = len(puzzle)
    F = createFillomino(puzzle, N)
    s = Solver()
    s.add(F)
    if (s.check() == sat):
        m = s.model()
        r = [ [ m.evaluate(Int("x%d%d" % (i,j))) for j in range(1, N+1) ]
             for i in range(1, N+1)]
        s =[ [ m.evaluate(Int("size%d%d" % (i,j))) for j in range(N) ]
                 for i in range(N)]
                 #print_matrix(r)
                 #print_matrix(s)
        num = 0
        for i in range(N):
            for j in range(N):
                val1 = r[i][j].as_long()
                val2 = s[i][j].as_long()
                if (val1 == val2):
                    num += 1
        return num
    else:
        return 0



def createVectors():
    inFile = open('mathinenglishfillomino.txt', 'r')
    outFile = open('vectors.txt', 'a')
    
    data = []
    for line in inFile:
        #print(line)
        data.append(json.loads(line))
    print(data)

    num = 1
    
    for i in range(len(data)/2):
        vec = []
        puzzle = data[2*i]
        difficulty= data[2*i + 1]
        v1 = difficulty
        v2 = num_cells(puzzle)
        v3 = num_empty(puzzle)
        v4 = num_regions(puzzle)
        v5 = optimal(puzzle)
        vec = [v1, v2, v3, v4, v5]
        json.dump(vec, outFile)
        outFile.write('\n')
        print("Done with puzzle " + str(num))
        num += 1
    inFile.close()
    outFile.close()

createVectors

