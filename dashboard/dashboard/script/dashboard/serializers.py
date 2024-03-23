from rest_framework import serializers
from .models import Gamer, Tournament, TemporaryUser

class GamerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamer
        fields = ('pseudo', 'victory', 'nb_game', 'nb_tournament')
