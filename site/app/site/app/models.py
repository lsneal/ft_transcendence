from django.db import models
from django.contrib.auth.models import AbstractUser

class Game(models.Model):
    player1 = models.CharField(default="null", max_length=50)
    player2 = models.CharField(default="null", max_length=50)

class User(AbstractUser):
    pseudo = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []