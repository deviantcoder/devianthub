import os
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, PostMedia
from .forms import PostForm, PostMediaFormSet
from django.contrib import messages


def feed(request):
    page = 'feed'
    posts = Post.objects.filter(draft=False)
    context = {
        'posts': posts,
        'page': page,
    }
    return render(request, 'posts/feed.html', context)


def create_post(request):
    page = 'create_post'

    post_form = PostForm()
    media_formset = PostMediaFormSet()

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        media_formset = PostMediaFormSet(request.POST, request.FILES)

        if post_form.is_valid() and media_formset.is_valid():
            post_type = request.POST.get('post_type', 'text')

            post = post_form.save(commit=False)
            post.post_type = post_type
            
            if post_type == 'text':
                post.body = request.POST.get('body_text', '')
            elif post_type == 'media':
                post.body = request.POST.get('body_media', '')
            else:
                post.body = request.POST.get('body_link', '')

            post.save()
            
            media_formset.instance = post
            media_formset.save()

            messages.success(request, 'Post created successfully!')

            return redirect('posts:feed')
        else:
            for form in media_formset:
                if form.errors:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.warning(request, f"{error}")
            
            if post_form.errors:
                messages.warning(request, post_form.errors)

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
        post_form = PostForm(request.POST, instance=post)
        if post_type == 'media':
            media_formset = PostMediaFormSet(request.POST, request.FILES, instance=post)

        if post_form.is_valid() and (media_formset.is_valid() if media_formset else True):
            post_form.save()

            if post_type == 'media':
                media_formset.save()

            messages.success(request, 'Post updated successfully!')

            return redirect('posts:feed')
        
    context = {
        'post_title': post.title,
        'form': post_form,
        'media_formset': media_formset,
        'post_type': post_type,
    }

    return render(request, 'posts/edit_post.html', context)


def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)

    media_files = [media.file.path for media in post.postmedia_set.all() if media.file]
    media_dir = os.path.dirname(media_files[0]) if media_files else None

    if request.method == 'POST':
        post.delete()

        if media_files:
            for file_path in media_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
        
        if media_dir and os.path.exists(media_dir):
            os.rmdir(media_dir)

        messages.info(request, 'Post was deleted')
        return redirect('/')

    context = {'object': post.title}

    return render(request, 'posts/delete_confirmation.html', context)

def post(request, pk):
    post = get_object_or_404(Post, id=pk)

    context = {
        'post': post,
    }

    return render(request, 'posts/post.html', context)
