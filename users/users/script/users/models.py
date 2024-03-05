from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class User(AbstractBaseUser):
    pseudo = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    a2f = models.BooleanField(default=False)
    totp_key = models.CharField(default="", max_length=32)
    password = models.CharField(max_length=255)
    username = None
    victory = models.IntegerField(default=100)
    nb_game = models.IntegerField(default=100)
    profile_image = models.ImageField(upload_to='default_img/', default='users/default_img/default.jpeg')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    
