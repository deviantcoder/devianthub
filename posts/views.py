from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm


def feed(request):
    posts = Post.objects.filter(draft=False)
    context = {
        'posts': posts,
    }
    return render(request, 'posts/feed.html', context)


def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)
