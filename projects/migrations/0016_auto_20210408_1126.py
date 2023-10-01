# Generated by Django 3.1.4 on 2021-04-08 11:26

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0015_auto_20210408_1101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='assign',
        ),
        migrations.AddField(
            model_name='project',
            name='assign',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='assDate',
            field=models.DateField(default=datetime.datetime(2021, 4, 8, 11, 26, 12, 155311)),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(default=datetime.datetime(2021, 4, 8, 11, 26, 12, 155336)),
        ),
    ]