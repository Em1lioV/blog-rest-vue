from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "blog"

# Define el enrutador para los ViewSets
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('token/', CookieTokenObtainPairView.as_view(), name='token-obtain'),
    path('users/posts/<int:user_id>/', UserPostsListViewByID.as_view(), name='user_posts_list_by_id'),
    path('users/posts/', UserPostsListViewByRequestUser.as_view(), name='user_posts_list_by_request_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token-refresh'),
    path('roles/',RoleListCreateView.as_view(),name='role-list-create'),
]

urlpatterns += router.urls