# Generated by Django 3.1 on 2021-06-23 04:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_auto_20210216_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 23, 16, 50, 38, 473821)),
        ),
    ]