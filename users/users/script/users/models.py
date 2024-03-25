from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class User(AbstractBaseUser):
    pseudo = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    a2f = models.BooleanField(default=False)
    totp_key = models.CharField(default="", max_length=32)
    password = models.CharField(max_length=255)
    modification_time = models.DateTimeField()
    username = None
    token_refresh = models.CharField(max_length=255, null=True, blank=True)

    profile_image = models.ImageField(upload_to='./default_img/', default='default.jpeg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, instance, validated_data):
        instance.modification_time = timezone.now()
        instance.save()
        return instance