# Generated by Django 3.1.2 on 2021-02-10 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0021_auto_20210201_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='pincode',
        ),
        migrations.AddField(
            model_name='order',
            name='mode_of_payment',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]