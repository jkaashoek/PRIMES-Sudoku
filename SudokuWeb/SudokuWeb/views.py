from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
#from django.contrib.auth.models import Puzzle
from models import *
from django import forms
from z3 import *
import random
import os

def index(request):
    if str(Puzzle.objects.all()) == str([]):
        show_form = False
    else:
        show_form = True
    return render(request, 'SudokuWeb/index.html', {'board':[], 'show_form':show_form})

def howtoplay(request):
	return render(request, 'SudokuWeb/howtoplay.html', {})

def checkedBoard(request, user_board, need_fixing):
    return render(request, 'SudokuWeb/checkedBoard.html', {'user_board':user_board, 'need_fixing':need_fixing})

def genRandSudoku(request):
    possible_objects = Puzzle.objects.all()
    final_puzzle = random.choice(possible_objects)
    board_id = final_puzzle.id
    print "DEBUG:", final_puzzle, board_id
    return redirect('displayBoard', board_id=board_id)

def rating(request, board_id):
    board = Puzzle.objects.get(id=board_id).boards
    rating = request.POST['optionsRadios']
    rating = int(rating[-1])
    rateob = Rating(
        rating = rating,
        board = board
    )
    rateob.save()
    return HttpResponseRedirect(reverse('index'))

def checkSudoku(request, board_id):
    board = Puzzle.objects.get(id=board_id).boards
    board = makeList(board)
    user_board = copyListOfLists(board)
    user_inputs = []
    for i in range(1,10):
        for j in range(1,10):
            string = str(i) + str(j)
            if string in request.POST.keys():
                square = request.POST[string]
                user_inputs.append((square, (i-1,j-1)))
    for uin in user_inputs:
        if uin[0] != '':
            location1 = uin[1][0]
            location2 = uin[1][1]
            user_board[location1][location2] = int(uin[0])
    final = []
    need_fixing, correct = checkCorrect(board, user_board)
    for i in range(9):
        row = []
        for j in range(9):
                row.append((user_board[i][j], atCol(i,j), atRow(i,j), (i,j) in need_fixing))
        final.append(row)
    return render(request, 'SudokuWeb/checkedBoard.html', {'board':final, 'correct':correct})
   # return HttpResponseRedirect('SudokuWeb/displayBoard' + str(user_board) + str(need_fixing))
    #return redirect('displayBoard', user_board='user_board', need_fixing='need_fixing')

def atCol(x, y):
    if (y+1)%3==0:
        return True
    return False

def atRow(x, y):
    if (x+1)%3==0:
        return True
    return False

def displayBoard(request, board_id):
    print "first"
    puzzle = Puzzle.objects.get(id=board_id)
    final_board = puzzle.boards
    board = makeList(final_board)
    return render(request, 'SudokuWeb/displayBoard.html', {'board':board})

def genSudoku(request):
    numEmpty = int(request.POST["numSquares"])
    numSolutions = int(request.POST["numSolutions"])
    possible_objects = Puzzle.objects.filter(numEmpty=numEmpty, numSolutions=numSolutions)
    final_puzzle = random.choice(possible_objects)
    board_id = final_puzzle.id
    print "DEBUG:", final_puzzle, board_id
    return redirect('displayBoard', board_id=board_id)

def addPuzzles(request):
    file_names = []
    for path, subdirs, files in os.walk('Puzzles'):
        #print "HERE"
        for filename in files:
            f = os.path.join(filename)
            if f != ".DS_Store":
                location = f.index("-")
                num_solutions = f[0:location]
                numEmpty = f[location+1:location+3]
                print num_solutions, numEmpty
                #if numEmpty >41 and num_solutions != 1:
                    #print "NUMBERS:",  num_solutions, numEmpty
                with open("Puzzles/" + f, "r") as myfile:
                    puzzles = myfile.readlines()
                    # print puzzles
                    list_puzzles =[]
                    for puzzle in puzzles:
                        puzzle.replace('\n', '')
                        strs = puzzle.replace('[','').split('],')
                        board = [map(int, s.replace(']','').split(',')) for s in strs]
                        #print board
                        puzzle = Puzzle(
                        numSolutions=num_solutions,
                        numEmpty=numEmpty,
                        boards = board
                        )
                        puzzle.save()
    return HttpResponseRedirect(reverse('index'))

def checkCorrect(board, user_board):
    need_fixing = []
    correct = True
    correct_board = createSudoku(board)
    for i in range(9):
        for j in range(9):
            correct_board[i][j] = correct_board[i][j].as_string()
            if user_board[i][j] != 0 and correct_board[i][j] != '0' and str(correct_board[i][j]) != str(user_board[i][j]):
                correct = False
                need_fixing.append((i,j))
    return need_fixing, correct

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
    s = Solver()
    s.add(valid_values + row_distinct + cols_distinct + three_by_three_distinct + already_set)
    if s.check() == sat:
        m = s.model()
        r = [ [ m.evaluate(X[i][j]) for j in range(9) ] for i in range(9) ]
    return r

def makeList(string):
    strs = string.replace('[','').split('],')
    board = [map(int, s.replace(']','').split(',')) for s in strs]
    return board

def copyListOfLists(lists):
    res = []
    for i in range(len(lists)):
        res1 = []
        for j in range(len(lists[i])):
            res1.append(lists[i][j])
        res.append(res1)
    return res
## Through form, get the values user inputs. We know the id of the board, so use that to find the board in the database. Fill in the board with the user's inputs. FIll in the board with z3 (there will only be one solutsion for now) Find where they differ (be sure those places are not places the user inputted a 0. Return a list of all of the locations that were different. In HTML, use for loops to recreate the user's board. While filling in the board, go through locations that were incorrect and if the user is incorrect, highlight the square red.
