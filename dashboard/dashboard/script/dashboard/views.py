from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F, Case, When, Value, FloatField
from .models import Gamer 
from .serializers import GamerSerializer 

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
        
        serialiazer = GamerSerializer(data={'pseudo': pseudo, 'id': user_id,})
        serialiazer.is_valid(raise_exception=True)
        serialiazer.save()
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa : ", serialiazer)
        return Response(serialiazer.data)




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