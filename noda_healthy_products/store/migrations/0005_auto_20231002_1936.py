# Generated by Django 3.0.7 on 2023-10-02 16:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20231002_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmedorder',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
