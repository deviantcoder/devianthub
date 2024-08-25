from django.shortcuts import render
from .models import Post
from .forms import PostForm


def feed(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/feed.html', context)


def create_post(request):
    form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)
