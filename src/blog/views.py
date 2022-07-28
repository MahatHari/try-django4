from django.shortcuts import render
from django.views import generic
from .models import Comment, Post

# Create your views here.


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by(
        "-created_on")  # latest post on top