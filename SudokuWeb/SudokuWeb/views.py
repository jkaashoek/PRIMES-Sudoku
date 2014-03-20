from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
#from django.contrib.auth.models import Puzzle
from models import *
from django import forms
import random

def index(request):
	return render(request, 'SudokuWeb/index.html', {'board':[]})

def howtoplay(request):
	return render(request, 'SudokuWeb/howtoplay.html', {})

def genSudoku(request):
    numEmpty = int(request.POST["numSquares"])
    numSolutions = int(request.POST["numSolutions"])
    print numEmpty, numSolutions
    possible_objects = Puzzle.objects.filter(numEmpty=numEmpty, numSolutions=numSolutions)
    possible_boards = []
    for puzzle in possible_objects:
        possible_boards.append(puzzle.boards)
    final_board = str(random.choice(possible_boards))
    strs = final_board.replace('[','').split('],')
    board = [map(int, s.replace(']','').split(',')) for s in strs]
    return render(request, 'SudokuWeb/index.html', {'board':board})

def addPuzzles(request):
    with open("1-40.txt", "r") as myfile:
        puzzles = myfile.readlines()
    list_puzzles =[]
    for puzzle in puzzles:
        puzzle.replace('\n', '')
        strs = puzzle.replace('[','').split('],')
        board = [map(int, s.replace(']','').split(',')) for s in strs]
        puzzle = Puzzle(
            numSolutions=1,
            numEmpty=40,
            boards = board
        )
        puzzle.save()
    return HttpResponseRedirect(reverse('index'))
