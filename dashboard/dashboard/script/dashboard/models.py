from django.contrib.auth.models import AbstractBaseUser
from django.db import models



class Gamer(models.Model):
    pseudo = models.CharField(max_length=50)
    victory = models.IntegerField(default=0)
    nb_game = models.IntegerField(default=  0)
    nb_tournament = models.IntegerField(default=0)
    class Game(models.Model):
        conceded_point = models.IntegerField()
        marked_point = models.IntegerField()
        opponent  = models.CharField(max_length=50)

class TemporaryUser(models.Model):
    pseudo = models.CharField(max_length=50)

class Tournament(models.Model):
    temporary_players = models.ManyToManyField(TemporaryUser)
    class TournamentGame(models.Model):
        tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
        conceded_point = models.IntegerField()
        marked_point = models.IntegerField()
