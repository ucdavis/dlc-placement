# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2023-05-05 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='languages',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
