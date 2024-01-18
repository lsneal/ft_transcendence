from django.shortcuts import render
from django.http import HttpResponse
from app.models import Listing, ContactUsForm, Band
from django.core.mail import send_mail
from django.shortcuts import redirect
from app.forms import BandForm, ListForm


def band_list(request):
    bands = Band.objects.all()
    return render(request, 'site/band_list.html', {'bands': bands})

def band_detail(request, id):
     band = Band.objects.get(id=id)
     return render(request, 'site/band_detail.html', {'band': band})

def band_update(request, id):
    band = Band.objects.get(id=id)

    if request.method == 'POST':
        form = BandForm(request.POST, instance=band)
        if form.is_valid():
            form.save()
        return redirect('band-detail', band.id)
    else:
        form = BandForm(instance=band)
    return render(request, 'site/band_update.html', {'form': form})

def band_delete(request, id):
    band = Band.objects.get(id=id)
    if request.method == 'POST':
        band.delete()
        return redirect('band-list')
    return render(request, 'site/band_delete.html', {'band': band})

def listings_update(request, id):
    list = Listing.objects.get(id=id)

    if request.method == 'POST':
        form = ListForm(request.POST, instance=list)
        if form.is_valid():
            form.save()
        return redirect('list-detail', list.id)
    else:
        form = ListForm(instance=list)
    return render(request, 'site/list_update.html', {'form': form})

def about(request):
    return render(request, 'site/about.html')

def listings(request):
    lists = Listing.objects.all()
    return render(request, 'site/listings.html', {'lists': lists})

def listings_detail(request, id):
    list = Listing.objects.get(id=id)
    return render(request, 'site/listings_detail.html', {'list': list})

def contact(request):
        if request.method == 'POST':
            form = ContactUsForm(request.POST)
            if form.is_valid():
                send_mail(
                    subject=f'Message form {form.cleaned_data["name"] or "anonyme"} via localhost Contact Us form',
                    message = form.cleaned_data['message'],
                    from_email=form.cleaned_data['email'],
                    recipient_list=['admin@lobozier.42.fr'],
                )
                return redirect('email-sent')
        else:
            form = ContactUsForm()
        return render(request, 'site/contact.html', {'form': form})

def home(request):
        return render(request, 'site/home.html')

def test(request):
        return render(request, 'site/test.html')

def email_sent(request):
    return render(request, 'site/email_sent.html')

def band_create(request):
    if request.method == 'POST':
        form = BandForm(request.POST)
        if form.is_valid():
            band = form.save()
            return redirect('band-detail', band.id)
    else:
        form = BandForm()
    return render(request,
                  'site/band_create.html',
                  {'form': form})

def listing_create(request):
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            list = form.save()
            return redirect('list-detail', list.id)
    else:
        form = ListForm()
    return render(request,
                  'site/list_create.html',
                  {'form': form})
