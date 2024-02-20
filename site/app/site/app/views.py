from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .utils import gen_otp_url, gen_qr_img
import onetimepass
import qrcode
import base64
import secrets


def home(request):
        return render(request, 'site/home.html')

def test(request):
        return render(request, 'site/test.html')

def qr_code(request):
    return render(request, 'site/qr_code.html') 

def register(request):
    # Verifie si la requete est une requete POST (c'est-a-dire un formulaire a ete soumis)
    if request.method == 'POST':
        # Cree une instance du formulaire CustomUserCreationForm avec les donnees de la requete POST
        user_register = CustomUserCreationForm(request.POST)

        print(user_register.is_valid())
        #if user_register.data is not None:
        print(user_register.data)
        print(user_register.errors)    
        if user_register.is_valid():

            username = user_register.cleaned_data.get('username')
            email = user_register.cleaned_data.get('email')
            password1 = user_register.cleaned_data.get('password1')
            password2 = user_register.cleaned_data.get('password2')

            check_if_user_exists = User.objects.filter(email=email).exists()
            print(check_if_user_exists)
            if check_if_user_exists is not None and user_register.is_valid():
                #if le username et email existe pas on le cree           
                #if not user.objects.filter(username=username).exists():
                #and user.objects.filter(email=email).exists()

                # Sauvegarde l'utilisateur dans la base de donnees
                user = user_register.save()
                # login un l'user apres avec login
                # Redirige l'utilisateur vers la page d'accueil (remplacez 'home' par le nom d'URL de votre page d'accueil)
                return render(request, 'site/register_success.html')
            else:
                return render(request, 'site/test.html')

    else:
        # Si la requete n'est pas une requete POST, cree une instance vide du formulaire
        user_register = CustomUserCreationForm()
    # Rend le modele 'register.html' avec le formulaire, qu'il soit vide ou contenant des donnees POST invalides
    return render(request, 'site/test.html', {'user_register': user_register})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        print(form.data)
        #print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print(username)
        #if user is not None:
        #ogin(request, user)
        #qr_code(request, username)

            otp_url = gen_otp_url(username) # fonction dans utils.py qui gen un url otp
            img = gen_qr_img(otp_url, username)
            return render(request, 'site/qr_code.html', {'otp_url': otp_url, 'img': img})
    else:
        form = AuthenticationForm()
    return render(request, 'site/home.html', {'form': form})
