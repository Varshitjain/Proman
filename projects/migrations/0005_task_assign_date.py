# Generated by Django 3.1.4 on 2020-12-07 12:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20201207_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assign_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]