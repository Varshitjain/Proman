# Generated by Django 3.1.4 on 2020-12-07 12:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20180403_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='efforts',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
