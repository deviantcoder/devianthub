from django.contrib import admin
from .models import Chat, Message
from django.forms import CheckboxSelectMultiple
from django.db import models

# admin.site.register(Chat)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['name', 'group_name', 'is_private', 'created']
    formfield_overrides = {
        models.ManyToManyField: {
            'widget': CheckboxSelectMultiple
        }
    }


admin.site.register(Message)
