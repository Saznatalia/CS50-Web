# Generated by Django 3.1 on 2021-11-07 22:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0019_auto_20210701_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 8, 11, 19, 9, 744739)),
        ),
    ]
