# Generated by Django 5.1.5 on 2025-02-03 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0015_like_like_recipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='like_recipe',
        ),
    ]
