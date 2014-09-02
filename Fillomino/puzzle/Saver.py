import json
from Puzzle1 import Puzzle
from genBoard import*
from Model1 import*
import random

def main():
    N = int(input("Enter N: "))
    nSolutions = int(input("How many solutions should the puzzle have? "))
    nEmpty = N*N
    count = int(input("how many puzzles this session? "))
        
    runTimes = open("runTimes" + str(N) + "x" + str(N) + ".txt", 'a') #comment out for no run times

    for i in range(count):
        print("Generating puzzle " + str(i))
        p = Puzzle(nSolutions, nEmpty, N)
        p.empty()
        filNam = str(N) + "-" + str(p.puzzleID()[0]) + "-" + str(p.puzzleID()[1]) + ".txt"
        out = open(filNam, 'a')
        
        emptyBoard = p.getPuzzle()
        fullBoard = p.getOriginalBoard()
        addTransformations(emptyBoard, fullBoard, out)
        out.close()

        #comment out for no run times
        runTimes.write(str(p.runTime()))
        runTimes.write('\n')
        runTimes.write(str(p.puzzleID()[1]))
        runTimes.write('\n')

    runTimes.close() #comment out for no run times

def addTransformations(emptyBoard, fullBoard, out):
    for i in range(4):
        json.dump(emptyBoard, out)
        out.write('\n')
        json.dump(fullBoard, out)
        out.write('\n')
        rotate(emptyBoard)
        rotate(fullBoard)
    
    verticalReflect(emptyBoard)
    verticalReflect(fullBoard)

    for i in range(4):
        json.dump(emptyBoard, out)
        out.write('\n')
        json.dump(fullBoard, out)
        out.write('\n')
        rotate(emptyBoard)
        rotate(fullBoard)


main()
