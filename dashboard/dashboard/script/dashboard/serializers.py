from rest_framework import serializers
from .models import Gamer, Game,Tournament, TemporaryUser

class GamerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamer
        fields = ['id', 'pseudo', 'victory', 'nb_game', 'nb_tournament']

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'gamer', 'conceded_point', 'marked_point', 'opponent']