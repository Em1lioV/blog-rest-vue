from django.urls import path
from .views import  *
app_name="blog"

urlpatterns = [
    path('posts/',PostListView.as_view(), name="blog-list"),
    path('post/<post_slug>',PostDetailView.as_view()),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('token/',CookieTokenObtainPairView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('token/refresh/', CookieTokenRefreshView.as_view()),
    path('user/',UserView.as_view()),
    path('user/navbar/',UserShortView.as_view()),
    path('register/',RegisterView.as_view()),
    path('addRole/',AddRoleView.as_view()),
    path('roles/',RoleListView.as_view()),
]