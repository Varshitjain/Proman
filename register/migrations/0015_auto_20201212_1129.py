# Generated by Django 3.1.4 on 2020-12-12 11:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0014_skills_workprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='workprofile',
            name='level',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='workprofile',
            name='skill',
            field=models.CharField(max_length=250),
        ),
        migrations.DeleteModel(
            name='Skills',
        ),
    ]
