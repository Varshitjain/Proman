# Generated by Django 3.1.4 on 2021-05-08 06:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0024_issue'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='creation',
            field=models.DateField(default=datetime.datetime(2021, 1, 1, 0, 0)),
        ),
        migrations.AddField(
            model_name='issue',
            name='deadline',
            field=models.DateField(default=datetime.datetime(2021, 5, 1, 0, 0)),
        ),
    ]
