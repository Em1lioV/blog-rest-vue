from django.urls import path
from .views import BlogListView,PostDetailView,PostUpdateView,PostDeleteView,AddRoleView,UserView,CustomTokenObtainPairView, CustomLogoutView,PostCreateView
from rest_framework_simplejwt.views import TokenRefreshView

app_name="blog"

urlpatterns = [
    path('posts/',BlogListView.as_view(), name="blog-list"),
    path('post/<post_slug>',PostDetailView.as_view()),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('token/',CustomTokenObtainPairView.as_view()),
    path('logout/',CustomLogoutView.as_view()),
    path('token-refresh/', TokenRefreshView.as_view()),
    path('user/',UserView.as_view()),
    path('addRole/',AddRoleView.as_view()),

]