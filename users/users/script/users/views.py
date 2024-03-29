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
from django.core.exceptions import ValidationError
from .authenticate import CustomAuthentication

from .models import User
from .utils import gen_otp_url, gen_key_user
import pyotp
from django.shortcuts import render
import qrcode

from functools import wraps
from rest_framework.decorators import api_view

def jwt_authentication(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = args[0].COOKIES.get('access_token')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            access_token_obj = AccessToken(token)
            return view_func(request, *args, **kwargs)
        except:
            try:
                response = Response()
                token = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=["HS256"])
                user = User.objects.get(id=token['user_id'])
                refresh = RefreshToken(user.token_refresh)
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value = access_token_obj,
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                return view_func(request, *args, **kwargs)
            except:
                raise AuthenticationFailed('Unauthenticated!')
    return wrapper

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
        if len(serializer.validated_data['password']) < 6:
            return Response({"password": "Password length must be greater than 6 character."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

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

        # return email for view a2f
        if user.a2f is True:
            response.data = { 'email': email, 'a2f': user.a2f }
            return response

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
        response.data = {"Success" : "Login successfully","data":data, "a2f": user.a2f}
        return response

class ActivateA2F(APIView):
    @jwt_authentication
    def post(self, request):
        access_token_obj = AccessToken(request.COOKIES.get('access_token'))
        user_code = request.data['totp_code']
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)

        response = Response()

        totp = pyotp.TOTP(user.totp_key)

        if totp.now() == user_code:
            user.a2f = True
            user.save()
            response.data = { 'message': 'success' }
        else:
            response.data = { 'message': 'failure' }
            return Response(response.data, status=status.HTTP_400_BAD_REQUEST)
        return response

    @jwt_authentication
    def get(self, request):
        access_token_obj = AccessToken(request.COOKIES.get('access_token'))
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
    
    @jwt_authentication
    def put(self, request):
        access_token_obj = AccessToken(request.COOKIES.get('access_token'))
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)
        response = Response()

        user.a2f = False
        user.save()

        response.data = { 'message': 'success disable 2fa'}

        return Response(response.data, status=status.HTTP_200_OK)
       
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
        return Response(response.data, status=status.HTTP_200_OK)

    def post(self, request):
        email = request.headers.get('email', None)
        user = User.objects.filter(email=email).first()

        user_code = request.data['totp']
        totp = pyotp.TOTP(user.totp_key)

        response = Response()

        if totp.now() != user_code:
            response.data = { 'status': 'failure' }
            return Response(response.data, status=status.HTTP_400_BAD_REQUEST)

        # connexion et creation du cookies si le code est bon
        data = get_tokens_for_user(user)
        response.set_cookie(
            key = settings.SIMPLE_JWT['AUTH_COOKIE'],
            value = data["access"],
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        user.token_refresh = response.set_cookie(
                 key = settings.SIMPLE_JWT['REFRESH_COOKIE'],
                 value = data["refresh"],
                 expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                 secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                 httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                 samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        user.save() 
        csrf.get_token(request)
        response.data = {"Success" : "Login successfully","data":data, "status": "success"}
        return response

class UserView(APIView):
    @jwt_authentication
    def get(self, request):
        access_token_obj = AccessToken(request.COOKIES.get('access_token'))
        response = Response()

        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)
        serialiazer = UserSerializer(user)

        response.data = {'data' : serialiazer.data}
        return response

    @jwt_authentication
    def put(self, request):
        oldpassword = request.data.get('oldpassword', None)

        access_token_obj = AccessToken(request.COOKIES.get('access_token'))
        
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