# Generated by Django 3.1 on 2021-06-30 04:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_auto_20210630_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 16, 39, 33, 117695)),
        ),
    ]
