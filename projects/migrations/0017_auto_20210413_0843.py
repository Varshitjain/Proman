# Generated by Django 3.1.4 on 2021-04-13 08:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_auto_20210408_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(),
        ),
    ]