from django.shortcuts import render


def chat(request):
    context = {}
    return render(request, 'chat/chat.html', context)
