from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

import jwt,datetime

from .models import Post,User
from .serializers import PostSerializer ,UserSerializer,RoleSerializer

class BlogListView(APIView):
    def get(self,request,*args,**kwargs):
        posts = Post.postobjects.all()[0:4]
        serializer = PostSerializer(posts,many=True)

        return Response(serializer.data)
    
class PostDetailView(APIView):
    def get(self,request,post_slug,*args,**kwargs):
        post = get_object_or_404(Post, slug = post_slug)

        serializer = PostSerializer(post)

        return Response(serializer.data)

class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class  LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise AuthenticationFailed('Credenciales incorrectas.')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {
            'jwt': token
        }

        return response
    
class AddRoleView(APIView):
    def post(self,request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Sin autenticación.')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token de autenticación expirado.')

        user_id = payload.get('id')
        if user_id is None:
            raise AuthenticationFailed('Token de autenticación no válido.')

        user = User.objects.filter(id=user_id).first()
        if user is None:
            raise AuthenticationFailed('Usuario no encontrado.')

        # Serializa el usuario y devuelve los datos
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message' : 'exito'
        }
        return response
