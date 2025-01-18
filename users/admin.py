from django.contrib import admin
from .models import Profile, UserActivityStats, SocialNetwork, SocialLink


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'display_name', 'created']


@admin.register(UserActivityStats)
class UserActivityStatsAdmin(admin.ModelAdmin):
    list_display = ['profile', 'post_upvotes', 'post_downvotes', 'comment_upvotes']


admin.site.register(SocialNetwork)
admin.site.register(SocialLink)
