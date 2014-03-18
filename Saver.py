import json
from Puzzle import Puzzle
from Generator import*
from Model import*

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

def main():
    nSolutions = int(input("How many solutions should the puzzle have? "))
    nEmpty = int(input("How many empty cells do you want? "))
    if (nEmpty <= 45):
        print("Generating and saving initial puzzle...")
        p = Puzzle(nSolutions, nEmpty)
        p.empty()

        filNam = str(p.puzzleID()[0]) + "-" + str(p.puzzleID()[1]) + ".txt"
        out = open(filNam, 'a')

        json.dump(p.getPuzzle(), out)
        print("Now adding more puzzles...")
        n = 0
        i = 1
        while(n < 50):
            print("Trying new puzzle " + str(i))
            fullBoard = copyListOfLists(p.getOriginalBoard())
            emptyBoard = copyListOfLists(p.getPuzzle())
            board = createMoreSudoku(fullBoard, emptyBoard)
            F = createSudoku(board)
            if (exactly_n_models(F, p.puzzleID()[0])):
                json.dump(board, out)
                n+= 1
                print("Another puzzle added: " + str(n) + " puzzles this session out of "

                      + str(i) + " tried")
            i += 1
    
    else:
        print("Generating and saving 50 puzzles with your preferences...")
        for i in range(50):
            print("Generating puzzle " + str(i + 1) + " of 50...")
            p = Puzzle(nSolutions, nEmpty)
            p.empty()

            filNam = str(p.puzzleID()[0]) + "-" + str(p.puzzleID()[1]) + ".txt"
            out = open(filNam, 'a')
        
            json.dump(p.getPuzzle(), out)
            

main()
