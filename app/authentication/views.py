import jwt

from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi

from .serializers import (RegisterSerializer, EmailVerificationSerializer, 
                          LoginSerializer, ResetPasswordEmailSerializer, 
                          SetNewPasswordSerializer, LogoutSerializer, 
                          BlackListSerializer, CourierRegister, CollectorRegister)
from .renderers import UserRenderer
from app.account.models import User, Blacklist, Courier, Collectors
from .utils import Util


class RegisterView(generics.GenericAPIView):
    
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user=user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = f'http://{current_site}{relativeLink}?token={str(token)}'

        email_body = f'Hi {user.username}! Use link below to verify your email.\n{absurl}'
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Verify your email address'
            }
        Util.send_mail(data=data)

        return Response(user_data,  status=status.HTTP_201_CREATED)
    

class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token',
        in_=openapi.IN_QUERY,
        description='Description',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email': 'Succesfully activated'},  status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation expired'},  status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token '},  status=status.HTTP_400_BAD_REQUEST)
 

class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailSerializer
    
    def post(self, request):
        data = {
            'request': request,
            'data': request.data
        }
        serializer = self.serializer_class(data=data)
        # serializer.is_valid(raise_exception=True)

        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user=user)

            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                'password-reset-confirm',
                kwargs={
                    'uidb64': uidb64,
                    'token': token
                }
            )
            absurl = f'http://{current_site}{relativeLink}'

            email_body = f'Hello, \nUse link below to reset your password \n{absurl}'
            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Reset your password'
                }
            Util.send_mail(data=data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        

class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'success': True, 'message': 'Credentials valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
                
        except DjangoUnicodeDecodeError as er:
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'succes': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AddToBlackListView(generics.CreateAPIView):
    queryset = Blacklist.objects.all()
    serializer_class = BlackListSerializer

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        blacklist = Blacklist.objects.create(customer=user, reason=request.data.get('reason'))

        serializer = self.serializer_class(blacklist)
        return Response(serializer.data)
    

class DeleteFromBlackListView(generics.DestroyAPIView):
    queryset = Blacklist.objects.all()
    serializer_class = BlackListSerializer

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        blacklist = Blacklist.objects.filter(customer=user).first()
        if not blacklist:
            return Response({'error': 'User not in the blacklist'}, status=status.HTTP_404_NOT_FOUND)

        blacklist.delete()

        return Response({'success': 'User removed from the blacklist'})


class CourierRegisterView(generics.CreateAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierRegister

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user=user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = f'http://{current_site}{relativeLink}?token={str(token)}'

        email_body = f'Hi {user.username}! Use link below to verify your email.\n{absurl}'
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Verify your email address'
            }
        Util.send_mail(data=data)

        return Response(user_data,  status=status.HTTP_201_CREATED)
    

class CollectorRegisterView(generics.CreateAPIView):
    queryset = Collectors.objects.all()
    serializer_class = CollectorRegister

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user=user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = f'http://{current_site}{relativeLink}?token={str(token)}'

        email_body = f'Hi {user.username}! Use link below to verify your email.\n{absurl}'
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Verify your email address'
            }
        Util.send_mail(data=data)

        return Response(user_data,  status=status.HTTP_201_CREATED)
    