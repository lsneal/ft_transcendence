from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F, Case, When, Value, FloatField
from .models import Gamer 
from .models import Game 
from .serializers import GamerSerializer, GameSerializer
from django.http import JsonResponse
import json

class HealthView(APIView):
    def get(self, request):
        response = Response()
        response.data = {
            'status': 'healthy'
        }
        return response

class ConnectUserStats(APIView):
    def post(self, request):
        pseudo = request.data.get('pseudo', None)
        user_id = request.data.get('id', None)

        try:
            user = Gamer.objects.get(pseudo=pseudo)
            return Response({'user': 'user already exist'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        gamer_serializer = GamerSerializer(data={'pseudo': pseudo, 'id': user_id,})
        gamer_serializer.is_valid(raise_exception=True)
        gamer = gamer_serializer.save()

        game_serializer = GameSerializer(data={'id': user_id,
                                            'gamer': gamer.pk})  
        game_serializer.is_valid(raise_exception=True)
        game_serializer.save()
        return Response(gamer_serializer.data)
    
    def get(self, request):
        pseudo = request.headers.get('pseudo', None)

        user_info = None
        if pseudo is not None:
            try:
                gamer = Gamer.objects.get(pseudo=pseudo)
                games = Game.objects.filter(gamer=gamer)
            except:
                return Response({'error': 'An error occured'}, status=status.HTTP_400_BAD_REQUEST)


            game_data = []
            for game in games:
                game_data.append({
                        'conceded_point': game.conceded_point,
                        'marked_point': game.marked_point,
                        'opponent': game.opponent,
                })
            user_info = {
                'pseudo':  gamer.pseudo,
                'victory': gamer.victory,
                'nb_game': gamer.nb_game,
                'nb_tournament': gamer.nb_tournament,
                'game_data': game_data,
            }
        return Response(user_info)
    
    def put(self, request):
        pseudo = request.headers.get('pseudo', None)
        gameEnd = request.headers.get('gameEnd', None)

        try:
            data = json.loads(request.body)
        except:
            return Response({'error': 'An error occured here'}, status=status.HTTP_400_BAD_REQUEST)
        
        conceded_point = data.get('conceded_point')
        marked_point = data.get('marked_point')
        opponent = data.get('opponent')

        if pseudo is not None:
            try:
                gamer = Gamer.objects.get(pseudo=pseudo)
                newGame = Game.objects.create(gamer=gamer, conceded_point=conceded_point, marked_point=marked_point, opponent=opponent)
                newGame.save()
                if gameEnd == "true":
                    win = request.headers.get('win', None)
                    if win == "true":
                        gamer.victory += 1
                    gamer.nb_game += 1
                    gamer.save()
            except:
                return Response({'error': 'An error occured with models'}, status=status.HTTP_400_BAD_REQUEST)
        return Response()

class PlayerRanking(APIView):
    def get(self, request):
        players = Gamer.objects.annotate(prc_win=Case(
            When(nb_game__gt=0, then=(F('victory') / F('nb_game')) * 100),
            default=Value(0),
            output_field=FloatField()
        )).filter(nb_game__gt=0).order_by('-prc_win').distinct()[:5]

        serialized_players = []
        for player in players:
            serialized_player = {
                'pseudo': player.pseudo,
                'nb_game': player.nb_game,
                'victory': player.victory,
                'prc_win': player.prc_win if player.nb_game != 0 else 0,
            }
            serialized_players.append(serialized_player)

        return Response(serialized_players)