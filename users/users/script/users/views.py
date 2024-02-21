from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import rest_framework_simplejwt, datetime, jwt
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
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response =  Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response

class ActivateA2F(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id = payload['id']).first()

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
            user.private_key = prvt_key
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
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id = payload['id']).first()

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
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id = payload['id']).first()

        user_code = request.data['totp']
        totp = pyotp.TOTP(user.private_key)

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
    

