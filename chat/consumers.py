import json
from django.shortcuts import get_object_or_404
from channels.generic.websocket import WebsocketConsumer
from .models import Chat, Message
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chat = get_object_or_404(Chat, name=self.chatroom_name)

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )

        # add and update online users
        if self.user.profile not in self.chat.online_users.all():
            self.chat.online_users.add(self.user.profile)
            self.update_online_count()

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )

        # add and remove online users
        if self.user.profile in self.chat.online_users.all():
            self.chat.online_users.remove(self.user.profile)
            self.update_online_count()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json.get('body')

        message = Message.objects.create(
            chat=self.chat,
            author=self.user.profile,
            body=body
        )

        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,
            event
        )

    def message_handler(self, event):
        message_id = event.get('message_id')
        message = Message.objects.get(id=message_id)

        context = {
            'message': message,
            'user': self.user
        }

        html = render_to_string('chat/partials/message_p.html', context=context)

        self.send(html)

    def update_online_count(self):
        online_count = self.chat.online_users.all().count() - 1

        event = {
            'type': 'online_count_handler',
            'online_count': online_count,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,
            event
        )

    def online_count_handler(self, event):
        online_count = event.get('online_count')
        html = render_to_string('chat/partials/online_count.html', {'online_count': online_count})

        self.send(text_data=html)
