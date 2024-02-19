from django.shortcuts import render
from django.http import HttpResponse
from .Matchmaking import Matchmaking
from .MatchmakingTournament import MatchmakingTournament
from django.http import JsonResponse
from rest_framework import permissions, viewsets

from .models import Game
from .models import User
from mysite.serializers import UserGameSerializer
from mysite.serializers import GameSerializer
from mysite.serializers import UserSerializer
from mysite.serializers import TournamentSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import rest_framework_simplejwt, datetime, jwt
from rest_framework.views import APIView

manager = Matchmaking()
managerTournament = MatchmakingTournament()

def home(request):
        return render(request, 'site/home.html')

def test(request):
        return render(request, 'site/test.html')

def pong(request):
        return render(request, 'site/pong.html')

class UserIdGameView(APIView):
    def get(self, request):
        if request.method == 'GET':
            serializer = UserGameSerializer(data={'user_id': 'Join'})
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)


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
            game = manager.joinGame()
            if game.player1 is not None and game.player2 is 'p2':
                serializer = Game.objects.get(pk=Game.objects.latest('id').id)
                serializer = GameSerializer(serializer, data={'player2': game.player2})
                serializer.is_valid()
                serializer.save()
                return Response(serializer.data)
            elif game.player1 is 'p1' and game.player2 is not 'p2':
                serializer = GameSerializer(data={'player1': game.player1})
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


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed ('Incorrect password')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        
        response =  Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id = payload['id']).first()
        serialiazer = UserSerializer(user)

        return Response(serialiazer.data)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response