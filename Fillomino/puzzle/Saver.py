import json
from Puzzle import Puzzle
from genBoard import*
from Model import*
import random

def main():
    N = int(input("Enter N: "))
    nSolutions = int(input("How many solutions should the puzzle have? "))
    nEmpty = N*N
    count = int(input("how many puzzles this session? "))

    for i in range(count):
        print("Generating puzzle " + str(i))
        p = Puzzle(nSolutions, nEmpty, N)
        p.empty()
        filNam = str(N) + "-" + str(p.puzzleID()[0]) + "-" + str(p.puzzleID()[1]) + ".txt"
        out = open(filNam, 'a')
        json.dump(p.getPuzzle(), out)
        out.write('\n')
        out.close()
        

main()
