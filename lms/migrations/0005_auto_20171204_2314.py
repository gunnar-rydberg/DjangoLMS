# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0004_activity_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]