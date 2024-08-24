from django.shortcuts import render
from .models import Post


def feed(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/feed.html', context)
