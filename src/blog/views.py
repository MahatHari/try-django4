from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Post


# Create your views here.


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by(
        "-created_on")  # latest post on top


class CreateUser(generic.CreateView):
    success_url = reverse_lazy("post_list")

    form_class = UserCreationForm
    queryset = User.objects.all()

    template_name = "registration/signup.html"  # template name
