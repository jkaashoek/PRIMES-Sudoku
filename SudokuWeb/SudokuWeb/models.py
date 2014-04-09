from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission


class Puzzle(models.Model):
    numSolutions = models.IntegerField(max_length=4)
    numEmpty = models.IntegerField(max_length=2)
    boards = models.TextField(max_length=100000000, null=True)
    def _unicode_(self):
        return (self.board)

class Rating(models.Model):
    board = models.TextField(max_length=100000000, null=True)
    board_id = models.IntegerField(max_length=30)
    time_took = models.IntegerField(max_length=50)
    rating = models.IntegerField(max_length=1)
    def _unicode_(self):
        return (self.rating)
