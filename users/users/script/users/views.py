from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import rest_framework_simplejwt, datetime, jwt

from django.conf import settings
from django.contrib.auth import authenticate, get_user
from django.middleware import csrf
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .oauth import AuthorizationCodeClient
from .authenticate import CustomAuthentication

from .models import User
from .utils import gen_otp_url, gen_qr_img, gen_key_user
import pyotp
from django.shortcuts import render
import qrcode

def qr_code(request):
    def get(request):
        img = 'users/qr_image/img.png'
        response = Response()

        response.data = {
            'qr': 'https://api.qrserver.com/v1/create-qr-code/?data='
        }
        return response

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        response =  Response()

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        data = get_tokens_for_user(user)
        response.set_cookie(
            key = settings.SIMPLE_JWT['AUTH_COOKIE'],
            value = data["access"],
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response.set_cookie(
            key = settings.SIMPLE_JWT['REFRESH_COOKIE'],
            value = data["refresh"],
            expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        csrf.get_token(request)
        response.data = {"Success" : "Login successfully","data":data}
        return response

class ActivateA2F(APIView):
    def post(self, request):
        token = request.COOKIES.get('access_token')
        user_code = request.data['totp']

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        access_token_obj = AccessToken(token)
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)

        response = Response()

        prvt_key = gen_key_user()
        user.totp_key = prvt_key
        otp_url = gen_otp_url(user.email, prvt_key) 
        img = gen_qr_img(otp_url, user.email)

        user.save()

        totp = pyotp.TOTP(user.totp_key)

        if totp.now() == user_code:
            #user.a2f = True
            response.data = { 'message': 'success' }
        else:
            response.data = { 'message': 'failure' }
        return response 

    def get(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        access_token_obj = AccessToken(token)
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)
        response = Response()

        prvt_key = gen_key_user()
        user.totp_key = prvt_key
        otp_url = gen_otp_url(user.email, prvt_key) 
        img = gen_qr_img(otp_url, user.email)
        user.save()

        qr = 'https://api.qrserver.com/v1/create-qr-code/?data=' + otp_url

        response.data = { 'url': qr }
        return response 
    
    #def put(self, request):
    #    token = request.COOKIES.get('access_token')
#
    #    if not token:
    #        raise AuthenticationFailed('Unauthenticated!')
#
    #    access_token_obj = AccessToken(token)
    #    user_id=access_token_obj['user_id']
    #    user=User.objects.get(id=user_id)
    #    response = Response()

        

class LoginA2F(APIView):
    def post(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
    
        access_token_obj = AccessToken(token)
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)

        user_code = request.data['totp']
        totp = pyotp.TOTP(user.totp_key)

        response = Response()
        if totp.now() == user_code:
            response.data = {
                'message': 'success'
            }
        else:
            response.data = {
                'message': 'failure'
            }
        return response
    
def getAccessToken(request):
    token = request.COOKIES.get('access_token')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    response = Response()

    try:
        access_token_obj = AccessToken(token)
    except:
        refresh_token = request.COOKIES.get('refresh_token')
        try:
            refresh = RefreshToken(refresh_token)
            access_token_obj = refresh.access_token
            response.set_cookie(
                key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                value = access_token_obj,
                expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
        except:
            print ('Error Refresh Token')

    return response, access_token_obj
    

class UserView(APIView):
    def get(self, request):
        
        response, access_token_obj = getAccessToken(request)
            
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)
        serialiazer = UserSerializer(user)

        response.data = {'data' : serialiazer.data}
        return response
    
    def put(self, request):
        password = request.data.get('password', None)
        #authentification = request.data.get('2FA', None)
        pseudo = request.data.get('pseudo', None)

        token = request.COOKIES.get('access_token')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        access_token_obj = AccessToken(token)
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)
        print(user)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('access_token')
        response.delete_cookie('csrftoken')
        response.delete_cookie('refresh_token')
        response.data = {
            'message': 'success'
        }
        return response

class HealthView(APIView):
    def get(self, request):
        response = Response()
        response.data = {
            'status': 'healthy'
        }
        return response

