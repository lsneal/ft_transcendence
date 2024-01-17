from django.shortcuts import render
from django.http import HttpResponse
from app.models import Band
from app.models import Listing

def band_list(request):
    bands = Band.objects.all()
    return render(request, 'site/band_list.html', {'bands': bands})

def band_detail(request, id):
     band = Band.objects.get(id=id)
     return render(request, 'site/band_detail.html', {'band': band})

def about(request):
    return render(request, 'site/about.html')

def listings(request):
    lists = Listing.objects.all()
    return render(request, 'site/listings.html', {'lists': lists})

def listings_detail(request, id):
    list = Listing.objects.get(id=id)
    return render(request, 'site/listings_detail.html', {'list': list})

def contact(request):
        return render(request, 'site/contact.html')

def home(request):
        return render(request, 'site/home.html')
