from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F, Case, When, Value, FloatField
from .models import Gamer 
from .serializers import GamerSerializer 

class UserStats(APIView):
    def get(self, request):
        response = Response() 
        serialiazer = GamerSerializer(user)
        
        response.data = {
            'victory': serialiazer.data['victory'],
            'nb_game': serialiazer.data['nb_game'],
            'img': serialiazer.data['profile_image'],
            'prc_win': ['serialiazer.prc_win'],
        }
        return response



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