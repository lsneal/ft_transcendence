from django.shortcuts import render
from django.http import HttpResponse
from .Matchmaking import Matchmaking
from .MatchmakingTournament import MatchmakingTournament
from django.http import JsonResponse
from rest_framework import permissions, viewsets

from .models import Game
# from .serializers import UserGameSerializer
from .serializers import GameSerializer
from .serializers import TournamentSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView

manager = Matchmaking()
managerTournament = MatchmakingTournament()

class HealthView(APIView):
    def get(self, request):
        response = Response()
        response.data = {
            'status': 'healthy'
        }
        return response

class CreateTournamentView(APIView):
    def post(self, request):
        if request.method == 'POST':
            managerTournament.joinTournament()
            serializer = TournamentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class JoinGameView(APIView):
    def post(self, request):
        if request.method == 'POST':
            player = request.data.get('pseudo', None)
            if type(player) == str:
                game = manager.joinGameOnline(player)
            else:
                game = manager.joinGame()
            if game.player1 != None and game.player2 == 'p2':
                serializer = Game.objects.get(pk=Game.objects.latest('id').id)
                serializer = GameSerializer(serializer, data={'player2': game.player2, 'player2_name': game.player2_name})
                serializer.is_valid()
                serializer.save()
                return Response(serializer.data)
            elif game.player1 == 'p1' and game.player2 != 'p2':
                serializer = GameSerializer(data={'player1': game.player1, 'player1_name': game.player1_name})
                serializer.is_valid()
                serializer.save()
                return Response(serializer.data)
            else:
                return Response("Error")

class GetGameView(APIView):
    def get(self, request, pk):
        if request.method == 'GET':
            game = Game.objects.get(id=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
