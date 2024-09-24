from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, PostMedia
from .forms import PostForm, PostMediaFormSet


def feed(request):
    posts = Post.objects.filter(draft=False)
    context = {
        'posts': posts,
    }
    return render(request, 'posts/feed.html', context)


def create_post(request):
    post_form = PostForm()
    media_formset = PostMediaFormSet()

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        media_formset = PostMediaFormSet(request.POST, request.FILES)

        if post_form.is_valid() and media_formset.is_valid():
            post_type = request.POST.get('post_type', 'text')

            post = post_form.save(commit=False)
            post.post_type = post_type
            post.save()
            
            media_formset.instance = post
            media_formset.save()

            return redirect('posts:feed')

    context = {
        'form': post_form,
        'media_formset': media_formset,
    }

    return render(request, 'posts/post_form.html', context)


def edit_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post_type = post.post_type
    post_form = PostForm(instance=post)
    media_formset = PostMediaFormSet(instance=post) if post_type == 'media' else None

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post, post_type=post_type)
        if post_type == 'media':
            media_formset = PostMediaFormSet(request.POST, request.FILES, instance=post)

        if post_form.is_valid() and (media_formset.is_valid() if media_formset else True):
            post_form.save()
            
            if post_type == 'media':
                media_formset.save()

            return redirect('posts:feed')
        
    context = {
        'post_title': post.title,
        'form': post_form,
        'media_formset': media_formset,
        'post_type': post_type,
    }

    return render(request, 'posts/edit_post.html', context)
