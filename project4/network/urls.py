
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/<int:post_id>", views.post_detail, name="post_detail"),
    path("posts", views.posts, name="posts"),
    path("api/posts", views.api_posts, name="api_posts")
]
