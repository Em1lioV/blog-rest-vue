from rest_framework import serializers
from .models import Post, User,Role
from django.utils.html import strip_tags
from html import unescape
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from django.utils.text import slugify
import re

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

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author']
    
    def create(self, validated_data):
        # Genera el slug basado en el título antes de crear el post
        validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)

class PostAuthorSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    author_name = serializers.CharField(source='author.name', read_only=True)
    author_profile_image = serializers.CharField(source='author.profile_image', read_only=True)
    author_role_description = serializers.CharField(source='author.role.description', read_only=True)

    class Meta:
        model = Post
        fields = [
            'title',
            'excerpt',
            'content',
            'published',
            'thumbnail',
            'slug',
            'author_id',
            'author_name',
            'author_profile_image',
            'author_role_description',
        ] 

class CustomPostAuthorSerializer(PostAuthorSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'published', 'thumbnail', 'slug', 'excerpt','content','author_id',
            'author_name',
            'author_profile_image',
            'author_role_description']
    
    def get_content(self, obj):
        # Deshacerse de entidades HTML
        cleaned_content = unescape(obj.content)
        
        # Agregar espacios entre los contenidos para evitar que se junten
        cleaned_content = re.sub(r'(?<=>)([^<]*)(?=<)', r'\1 ', cleaned_content)

        # Eliminar etiquetas HTML, limitar a 200 caracteres y ajustar espacios
        cleaned_content = strip_tags(cleaned_content)[:200]
        cleaned_content = re.sub(r'\s+', ' ', cleaned_content)

        return cleaned_content

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Sobrescribir el valor de content en la representación
        representation['content'] = self.get_content(instance)
        return representation


class UserSerializer(serializers.ModelSerializer):
     role_description = serializers.ReadOnlyField(source='role.description')
     
     class Meta:
          model = User
          fields = ['id','name','email','profile_image', 'password','role','role_description']
          extra_kwargs = {
               'password': {'write_only':True}
          }
     
     def create(self, validated_data):
          password = validated_data.pop('password',None)
          instance = self.Meta.model(**validated_data)
          if password is not None:
               instance.set_password(password)
          instance.save()
          return instance

class UserShortSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['id','name','profile_image']


class RoleSerializer(serializers.ModelSerializer):
     class Meta:
          model = Role
          fields = ['id','description']