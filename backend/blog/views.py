from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView 
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework import status,generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout 
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import exceptions
from rest_framework import filters

import os

from .models import Post,Role
from .serializers import PostSerializer ,UserSerializer,RoleSerializer,CookieTokenRefreshSerializer, UserShortSerializer,PostListSerializer


class CookieTokenObtainPairView(TokenObtainPairView):
  def finalize_response(self, request, response, *args, **kwargs):
    if response.data.get('refresh'):
        cookie_max_age = 3600 * 24 * 14 # 14 days
        response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
        del response.data['refresh']
    return super().finalize_response(request, response, *args, **kwargs)

class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer

class LogoutView(APIView):
    def post(self, request):
        permission_classes = [IsAuthenticated]
        
        response = Response({'detail': 'Successfully logged out'})
        response.delete_cookie('access_token')  # Example for clearing a token stored in a cookie
        response.delete_cookie('refresh_token')  # Example for clearing a refresh token stored in a cookie

        # Invalidate the token on the server side (blacklist the token)
        refresh_token = request.COOKIES.get('refresh_token')  # Example: Get the refresh token from cookies
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except TokenError:
                pass  # Token might be invalid or expired, no need to worry

        # Log the user out (optional)
        logout(request)
        # Implement your logout logic here if needed

        return response


class BlogListView(APIView):
    def get(self,request,*args,**kwargs):
        posts = Post.postobjects.all()[0:4]
        serializer = PostSerializer(posts,many=True)

        return Response(serializer.data)


    

class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'excerpt']

    def get_queryset(self):
        # Filter only published posts
        return Post.objects.filter(status='published')


class PostDetailView(APIView):
    def get(self,request,post_slug,*args,**kwargs):
        post = get_object_or_404(Post, slug = post_slug)

        serializer = PostSerializer(post)

        return Response(serializer.data)
    
class PostCreateView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Asigna el autor al usuario autenticado y establece el valor del campo 'slug' antes de guardar
        serializer.save(author=self.request.user)
        
class PostDeleteView(generics.DestroyAPIView):
    serializer_class = Post
    def get_object(self):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)
    
class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)
    





class RegisterView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            # Log information about the incoming request
          

            # Serialize and save user data
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Log information about the successful registration
       

            # Return a response with the serialized data
            return Response(serializer.data)
        except Exception as e:
            # Log the exception for further debugging
    

            # Return a response with details about the error
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RoleListView(generics.ListCreateAPIView):
    serializer_class = RoleSerializer

    def get_queryset(self):
        queryset = Role.objects.all()
        description = self.request.query_params.get('description')
        if description:
            queryset = queryset.filter(description__icontains=description)
        return queryset
    
class AddRoleView(APIView):
    def post(self,request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class UserView(APIView):
    def get(self, request):
        permission_classes = [IsAuthenticated]
        user = request.user
        serializer = UserSerializer(user)

        return Response(serializer.data)
    
class UserShortView(APIView):
    def get(self, request):
        permission_classes = [IsAuthenticated]
        user = request.user
        serializer = UserShortSerializer(user)

        return Response(serializer.data)
