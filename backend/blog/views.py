from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import status,generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout 


from .models import Post,User
from .serializers import PostSerializer ,UserSerializer,RoleSerializer



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Cierra la sesión del usuario autenticado
        logout(request)
        return Response({"detail": "Sesión cerrada con éxito."}, status=status.HTTP_200_OK)

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
    
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer

class PostDeleteView(generics.DestroyAPIView):
    serializer_class = PostSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)
    
class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)

class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AddRoleView(APIView):
    def post(self,request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Serializa el usuario y devuelve los datos
        serializer = UserSerializer(user)
        return Response(serializer.data)
    