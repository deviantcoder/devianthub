from django.contrib import admin
from .models import Post, PostMedia


class PostMediaInline(admin.StackedInline):
    model = PostMedia
    extra = 1
    max_num = 10


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_type', 'created']
    inlines = [PostMediaInline]


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ['file', 'post', 'created']
