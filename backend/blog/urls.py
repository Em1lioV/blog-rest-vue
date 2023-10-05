from django.urls import path
from .views import BlogListView,PostDetailView,RegisterView,AddRoleView,LoginView,LogoutView,UserView
app_name="blog"

urlpatterns = [
    path('posts/',BlogListView.as_view(), name="blog-list"),
    path('post/<post_slug>',PostDetailView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('user/',UserView.as_view()),
    path('addRole/',AddRoleView.as_view()),

]