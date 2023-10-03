from django.urls import path
from .views import BlogListView,PostDetailView
app_name="blog"

urlpatterns = [
    path('posts/',BlogListView.as_view(), name="blog-list"),
    path('post/<post_slug>',PostDetailView.as_view()),
]