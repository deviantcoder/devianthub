# Generated by Django 5.1 on 2024-10-30 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_postmedia_options_alter_postmedia_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmedia',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
