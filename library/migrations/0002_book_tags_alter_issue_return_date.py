# Generated by Django 5.2 on 2025-04-18 19:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='issue',
            name='return_date',
            field=models.DateField(default=datetime.datetime(2025, 5, 3, 0, 52, 27, 201504)),
        ),
    ]
