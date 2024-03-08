from rest_framework import serializers
from .models import Post, User,Role,Tag
from django.db import IntegrityError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id','description']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['slug','name']

class TagDetailSerializer(serializers.ModelSerializer):
    follower_count = serializers.IntegerField(read_only=True,source='follower_count')
    post_count = serializers.IntegerField(read_only=True,source='post_count')
    
    class Meta:
        model = Tag
        fields = ['slug','name','follower_count','post_count']
          
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
        fields = ['id','title', 'excerpt', 'content', 'published','updated_at', 'boosts_count' ,'thumbnail','tags','status', 'slug','author']

class PostAuthorSerializer(serializers.ModelSerializer):
    author = UserShortSerializer()
    unique_slug = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','title', 'excerpt','content_preview','published', 'thumbnail','status','tags', 'slug','unique_slug','author']
    
    def get_unique_slug(self, obj):
        return f"{obj.slug}-{obj.id}"

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role', write_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'fullname','firstName', 'lastName', 'initials', 'email', 'profile_image', 'password', 'role','role_id']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        role_id = validated_data.pop('role_id', None)
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if role_id:
            user.role_id = role_id
        if password:
            user.set_password(password)
        try:
            user.save()
        except IntegrityError:
            raise serializers.ValidationError({'email': ['El usuario con este correo electrónico ya existe.']})
        return user
    



