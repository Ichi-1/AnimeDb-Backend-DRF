# Generated by Django 4.0.6 on 2022-08-21 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_remove_customuser_last_online_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='location',
        ),
    ]