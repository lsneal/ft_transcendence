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
    
class Login42View(APIView):
    def get(self, request):    
        client = AuthorizationCodeClient(
            client_id="u-s4t2ud-11f2f99d539fd7e0882f03a1a9d8956a5e81f1122575411181eff146d684e7f3",
            client_secret="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",
            redirect_uri="https://localhost/login42/",
            auth_endpoint="https://api.intra.42.fr/oauth/authorize",
            token_endpoint="https://api.intra.42.fr/oauth/token"
        )

        auth_url = client.get_authorization_url()
        return Response(auth_url)

    def post(self, request):
        client = AuthorizationCodeClient(
            client_id="u-s4t2ud-11f2f99d539fd7e0882f03a1a9d8956a5e81f1122575411181eff146d684e7f3",
            client_secret="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",
            redirect_uri="https://localhost/login42/",
            auth_endpoint="https://api.intra.42.fr/oauth/authorize",
            token_endpoint="https://api.intra.42.fr/oauth/token"
        )

        code = request.data.get('code', None)
        token_info = client.get_token(code)
        print(token_info)
        response = Response()
        response.set_cookie(
            key = '42access_token',
            value = token_info['access_token'],
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response.set_cookie(
            key = '42refresh_token',
            value = token_info['refresh_token'],
            expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        csrf.get_token(request)
        return response


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

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        access_token_obj = AccessToken(token)
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)

        otp_bool = request.data['a2f']
        user.a2f = otp_bool
        response = Response()

        print(otp_bool)
        if not otp_bool:
            response.data = {
                '2FA': 'disable'
            }
        if otp_bool:
            prvt_key = gen_key_user()
            user.totp_key = prvt_key
            otp_url = gen_otp_url(user.email, prvt_key) 
            img = gen_qr_img(otp_url, user.email)

            user.save()

            qr = 'https://api.qrserver.com/v1/create-qr-code/?data=' + otp_url

            response.data = {
                '2FA': 'enabled',
                'url': qr
            }
        return response 

class LoginA2F(APIView):
    def get(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        access_token_obj = AccessToken(token)
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)

        response = Response()

        if user.a2f is True:
            response.data = {
                '2FA': 'Enabled'
            }    
        elif user.a2f is False:
            response.data = {
                '2FA': 'Disabled'
            }
        return response

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

