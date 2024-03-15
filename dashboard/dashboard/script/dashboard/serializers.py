from rest_framework import serializers
from .models import Gamer, Game, Tournament, TemporaryUser

class GamerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamer
        fields = ('id', 'pseudo', 'victory', 'nb_game', 'nb_tournament')

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'conceded_point', 'marked_point', 'opponent')

class TemporaryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryUser
        fields = ('id', 'pseudo')

class TournamentSerializer(serializers.ModelSerializer):
    temporary_players = TemporaryUserSerializer(many=True)

    class Meta:
        model = Tournament
        fields = ('id', 'temporary_players')
