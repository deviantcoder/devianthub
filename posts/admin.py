from django.contrib import admin
from .models import Post, PostMedia


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']


admin.site.register(PostMedia)
