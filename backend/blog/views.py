from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,ListCreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import action


from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from rest_framework.permissions import IsAuthenticated

from rest_framework import filters


from .models import Post,Role,User
from .serializers import *


class CookieTokenObtainPairView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer
  def finalize_response(self, request, response, *args, **kwargs):
    if response.data.get('refresh'):
        cookie_max_age = 3600 * 24 * 14 # 14 days
        response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
        del response.data['refresh']
    return super().finalize_response(request, response, *args, **kwargs)

class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Verifica si la clave 'refresh' está presente en los datos de la respuesta
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            # Establece la cookie 'refresh_token'
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True)
            # Elimina la clave 'refresh' de los datos de la respuesta
            del response.data['refresh']

        return response

class LogoutView(APIView):
    def post(self, request):   
        response = Response({'detail': 'Successfully logged out'})

        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except TokenError:
                pass 

        response.delete_cookie('access_token')  
        response.delete_cookie('refresh_token') 

        return response

from rest_framework import viewsets

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status='published')
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'excerpt']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Asignar el autor al usuario autenticado y establecer el valor del campo 'slug'
        serializer.save(author=self.request.user)

    def get_queryset(self):
        if self.action == 'list':
            queryset = Post.objects.filter(status='published').select_related('author__role')
        else:
            queryset = Post.objects.filter(status='published')
        return queryset

    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return PostAuthorSerializer  # Reemplaza ListPostSerializer con tu propio serializer
        return PostSerializer  # Reemplaza PostSerializer con tu propio serializer

class UserPostsListViewByID(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            return Post.objects.filter(author=user, status='published')
        else:
            return Post.objects.none()  # Devuelve una lista vacía si no se proporciona user_id

class UserPostsListViewByRequestUser(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_user_object(self, pk=None):
        return get_object_or_404(self.queryset, pk=pk)

    def get_user_serializer(self, user, request_user):
        if user == request_user:
            return UserSerializer(user, context={'request': self.request}) 
        else:
            return UserShortSerializer(user, context={'request': self.request})

    def retrieve(self, request, pk=None):
        user = self.get_user_object(pk=pk)
        serializer = self.get_user_serializer(user, request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def partial(self, request):
        user = request.user
        serializer = UserShortSerializer(user, context={'request': self.request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def logged(self, request):
        user = request.user
        serializer = UserSerializer(user, context={'request': self.request})
        return Response(serializer.data)

class RoleListCreateView(ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        description = self.request.query_params.get('description')
        if description:
            queryset = queryset.filter(description__icontains=description)
        return queryset



