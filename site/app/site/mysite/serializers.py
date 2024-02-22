from rest_framework import serializers
from app.models import Game
from app.models import User
from app.models import UserGame
from app.models import TournamentGame

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'player1', 'player2']

class UserGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGame
        fields = ['id', 'user_id']

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentGame
        fields = ['id', 'users', 'nb_user']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'pseudo', 'password']
        extra_kwargs= {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance