from django.db import models
from django.contrib.auth.models import AbstractUser


class   User(AbstractUser):

    name = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class UserProfile(models.Model):
    user = models.fields.CharField(max_length=20)