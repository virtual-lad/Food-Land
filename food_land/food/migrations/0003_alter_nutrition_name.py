# Generated by Django 5.1.5 on 2025-01-30 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_remove_ingredient_amount_nutrition_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutrition',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
