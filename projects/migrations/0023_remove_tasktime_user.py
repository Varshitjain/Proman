# Generated by Django 3.1.4 on 2021-04-29 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_tasktime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasktime',
            name='user',
        ),
    ]
