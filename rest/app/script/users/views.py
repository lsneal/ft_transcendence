from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import rest_framework_simplejwt, datetime, jwt

from .models import User

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from .utils import gen_otp_url, gen_qr_img
import pyotp

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    
class LoginView(APIView):
    def post(self, request):
        
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed ('Incorrect password')
        

        #token_obtain_pair_view = TokenObtainPairView.as_view()
        #respons = token_obtain_pair_view(request._request)

        #if respons.status_code == status.HTTP_200_OK:
        #    access_token = respons.data['access']
        #    refresh_token = respons.data['refresh']

        #response = Response()
        #response.set_cookie(key='jwt', value=access_token, httponly=True)
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        
        response.data = {
            'jwt': token
        }
        
        #if user.a2f is True:
          #  totp = pyotp.TOTP(user.totp_key)
          #  code_user = request.data('OTP')              
          #  if totp.now() == code_user:
                # code bon
          #  else
                # code pas bon

        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id = payload['id']).first()
        serialiazer = UserSerializer(user)

        return Response(serialiazer.data)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response