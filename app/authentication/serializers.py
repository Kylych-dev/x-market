from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from app.account.models import User, Blacklist


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, 
        min_length=6,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                "The username should only contain alphanumeric characters"
            )
        
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.password = make_password(password)
        instance.save()
        return instance
    

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=255, min_length=3, read_only=True)

    class Meta:
        model = User 
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise  AuthenticationFailed('Invalid credentials, try again')
        
        if user.blacklist:
            raise AuthenticationFailed('Your account is blacklisted. Please contact the administrator to resolve this issue')
        
        if not user.is_active:
            raise  AuthenticationFailed('Account disabled, contact admin')

        if not user.is_verified:
            raise  AuthenticationFailed('Email is not verified')
        
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=3)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
 
    class Meta:
        fields = ['password', 'token', 'uidb64']
    
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ("Token is expired or invalid",)
    }
    # Use ./manage.py flushexpiredtokens to delete expired tokens

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except:
            self.fail("bad_token")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',]


class BlackListSerializer(serializers.ModelSerializer):
    customer = UserSerializer()

    class Meta:
        model = Blacklist
        fields = '__all__'


class CourierRegister(serializers.Serializer):
    pass