# Generated by Django 3.1.2 on 2020-12-26 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0004_jobseeker_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseeker',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
