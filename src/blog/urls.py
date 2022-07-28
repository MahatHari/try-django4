from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostList.as_view(), name="post_list"),
    path("user/new/", views.CreateUser.as_view(), name="new_user")
]
