# Generated by Django 3.1 on 2021-11-08 22:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0023_auto_20211108_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 9, 11, 1, 27, 656119)),
        ),
    ]