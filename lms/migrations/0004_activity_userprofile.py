# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-03 17:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lms', '0003_permissionssupport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=1000)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('activity_type', models.CharField(choices=[('l', 'Lecture'), ('e', 'E-Learning'), ('x', 'Exercise'), ('o', 'Other')], default='l', max_length=1)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.Module')),
            ],
            options={
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.Course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
