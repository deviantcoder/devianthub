# Generated by Django 5.1 on 2024-11-06 17:18

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_alter_postmedia_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostStats',
            fields=[
                ('upvotes', models.PositiveIntegerField(blank=True, default=0)),
                ('downvotes', models.PositiveIntegerField(blank=True, default=0)),
                ('comments', models.PositiveIntegerField(blank=True, default=0)),
                ('reposts', models.PositiveIntegerField(blank=True, default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
