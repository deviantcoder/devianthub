# Generated by Django 5.1 on 2024-11-12 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_profile_email_alter_profile_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='display_name',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
