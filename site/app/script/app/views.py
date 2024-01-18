from django.shortcuts import render
from django.http import HttpResponse
from app.models import Listing, ContactUsForm, Band
from django.core.mail import send_mail
from django.shortcuts import redirect

def band_list(request):
    bands = Band.objects.all()
    return render(request, 'site/band_list.html', {'bands': bands})

def band_detail(request, id):
     band = Band.objects.get(id=id)
     return render(request, 'site/band_detail.html', {'band': band})

#def band_list(request):
    #band = Band.objects.all()
#    return render(request, 'site/band_create.html')

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