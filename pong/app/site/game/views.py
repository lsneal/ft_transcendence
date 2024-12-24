from django.http import HttpResponse
from .Matchmaking import Matchmaking
from .MatchmakingTournament import MatchmakingTournament
from django.http import JsonResponse

from .models import Game
from rest_framework import status
from .serializers import GameSerializer
from .serializers import TournamentSerializer
from rest_framework.response import Response
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
            try:
                managerTournament.joinTournament()
                serializer = TournamentSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except:
                return Response({'error': 'An error occured when creating a tournament'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data)

class JoinGameOnlineView(APIView):
    def post(self, request):
        if request.method == 'POST':

            player = request.data.get('pseudo', None)
            game = manager.joinGameOnline(player)
            if game.player1 != None and game.player2 == 'p2':
                try:
                    serializer = Game.objects.get(pk=Game.objects.latest('id').id)
                    serializer = GameSerializer(serializer, data={'player2': game.player2, 'player2_name': game.player2_name})
                    serializer.is_valid()
                    serializer.save()
                except:
                    return Response({'error': 'An error occured when joining an online game'}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.data)
            elif game.player1 == 'p1' and game.player2 != 'p2':
                try:
                    serializer = GameSerializer(data={'player1': game.player1, 'player1_name': game.player1_name})
                    serializer.is_valid()
                    serializer.save()
                except:
                    return Response({'error': 'An error occured when joining an online game'}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.data)
            else:
                return Response("Error")

class JoinGameView(APIView):
    def post(self, request):
        if request.method == 'POST':
            game = manager.joinGame()
            if game.player1 != None and game.player2 == 'p2':
                try:
                    serializer = Game.objects.get(pk=Game.objects.latest('id').id)
                    serializer = GameSerializer(serializer, data={'player2': game.player2, 'player2_name': game.player2_name})
                    serializer.is_valid()
                    serializer.save()
                except:
                    return Response({'error': 'An error occured when joining a local game'}, status=status.HTTP_400_BAD_REQUEST)

                return Response(serializer.data)
            elif game.player1 == 'p1' and game.player2 != 'p2':
                try:
                    serializer = GameSerializer(data={'player1': game.player1, 'player1_name': game.player1_name})
                    serializer.is_valid()
                    serializer.save()
                except:
                    return Response({'error': 'An error occured when joining a local game'}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.data)
            else:
                return Response("Error")

class GetGameView(APIView):
    def get(self, request, pk):
        if request.method == 'GET':
            game = Game.objects.get(id=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
