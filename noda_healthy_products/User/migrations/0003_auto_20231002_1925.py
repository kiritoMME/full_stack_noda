# Generated by Django 3.0.7 on 2023-10-02 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_alter_city_id_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
