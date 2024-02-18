from rest_framework import serializers
from .models import Post, User,Role
from django.utils.html import strip_tags
from html import unescape
from django.db import IntegrityError
from autoslug import AutoSlugField
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer

import re


class RoleSerializer(serializers.ModelSerializer):
     class Meta:
          model = Role
          fields = ['id','description']

class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'Credenciales inválidas. Por favor, verifica tu correo electrónico y contraseña.'
    }
    username_field = 'email'

class UserShortSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    
    class Meta:
          model = User
          fields = ['id','fullname','profile_image','initials','role']
          
    def get_fullname(self, obj):
        return obj.fullname
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'excerpt', 'content', 'published', 'thumbnail','status', 'slug']

class PostAuthorSerializer(serializers.ModelSerializer):
    author = UserShortSerializer()
    class Meta:
        model = Post
        fields = ['id','title', 'excerpt', 'content', 'published', 'thumbnail','status', 'slug','author']


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'initials', 'email', 'profile_image', 'password', 'role', 'fullname']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        try:
            instance.save()
        except IntegrityError:
            raise serializers.ValidationError({'email': ['El usuario con este correo electrónico ya existe.']})
        return instance

    def get_fullname(self, obj):
        return obj.fullname
    


