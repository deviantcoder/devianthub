import json
from django.shortcuts import get_object_or_404
from channels.generic.websocket import WebsocketConsumer
from .models import Chat, Message
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope.get('user')
        self.chatroom_name = 'public-chat'
        self.chat = get_object_or_404(Chat, name='public-chat')

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )

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
