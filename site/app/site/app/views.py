from django.shortcuts import render
from django.http import HttpResponse

def home(request):
        return render(request, 'site/home.html')

def test(request):
        return render(request, 'site/test.html')

def pong(request):
        return render(request, 'site/pong.html')
