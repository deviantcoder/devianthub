# Generated by Django 5.1 on 2024-11-15 08:51

import django.core.validators
import django.db.models.deletion
import posts.models
import utils.file_utils
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_alter_comment_id'),
        ('users', '0009_alter_profile_banner_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmedia',
            name='file',
            field=models.FileField(upload_to=posts.models.upload_to, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'mov', 'avi')), utils.file_utils.validate_file_size]),
        ),
        migrations.CreateModel(
            name='UpvotePost',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
