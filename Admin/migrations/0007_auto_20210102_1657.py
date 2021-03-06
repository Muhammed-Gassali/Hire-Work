# Generated by Django 3.1.2 on 2021-01-03 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0006_jobseeker_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseeker',
            name='available',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='experience',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='id_proof',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
