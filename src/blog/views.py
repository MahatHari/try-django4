from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Comment, Post
from .forms import PostForm, CommentForm


# Create your views here.


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by(
        "-created_on")  # latest post on top
    # template_name='post_list.html'


class PostDetail(generic.DetailView):
    queryset = Post.objects.all().order_by('-created_on')
    #template_name = "blog/post_detail.html"


class CreatePost(LoginRequiredMixin, generic.CreateView):
    login_url = reverse_lazy("login")  # navigate to login page
    # after success navigate to post_list page
    success_url = reverse_lazy("post_list")

    # create form
    form_class = PostForm
    queryset = Post.objects.all()
    template_name = "blog/post_form.html"

    def post(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.POST['author'] = request.user
        request.POST._mutable = False

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CreateUser(generic.CreateView):
    success_url = reverse_lazy("post_list")

    form_class = UserCreationForm
    queryset = User.objects.all()

    template_name = "registration/signup.html"  # template name
