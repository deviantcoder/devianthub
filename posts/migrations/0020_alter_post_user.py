# Generated by Django 5.1 on 2025-01-07 17:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0019_alter_votepost_options_alter_commentstats_comment_and_more'),
        ('users', '0009_alter_profile_banner_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='users.profile'),
        ),
    ]