from uuid import uuid4
from django.db import models
from users.models import Profile


class Chat(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

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
