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

from .models import User

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
        csrf.get_token(request)
        response.data = {"Success" : "Login successfully","data":data}
        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        access_token_obj = AccessToken(token)
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)
        serialiazer = UserSerializer(user)

        return Response(serialiazer.data)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('access_token')
        response.delete_cookie('csrftoken')
        response.data = {
            'message': 'success'
        }
        return response
    
class Login42View(APIView):

    def post(self, request):
        response = Response()
        client = AuthorizationCodeClient(
            client_id="u-s4t2ud-11f2f99d539fd7e0882f03a1a9d8956a5e81f1122575411181eff146d684e7f3",
            client_secret="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",
            redirect_uri="https://localhost/login42/",
            auth_endpoint="https://api.intra.42.fr/oauth/authorize",
            token_endpoint="https://api.intra.42.fr/oauth/token"
        )

        code = request.data.get('code')
        token_info = client.get_token(code)
        response.data = {
            'message': token_info
        }
        return response

    def get(self, request):
        response = Response()
        client = AuthorizationCodeClient(
            client_id="u-s4t2ud-11f2f99d539fd7e0882f03a1a9d8956a5e81f1122575411181eff146d684e7f3",
            client_secret="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",
            redirect_uri="https://localhost/login42/",
            auth_endpoint="https://api.intra.42.fr/oauth/authorize",
            token_endpoint="https://api.intra.42.fr/oauth/token"
        )

        auth_url = client.get_authorization_url()
        response.data = {
            auth_url
        }
        return response
    
from authlib.oauth2.rfc6749 import grants
from authlib.common.security import generate_token

class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def save_authorization_code(self, code, request):
        client = request.client
        auth_code = AuthorizationCode(
            code=code,
            client_id=client.client_id,
            redirect_uri=request.redirect_uri,
            response_type=request.response_type,
            scope=request.scope,
            user=request.user,
        )
        auth_code.save()
        return auth_code

    def query_authorization_code(self, code, client):
        try:
            item = AuthorizationCode.objects.get(code=code, client_id=client.client_id)
        except AuthorizationCode.DoesNotExist:
            return None

        if not item.is_expired():
            return item

    def delete_authorization_code(self, authorization_code):
        authorization_code.delete()

    def authenticate_user(self, authorization_code):
        return authorization_code.user

# register it to grant endpoint
server.register_grant(AuthorizationCodeGrant)

    

