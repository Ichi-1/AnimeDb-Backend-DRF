# Generated by Django 4.0.6 on 2022-07-31 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anidb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anime',
            old_name='show_type',
            new_name='kind',
        ),
        migrations.RenameField(
            model_name='anime',
            old_name='release_season',
            new_name='season',
        ),
        migrations.RenameField(
            model_name='anime',
            old_name='release_start_year',
            new_name='year',
        ),
        migrations.RenameField(
            model_name='anime',
            old_name='release_end_year',
            new_name='year_end',
        ),
    ]
