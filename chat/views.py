from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm
from .models import Message, Chat
from django.contrib.auth.decorators import login_required
from django.http import Http404
from users.models import Profile


def test(request):
    return render(request, 'chat/new_chat.html')


@login_required(login_url='users:login')
def chat_home(request):
    return render(request, 'chat/chat.html', {'page': 'chat_home'})


@login_required(login_url='users:login')
def chat(request, chatroom_name='public-chat'):
    chat = get_object_or_404(Chat, name=chatroom_name)
    messages = chat.chat_messages.all()

    form = MessageForm()

    other_user = None

    if chat.is_private:
        if request.user.profile not in chat.members.all():
            raise Http404()
        for member in chat.members.all():
            if member != request.user.profile:
                other_user = member
                break

    if request.headers.get('HX-Request'):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.author = request.user.profile

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
    }
    
    return render(request, 'chat/chat.html', context)


@login_required(login_url='users:login')
def get_or_create_chat(request, username):
    if request.user.profile.username == username:
        return redirect('/')
    
    other_user = Profile.objects.get(username=username)
    my_chats = request.user.profile.chats.filter(is_private=True)

    if my_chats.exists():
        for chat in my_chats:
            if other_user in chat.members.all():
                chat = chat
                break
            else:
                chat = Chat.objects.create(is_private=True)
                chat.members.add(other_user, request.user.profile)
    else:
        chat = Chat.objects.create(is_private=True)
        chat.members.add(other_user, request.user.profile)

    return redirect('chat:chatroom', chat.name)
