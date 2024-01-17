from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Band(models.Model):

    def __str__(self):
        return f'{self.name}'

    class Genre(models.TextChoices):
        HIP_HOP = 'HH'
        SYNTH_POP = 'SP'
        ALTERNATIVE_ROCK = 'AR'

    name = models.fields.CharField(max_length=100)
    genre = models.fields.CharField(default="", choices=Genre.choices, max_length=5)
    biography = models.fields.CharField(default="", max_length=100)
    year = models.fields.IntegerField(default=1900,
        validators=[MinValueValidator(1900), MaxValueValidator(2024)]
    )
    active = models.fields.BooleanField(default=True)
    official_homepage = models.fields.URLField(null=True, blank=True)

class Listing(models.Model):

    def __str__(self):
        return f'{self.title}'

    class Type(models.TextChoices):
        Records = 'R'
        Clothing = 'C'
        Posters = 'P'
        Miscellaneous = 'M'

    title = models.fields.CharField(max_length=100)
    description = models.fields.CharField(default="",max_length=500)
    sold = models.fields.BooleanField(default=False)
    year = models.fields.IntegerField(default=2018,
        validators=[MinValueValidator(2018), MaxValueValidator(2024)]
    )
    type = models.fields.CharField(default="", choices=Type.choices)
    band = models.ForeignKey(Band, null=True, on_delete=models.SET_NULL)

