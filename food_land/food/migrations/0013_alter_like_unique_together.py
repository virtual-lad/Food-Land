# Generated by Django 5.1.5 on 2025-02-03 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0012_remove_like_like_recipe'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set(),
        ),
    ]
