from rest_framework import serializers
from .models import Post, User,Role
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer

class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

class PostSerializer(serializers.ModelSerializer):
     class Meta:
          model = Post
          fields = '__all__'

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