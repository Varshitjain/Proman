# Generated by Django 3.1.4 on 2020-12-07 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_task_assign_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assign_date',
        ),
    ]