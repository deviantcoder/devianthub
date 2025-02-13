import shortuuid
from uuid import uuid4
from django.db import models
from users.models import Profile


class Chat(models.Model):
    name = models.CharField(max_length=100, unique=True, default=shortuuid.uuid)

    group_name = models.CharField(max_length=100, null=True, blank=True)
    admin = models.ForeignKey(Profile, related_name='groups', null=True, blank=True, on_delete=models.SET_NULL)

    online_users = models.ManyToManyField(Profile, related_name='online_in_chat', blank=True)

    members = models.ManyToManyField(Profile, related_name='chats', blank=True)
    is_private = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.group_name or self.name
    

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_messages')
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    body = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.chat}: {self.author}'
    
    class Meta:
        ordering = ['-created']

    def time_sent(self):
        return self.created.strftime('%I:%M %p')
