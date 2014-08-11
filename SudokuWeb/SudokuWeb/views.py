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

def index(request):
    request.session["num_click"] = 0
    if str(Puzzle.objects.all()) == str([]):
        show_form = False
    else:
        show_form = True
    return render(request, 'SudokuWeb/index.html', {'board':[], 'show_form':show_form})

def about(request):
    return render(request, 'SudokuWeb/about.html', {})

def howtoplay(request):
	return render(request, 'SudokuWeb/howtoplay.html', {})

def checkedBoard(request, user_board, need_fixing):
    return render(request, 'SudokuWeb/checkedBoard.html', {'user_board':user_board, 'need_fixing':need_fixing})

def genRandSudoku(request):
    num_rows = Puzzle.objects.all().count()
    rand_id = random.randint(0, num_rows) 
    final_puzzle = Puzzle.objects.get(id = rand_id)
    board_id = final_puzzle.id
    request.session['start_time'] = time.time()
    return redirect('displayBoard', board_id=board_id)

def rating(request, board_id):
    board = Puzzle.objects.get(id=board_id).boards
    rating = request.POST['optionsRadios']
    rating = int(rating[-1])
    rateob = Rating(
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
    board = Puzzle.objects.get(id=board_id).boards
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
    return render(request, 'SudokuWeb/checkedBoard.html', {'board':final, 'correct':correct, 'timesofar':int(time_so_far)})
   # return HttpResponseRedirect('SudokuWeb/displayBoard' + str(user_board) + str(need_fixing))
    #return redirect('displayBoard', user_board='user_board', need_fixing='need_fixing')

def checkCorrect(board_id, user_board):
    need_fixing = []
    correct = True
    correct_board = findClosest(board_id, user_board)
    print "SOLUTION FOUND:", correct_board
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
        print "NUM EQUAL:", findNumEqual(board, solution), greatestequal
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
    puzzle = Puzzle.objects.get(id=board_id)
    solutions = []
    for i in range(1,30):
        try_solution = "solution" + str(i)
        trying = getattr(puzzle, try_solution)
        if trying != None:
            solution = makeList(trying)
            solutions.append(solution)
    print "ALL SOLS FOR BOARD:", solutions
    return solutions

def atCol(x, y):
    if (y+1)%3==0:
        return True
    return False

def atRow(x, y):
    if (x+1)%3==0:
        return True
    return False

def displayBoard(request, board_id):
    puzzle = Puzzle.objects.get(id=board_id)
    final_board = puzzle.boards
    board = makeList(final_board)
    request.session['start_time'] = time.time()
    request.session['old_board'] = board
    return render(request, 'SudokuWeb/displayBoard.html', {'board':board})

def genSudoku(request):
    numEmpty = int(request.POST["numSquares"])
    numSolutions = int(request.POST["numSolutions"])
    possible_objects = Puzzle.objects.filter(numEmpty=numEmpty, numSolutions=numSolutions)
    final_puzzle = random.choice(possible_objects)
    board_id = final_puzzle.id
    return redirect('displayBoard', board_id=board_id)

def addPuzzles(request):
    file_names = []
    for path, subdirs, files in os.walk('puzzles_sols'):
        for filename in files:
            f = os.path.join(filename)
            if f != ".DS_Store":
                location1 = f.index("-")
                location2 = f.index(".")
                num_solutions = int(f[0:location1])
                numEmpty = f[location1+1:location2]
                i = 0
                with open("puzzles_sols/" + f, "r") as myfile:
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
                        dbpuz = Puzzle()
                        dbpuz.numSolutions=num_solutions
                        dbpuz.numEmpty=numEmpty
                        dbpuz.boards = board
                        for k in range(len(solutions)):
                            solname = "solution" + str(k+1)
                            setattr(dbpuz, solname, solutions[k])
                        dbpuz.save()
                        addon = num_solutions + 1
                        i += addon
    return HttpResponseRedirect(reverse('index'))

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
