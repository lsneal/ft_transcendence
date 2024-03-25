from django.db import models
from django.contrib.postgres.fields import ArrayField

class Game(models.Model):
    player1 = models.CharField(default="null", max_length=50)
    player2 = models.CharField(default="null", max_length=50)
    player1_name = models.CharField(default="null", max_length=50)
    player2_name = models.CharField(default="null", max_length=50)

class TournamentGame(models.Model):
    nb_user = models.PositiveIntegerField()
    users = ArrayField(models.CharField())