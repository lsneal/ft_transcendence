from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import rest_framework_simplejwt, datetime, jwt
import json

from .settings import SECRET_KEY
from django.conf import settings
from django.contrib.auth import authenticate, get_user
from django.middleware import csrf
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .oauth import AuthorizationCodeClient, getInfoClient
from .authenticate import CustomAuthentication

from .models import User
from .utils import gen_otp_url, gen_key_user
import pyotp
from django.shortcuts import render
import qrcode

from functools import wraps
from rest_framework.decorators import api_view

#def jwt_authentication(view_func):
#    @wraps(view_func)
#    def wrapper(request, *args, **kwargs):
#        token = request.COOKIES.get('access_token')
#
#        if not token:
#            raise AuthenticationFailed('Unauthenticated!')
#
#        try:
#            access_token_obj = AccessToken(token)
#        except:
#            try:
#                token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#                user = User.objects.get(id=token['user_id'])
#                refresh_token = user.token_refresh
#                refresh = RefreshToken(refresh_token)
#                access_token_obj = refresh.access_token
#
#                response = view_func(request, *args, **kwargs)
#
#                response.set_cookie(
#                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
#                    value=str(access_token_obj),
#                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
#                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
#                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
#                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
#                )
#
#                return response
#            except Exception as e:
#                print('Error:', e)
#                raise AuthenticationFailed('Invalid Token!')
#
#    return wrapper

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
        print (code, " " ,token_info)
        
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
    def get(self, request):
        token = request.COOKIES.get('access_token')
        access_token_obj = AccessToken(token)
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)
        
        access_token_obj = AccessToken(token)
        
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)
    
        email = request.data.get('email', None)
        #user = User.objects.filter(email=email).first()

        print("email  {email}")

        response = Response()
        if user.a2f is True:
            response.data = {
                'message': 'True'
            }
        else:
            response.data = {
                'message': 'False'
            }
        return response
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
        user.token_refresh = data["refresh"]
        user.save() 
        csrf.get_token(request)
        response.data = {"Success" : "Login successfully","data":data}
        return response

class ActivateA2F(APIView):
    def post(self, request):
        token = request.COOKIES.get('access_token')
        user_code = request.data['totp_code']

        access_token_obj = AccessToken(token)
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)

        response = Response()

        if user.a2f is True:
            response.data = { 'message': 'error' }
            return response

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        totp = pyotp.TOTP(user.totp_key)

        if totp.now() == user_code:
            user.a2f = True
            user.save()
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

        if user.a2f is True:
            response.data = { 'message': 'error' }
            return response
        else:
            prvt_key = gen_key_user()
            user.totp_key = prvt_key
            otp_url = gen_otp_url(user.email, prvt_key) 
            user.save()

        qr = 'https://api.qrserver.com/v1/create-qr-code/?data=' + otp_url

        response.data = { 'url': qr }
        return response 
    
    def put(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
           raise AuthenticationFailed('Unauthenticated!')

        access_token_obj = AccessToken(token)
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)
        response = Response()

        user.a2f = False
        user.save()

        response.data = { 'message': 'success disable 2fa'}

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
            response.data = { 'message': 'True' }
        else:
            response.data = { 'message': 'False' }
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
            response.data = { 'message': 'success' }
        else:
            response.data = { 'message': 'failure' }
        return response



def getAccessToken(self, request):
    token = request.COOKIES.get('access_token')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    response = Response()
    try:
        access_token_obj = AccessToken(token)
    except:
        token = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=["HS256"], options={"verify_signature": False})
        user = User.objects.get(id=token['user_id'])
        refresh_token = user.token_refresh
        try:
            refresh = RefreshToken(str(refresh_token))
            access_token_obj = AccessToken(str(refresh.access_token))
            response.set_cookie(
                key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                value = access_token_obj,
                expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
        except:
            print ('Error Refresh Token') #Need to Raise Exception in case refresh token doesn't work and disconnect the person 

    return response, access_token_obj
    

class UserView(APIView):
    def get(self, request):
        response, access_token_obj = getAccessToken(self, request)

        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)
        serialiazer = UserSerializer(user)

        response.data = {'data' : serialiazer.data}
        return response
    
    #Change get cookie
    def put(self, request):
        oldpassword = request.data.get('oldpassword', None)

        token = request.COOKIES.get('access_token')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        access_token_obj = AccessToken(token)
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)

        if not user.check_password(oldpassword):
            return Response('Wrong Password')
        
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


############ Need to check if connected and raise expection ###################
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('access_token')
        response.delete_cookie('csrftoken')
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