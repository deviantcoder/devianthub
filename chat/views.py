from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm, GroupForm
from .models import Message, Chat
from django.contrib.auth.decorators import login_required
from django.http import Http404
from users.models import Profile
from django.contrib import messages


@login_required(login_url='users:login')
def chat_home(request):
    group_form = GroupForm()

    context = {
        'page': 'chat_home',
        'group_form': group_form,
    }

    return render(request, 'chat/chat.html', context)


@login_required(login_url='users:login')
def chat(request, chatroom_name='public-chat'):
    current_user = request.user.profile

    chat = get_object_or_404(Chat, name=chatroom_name)
    messages = chat.chat_messages.all()
    
    form = MessageForm()
    group_form = GroupForm()

    other_user = None

    if chat.is_private:
        if current_user not in chat.members.all():
            raise Http404()
        for member in chat.members.all():
            if member != current_user:
                other_user = member
                break

    if chat.group_name:
        if current_user not in chat.members.all():
            chat.members.add(current_user)

    if request.headers.get('HX-Request'):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.author = current_user

            message.save()

            context = {
                'message': message,
                'profile': request.user
            }

            return render(request, 'chat/partials/message_p.html', context)

    context = {
        'form': form,
        'messages': messages,
        'chat_name': chat.name,
        'other_user': other_user,
        'chat': chat,
        'group_form': group_form,
    }
    
    return render(request, 'chat/chat.html', context)


@login_required(login_url='users:login')
def get_or_create_chat(request, username):
    if request.user.profile.username == username:
        return redirect('/')

    try:
        other_user = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        return redirect('/')
    
    chat = request.user.profile.chats.distinct().filter(is_private=True, members=other_user).first()

    if not chat:
        chat = Chat.objects.create(is_private=True)
        chat.members.add(request.user.profile, other_user)

    return redirect('chat:chatroom', chat.name)


@login_required(login_url='users:login')
def create_group(request):
    form = GroupForm()

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)

            group.admin = request.user.profile
            group.save()

            group.members.add(request.user.profile)

            messages.success(request, 'Group created')

            return redirect('chat:chatroom', group.name)

    return redirect('/')


@login_required(login_url='users:login')
def edit_group(request, chat_name):
    group = get_object_or_404(Chat, name=chat_name)

    form = GroupForm(instance=group)

    if request.user.profile != group.admin:
        raise Http404()
    
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()

            remove_members = request.POST.getlist('remove_members')

            for member_id in remove_members:
                member = get_object_or_404(Profile, id=member_id)
                group.members.remove(member)

            return redirect('chat:chatroom', chat_name)
    
    context = {
        'form': form,
        'group': group,
    }
    
    return render(request, 'chat/edit_group.html', context)



@login_required(login_url='users:login')
def delete_group(request, chat_name):
    group = get_object_or_404(Chat, name=chat_name)

    if request.user.profile != group.admin:
        raise Http404()
    
    if request.method == 'POST':
        try:
            group.delete()
            messages.success(request, 'Group deleted')
        except Chat.DoesNotExist:
            messages.error(request, 'Group does not exist')

        return redirect('chat:chat')
    
    context = {
        'group': group
    }

    return render(request, 'chat/delete_group.html', context)


@login_required(login_url='users:login')
def leave_group(request, chat_name):
    group = get_object_or_404(Chat, name=chat_name)
    current_user = request.user.profile

    if current_user not in group.members.all():
        raise Http404()

    if request.method == 'POST':
        group.members.remove(current_user)

        if current_user == group.admin:
            group.admin = group.members.first() if group.members.exists() else None
            group.save()
        
        messages.success(request, 'You left the group')

        return redirect('chat:chat')
