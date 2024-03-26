from rest_framework import serializers
from game.models import Game
from game.models import TournamentGame

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'player1', 'player2', 'player1_name', 'player2_name']

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentGame
        fields = ['id', 'users', 'nb_user']