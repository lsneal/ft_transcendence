from django.shortcuts import render
from django.http import HttpResponse
from .Matchmaking import Matchmaking
from django.http import JsonResponse
from rest_framework import permissions, viewsets
from mysite.serializers import GameSerializer
from .models import Game
from .models import User
from mysite.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import rest_framework_simplejwt, datetime, jwt
from rest_framework.views import APIView

manager = Matchmaking()

def home(request):
        return render(request, 'site/home.html')

def test(request):
        return render(request, 'site/test.html')

def pong(request):
        return render(request, 'site/pong.html')

def Matchmake(request):
        result = manager.joinGame(request.user)
        return JsonResponse({
                        'id': result
                })

class GameViewSet(viewsets.ModelViewSet):
        queryset = Game.objects.all().order_by('-id')
        serializer_class = GameSerializer
        permissions_classes = [permissions.IsAuthenticated]

# class GameJoinViewSet():
    #  def put(self, request):
        # if self.player2 is None:
            # self.player2 = request.player2
            # self.save()
        # return Response(self.player2)

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