from django.contrib import admin
from .models import Post, PostMedia


class PostMediaInline(admin.StackedInline):
    model = PostMedia
    extra = 1
    max_num = 10


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_type', 'created', 'updated']
    inlines = [PostMediaInline]


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'post', 'file_extension', 'created']

    def file_name(self, obj):
        return obj.file.name[:15]

    def file_extension(self, obj):
        return obj.file_ext()['ext']
    
    file_name.short_description = 'File name'
    file_extension.short_description = 'File extension'
