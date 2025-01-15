from django.contrib import admin
from .models import Post, PostMedia, PostStats, Comment, VotePost, CommentStats, VoteComment
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin


class PostMediaInline(admin.StackedInline):
    model = PostMedia
    extra = 1
    max_num = 10


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'post_type', 'draft', 'created', 'updated']
    inlines = [PostMediaInline]


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'post', 'file_extension', 'created', 'file_tag']

    def file_name(self, obj):
        return obj.file.name[:15]

    def file_extension(self, obj):
        return obj.file_ext()['ext']

    def file_tag(self, obj):
        if obj.file_ext()['type'] == 'image':
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.file.url))
        return format_html(
            '<video controls style="max-width:200px; max-height:200px"><source src="{file}" type="video/{ext}"></video>'.format(file=obj.file.url, ext=obj.file_ext()['ext'])
        )

    file_name.short_description = 'File name'
    file_extension.short_description = 'File extension'


@admin.register(PostStats)
class PostStatsAdmin(admin.ModelAdmin):
    list_display = ['post', 'upvotes', 'downvotes', 'comments', 'reposts']


@admin.register(VotePost)
class VotePostAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'vote_type', 'user', 'created']

    def post_id(self, obj):
        return obj.post.id


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ['user', 'post', 'created']


@admin.register(CommentStats)
class CommentsStatsAdmin(admin.ModelAdmin):
    list_display = ['comment_text', 'upvotes', 'downvotes']

    def comment_text(self, obj):
        return obj.comment.body[:20]


admin.site.register(VoteComment)