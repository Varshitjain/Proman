# Generated by Django 3.1.4 on 2021-05-13 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0026_auto_20210513_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empprofile',
            name='last_evaluation',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='empprofile',
            name='satisfaction_level',
            field=models.FloatField(null=True),
        ),
    ]