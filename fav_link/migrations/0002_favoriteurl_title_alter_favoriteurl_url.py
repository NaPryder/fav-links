# Generated by Django 5.0.4 on 2024-04-15 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fav_link', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoriteurl',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='favoriteurl',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]
