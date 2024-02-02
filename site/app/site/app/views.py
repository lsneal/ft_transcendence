from django.shortcuts import render
from django.http import HttpResponse
from .Matchmaking import Matchmaking
from django.http import JsonResponse

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