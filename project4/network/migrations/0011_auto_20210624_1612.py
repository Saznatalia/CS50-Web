# Generated by Django 3.1 on 2021-06-24 04:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_auto_20210624_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 24, 16, 12, 24, 690797)),
        ),
    ]
