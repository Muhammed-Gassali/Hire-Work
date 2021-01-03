# Generated by Django 3.1.2 on 2020-12-24 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobSeeker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=300, null=True)),
                ('expected_salary', models.IntegerField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.category')),
            ],
        ),
    ]
