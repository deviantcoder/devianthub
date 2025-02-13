import os

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q

from .models import Post, VotePost, PostStats, Comment, CommentStats, VoteComment
from .forms import PostForm, PostMediaFormSet, CommentForm
from users.models import UserActivityStats


def feed(request):
    page = 'feed'
    posts = Post.objects.filter(draft=False)
    context = {
        'page': page,
        'posts': posts,
    }
    return render(request, 'posts/feed.html', context)


def posts_json(request, **kwargs):
    upper_index = kwargs.get('num_posts')
    lower_index = upper_index - 3

    posts = Post.objects.filter(draft=False).distinct().order_by('-created')[lower_index:upper_index]
    posts_num = Post.objects.filter(draft=False).count()

    size = True if upper_index >= posts_num else False

    context = {
        'posts': posts,
        'page': 'feed'
    }

    posts_html = render_to_string('posts/posts_loading.html', context, request=request)

    return JsonResponse({'data': posts_html, 'max': size,})


def comments_json(request, **kwargs):
    post_id = kwargs.get('post_id', 'Post ID was not found')

    upper_index = kwargs.get('visible')
    lower_index = upper_index - 3

    post = get_object_or_404(Post, id=post_id)

    parent_comments = Comment.objects.filter(post=post, parent__isnull=True)[lower_index:upper_index]

    comments_num = Comment.objects.filter(post=post, parent__isnull=True).count()

    all_comments = Comment.objects.filter(
        tree_id__in=parent_comments.values_list('tree_id', flat=True)
    ).order_by('tree_id', 'lft')

    comments_html = render_to_string('posts/comments_loading.html', {'comments': all_comments}, request=request)

    size = True if upper_index >= comments_num else False

    return JsonResponse({'data': comments_html, 'max': size,})


@login_required(login_url='account_login')
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

            post.user = request.user.profile
            
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


@login_required(login_url='account_login')
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


@login_required(login_url='account_login')
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
    page = 'post'

    post = get_object_or_404(Post, id=pk)
    form = CommentForm()
    
    comments = post.comments.filter(status=True)

    context = {
        'post': post,
        'form': form,
        'all_comments': comments,
        'page': page,
    }

    return render(request, 'posts/post.html', context)


@login_required(login_url='account_login')
def comment_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post_stats, _ = PostStats.objects.get_or_create(post=post)
    user = request.user.profile
    user_stats, _ = UserActivityStats.objects.get_or_create(profile=user)

    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = user

        post_stats.comments = F('comments') + 1

        comment.save()
        post_stats.save()

        user_stats.written_comments.add(comment)

        messages.success(request, 'Comment was created!')

    return redirect('posts:post', pk)


@login_required(login_url='account_login')
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    post_stats = get_object_or_404(PostStats, post=comment.post)

    try:
        comment.delete()
        
        if post_stats.comments != 0:
            post_stats.comments = F('comments') - 1
            post_stats.save()

        messages.success(request, 'Comment was deleted!')
    except:
        messages.error(request, 'error occured')

    return redirect('posts:post', comment.post.id)


@login_required(login_url='account_login')
def vote_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=pk)
        user = request.user.profile
        post_stats, _ = PostStats.objects.get_or_create(post=post)
        user_stats, _ = UserActivityStats.objects.get_or_create(profile=user)
        
        vote_type = request.POST.get('vote_type')

        vote, created = VotePost.objects.get_or_create(post=post, user=user)

        if created:
            vote.vote_type = vote_type
            vote.save()

            if vote_type == 'upvote':
                post_stats.upvotes = F('upvotes') + 1
                user_stats.upvoted_posts.add(post)
            else:
                post_stats.downvotes = F('downvotes') + 1
                user_stats.downvoted_posts.add(post)
        else:
            if vote.vote_type == vote_type:
                vote.delete()
                if vote.vote_type == 'upvote':
                    post_stats.upvotes = F('upvotes') - 1
                    user_stats.upvoted_posts.remove(post)
                else:
                    post_stats.downvotes = F('downvotes') - 1
                    user_stats.downvoted_posts.remove(post)
            else:
                if vote.vote_type == 'upvote':
                    post_stats.upvotes = F('upvotes') - 1
                    user_stats.upvoted_posts.remove(post)
                else:
                    post_stats.downvotes = F('downvotes') - 1
                    user_stats.downvoted_posts.remove(post)

                vote.vote_type = vote_type
                vote.save()

                if vote_type == 'upvote':
                    post_stats.upvotes = F('upvotes') + 1
                    user_stats.upvoted_posts.add(post)
                else:
                    post_stats.downvotes = F('downvotes') + 1
                    user_stats.downvoted_posts.add(post)
        
        post_stats.save()
        post_stats.refresh_from_db()

    return redirect('posts:feed')


@login_required(login_url='account_login')
def vote_comment(request, pk):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=pk)
        user = request.user.profile
        comment_stats, _ = CommentStats.objects.get_or_create(comment=comment)
        user_stats, _ = UserActivityStats.objects.get_or_create(profile=user)

        vote_type = request.POST.get('vote_type')

        vote, created = VoteComment.objects.get_or_create(comment=comment, user=user)

        if created:
            vote.vote_type = vote_type
            vote.save()

            if vote_type == 'upvote':
                comment_stats.upvotes = F('upvotes') + 1
                user_stats.upvoted_comments.add(comment)
            else:
                comment_stats.downvotes = F('downvotes') + 1
                user_stats.downvoted_comments.add(comment)
        else:
            if vote.vote_type == vote_type:
                vote.delete()
                if vote.vote_type == 'upvote':
                    comment_stats.upvotes = F('upvotes') - 1
                    user_stats.upvoted_comments.remove(comment)
                else:
                    comment_stats.downvotes = F('downvotes') - 1
                    user_stats.downvoted_comments.remove(comment)
            else:
                if vote.vote_type == 'upvote':
                    comment_stats.upvotes = F('upvotes') - 1
                    user_stats.upvoted_comments.remove(comment)
                else:
                    comment_stats.downvotes = F('downvotes') - 1
                    user_stats.downvoted_comments.remove(comment)

                vote.vote_type = vote_type
                vote.save()

                if vote.vote_type == 'upvote':
                    comment_stats.upvotes = F('upvotes') + 1
                    user_stats.upvoted_comments.add(comment)
                else:
                    comment_stats.downvotes = F('downvotes') + 1
                    user_stats.downvoted_comments.add(comment)

        comment_stats.save()

    return redirect('posts:post', comment.post.id)
