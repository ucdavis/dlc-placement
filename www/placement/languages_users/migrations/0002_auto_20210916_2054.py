# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2021-09-16 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages_users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='languagesusers',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]