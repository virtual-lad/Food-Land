# Generated by Django 5.1.5 on 2025-02-03 11:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0013_alter_like_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'recipe')},
        ),
    ]
