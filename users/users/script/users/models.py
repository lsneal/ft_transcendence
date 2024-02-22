from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class User(AbstractBaseUser):
    pseudo = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=255)
    #sa2f = models.BooleanField(default=False)
    #totp_key = models.CharField(max_length=32, unique=True)
    access_token = models.CharField(max_length=50)
    refresh_token = models.CharField(max_length=50)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



    

