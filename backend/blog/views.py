from django.shortcuts import get_object_or_404
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,ListCreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import action

from datetime import timedelta
from django.utils import timezone
from django.utils.text import slugify

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from rest_framework.permissions import IsAuthenticated,IsAdminUser

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
        # Procesar las etiquetas
        tags_data = self.request.data.getlist('tags[]') 
        tags = []
        for tag_name in tags_data:
            tag_slug = slugify(tag_name)
            tag, created = Tag.objects.get_or_create(slug=tag_slug, defaults={'name': tag_name.strip().title()})
            
            tags.append(tag)

        serializer.save(author=self.request.user, tags=tags)

    def get_queryset(self):
        queryset = super().get_queryset()

        feed = self.request.query_params.get('feed')
        tag_slug = self.request.query_params.get('tag')

        if feed == 'follow':
            if self.request.user.is_authenticated:
                queryset = queryset.filter(author__in=self.request.user.following.all())

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=tag)

        return queryset

    def get_serializer_class(self):
        if self.action in ['list']:
            return PostAuthorSerializer  # Reemplaza ListPostSerializer con tu propio serializer
        return PostSerializer  # Reemplaza PostSerializer con tu propio serializer
    
    @action(detail=False, methods=['get'])
    def posts_by_tag(self, request, tag_slug=None):
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = self.queryset.filter(tags=tag)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def boost(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        if user.boosted_posts.filter(id=post.id).exists():
            user.boosted_posts.remove(post)
            boosted = False
        else:
            user.boosted_posts.add(post)
            boosted = True
        user.save()
                
        return Response({'boosted': boosted}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        if user.bookmarks.filter(id=post.id).exists():
            user.bookmarks.remove(post)
            is_bookmarked = False
        else:
            user.bookmarks.add(post)
            is_bookmarked = True
        user.save()
                
        return Response({'is_bookmarked': is_bookmarked}, status=status.HTTP_200_OK)
        

class UserPostsListViewByID(ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            return Post.objects.filter(author=user, status='published')
        else:
            return Post.objects.none() 

class UserPostsListViewByRequestUser(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['firstName', 'lastName']
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy','logged',]:
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
    
    @action(detail=True, methods=['post'])
    def toggle_follow(self, request, pk=None):
        user_to_follow = get_object_or_404(User, pk=pk)
        user = request.user

        if user != user_to_follow:  # Evita que un usuario se siga a sí mismo
            if user.following.filter(id=user_to_follow.id).exists():
                user.following.remove(user_to_follow)
                
            else:
                user.following.add(user_to_follow)
                
            updated_user = User.objects.get(id=pk)
            serializer = UserShortSerializer(updated_user, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No puedes seguirte a ti mismo"}, status=status.HTTP_400_BAD_REQUEST)

        
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return TagDetailSerializer 
        return TagSerializer 

    def get_permissions(self):
        if self.action in ['toggle_follow']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def recommend_tags(self, request):
        numero_de_tags = int(request.query_params.get('numero_de_tags', 5))
        dias_recientes = int(request.query_params.get('dias_recientes', 30))

        fecha_limite = timezone.now() - timedelta(days=dias_recientes)
        
        # Utilizar agregación para contar las publicaciones recientes y las tags relacionadas
        tags_recomendadas = Tag.objects.filter(posts__status='published', posts__published__gte=fecha_limite) \
            .order_by('-post_count')[:numero_de_tags]

        serializer = TagFollowingSerializer(tags_recomendadas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_follow(self, request, pk=None):
        tag = get_object_or_404(Tag, slug=pk)
        user = request.user

        if user.followed_tags.filter(slug=pk).exists():
            user.followed_tags.remove(tag)
        else:
            user.followed_tags.add(tag)
        user.save()
        
        updated_tag = Tag.objects.get(slug=pk)

        serializer = TagFollowingSerializer(updated_tag, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserFollowingTagsListView(ListAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.followed_tags.all()

class RoleListCreateView(ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        description = self.request.query_params.get('description')
        if description:
            queryset = queryset.filter(description__icontains=description)
        return queryset



