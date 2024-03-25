from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F, Case, When, Value, FloatField
from .models import Gamer 
from .models import Game 
from .serializers import GamerSerializer, GameSerializer
from django.http import JsonResponse
import json

class UserStats(APIView):
    def get(self, request):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ", dict(request.data))
        #gamer = Gamer.objects.get(pseudo= request.data.)
        #response = Response() 
        #response.data = {
        #    'pseudo':  gamer.pseudo,
        #    'victory': gamer.victory,
        #    'nb_game': gamer.nb_game,
        #}
        return response

class ConnectUserStats(APIView):
    def post(self, request):
        pseudo = request.data.get('pseudo', None)
        user_id = request.data.get('id', None)
        
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
            gamer = Gamer.objects.get(pseudo=pseudo)
            games = Game.objects.filter(gamer=gamer)

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

        data = json.loads(request.body)
        conceded_point = data.get('conceded_point')
        marked_point = data.get('marked_point')
        opponent = data.get('opponent')

        if pseudo is not None:
            gamer = Gamer.objects.get(pseudo=pseudo)
            newGame = Game.objects.create(gamer=gamer, conceded_point= conceded_point,marked_point= marked_point,opponent= opponent)
            newGame.save()
            if gameEnd == "true":
                win = request.headers.get('win', None)
                if win == "true":
                    gamer.victory += 1
                gamer.nb_game += 1
                gamer.save()
        return Response()

class PlayerRanking(APIView):
    def get(self, request):
        players = Gamer.objects.annotate(prc_win=Case(
            When(nb_game__gt=0, then=(F('victory') / F('nb_game')) * 100),
            default=Value(0),
            output_field=FloatField()
        )).filter(nb_game__gt=0).order_by('-prc_win')[:5]
        
        serialized_players = []
        for player in players:
            if player.nb_game != 0:
                prc_win = player.prc_win
            else:
                prc_win = 0
            serialized_player = {
                'pseudo': player.pseudo,
                'nb_game': player.nb_game,
                'victory': player.victory,
            }
            serialized_players.append(serialized_player)

        
        return Response(serialized_players)