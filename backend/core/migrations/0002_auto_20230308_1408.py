# Generated by Django 3.2.16 on 2023-03-08 19:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(default=datetime.date(2023, 3, 8)),
        ),
    ]