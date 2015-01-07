from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
#from django.contrib.auth.models import Puzzle
from models import *
from django import forms
from z3 import *
import time
import random
import os
import sys
import settings

def index(request):
    if str(Sudoku.objects.all()) == str([]):
        show_form = False
    else:
        show_form = True
    return render(request, 'SudokuWeb/index.html',  {'show_form':show_form})

def addPuzzles(request):
    addFillomino()
    addSudokus()
    return HttpResponseRedirect(reverse('index'))

## ---------------------- FILLOMINO PUZZLE CODE ----------------------
def Fillomino_Home(request):
    request.session["num_fillo_clicks"] = 0
    sizes = []
    fillos = Fillomino.objects.all()
    for puzzle in fillos:
        if puzzle.size not in sizes:
            sizes.append(puzzle.size)
    sizes.sort()
    return render(request, 'SudokuWeb/FillominoHome.html', {'sizes':sizes})

def addFillomino():
    for path, subdirs, files in os.walk('fillomino_puzzles'):
        for filename in files:
            f = os.path.join(filename)
            if f != ".DS_Store":
                location1 = f.index("-")
                location2 = f.rfind("-")
                location3 = f.index(".")
                size = int(f[0:location1])
                numSolutions = int(f[location1+1:location2])
                numEmpty = int(f[location2+1:location3])
                with open("fillomino_puzzles/" + f, "r") as myfile:
                    count = 0
                    boards = myfile.readlines()
                    for board in boards:
                        if count % 2 == 0:
                            fillo = Fillomino()
                            fillo.boards = boards[count]
                            fillo.solution = boards[count+1]
                            fillo.numEmpty = numEmpty
                            fillo.size = size
                            fillo.save()
                        count += 1
    return

def genFillomino(request, size):
    poss_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    boards = Fillomino.objects.filter(size=size)
    selected = random.choice(boards)
    board_id = selected.id
    return redirect('displayFillomino', board_id=board_id)

def displayFillomino(request, board_id):
    puzzle = Fillomino.objects.get(id=board_id)
    board = makeList(puzzle.boards)
    request.session['start_fillo'] = time.time()
    request.session['old_fillo'] =board
    return render(request, 'SudokuWeb/displayFillomino.html', {'board':board}) 

def genRandFillomino(request):
    num_rows = Fillomino.objects.all().count()
    rand_id = random.randint(0, num_rows) 
    final_puzzle_id = makeList(Fillomino.objects.get(id = rand_id).id)
    return redirect('displayFillomino', board_id=final_puzzle_id)

def checkFillomino(request, board_id):
    request.session["num_fillo_clicks"] += 1
    answers = request.POST
    print answers
    incorrect = []
    puzzle = Fillomino.objects.get(id=board_id)
    solution = makeList(puzzle.solution)
    board = makeList(puzzle.boards)
    user_board = copyListOfLists(board)
    old_board = request.session['old_fillo']
    for i in range(puzzle.size):
        for j in range(puzzle.size):
            square = str(i+1) + str(j+1)
            if square in answers.keys() and answers[square] != '':
                old_board[int(square[0])-1][int(square[1])-1] = int(answers[square])
    user_board = copyListOfLists(old_board)
    request.session['old_fillo'] = user_board
    fillo_time_so_far = time.time() - request.session['start_fillo']
    for i in range(len(solution)):
        for j in range(len(solution)):
            if user_board[i][j] != 0 and user_board[i][j] != solution[i][j]:
                incorrect.append((i,j))
    final = []
    for i in range(len(solution)):
        row = []
        for j in range(len(solution)):
            if (i,j) in incorrect:
                row.append((user_board[i][j], 0))
            else:
                row.append((user_board[i][j], 1))
        final.append(row)
    if incorrect == [] and isFull(user_board):
        request.session['fillo_time'] = fillo_time_so_far
        correct = True
    else:
        correct = False
    print "DEBUG", fillo_time_so_far
    return render(request, 'SudokuWeb/checkedFillomino.html', {'board':final, 'correct':correct, 'time_so_far':int(fillo_time_so_far)})

