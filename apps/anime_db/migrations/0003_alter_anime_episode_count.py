# Generated by Django 4.0.6 on 2022-07-22 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime_db', '0002_rename__id_anime_uuid_alter_anime_age_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='episode_count',
            field=models.IntegerField(verbose_name='Episodes count'),
        ),
    ]
