from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission


class Sudoku(models.Model):
    numSolutions = models.IntegerField(max_length=4)
    numEmpty = models.IntegerField(max_length=2)
    boards = models.TextField(max_length=100000000, null=True)
    solution1 = models.TextField(max_length=100000000, null=True)
    solution2 = models.TextField(max_length=100000000, null=True)
    solution3 = models.TextField(max_length=100000000, null=True)
    solution4 = models.TextField(max_length=100000000, null=True)
    solution5 = models.TextField(max_length=100000000, null=True)
    solution6 = models.TextField(max_length=100000000, null=True)
    solution7 = models.TextField(max_length=100000000, null=True)
    solution8 = models.TextField(max_length=100000000, null=True)
    solution9 = models.TextField(max_length=100000000, null=True)
    solution10 = models.TextField(max_length=100000000, null=True)
    solution11 = models.TextField(max_length=100000000, null=True)
    solution12 = models.TextField(max_length=100000000, null=True)
    solution13 = models.TextField(max_length=100000000, null=True)
    solution14 = models.TextField(max_length=100000000, null=True)
    solution15 = models.TextField(max_length=100000000, null=True)
    solution16 = models.TextField(max_length=100000000, null=True)
    solution17 = models.TextField(max_length=100000000, null=True)
    solution18 = models.TextField(max_length=100000000, null=True)
    solution19 = models.TextField(max_length=100000000, null=True)
    solution20 = models.TextField(max_length=100000000, null=True)
    solution21 = models.TextField(max_length=100000000, null=True)
    solution22 = models.TextField(max_length=100000000, null=True)
    solution23 = models.TextField(max_length=100000000, null=True)
    solution24 = models.TextField(max_length=100000000, null=True)
    solution25 = models.TextField(max_length=100000000, null=True)
    solution26 = models.TextField(max_length=100000000, null=True)
    solution27= models.TextField(max_length=100000000, null=True)
    solution28 = models.TextField(max_length=100000000, null=True)
    solution29 = models.TextField(max_length=100000000, null=True)
    solution30 = models.TextField(max_length=100000000, null=True)
     ## for i in range(30):
    ##     i = str(i)
    ##     solution + i = models.TextField(max_length=100000000, null=True)
    def _unicode_(self):
        return (self.board)

class Fillomino(models.Model):
    # numSolutions = models.IntegerField(max_length=4)
    numEmpty = models.IntegerField(max_length=2)
    boards = models.TextField(max_length=100000000, null=True)
    size = models.IntegerField(max_length=2)
    solution = models.TextField(max_length=100000000, null=True)

class FillominoRating(models.Model):
    board = models.TextField(max_length=100000000, null=True)
    board_id = models.IntegerField(max_length=30)
    time_took = models.IntegerField(max_length=50)
    num_clicks = models.IntegerField(max_length=50)
    rating = models.IntegerField(max_length=1)
    def _unicode_(self):
        return (self.rating)

class SudokuRating(models.Model):
    board = models.TextField(max_length=100000000, null=True)
    board_id = models.IntegerField(max_length=30)
    time_took = models.IntegerField(max_length=50)
    num_clicks = models.IntegerField(max_length=50)
    rating = models.IntegerField(max_length=1)
    def _unicode_(self):
        return (self.rating)

