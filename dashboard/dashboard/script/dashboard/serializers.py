from rest_framework import serializers
from .models import Gamer, Game

class GamerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamer
        fields = ['id', 'pseudo', 'victory', 'nb_game', 'email']

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'gamer', 'conceded_point', 'marked_point', 'opponent']