def isFull(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return False
    return True

def ratingFillomino(request, board_id):
    board = Fillomino.objects.get(id=board_id).boards
    rating = request.POST['optionsRadios']
    rating = int(rating[-1])
    rateob = FillominoRating(
        board_id = board_id,
        rating = rating,
        board = board,
        time_took = request.session['fillo_time'],
        num_clicks = request.session['num_fillo_clicks'],
    )
    rateob.save()
    return HttpResponseRedirect(reverse('index'))

## ---------------------- SUDOKU PUZZLE CODE ----------------------

def Sudoku_Home(request):
    emptytosolutions = {}
    request.session["num_click"] = 0
    for i in range(55):
        numsolutions = []
        filteredboards = Sudoku.objects.get(numEmpty=i)
        for board in filteredboards:
            numsolutions.append(board.numSolutions)
        emptytosolutions[i] = numsolutions
        
    return render(request, 'SudokuWeb/SudokuHome.html', {'board':[], 'emptytosolutions':emptytosolutions})

def about(request):
    return render(request, 'SudokuWeb/about.html', {})

def howtoplaySudoku(request):
	return render(request, 'SudokuWeb/howtoplaySudoku.html', {})

def checkedBoard(request, user_board, need_fixing):
    return render(request, 'SudokuWeb/checkedSudoku.html', {'user_board':user_board, 'need_fixing':need_fixing})

def genRandSudoku(request):
    num_rows = Sudoku.objects.all().count()
    rand_id = random.randint(0, num_rows) 
    final_puzzle = Sudoku.objects.get(id = rand_id)
    board_id = final_puzzle.id
    request.session['start_time'] = time.time()
    return redirect('displaySudoku', board_id=board_id)

def ratingSudoku(request, board_id):
    board = Sudoku.objects.get(id=board_id).boards
    rating = request.POST['optionsRadios']
    rating = int(rating[-1])
    rateob = SudokuRating(
        board_id = board_id,
        rating = rating,
        board = board,
        time_took = request.session['time_took'],
        num_clicks = request.session['num_click'],
    )
    rateob.save()
    return HttpResponseRedirect(reverse('index'))

def checkSudoku(request, board_id):
    request.session["num_click"] += 1
    board = Sudoku.objects.get(id=board_id).boards
    board = makeList(board)
    user_board = copyListOfLists(board)
    oboard = request.session['old_board']
    for i in range(1,10):
        for j in range(1,10):
            string = str(i) + str(j)
            if string in request.POST.keys():
                square = request.POST[string]
                if square != '':
                    oboard[i-1][j-1] = int(square)
    user_board = copyListOfLists(oboard)
    request.session['old_board'] = user_board
    final = []
    need_fixing, correct = checkCorrect(board_id, user_board)
    time_so_far = time.time() - request.session['start_time']
    if need_fixing == []:
        request.session['time_took'] = time_so_far
    for i in range(9):
        row = []
        for j in range(9):
                row.append((user_board[i][j], atCol(i,j), atRow(i,j), (i,j) in need_fixing))
        final.append(row)
    return render(request, 'SudokuWeb/checkedSudoku.html', {'board':final, 'correct':correct, 'timesofar':int(time_so_far)})

def checkCorrect(board_id, user_board):
    need_fixing = []
    correct = True
    correct_board = findClosest(board_id, user_board)
    for i in range(9):
        for j in range(9):
            if user_board[i][j] != 0 and correct_board[i][j] != '0' and str(correct_board[i][j]) != str(user_board[i][j]):
                need_fixing.append((i,j))
    for i in range(9):
        for j in range(9):
            if user_board[i][j] == 0:
                correct = False
    if need_fixing != []:
        correct = False
    return need_fixing, correct

def findClosest(board_id, board):
    solutions = getSolutions(board_id)
    solution_goingfor = []
    greatestequal = 0
    for solution in solutions:
        if findNumEqual(board, solution) >= greatestequal:
            greatestequal = findNumEqual(board, solution)
            if solution_goingfor == []:
                solution_goingfor.append(solution)
            else:
                solution_goingfor.remove(solution_goingfor[0])
                solution_goingfor.append(solution)
    return solution_goingfor[0]

def findNumEqual(board, solution):
    numequal = 0
    for i in range(9):
        for j in range(9):
            if int(board[i][j]) == int(solution[i][j]):
                numequal += 1
    return numequal
                
def getSolutions(board_id):
    puzzle = Sudoku.objects.get(id=board_id)
    solutions = []
    for i in range(1,30):
        try_solution = "solution" + str(i)
        trying = getattr(puzzle, try_solution)
        if trying != None:
            solution = makeList(trying)
            solutions.append(solution)
    return solutions

def atCol(x, y):
    if (y+1)%3==0:
        return True
    return False

def atRow(x, y):
    if (x+1)%3==0:
        return True
    return False

def displaySudoku(request, board_id):
    puzzle = Sudoku.objects.get(id=board_id)
    final_board = puzzle.boards
    board = makeList(final_board)
    request.session['start_time'] = time.time()
    request.session['old_board'] = board
    return render(request, 'SudokuWeb/displaySudoku.html', {'board':board})

def genSudoku(request):
    numEmpty = int(request.POST["numSquares"])
    numSolutions = int(request.POST["numSolutions"])
    possible_objects = Sudoku.objects.filter(numEmpty=numEmpty, numSolutions=numSolutions)
    final_puzzle = random.choice(possible_objects)
    board_id = final_puzzle.id
    return redirect('displaySudoku', board_id=board_id)

def addSudokus():
    file_names = []
    for path, subdirs, files in os.walk(settings.BASE_DIR + '/puzzles_sols'):
        for filename in files:
            f = os.path.join(filename)
            if f != ".DS_Store":
                location1 = f.index("-")
                location2 = f.index(".")
                num_solutions = int(f[0:location1])
                numEmpty = f[location1+1:location2]
                i = 0
                with open(settings.BASE_DIR+"/puzzles_sols/" + f, "r") as myfile:
                    boards = myfile.readlines()
                    while i < len(boards):
                        solutions = []
                        puzzle = boards[i]
                        puzzle.replace('\n', '')
                        board = makeList(puzzle)
                        sol = 1
                        while sol <= num_solutions:
                            j = i + sol
                            try:
                                solution = boards[j]
                                solution.replace('\n', '')
                                solutions.append(makeList(solution))
                                sol += 1
                            except:
                                sol += 1
                        dbpuz = Sudoku()
                        dbpuz.numSolutions=num_solutions
                        dbpuz.numEmpty=numEmpty
                        dbpuz.boards = board
                        for k in range(len(solutions)):
                            solname = "solution" + str(k+1)
                            setattr(dbpuz, solname, solutions[k])
                        dbpuz.save()
                        addon = num_solutions + 1
                        i += addon
    return 

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

## GENERAL CODE

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

