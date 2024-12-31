from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm
from .models import Message, Chat
from django.contrib.auth.decorators import login_required


@login_required(login_url='users:login')
def chat(request):
    chat = get_object_or_404(Chat, name='public-chat')
    messages = chat.chat_messages.all()

    form = MessageForm()

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
    }
    
    return render(request, 'chat/chat.html', context)
