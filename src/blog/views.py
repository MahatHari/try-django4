
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Comment, Post
from .forms import PostForm, CommentForm


# Create your views here.
# class based views

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


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('login')

    queryset = Post.objects.all()
    form_class = PostForm
    # uses same template as CreatePost, post_form.html

    def get_success_url(self):
        return reverse_lazy('post_detail', args=({self.object.id, }))


class PostDraftList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    queryset = Post.objects.filter(status=0).order_by('-created_on')

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class PostArchivedList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    queryset = Post.objects.filter(status=2).order_by('-created_on')

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

# function based view


@login_required
def add_comment(request, pk):
    post = Post.objects.filter(pk=pk).first()
    if request.method == "POST":
        request.POST._mutable = True
        request.POST["author"] = request.user
        request.POST["post"] = post
        request.POST._mutable = False
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = CommentForm()
    return render(request, "blog/comment_form.html", {"form": form})


@login_required
def comment_approve(request, pk):
    comment = Comment.objects.filter(pk=pk)
    post_pk = comment.first().post.pk
    comment.update(approved_comment=True)
    return redirect("post_detail", post_pk)


@login_required
def comment_remove(request, pk):
    comment = Comment.objects.filter(pk=pk)
    post_pk = comment.first().post.pk
    comment.delete()
    return redirect('post_detail', post_pk)


class CreateUser(generic.CreateView):
    success_url = reverse_lazy("post_list")

    form_class = UserCreationForm
    queryset = User.objects.all()

    template_name = "registration/signup.html"  # template name
