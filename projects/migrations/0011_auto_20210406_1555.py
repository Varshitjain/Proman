# Generated by Django 3.1.4 on 2021-04-06 15:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20201212_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assign_date',
            field=models.DateField(default=datetime.datetime(2021, 4, 6, 15, 55, 16, 73576)),
        ),
        migrations.AddField(
            model_name='task',
            name='deadline',
            field=models.DateField(default=datetime.datetime(2021, 4, 6, 15, 55, 16, 73605)),
        ),
    ]
