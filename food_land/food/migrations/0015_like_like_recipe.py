# Generated by Django 5.1.5 on 2025-02-03 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0014_alter_like_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='like_recipe',
            field=models.BooleanField(default=False),
        ),
    ]
