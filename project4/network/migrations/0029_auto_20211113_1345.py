# Generated by Django 3.1 on 2021-11-13 00:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0028_auto_20211113_1320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='author',
        ),
    ]
