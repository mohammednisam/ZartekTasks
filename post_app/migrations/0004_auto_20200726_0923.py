# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-07-26 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0003_auto_20200726_0914'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbluserreview',
            name='bln_review',
        ),
        migrations.AddField(
            model_name='tbluserreview',
            name='int_dislike',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tbluserreview',
            name='int_like',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]