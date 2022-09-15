# Generated by Django 4.0.6 on 2022-09-15 08:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('anime_db', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='user_favorites',
            field=models.ManyToManyField(blank=True, related_name='favorites_anime', to=settings.AUTH_USER_MODEL),
        ),
    ]
