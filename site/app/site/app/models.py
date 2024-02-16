from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

class Game(models.Model):
    player1 = models.CharField(default="null", max_length=50)
    player2 = models.CharField(default="null", max_length=50)

class UserGame(models.Model):
    user_id = models.CharField(default="null", max_length=50)

class TournamentGame(models.Model):
    nb_user = models.PositiveIntegerField()
    users = ArrayField(models.CharField())

class User(AbstractUser):
    pseudo = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []