# Generated by Django 4.2.11 on 2024-11-08 10:59

import catalog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True, validators=[catalog.models.validate_min_length])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100, validators=[catalog.models.validate_min_length])),
            ],
        ),
    ]
